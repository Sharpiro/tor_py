# from py_socket.cells import (
#     unpack_variable_cell, pack_variable_cell, cell_type, CellType,
#     VersionsPayload, pack_versions_payload, unpack_versions_payload,
#     VariableCell
# )
# from py_socket.sockets import create_tls_socket
# from py_socket.clients import TorClient
# import base64
# import hashlib
# from nacl.public import PrivateKey, Box, PublicKey, encoding
# import binascii
# from temp import smult_curve25519, smult_curve25519_base
# # external_url = "109.70.100.11"
external_url = "128.31.0.61"
# import curve25519


# ntor_onion_key = base64.b64decode("7jxzpYYdzuvsWgyGQIjfaIcdyw2nLliAdDVsAxVm3Bw=")
# master_key_ed25519 = base64.b64decode("OJi2i6K6x9JhhyU2sD5iiamiK/1hLMzGc7w69HHVQQM=")
# rsa_signing_key = base64.b64decode("MIGJAoGBAMOi1FV0CdvtCBXiokmeYjyzs9aeSj3FOVbii64F8kE/+sshO2TbMv1PTjNnC6FeZ0v0AW6i35tWjFdyRzKdC3XPk1bS1A5C5xZupC+/jsPRB3w0GITWalSWLvbNQwuix9v4hS4wKySdypx7JU0KSFt1pbZHOf7OsbnO047w4EApAgMBAAE=")
# expected_server_identity_digest = hashlib.sha1(rsa_signing_key).digest()
# actual_server_identity_digest = bytes.fromhex("9715C81BA8C5B0C698882035F75C67D6D643DBE3")
# print(len(rsa_signing_key)*8)
# print(list(expected_server_identity_digest))
# print(list(actual_server_identity_digest))
# assert expected_server_identity_digest == actual_server_identity_digest

# socket_info = create_tls_socket(external_url)
# tor_client = TorClient(socket_info)
# tor_client.initialize()
# temp_hmac = list(tor_client.hmacSha(b"test", b"test2"))
# print(temp_hmac)
# print(bytes([0])+bytes([1]))

# print(curve25519.)


# a_priv = PrivateKey("59d8ccde721ece1f1bdf3dbc6f4d0ef490e276188ccb0d139f0fca43db1132ff", encoding.HexEncoder)
# a_pub = a_priv.public_key

# b_priv = PrivateKey("05933785fb85d99dc155fcf669360787a2965089d3e33e38874ffc9fddbb5f4a", encoding.HexEncoder)
# b_pub = b_priv.public_key

# k_a_b = Box(a_priv, b_pub).shared_key()
# k_b_a = Box(b_priv, a_pub).shared_key()

# sha = hashlib.sha256(k_b_a).hexdigest()

# print( "Alice private: ",binascii.hexlify(a_priv._private_key))
# print( "Alice public: ",binascii.hexlify(a_pub._public_key))

# print( "Bob private: ",binascii.hexlify(b_priv._private_key))
# print( "Bob public: ",binascii.hexlify(b_pub._public_key))

# print( "Bob shared: ",binascii.hexlify(k_a_b))
# print( "Alice shared: ",binascii.hexlify(k_b_a))

# print( "sha: ", sha)


# # a = urandom(32)
# a = bytes(bytearray.fromhex("59d8ccde721ece1f1bdf3dbc6f4d0ef490e276188ccb0d139f0fca43db1132ff"))
# a_pub = smult_curve25519_base(a)

# # b = urandom(32)
# b = bytes(bytearray.fromhex("05933785fb85d99dc155fcf669360787a2965089d3e33e38874ffc9fddbb5f4a"))
# b_pub = smult_curve25519_base(b)

# k_ab = smult_curve25519(a, b_pub)
# k_ba = smult_curve25519(b, a_pub)

# print("Alice private: ", binascii.hexlify(a))
# print("Alice public: ", binascii.hexlify(a_pub))

# print("Bob private: ", binascii.hexlify(b))
# print("Bob public: ", binascii.hexlify(b_pub))

# print("Bob shared: ", binascii.hexlify(k_ba))
# print("Alice shared: ", binascii.hexlify(k_ab))

# sha = hashlib.sha256(k_ba).hexdigest()

# print("sha: ", sha)

from os import urandom
from temp2 import scalarmult, scalarmult_base

# Private keys in Curve25519 can be any 32-byte string.
# a = urandom(32)
a = bytes(bytearray.fromhex("59d8ccde721ece1f1bdf3dbc6f4d0ef490e276188ccb0d139f0fca43db1132ff"))
a_pub = bytes([ord(i) for i in scalarmult_base(a)])

# b = urandom(32)
b = bytes(bytearray.fromhex("05933785fb85d99dc155fcf669360787a2965089d3e33e38874ffc9fddbb5f4a"))
b_pub = bytes([ord(i) for i in scalarmult_base(b)])

# perform Diffie-Hellman computation for alice and bob
k_ab = bytes([ord(i) for i in scalarmult(a, b_pub)]).hex()
k_ba = bytes([ord(i) for i in scalarmult(b, a_pub)]).hex()

# keys should be the same
assert k_ab == k_ba