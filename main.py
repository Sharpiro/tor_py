from py_socket.cells import (
    unpack_variable_cell, pack_variable_cell, cell_type, CellType,
    VersionsPayload, pack_versions_payload, unpack_versions_payload,
    VariableCell
)
from py_socket.sockets import create_tls_socket
from py_socket.clients import TorClient
import base64
import hashlib
# # external_url = "109.70.100.11"
external_url = "128.31.0.61"

# ntor_onion_key = base64.b64decode("7jxzpYYdzuvsWgyGQIjfaIcdyw2nLliAdDVsAxVm3Bw=")
# master_key_ed25519 = base64.b64decode("OJi2i6K6x9JhhyU2sD5iiamiK/1hLMzGc7w69HHVQQM=")
# rsa_signing_key = base64.b64decode("MIGJAoGBAMOi1FV0CdvtCBXiokmeYjyzs9aeSj3FOVbii64F8kE/+sshO2TbMv1PTjNnC6FeZ0v0AW6i35tWjFdyRzKdC3XPk1bS1A5C5xZupC+/jsPRB3w0GITWalSWLvbNQwuix9v4hS4wKySdypx7JU0KSFt1pbZHOf7OsbnO047w4EApAgMBAAE=")
# expected_server_identity_digest = hashlib.sha1(rsa_signing_key).digest()
# actual_server_identity_digest = bytes.fromhex("9715C81BA8C5B0C698882035F75C67D6D643DBE3")
# print(len(rsa_signing_key)*8)
# print(list(expected_server_identity_digest))
# print(list(actual_server_identity_digest))
# assert expected_server_identity_digest == actual_server_identity_digest

socket_info = create_tls_socket(external_url)
tor_client = TorClient(socket_info)
tor_client.initialize()
