from sockets.tor_socket import TorClient
# from sockets.my_socket import create_tls_socket
# from variable_cell import create_variable_cell
# from sockets.http_socket import create_http_socket


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


# buffer = bytes([0, 0]) + bytes([7]) + bytes([0, 2]) + bytes([0, 3]) + bytes(50)
# versionCell, bytes_consumed = create_variable_cell(buffer)
# print(versionCell)
# print(bytes_consumed)

# http_socket = create_http_socket("google.com")
# socket = create_tls_socket("google.com")
temp = TorClient(None)
print(temp)