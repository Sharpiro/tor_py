import socket
import ssl
from py_socket.sockets.my_socket import SocketInfo, _get_host_and_port, _wrap_tls_socket, create_tls_socket


class HttpSocket(SocketInfo):

    def __init__(self, url: str, host: str, port: int, socket):
        super().__init__(url, host, port, socket)

    def http_get(self):
        request = bytearray("GET / HTTP/1.1\r\nHost: " + self.host + "\r\n\r\n", "utf8")
        self.socket.send(request)
        initial_response = self.socket.recv(1024)
        print(initial_response)
        return

def create_http_socket(url):
    tls_socket = create_tls_socket(url)
    http_socket = HttpSocket(tls_socket.url, tls_socket.host, tls_socket.port, tls_socket.socket)
    return http_socket

def create_http_proxy_socket(url, proxyUrl):
    proxy_host, proxy_port = _get_host_and_port(proxyUrl)
    host, _ = _get_host_and_port(url)
    plain_socket = socket.create_connection((proxy_host, proxy_port))
    _http_connect(plain_socket, url)
    tls_socket = _wrap_tls_socket(plain_socket, host)
    return tls_socket

def _http_connect(proxy_socket, url):
    request = bytearray(f"CONNECT {url} HTTP/1.1\r\n\r\n", "utf8")
    proxy_socket.send(request)
    initial_response = proxy_socket.recv(1024)
    print(initial_response)
    return