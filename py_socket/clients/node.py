from py_socket.sockets import SocketInfo
import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Cipher.AES import AESCipher
from Crypto.Util import Counter


class Node:
    def __init__(self, ip_addr: str, onion_key: str, rsa_signing_key: str, socket: SocketInfo = None):
        self.ip_addr = ip_addr
        self.onion_key = base64.b64decode(onion_key)
        self.rsa_signing_key = base64.b64decode(rsa_signing_key)
        self.server_identity_digest = hashlib.sha1(self.rsa_signing_key).digest()
        self.socket = socket
        self.buffer: bytes
        self.version: int
        self._key_forward: str
        self._key_backward: str
        self._digest_forward = hashlib.sha1()
        self._digest_backward = hashlib.sha1()
        self._cipher_forward: AESCipher
        self._cipher_backward: AESCipher

    def init_ciphers(self, key_forward: str, key_backward: str):
        self._key_forward = key_forward
        self._key_backward = key_backward
        self._cipher_forward = AES.new(key_forward, AES.MODE_CTR, counter=Counter.new(128, initial_value=0))
        self._cipher_backward = AES.new(key_backward, AES.MODE_CTR, counter=Counter.new(128, initial_value=0))

    def update_digest_forward(self, data: bytes):
        self._digest_forward.update(data)

    def get_digest_forward(self) -> bytes:
        return self._digest_forward.digest()

    def update_digest_backward(self, data: bytes):
        self._digest_backward.update(data)

    def get_digest_backward(self) -> bytes:
        return self._digest_backward.digest()

    def encrypt_forward(self, plaintext) -> bytes:
        ciphertext = self._cipher_forward.encrypt(plaintext)
        return ciphertext

    def decrypt_forward(self, ciphertext) -> bytes:
        plaintext = self._cipher_forward.decrypt(ciphertext)
        return plaintext

    def encrypt_backward(self, plaintext) -> bytes:
        ciphertext = self._cipher_backward.encrypt(plaintext)
        return ciphertext

    def decrypt_backward(self, ciphertext) -> bytes:
        plaintext = self._cipher_backward.decrypt(ciphertext)
        return plaintext

    def to_json(self) -> str:
        obj = {
            "a": "a",
        }
        return obj
