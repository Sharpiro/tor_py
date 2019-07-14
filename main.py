from py_socket.cells import (
    unpack_variable_cell, pack_variable_cell, cell_type, CellType,
    VersionsPayload, pack_versions_payload, unpack_versions_payload,
    VariableCell
)
from py_socket.sockets import create_tls_socket, wrap_tls_socket
from py_socket.clients import TorClient, Node, HttpGenerator, RouterService
from py_socket.tools import get_url_info


# router_service = RouterService("128.31.0.61")
# router_info = router_service.get_router()
# guard_node = Node("128.31.0.61", "f+XpLjonwta50/OeD71k0oFenh2D+rL/P0f2CxhsbFo=", "MIGJAoGBAMOi1FV0CdvtCBXiokmeYjyzs9aeSj3FOVbii64F8kE/+sshO2TbMv1PTjNnC6FeZ0v0AW6i35tWjFdyRzKdC3XPk1bS1A5C5xZupC+/jsPRB3w0GITWalSWLvbNQwuix9v4hS4wKySdypx7JU0KSFt1pbZHOf7OsbnO047w4EApAgMBAAE=")
# exit_node = Node("176.10.99.201", "yOJokRL2ooq99RZPJ04mNDSfQIZtTA78dKp+c096zU0=", "MIGJAoGBAMw558IiHkrZhEHW83ZjEdWj+vFOP0bHTQqHP+NI7umefWc4VMHcjD0JSclaU2QL/B3mbkNNsct1Zc3nF7HV8F4tG1us1caA36p/Wxzgd8vRHwTixvz82II4KLE02OudCmgWg956JhN0lrI/mRj2SMsOfIMsq+V09qFkrM1HzsDZAgMBAAE=")

# guard_node.socket = create_tls_socket(guard_node.url)

# tor_client = TorClient(guard_node, exit_node)
# tor_client.create_circuit()

# http_url = "http://statichostsharp.blob.core.windows.net/misc/tor.txt"
# url_info = get_url_info(http_url)

# tor_client.send_relay_resolve(url_info.hostname)
# ip_address_bytes = tor_client.recv_relay_resolved()
# ip_address = ".".join(str(x) for x in ip_address_bytes)
# addr_port = bytes(f"{ip_address}:{url_info.port}\x00", "utf8")
# tor_client.send_relay_begin(addr_port)
# tor_client.receive_relay_connected()

# http_generator = HttpGenerator(url_info.hostname)
# get_request = http_generator.create_get_request(url_info.path)
# tor_client.send_relay_data(get_request)
# res = tor_client.receive_more()
# print(res)
