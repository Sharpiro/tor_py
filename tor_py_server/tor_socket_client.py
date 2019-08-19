from py_socket import(
    TorClient, unpack_created2_payload, get_url_info, unpack_relay_payload,
    RelayType, unpack_relay_connected_payload)
from py_socket.clients.http_generator import HttpGenerator

from tor_py_server.socket_wrapper import SocketWrapper
import asyncio


class TorSocketClient:
    def __init__(self, tor_client: TorClient, socket_wrapper: SocketWrapper):
        self.tor_client = tor_client
        self.socket_wrapper = socket_wrapper

    async def start(self):
        # initial connection
        versions_payload = self.tor_client.create_versions_payload()
        versions_cell = self.tor_client.create_versions_cell(versions_payload)
        # serialized_cell["payload"] = versions_payload.serialize()
        send_versions_data = {
            "cell": versions_cell.serialize(),
            "payload": versions_payload.serialize()
        }
        self.tor_client.send_cell(versions_cell)
        await self.socket_wrapper.send_message("sendVersions", send_versions_data)
        self.tor_client.recv_versions()
        # await self.socket_wrapper.send_message("recv_versions", "recv_versions")
        self.tor_client.recv_certs()
        # await self.socket_wrapper.send_message("recv_certs", "recv_certs")
        self.tor_client.recv_auth_challenge()
        # await self.socket_wrapper.send_message("recv_auth_challenge", "recv_auth_challenge")
        self.tor_client.recv_net_info()
        # await self.socket_wrapper.send_message("recv_net_info", "recv_net_info")

        # create2
        create_handshake_data = self.tor_client.get_ntor_handshake_data(self.tor_client.guard_node)
        create2_cell = self.tor_client.create_create2(create_handshake_data)
        self.tor_client.send_cell(create2_cell)
        create2_data = {
            "cell": create2_cell.serialize(),
            "handshakeData": create_handshake_data.serialize()
        }
        await self.socket_wrapper.send_message("sendCreate2", create2_data)

        # created2
        created2_cell = self.tor_client.recv_cell(self.tor_client.guard_node, TorClient.CELL_SIZE)
        created2_payload = unpack_created2_payload(created2_cell.payload)
        self.tor_client.process_created2(create_handshake_data, created2_payload, self.tor_client.guard_node)
        created2_data = {
            "cell": created2_cell.serialize(),
            "payload": created2_payload.serialize()
        }
        await self.socket_wrapper.send_message("recvCreated2", created2_data)

        # extend2
        extend_handshake_data = self.tor_client.get_ntor_handshake_data(self.tor_client.exit_node)
        extend_cell = self.tor_client.create_relay_extend2_cell(extend_handshake_data)
        self.tor_client.send_cell(extend_cell)
        extend2_data = {
            "cell": extend_cell.serialize(),
            "handshakeData": extend_handshake_data.serialize()
        }
        await self.socket_wrapper.send_message("sendExtend2", extend2_data)

        # extended2
        extended2_cell = self.tor_client.recv_cell(self.tor_client.guard_node, TorClient.CELL_SIZE)
        created2_payload = unpack_created2_payload(extended2_cell.payload[11:])
        self.tor_client.process_created2(extend_handshake_data, created2_payload, self.tor_client.exit_node)
        extended2_data = {
            "cell": extended2_cell.serialize(),
            "payload": created2_payload.serialize()
        }
        await self.socket_wrapper.send_message("recvExtended2", extended2_data)

        # send http request
        http_url = "http://torpy.blob.core.windows.net/tor-blobs/tor.txt"
        url_info = get_url_info(http_url)

        relay_resolve_cell = self.tor_client.create_relay_resolve(url_info.hostname)
        self.tor_client.send_cell(relay_resolve_cell)
        relay_resolve_data = {
            "cell": relay_resolve_cell.serialize(),
            "hostname": url_info.hostname
        }
        await self.socket_wrapper.send_message("sendRelayResolve", relay_resolve_data)

        relay_resolved_cell = self.tor_client.recv_cell(self.tor_client.exit_node, TorClient.CELL_SIZE)
        relay_payload = unpack_relay_payload(relay_resolved_cell.payload)
        ip_address_bytes = relay_payload.data[2:6]
        ip_address = ".".join(str(x) for x in ip_address_bytes)
        relay_resolved_data = {
            "cell": relay_resolved_cell.serialize(),
            "ipAddress": ip_address
        }
        await self.socket_wrapper.send_message("recvRelayResolved", relay_resolved_data)

        addr_port = bytes(f"{ip_address}:{url_info.port}\x00", "utf8")
        relay_begin_cell = self.tor_client.get_encrypted_relay_cell(RelayType.RELAY_BEGIN, addr_port)
        # self.tor_client.send_relay_begin(addr_port)
        self.tor_client.send_cell(relay_begin_cell)
        relay_begin_data = {
            "cell": relay_begin_cell.serialize(),
            "addrPort": str(addr_port, "utf8")[:-1]
        }
        await self.socket_wrapper.send_message("sendRelayBegin", relay_begin_data)

        relay_connected_cell = self.tor_client.recv_cell(self.tor_client.exit_node, TorClient.CELL_SIZE)
        relay_payload = unpack_relay_payload(relay_connected_cell.payload)
        relay_connected_payload = unpack_relay_connected_payload(relay_payload.data[:relay_payload.length])
        relay_connected_data = {
            "cell": relay_connected_cell.serialize(),
            "payload": {
                "ipAddress": relay_connected_payload.ip_address,
                "ttl": relay_connected_payload.ttl
            }
        }
        await self.socket_wrapper.send_message("recvRelayConnected", relay_connected_data)

        http_generator = HttpGenerator(url_info.hostname)
        get_request = http_generator.create_get_request(url_info.path)
        relay_cell = self.tor_client.create_relay_cell(get_request)
        self.tor_client.send_cell(relay_cell)
        relay_data = {
            "cell": relay_cell.serialize(),
            "payload": str(get_request, "utf8")
        }
        await self.socket_wrapper.send_message("sendRelayData", relay_data)

        recv_relay_data_cell = self.tor_client.recv_cell(self.tor_client.exit_node, TorClient.CELL_SIZE)
        relay_payload = unpack_relay_payload(recv_relay_data_cell.payload)
        relay_data = {
            "cell": recv_relay_data_cell.serialize(),
            "payload": str(relay_payload.data[:relay_payload.length], "utf8")
        }
        await self.socket_wrapper.send_message("recvRelayData", relay_data)

        # todo: add relay end
