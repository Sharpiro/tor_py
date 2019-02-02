# tls_socket = ssl.wrap_socket(plain_socket,
#                        ciphers="HIGH:-aNULL:-eNULL:-PSK:RC4-SHA:RC4-MD5",
#                        ssl_version=ssl.PROTOCOL_TLSv1,
#                        cert_reqs=ssl.CERT_REQUIRED,
#                        ca_certs='/etc/ssl/certs/ca-bundle.crt')

# plain_socket.listen(1)
# print("listening...")
# conn, addr = s.accept()
# print('Connected by', addr)
# while 1:
#     data = conn.recv(1024)
#     if not data: break
#     conn.sendall(data)
# conn.close()