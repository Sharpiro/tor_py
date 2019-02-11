import socket
import ssl
import pprint


class MySocket:
    def __init__(self, url, proxyUrl=None):
        self.url = url
        self.proxyUrl = proxyUrl
        self.host, self.port = self.get_host_and_port(url)
        if proxyUrl == None:
            self.my_socket = self.get_socket_no_proxy()
        else:
            self.my_socket = self.get_socket_proxy()

    def get_host_and_port(self, url):
        host_and_port = url.split(":")
        host = host_and_port[0]
        port = 443 if len(host_and_port) == 1 else int(host_and_port[1])
        return (host, port)

    def get_socket_no_proxy(self):
        host, port = self.get_host_and_port(self.url)
        plain_socket = socket.create_connection((host, port))
        tls_socket = self.get_tls_socket(plain_socket, host)
        return tls_socket

    def get_socket_proxy(self):
        proxy_host, proxy_port = self.get_host_and_port(self.proxyUrl)
        host, _ = self.get_host_and_port(self.url)
        plain_socket = socket.create_connection((proxy_host, proxy_port))
        self.http_connect(plain_socket, self.url)
        tls_socket = self.get_tls_socket(plain_socket, host)
        return tls_socket

    def get_tls_socket(self, socket, host):
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        tls_socket = context.wrap_socket(socket, server_hostname=host)
        return tls_socket

    def http_connect(self, proxy_socket, url):
        request = bytearray(f"CONNECT {url} HTTP/1.1\r\n\r\n", "utf8")
        proxy_socket.send(request)
        initial_response = proxy_socket.recv(1024)
        print(initial_response)
        return

    def http_get(self):
        request = bytearray("GET / HTTP/1.1\r\nHost: " +
                            self.host + "\r\n\r\n", "utf8")
        self.my_socket.send(request)
        initial_response = self.my_socket.recv(1024)
        print(initial_response)
        return

    def receive(self):
        while True:
            initial_response = self.my_socket.recv(1024)
            print(list(initial_response))
        return


# external_url = "109.70.100.11"
external_url = "128.31.0.61"
inernal_url = ''
proxy_url = ""

no_proxy_socket = MySocket(external_url)
# fake_versions_cell = bytes([7]) + bytes([0, 0, 0, 0]) + bytes([0, 6]) + bytes([0, 1, 0, 3, 0, 5])
fake_versions_cell = bytes([0, 0])+ bytes([7]) + bytes([0, 6]) + bytes([0, 1, 0, 3, 0, 5])
# fake_create2_cell = bytes([1, 33, 248, 96]) + bytes([10]) + bytes([0, 2]) + bytes([0, 84]) + bytes(500)
no_proxy_socket.my_socket.send(fake_versions_cell)
no_proxy_socket.receive()

# proxy_socket = MySocket(external_url, proxy_url)
# proxy_socket.http_get()


# headers_end = 0
# for i, _ in enumerate(initial_response):
#     if i + 4 >= len(initial_response): break
#     if initial_response[i] != ord("\r") or initial_response[i+1] != ord('\n'): continue
#     if initial_response[i+2] != ord("\r") or initial_response[i+3] != ord('\n'): continue
#     headers_end = i
#     break

# headers = initial_response[0:headers_end]
# headers_text = headers.decode()

# split = headers_text.split("\r\n")
# pprint.pprint(split)
# content_length = split[len(split)-1]
# pprint.pprint(int(content_length.split(":")[1].strip()))
