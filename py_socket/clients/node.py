from py_socket.sockets import SocketInfo


class Node:
    def __init__(self, url: str, onion_key: str, rsa_signing_key: str, socket: SocketInfo = None):
        self.url = url
        self.onion_key = onion_key
        self.rsa_signing_key = rsa_signing_key
        self.socket = socket
        self.buffer: bytes
        self.version: int
        self.digest_forward: str
        self.digest_backward: str
        self.key_forward: str
        self.key_backward: str
