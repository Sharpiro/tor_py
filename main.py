from py_socket.cells import (
    unpack_variable_cell, pack_variable_cell, cell_type, CellType,
    VersionsPayload, pack_versions_payload, unpack_versions_payload,
    VariableCell
)
from py_socket.sockets import create_tls_socket
from py_socket.clients import TorClient

# # external_url = "109.70.100.11"
external_url = "128.31.0.61"
# inernal_url = ''
# proxy_url = ""

socket_info = create_tls_socket(external_url)
tor_client = TorClient(socket_info)
tor_client.send_versions()

# # fake_versions_cell = bytes([7]) + bytes([0, 0, 0, 0]) + bytes([0, 6]) + bytes([0, 1, 0, 3, 0, 5])
# fake_create2_cell = bytes([1, 33, 248, 96]) + bytes([10]) + bytes([0, 2]) + bytes([0, 84]) + bytes(500)
# no_proxy_socket.my_socket.send(fake_versions_cell)
# no_proxy_socket.receive()

# proxy_socket = MySocket(external_url, proxy_url)
# proxy_socket.http_get()

# print(list((pack('hhl', 1, 2, 3))))

# http_socket = create_http_socket("google.com")
# socket = create_tls_socket("google.com")
# temp = TorClient(None)
# print(temp)
