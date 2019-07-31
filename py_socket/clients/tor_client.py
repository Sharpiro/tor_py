from time import time
from py_socket.sockets import SocketInfo
from py_socket.cells import (
    VersionsPayload, pack_versions_payload, VariableCell,
    CellType, pack_variable_cell, unpack_variable_cell,
    unpack_versions_payload, unpack_cell, unpack_net_info_payload,
    pack_net_info_payload, NetInfoPayload, Cell, pack_cell, unpack_certs_payload,
    RelayPayload, unpack_relay_payload, pack_relay_payload, unpack_created2_payload,
    Created2Payload, RelayType, NtorHandshakeData
)
from py_socket.tools import get_url_info
from py_socket.clients.node import Node
import base64
import hashlib
import hmac
import secrets
from py_socket.crypto.curve25519 import scalarmult, scalarmult_base
from Crypto.Cipher import AES
from Crypto.Util import Counter


class TorClient:
    CIRCUIT_ID_SIZE = 2
    MAX_BUFFER_SIZE = 5000
    CELL_SIZE = 512
    PROTO_ID = b"ntor-curve25519-sha256-1"

    def __init__(self, guard_node: Node, exit_node: Node):
        self.guard_node = guard_node
        self.exit_node = exit_node
        self.nodes = [guard_node, exit_node]
        self.circuit_id = 60_000
        self.stream_id = 25_000

    def create_circuit(self):
        """
        Main entry function.
        """
        versions_payload = self.create_versions_payload()
        versions_cell = self.create_versions_cell(versions_payload)
        self.send_cell(versions_cell)
        self.recv_versions()
        self.recv_certs()
        self.recv_auth_challenge()
        self.recv_net_info()

        # create first hop
        handshake_data = self.get_ntor_handshake_data(self.guard_node)
        create2_cell = self.create_create2(handshake_data)
        self.send_cell(create2_cell)
        created2_cell = self.recv_cell(self.guard_node, TorClient.CELL_SIZE)
        created2_payload = unpack_created2_payload(created2_cell.payload)
        self.recv_created2(handshake_data, created2_payload, self.guard_node)

        # create second hop
        create_info = self.send_relay_extend2()
        extended2_cell = self.recv_cell(self.guard_node, TorClient.CELL_SIZE)
        created2_payload = unpack_created2_payload(extended2_cell.payload[11:])
        self.recv_created2(create_info, created2_payload, self.exit_node)

    def send_cell(self, cell) -> bytes:
        if cell.command == CellType.versions:
            cell_buffer = pack_variable_cell(cell)
        elif cell.command == CellType.create2:
            cell_buffer = pack_cell(cell)
        else:
            raise Exception("invalid cell type")
        self.guard_node.socket.socket.send(cell_buffer)

    def create_versions_payload(self) -> VersionsPayload:
        versions_payload = VersionsPayload([3])
        return versions_payload

    def create_versions_cell(self, versions_payload: VersionsPayload) -> VariableCell:
        payload_buffer = pack_versions_payload(versions_payload)
        variable_cell = VariableCell(0, CellType.versions, payload_buffer)
        return variable_cell

    def recv_versions(self):
        self.guard_node.buffer = self.guard_node.socket.socket.recv(self.MAX_BUFFER_SIZE)
        variable_cell, bytes_consumed = unpack_variable_cell(self.guard_node.buffer)
        self.guard_node.buffer = self.guard_node.buffer[bytes_consumed:]
        versions_payload = unpack_versions_payload(variable_cell.payload)
        self.guard_node.version = versions_payload.versions[0]
        if self.guard_node.version != 3:
            raise Exception("Only version 3 is supported at this time")

        # print(variable_cell)
        # print(versions_payload)
        # print(bytes_consumed)
        # print(_version)
        # print(self.guard_node.buffer[:20])

    def recv_certs(self):
        variable_cell, bytes_consumed = unpack_variable_cell(self.guard_node.buffer)
        certs_payload = unpack_certs_payload(variable_cell.payload)
        _ = certs_payload
        _temp = base64.b64encode(certs_payload.certs[2].cert)
        self.guard_node.buffer = self.guard_node.buffer[bytes_consumed:]

    def recv_auth_challenge(self):
        _, bytes_consumed = unpack_variable_cell(self.guard_node.buffer)
        self.guard_node.buffer = self.guard_node.buffer[bytes_consumed:]

    def recv_net_info(self):
        cell, bytes_consumed = unpack_cell(self.guard_node.buffer)
        _temp = list(self.guard_node.buffer)
        self.guard_node.buffer = self.guard_node.buffer[bytes_consumed:]
        _ = unpack_net_info_payload(cell.payload)

        res_net_info_payload = NetInfoPayload(
            int(time()), 4, 4, bytes([0, 0, 0, 0]), 1, 4, 4, bytes([0, 0, 0, 0]))
        res_net_info_payload_buffer = pack_net_info_payload(
            res_net_info_payload)
        res__cell = Cell(
            0, CellType.net_info, res_net_info_payload_buffer)
        res_cell_buffer = pack_cell(res__cell)
        _ = list(res_cell_buffer)
        self.guard_node.socket.socket.send(res_cell_buffer)

    def create_create2(self, handshake_data: NtorHandshakeData):
        # handshake_data = self.get_ntor_handshake_data(self.guard_node)

        cell = Cell(self.circuit_id, CellType.create2, handshake_data.pack())
        # return cell, handshake_data.eph_my_private_key, handshake_data.eph_my_public_key
        return cell

    def get_ntor_handshake_data(self, node: Node):
        eph_my_private_key: bytes = secrets.token_bytes(32)
        eph_my_public_key = scalarmult_base(eph_my_private_key)
        ntor_handshake_data = NtorHandshakeData(
            eph_my_private_key, eph_my_public_key, node.server_identity_digest, node.onion_key)
        return ntor_handshake_data

    def recv_cell(self, node: Node, max_size):
        node.buffer = node.socket.socket.recv(max_size)
        cell_buffer = node.buffer
        cell_type = CellType(cell_buffer[TorClient.CIRCUIT_ID_SIZE])
        cell_payload = cell_buffer[TorClient.CIRCUIT_ID_SIZE + 1:]
        if cell_type == CellType.destroy:
            raise Exception("tor protocol exception")
        elif cell_type == CellType.created2:
            pass
        elif cell_type == CellType.relay:
            decrypted_payload = node.decrypt_backward(cell_payload)
            self._verify_digest(node, decrypted_payload, "backward")
            cell_buffer = cell_buffer[:3] + decrypted_payload
        else:
            raise Exception(f"Received unexpected cell type '{cell_type}'")

        cell, bytes_consumed = unpack_cell(cell_buffer)
        node.buffer = node.buffer[bytes_consumed:]

        return cell

    def recv_created2(self, handshake_data: NtorHandshakeData, created2_payload: Created2Payload, node: Node):
        t_mac = self.PROTO_ID + b":mac"
        t_key = self.PROTO_ID + b":key_extract"
        t_verify = self.PROTO_ID + b":verify"

        eph_server_public_key = created2_payload.eph_server_public_key

        eph_shared_key = scalarmult(handshake_data.eph_my_private_key, eph_server_public_key)
        long_shared_key = scalarmult(handshake_data.eph_my_private_key, node.onion_key)

        secret_input = (eph_shared_key + long_shared_key + node.server_identity_digest + node.onion_key +
                        handshake_data.eph_my_public_key + eph_server_public_key + self.PROTO_ID)

        key_seed = self.hmacSha(secret_input, t_key)
        verify = self.hmacSha(secret_input, t_verify)
        auth_input = (verify + node.server_identity_digest + node.onion_key + eph_server_public_key
                      + handshake_data.eph_my_public_key + self.PROTO_ID + b"Server")

        actual_auth = self.hmacSha(auth_input, t_mac)

        assert created2_payload.server_auth == actual_auth

        digest_forward, digest_backward, key_forward, key_backward = self._compute_keys(key_seed)
        node.update_digest_forward(digest_forward)
        node.update_digest_backward(digest_backward)
        node.init_ciphers(key_forward, key_backward)

    def send_relay_extend2(self):
        link_specifiers_count = bytes([2])
        ip_specifier = bytes([0, 6]) + bytes([176, 10, 99, 201]) + bytes([1, 187])
        identity_specifier = bytes([2, 20]) + self.exit_node.server_identity_digest
        # temp_spec = bytes([3, 32]) + base64.b64decode("lC8MDUpVwPFZyej8EgR0x0NAqqZa8LiIhULeDf1y06g=")
        # todo: may need to add ed25519 link specifier
        # link_specifiers_bytes = link_specifiers_count + ip_specifier + identity_specifier + temp_spec
        link_specifiers_bytes = link_specifiers_count + ip_specifier + identity_specifier

        handshake_data = self.get_ntor_handshake_data(self.exit_node)

        relay_data = link_specifiers_bytes + handshake_data.pack()
        relay_payload = RelayPayload(RelayType.RELAY_EXTEND2, relay_data=relay_data)
        relay_payload_buffer = pack_relay_payload(relay_payload)
        self.guard_node.update_digest_forward(relay_payload_buffer)
        relay_payload.digest = self.guard_node.get_digest_forward()[:4]
        relay_payload_buffer = pack_relay_payload(relay_payload)

        encrypted_payload = self.guard_node.encrypt_forward(relay_payload_buffer)

        cell = Cell(self.circuit_id, CellType.relay_early, encrypted_payload)
        cell_buffer = pack_cell(cell)
        self.guard_node.socket.socket.send(cell_buffer)

        return handshake_data.eph_my_private_key, handshake_data.eph_my_public_key

    def receive_relay_connected(self):
        debug_res = self.guard_node.socket.socket.recv(TorClient.MAX_BUFFER_SIZE)

        if debug_res[2] == 4:
            raise Exception("tor protocol exception")

        debug_decrypt = self.get_decrypted_payload(debug_res[3:])
        self._verify_digest(self.exit_node, debug_decrypt, "backward")
        if debug_decrypt[0] != 4:
            raise Exception("relay connection request was unsuccessful")
        pass

    def receive_data(self):
        buffer = self.guard_node.socket.socket.recv(TorClient.MAX_BUFFER_SIZE)

        if buffer[2] == 4:
            raise Exception("tor protocol exception")

        recv_length = len(buffer)
        total_cells, rem = divmod(recv_length, 512)
        if rem != 0:
            raise Exception("invalid cell length")
        if total_cells < 1:
            raise Exception("invalid cells delivered")

        cells = []
        relay_data = bytes()
        for i in range(total_cells):
            start = 512 * i
            end = 512 * (i+1)
            cell, _ = unpack_cell(buffer[start:end])
            cell.payload = self.get_decrypted_payload(cell.payload)
            self._verify_digest(self.exit_node, cell.payload, "backward")
            cells.append(cell)
            relay_payload = unpack_relay_payload(cell.payload)
            relay_data += relay_payload.data[:relay_payload.length]
            pass

        return relay_data

    def _verify_digest(self, node, data, direction):
        expected_digest = data[5:9]
        data_no_digest = data[:5] + bytes(4) + data[9:]
        node.update_digest_backward(data_no_digest)
        actual_digest = node.get_digest_backward()[:4]
        assert expected_digest == actual_digest

    def send_relay_resolve(self, hostname):
        hostname_bytes = bytes(hostname, "utf8") + b'\x00'

        cell = self.get_encrypted_relay_cell(RelayType.RELAY_RESOLVE, hostname_bytes)
        cell_buffer = pack_cell(cell)

        self.guard_node.socket.socket.send(cell_buffer)

    def recv_relay_resolved(self):
        debug_res = self.guard_node.socket.socket.recv(TorClient.MAX_BUFFER_SIZE)
        if debug_res[2] == 4:
            raise Exception("tor protocol exception")

        relay_payload_bytes = self.get_decrypted_payload(debug_res[3:])
        self._verify_digest(self.exit_node, relay_payload_bytes, "backward")
        relay_payload = unpack_relay_payload(relay_payload_bytes)
        addr = relay_payload.data[2:6]
        return addr

    def send_relay_begin(self, addr_port):
        cell = self.get_encrypted_relay_cell(RelayType.RELAY_BEGIN, addr_port)
        cell_buffer = pack_cell(cell)

        self.guard_node.socket.socket.send(cell_buffer)

    def get_encrypted_relay_cell(self, relay_type: RelayType, relay_data: bytes) -> Cell:
        relay_payload = RelayPayload(relay_type, stream_id=self.stream_id, relay_data=relay_data)
        relay_payload_buffer = pack_relay_payload(relay_payload)
        self.exit_node.update_digest_forward(relay_payload_buffer)
        relay_payload.digest = self.exit_node.get_digest_forward()[:4]
        relay_payload_buffer = pack_relay_payload(relay_payload)

        encrypted_payload = self.get_encrypted_payload(relay_payload_buffer)
        cell = Cell(self.circuit_id, CellType.relay, encrypted_payload)
        return cell

    def get_encrypted_payload(self, relay_payload_buffer):
        encrypted_payload_buffer = relay_payload_buffer
        for node in self.nodes[::-1]:
            encrypted_payload_buffer = node.encrypt_forward(encrypted_payload_buffer)
        return encrypted_payload_buffer

    def get_decrypted_payload(self, encrypted_payload_buffer):
        decrypted_payload_buffer = encrypted_payload_buffer
        for node in self.nodes:
            decrypted_payload_buffer = node.decrypt_backward(decrypted_payload_buffer)
        return decrypted_payload_buffer

    def send_relay_data(self, relay_data):
        relay_payload = RelayPayload(RelayType.RELAY_DATA, stream_id=self.stream_id, relay_data=relay_data)
        relay_payload_buffer = pack_relay_payload(relay_payload)
        self.exit_node.update_digest_forward(relay_payload_buffer)
        relay_payload.digest = self.exit_node.get_digest_forward()[:4]
        relay_payload_buffer = pack_relay_payload(relay_payload)

        encrypted_payload = self.get_encrypted_payload(relay_payload_buffer)
        cell = Cell(self.circuit_id, CellType.relay, encrypted_payload)
        cell_buffer = pack_cell(cell)

        self.guard_node.socket.socket.send(cell_buffer)

    def _compute_keys(self, key_seed):
        N = 72
        HASH_LEN = 20
        KEY_LEN = 16

        m_expand = self.PROTO_ID + b":key_expand"
        k_1 = self.hmacSha(m_expand + bytes([1]), key_seed)
        k_2 = self.hmacSha(k_1 + m_expand + bytes([2]), key_seed)
        k_3 = self.hmacSha(k_2 + m_expand + bytes([3]), key_seed)
        all_bytes = k_1 + k_2 + k_3
        digest_forward: bytes = all_bytes[:HASH_LEN]
        digest_backward: bytes = all_bytes[HASH_LEN: HASH_LEN*2]
        key_forward: bytes = all_bytes[HASH_LEN*2: HASH_LEN*2 + KEY_LEN]
        key_backward: bytes = all_bytes[HASH_LEN*2 + KEY_LEN: HASH_LEN*2 + KEY_LEN*2]

        assert len(digest_forward)+len(digest_backward)+len(key_forward)+len(key_backward) == N

        return digest_forward, digest_backward, key_forward, key_backward

    def hmacSha(self, message, key) -> bytes:
        return hmac.new(key, message, hashlib.sha256).digest()
