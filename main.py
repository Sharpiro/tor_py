from py_socket.cells import (
    unpack_variable_cell, pack_variable_cell, cell_type, CellType,
    VersionsPayload, pack_versions_payload, unpack_versions_payload,
    VariableCell
)
from py_socket.sockets import create_tls_socket
from py_socket.clients import TorClient
from Crypto.Cipher import AES
from Crypto.Util import Counter
import hmac
import hashlib

import secrets
# external_url = "128.31.0.61"
external_url = "199.249.230.68"  # exit node

socket_info = create_tls_socket(external_url)
tor_client = TorClient(socket_info)
tor_client.initialize()

# seed = b'12345'
# data = b'54321'
# print(list(hashlib.sha1(seed + data).digest()))

# hashAlg = hashlib.sha1(seed)
# hashAlg.update(data)

# print(list(hashAlg.digest()))


# hashAlg2 = hashlib.new("sha1", seed)
# hashAlg2.update(data)

# print(list(hashAlg2.digest()))

# from Crypto.Cipher import AES
# from Crypto.Util import Counter

# key = bytes(16)
# message = "plain"
# cipher = AES.new(key, AES.MODE_CTR, counter=Counter.new(128))
# ciphertext = cipher.encrypt(message)
# pass


# def HMAC(key, msg):
#     "Return the HMAC-SHA256 of 'msg' using the key 'key'."
#     H = hmac.new(key, b"", hashlib.sha256)
#     H.update(msg)
#     return H.digest()


# def H(msg, tweak):
#     """Return the hash of 'msg' using tweak 'tweak'.  (In this version of ntor,
#        the tweaked hash is just HMAC with the tweak as the key.)"""
#     return HMAC(key=tweak,
#                 msg=msg)


# def kdf_rfc5869(key, salt, info, n):

#     prk = HMAC(key=salt, msg=key)

#     out = b""
#     last = b""
#     i = 1
#     while len(out) < n:
#         m = last + info + bytes([i])
#         last = h = HMAC(key=prk, msg=m)
#         out += h
#         i = i + 1
#     return out[:n]


# proto_id = b"ntor-curve25519-sha256-1"
# t_key = proto_id + b":key_extract"
# m_expand = proto_id + b":key_expand"
# secret_input = bytes(32)

# expected = kdf_rfc5869(key=secret_input, salt=t_key, info=m_expand, n=72)

# actual_seed = tor_client.outer_compute_keys(secret_input, t_key)
# actual = tor_client.compute_keys(actual_seed)


# assert expected[:20] == actual[0]
# assert expected[20:40] == actual[1]
# assert expected[40:56] == actual[2]
# assert expected[56:72] == actual[3]

# print(len(expected))
# print(len(actual[0]+actual[1]+actual[2]+actual[3]))
