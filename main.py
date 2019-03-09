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
# expected_fingerprint = bytes.fromhex("9715C81BA8C5B0C698882035F75C67D6D643DBE3")
# ntor_onion_key = base64.b64decode("7jxzpYYdzuvsWgyGQIjfaIcdyw2nLliAdDVsAxVm3Bw=")
# master_key_ed25519 = base64.b64decode("OJi2i6K6x9JhhyU2sD5iiamiK/1hLMzGc7w69HHVQQM=")
# server_identity_digest = hashlib.sha256(master_key_ed25519).digest()
# print(list(expected_fingerprint))
# # fake_public_key = master_key_ed25519
# handshake_data = server_identity_digest + ntor_onion_key + fake_public_key
# print(list(ntor_onion_key))
# print(list(master_key_ed25519))
# print(list(server_identity_digest))
# print(list(handshake_data))

socket_info = create_tls_socket(external_url)
tor_client = TorClient(socket_info)
tor_client.initialize()
