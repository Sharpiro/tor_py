from py_socket.sockets.socket_info import SocketInfo, _get_host_and_port, wrap_tls_socket, create_tls_socket


class HttpGenerator():

    def __init__(self, host: str):
        self.host = host

    def create_get_request(self, path: str):
        request = bytes(f"GET {path} HTTP/1.1\r\nHost: {self.host}\r\nAccept: */*\r\n\r\n", "utf8")
        return request
