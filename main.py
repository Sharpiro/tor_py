from py_socket.cells import (
    unpack_variable_cell, pack_variable_cell, cell_type, CellType,
    VersionsPayload, pack_versions_payload, unpack_versions_payload,
    VariableCell
)
from py_socket.sockets import create_tls_socket
from py_socket.clients import TorClient
from Crypto.Cipher import AES
from Crypto.Util import Counter

import secrets
external_url = "128.31.0.61"

socket_info = create_tls_socket(external_url)
tor_client = TorClient(socket_info)
tor_client.initialize()
