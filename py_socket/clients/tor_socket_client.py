from py_socket.clients.tor_client import TorClient, unpack_created2_payload, get_url_info
from py_socket.clients.http_generator import HttpGenerator
from socket_wrapper import SocketWrapper
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
        await self.socket_wrapper.send_message("send_versions", send_versions_data)
        self.tor_client.recv_versions()
        self.tor_client.recv_certs()
        self.tor_client.recv_auth_challenge()
        self.tor_client.recv_net_info()

        # create first hop
        handshake_data = self.tor_client.get_ntor_handshake_data(self.tor_client.guard_node)
        create2_cell = self.tor_client.create_create2(handshake_data)
        self.tor_client.send_cell(create2_cell)
        create2_data = {
            "cell": create2_cell.serialize(),
            "payload": handshake_data.serialize()
        }
        await self.socket_wrapper.send_message("send_create2", create2_data)
        created2_cell = self.tor_client.recv_cell(self.tor_client.guard_node, TorClient.CELL_SIZE)
        # created2_payload = unpack_created2_payload(created2_cell.payload)
        created2_data = {
            "cell": created2_cell.serialize(),
            "payload": "created2_payload"
        }
        await self.socket_wrapper.send_message("recv_created2", created2_data)

        # create second hop
        # create_info = self.tor_client.send_relay_extend2()
        # await self.socket_wrapper.websocket.send("Sent relay extend2 cell")
        # extended2_cell = self.tor_client.recv_cell(self.tor_client.guard_node, TorClient.CELL_SIZE)
        # await self.socket_wrapper.websocket.send("Received relay extended2 cell")
        # created2_payload = unpack_created2_payload(extended2_cell.payload[11:])
        # self.tor_client.recv_created2(create_info, created2_payload, self.tor_client.exit_node)
        # await self.socket_wrapper.websocket.send("Second hop in circuit created")

        # # send http request
        # http_url = "http://statichostsharp.blob.core.windows.net/misc/tor.txt"
        # url_info = get_url_info(http_url)
        # await self.socket_wrapper.websocket.send(f"Sending request to {http_url}")

        # self.tor_client.send_relay_resolve(url_info.hostname)
        # await self.socket_wrapper.websocket.send("Sent relay resolve cell")
        # ip_address_bytes = self.tor_client.recv_relay_resolved()
        # ip_address = ".".join(str(x) for x in ip_address_bytes)
        # addr_port = bytes(f"{ip_address}:{url_info.port}\x00", "utf8")
        # await self.socket_wrapper.websocket.send("Received relay resolved cell")
        # self.tor_client.send_relay_begin(addr_port)
        # await self.socket_wrapper.websocket.send("Sent relay begin cell")
        # self.tor_client.receive_relay_connected()
        # await self.socket_wrapper.websocket.send("Received relay connected cell")

        # http_generator = HttpGenerator(url_info.hostname)
        # get_request = http_generator.create_get_request(url_info.path)
        # self.tor_client.send_relay_data(get_request)
        # await self.socket_wrapper.websocket.send("Sent relay data cell")
        # res = self.tor_client.receive_data()
        # await self.socket_wrapper.websocket.send("Received relay data cell")
        # await self.socket_wrapper.websocket.send(res.decode())
