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
        unpack_certs_payload(variable_cell.payload)
        self._buffer = self._buffer[bytes_consumed:]

    def recv_auth_challenge(self):
        _, bytes_consumed = unpack_variable_cell(self._buffer)
        self._buffer = self._buffer[bytes_consumed:]

    def recv_net_info(self):
        variable_cell, bytes_consumed = unpack_cell(self._buffer)
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
        ntor_onion_key = base64.b64decode("7jxzpYYdzuvsWgyGQIjfaIcdyw2nLliAdDVsAxVm3Bw=")
        # master_key_ed25519 = base64.b64decode("OJi2i6K6x9JhhyU2sD5iiamiK/1hLMzGc7w69HHVQQM=")
        # server_identity_digest = hashlib.sha1(master_key_ed25519).digest()
        server_identity_digest = bytes.fromhex("9715C81BA8C5B0C698882035F75C67D6D643DBE3")
        fake_public_key = ntor_onion_key
        handshake_data = server_identity_digest + ntor_onion_key + fake_public_key
        handshake_data_length = len(handshake_data)
        # print(list(ntor_onion_key))
        # print(list(master_key_ed25519))
        # print(list(server_identity_digest))
        # print(list(handshake_data))
        payload_buffer = bytes([0, 2, 0, handshake_data_length]) + handshake_data
        cell = Cell(60000, CellType.create2, payload_buffer)
        cell_buffer = pack_cell(cell)
        temp_payload = list(cell_buffer)
        self.socket_info.socket.send(cell_buffer)
        self._buffer = self.socket_info.socket.recv(TorClient.MAX_BUFFER_SIZE)
        temp = list(self._buffer)
        return temp


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
