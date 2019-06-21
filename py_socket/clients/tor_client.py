from time import time
from py_socket.sockets import SocketInfo
from py_socket.cells import (
    VersionsPayload, pack_versions_payload, VariableCell,
    CellType, pack_variable_cell, unpack_variable_cell,
    unpack_versions_payload, unpack_cell, unpack_net_info_payload,
    pack_net_info_payload, NetInfoPayload, Cell, pack_cell, unpack_certs_payload
)
import base64
import hashlib
import hmac
from nacl.public import PrivateKey, Box, PublicKey


class TorClient:
    MAX_BUFFER_SIZE = 5000

    socket_info: SocketInfo = None

    _buffer: bytes = None
    _version: int = 0

    def __init__(self, socket_info: SocketInfo):
        self.socket_info = socket_info

    def initialize(self):
        self.send_versions()
        self.recv_versions()
        self.recv_certs()
        self.recv_auth_challenge()
        self.recv_net_info()
        self.send_create()

    def send_versions(self):
        versions_payload = VersionsPayload([3])
        payload_buffer = pack_versions_payload(versions_payload)
        variable_cell = VariableCell(0, CellType.versions, payload_buffer)
        variable_cell_buffer = pack_variable_cell(variable_cell)
        self.socket_info.socket.send(variable_cell_buffer)

    def recv_versions(self):
        self._buffer = self.socket_info.socket.recv(self.MAX_BUFFER_SIZE)
        variable_cell, bytes_consumed = unpack_variable_cell(self._buffer)
        self._buffer = self._buffer[bytes_consumed:]
        versions_payload = unpack_versions_payload(variable_cell.payload)
        _version = versions_payload.versions[0]
        # print(variable_cell)
        # print(versions_payload)
        # print(bytes_consumed)
        # print(_version)
        # print(self._buffer[:20])

    def recv_certs(self):
        variable_cell, bytes_consumed = unpack_variable_cell(self._buffer)
        certs_payload = unpack_certs_payload(variable_cell.payload)
        _ = certs_payload
        temp = base64.b64encode(certs_payload.certs[2].cert)
        self._buffer = self._buffer[bytes_consumed:]

    def recv_auth_challenge(self):
        _, bytes_consumed = unpack_variable_cell(self._buffer)
        self._buffer = self._buffer[bytes_consumed:]

    def recv_net_info(self):
        variable_cell, bytes_consumed = unpack_cell(self._buffer)
        temp = list(self._buffer)
        self._buffer = self._buffer[bytes_consumed:]
        _ = unpack_net_info_payload(variable_cell.payload)

        res_net_info_payload = NetInfoPayload(
            int(time()), 4, 4, bytes([0, 0, 0, 0]), 1, 4, 4, bytes([0, 0, 0, 0]))
        res_net_info_payload_buffer = pack_net_info_payload(
            res_net_info_payload)
        res__cell = Cell(
            0, CellType.net_info, res_net_info_payload_buffer)
        res_cell_buffer = pack_cell(res__cell)
        _ = list(res_cell_buffer)
        self.socket_info.socket.send(res_cell_buffer)
        # self.socket_info.socket.recv(self.MAX_BUFFER_SIZE)
        pass

    def send_create(self):
        proto_id = b"ntor-curve25519-sha256-1"
        t_mac = proto_id + b":mac"
        t_key = proto_id + b":key_extract"
        t_verify = proto_id + b":verify"
        ntor_onion_key = base64.b64decode("5MwtdhPC8TJhO4LimkeubrfjkRlnw6Cs4pXX1pnEKV0=")
        rsa_signing_key = base64.b64decode(
            "MIGJAoGBAMOi1FV0CdvtCBXiokmeYjyzs9aeSj3FOVbii64F8kE/+sshO2TbMv1PTjNnC6FeZ0v0AW6i35tWjFdyRzKdC3XPk1bS1A5C5xZupC+/jsPRB3w0GITWalSWLvbNQwuix9v4hS4wKySdypx7JU0KSFt1pbZHOf7OsbnO047w4EApAgMBAAE=")
        server_identity_digest = hashlib.sha1(rsa_signing_key).digest()
        # actual_server_identity_digest = bytes.fromhex("9715C81BA8C5B0C698882035F75C67D6D643DBE3")
        # assert expected_server_identity_digest == actual_server_identity_digest

        eph_my_private_key_object = PrivateKey.generate()
        eph_my_public_key = eph_my_private_key_object.public_key._public_key
        handshake_data = server_identity_digest + ntor_onion_key + eph_my_public_key
        handshake_data_length = len(handshake_data)
        # print(list(ntor_onion_key))
        # print(list(master_key_ed25519))
        # print(list(server_identity_digest))
        # print(list(handshake_data))
        payload_buffer = bytes([0, 2, 0, handshake_data_length]) + handshake_data
        # payload_buffer = bytes([0, handshake_data_length]) + handshake_data
        cell = Cell(60000, CellType.create2, payload_buffer)
        cell_buffer = pack_cell(cell)
        self.socket_info.socket.send(cell_buffer)
        self._buffer = self.socket_info.socket.recv(TorClient.MAX_BUFFER_SIZE)
        temp = list(self._buffer)
        eph_server_public_key = self._buffer[5:32 + 5]
        temp2 = list(eph_server_public_key)
        self._buffer = self._buffer[37:37+32]
        server_auth = list(self._buffer)

        eph_shared_key = Box(eph_my_private_key_object, PublicKey(eph_server_public_key)).shared_key()
        long_shared_key = Box(eph_my_private_key_object, PublicKey(ntor_onion_key)).shared_key()

        secret_input = (eph_shared_key + long_shared_key + server_identity_digest + ntor_onion_key +
                        eph_my_public_key + eph_server_public_key + proto_id)

        key_seed = self.hmacSha(secret_input, t_key)
        verify = self.hmacSha(secret_input, t_verify)
        auth_input = (verify + server_identity_digest + ntor_onion_key + eph_server_public_key
                      + eph_my_public_key + proto_id + b"Server")

        expected_auth = list(self.hmacSha(auth_input, t_mac))

        assert server_auth == expected_auth

        return temp

    def hmacSha(self, message, key):
        return hmac.new(key, message, hashlib.sha256).digest()


'''
struct fixed_cell
{
    uint16 circuti_id
    uint8 command
    uint8[509] payload
}

struct variable_cell
{
    uint16 circuti_id
    uint8 command
    uint16 payload_length
    uint8[payload_length] payload
}
'''
