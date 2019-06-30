from py_socket.sockets import SocketInfo
import hashlib
import base64


class Node:
    def __init__(self, url: str, onion_key: str, rsa_signing_key: str, socket: SocketInfo = None):
        self.url = url
        # self.onion_key = onion_key
        self.onion_key = base64.b64decode(onion_key)
        self.rsa_signing_key = base64.b64decode(rsa_signing_key)
        self.server_identity_digest = hashlib.sha1(self.rsa_signing_key).digest()
        self.socket = socket
        self.buffer: bytes
        self.version: int
        self.key_forward: str
        self.key_backward: str
        self._digest_forward = hashlib.sha1()
        self._digest_backward = hashlib.sha1()

    def update_digest_forward(self, data: bytes):
        self._digest_forward.update(data)

    def get_digest_forward(self) -> bytes:
        return self._digest_forward.digest()

    def update_digest_backward(self, data: bytes):
        self._digest_backward.update(data)

    def get_digest_backward(self) -> bytes:
        return self._digest_backward.digest()
