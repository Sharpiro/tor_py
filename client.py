import socket
import ssl
import pprint


class MySocket:
    def __init__(self, url: str, proxyUrl: str = None):
        self.url = url
        self.proxyUrl = proxyUrl
        self.host, self.port = self.get_host_and_port(url)
        if proxyUrl == None:
            self.tls_socket = self.get_socket_no_proxy()
        else:
            self.tls_socket = self.get_socket_proxy()

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
        self.tls_socket.send(request)
        initial_response = self.tls_socket.recv(1024)
        print(initial_response)
        return

    def receive(self):
        while True:
            initial_response = self.tls_socket.recv(1024)
            print(list(initial_response))
        return


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
