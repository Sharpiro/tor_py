from cells import (
    unpack_variable_cell, pack_variable_cell, cell_type, CellType,
    VersionsPayload, pack_versions_payload, unpack_versions_payload,
    VariableCell
)
import unittest

# # external_url = "109.70.100.11"
# external_url = "128.31.0.61"
# inernal_url = ''
# proxy_url = ""

# no_proxy_socket = MySocket(external_url)
# tor_socket = TorSocket(no_proxy_socket)
# tor_socket.send_versions()

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

# import struct

# int_list = [3, 4, 5]
# fmt = ">" + "H" * len(int_list)
# data = struct.pack(fmt, *int_list)
# print(list(data))

# new_list = list(struct.unpack(fmt, data))
# print(new_list)

# print(CellType.versions.name)
# print(CellType.versions.value)


# create versions payload for sending
versions_payload = VersionsPayload([3, 4, 5])
print(versions_payload)
versions_payload_buffer = pack_versions_payload(versions_payload)
print(list(versions_payload_buffer))
versions_payload = unpack_versions_payload(versions_payload_buffer)
print(versions_payload)

# create variable cell for sending
variable_cell = VariableCell(0, CellType.versions, versions_payload_buffer)
print(variable_cell)
buffer = pack_variable_cell(variable_cell) + bytes(5)
print(list(buffer))
variable_cell, bytes_consumed = unpack_variable_cell(buffer)
print(variable_cell)
print(bytes_consumed)
buffer = buffer[bytes_consumed:]
print(list(buffer))

# buffer = bytes([0, 0]) + bytes([7]) + bytes([0, 2]) + bytes([0, 3]) + bytes(5)
# print(list(buffer))
# variable_cell, bytes_consumed = unpack_variable_cell(buffer)
# print(variable_cell)
# print(bytes_consumed)
# buffer = buffer[bytes_consumed:]
# print(list(buffer))

# print(list(buffer))
