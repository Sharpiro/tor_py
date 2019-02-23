from py_socket.sockets import SocketInfo
from py_socket.cells import (
    VersionsPayload, pack_versions_payload, VariableCell,
    CellType, pack_variable_cell, unpack_variable_cell,
    unpack_versions_payload, unpack_cell
)


class TorClient:
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

    def send_versions(self):
        versions_payload = VersionsPayload([3])
        payload_buffer = pack_versions_payload(versions_payload)
        variable_cell = VariableCell(0, CellType.versions, payload_buffer)
        variable_cell_buffer = pack_variable_cell(variable_cell)
        self.socket_info.socket.send(variable_cell_buffer)

    def recv_versions(self):
        self._buffer = self.socket_info.socket.recv(5000)
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
        _, bytes_consumed = unpack_variable_cell(self._buffer)
        self._buffer = self._buffer[bytes_consumed:]

    def recv_auth_challenge(self):
        _, bytes_consumed = unpack_variable_cell(self._buffer)
        self._buffer = self._buffer[bytes_consumed:]

    def recv_net_info(self):
        variable_cell, bytes_consumed = unpack_cell(self._buffer)
        self._buffer = self._buffer[bytes_consumed:]
        time = list(variable_cell.payload[: 4])
        other_address_type = list(variable_cell.payload[(4): (4 + (2))])
        other_address = list(variable_cell.payload[4 + 2: (4 + 2 + 4)])
        unknown = list(variable_cell.payload[(4 + 6): ((4 + 6)) + (1)])
        my_addr_type = list(variable_cell.payload[(4 + 6) + (1): ((4 + 6) + (1)) + 2])
        my_addr = list(variable_cell.payload[(4 + 6) + 1 + 2: ((4 + 6) + (1)) + 2 + 4])
        print(list(variable_cell.payload[:25]))
        print(time)
        print(other_address_type)
        print(other_address)
        print(unknown)
        print(my_addr_type)
        print(my_addr)


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
