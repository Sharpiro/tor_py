from py_socket.cells import (
    unpack_variable_cell, pack_variable_cell, cell_type, CellType,
    VersionsPayload, pack_versions_payload, unpack_versions_payload,
    VariableCell
)
from py_socket.sockets import create_tls_socket
from py_socket.clients import TorClient
from Crypto.Cipher import AES
from Crypto.Util import Counter

print(AES)
# import base64
# import hashlib
# import binascii
# # # external_url = "109.70.100.11"
# from curve25519 import scalarmult, scalarmult_base
import secrets
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

# temp = Crypto.Util.Counter
key = b'\xba\x98\xc0l\xee"\x8e|\x06\x14g\xc5\x93\xb5\x18\xb0\x01\x9f \xa3\xa8\xb0\xedgC&\xaa\xb9gg\x00\xec'
obj = AES.new(key, AES.MODE_CTR, counter=Counter.new(128))
# message = b"The answer is no"
message = bytes([1,2,3,4,5])
ciphertext = obj.encrypt(message)
print(ciphertext)
obj2 = AES.new(key, AES.MODE_CTR, counter=Counter.new(128))
print(obj2.decrypt(ciphertext))
