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
        await self.socket_wrapper.websocket.send(f"Handshaking w/ guard node {self.tor_client.guard_node.ip_addr}:{self.tor_client.guard_node.socket.port}")
        versions_cell = self.tor_client.create_versions()
        self.tor_client.send_cell(versions_cell)
        await self.socket_wrapper.websocket.send("Sent versions cell")
        self.tor_client.recv_versions()
        await self.socket_wrapper.websocket.send("Received versions cell")
        self.tor_client.recv_certs()
        await self.socket_wrapper.websocket.send("Received certs cell")
        self.tor_client.recv_auth_challenge()
        await self.socket_wrapper.websocket.send("Received auth challenge cell")
        self.tor_client.recv_net_info()
        await self.socket_wrapper.websocket.send("Received net info cell")

        # create first hop
        await self.socket_wrapper.websocket.send(f"Creating circuit w/ guard node {self.tor_client.guard_node.ip_addr}")
        create2_cell, *create_info = self.tor_client.create_create2()
        self.tor_client.send_cell(create2_cell)
        await self.socket_wrapper.websocket.send("Sent create2 cell")
        created2_cell = self.tor_client.recv_cell(self.tor_client.guard_node, TorClient.CELL_SIZE)
        created2_payload = unpack_created2_payload(created2_cell.payload)
        self.tor_client.recv_created2(create_info, created2_payload, self.tor_client.guard_node)
        await self.socket_wrapper.websocket.send("Received created2 cell")
        await self.socket_wrapper.websocket.send("First hop in circuit created")

        # create second hop
        await self.socket_wrapper.websocket.send(f"Extending circuit to exit node {self.tor_client.exit_node.ip_addr}")
        create_info = self.tor_client.send_relay_extend2()
        await self.socket_wrapper.websocket.send("Sent relay extend2 cell")
        extended2_cell = self.tor_client.recv_cell(self.tor_client.guard_node, TorClient.CELL_SIZE)
        await self.socket_wrapper.websocket.send("Received relay extended2 cell")
        created2_payload = unpack_created2_payload(extended2_cell.payload[11:])
        self.tor_client.recv_created2(create_info, created2_payload, self.tor_client.exit_node)
        await self.socket_wrapper.websocket.send("Second hop in circuit created")

        # send http request
        http_url = "http://statichostsharp.blob.core.windows.net/misc/tor.txt"
        url_info = get_url_info(http_url)
        await self.socket_wrapper.websocket.send(f"Sending request to {http_url}")

        self.tor_client.send_relay_resolve(url_info.hostname)
        await self.socket_wrapper.websocket.send("Sent relay resolve cell")
        ip_address_bytes = self.tor_client.recv_relay_resolved()
        ip_address = ".".join(str(x) for x in ip_address_bytes)
        addr_port = bytes(f"{ip_address}:{url_info.port}\x00", "utf8")
        await self.socket_wrapper.websocket.send("Received relay resolved cell")
        self.tor_client.send_relay_begin(addr_port)
        await self.socket_wrapper.websocket.send("Sent relay begin cell")
        self.tor_client.receive_relay_connected()
        await self.socket_wrapper.websocket.send("Received relay connected cell")

        http_generator = HttpGenerator(url_info.hostname)
        get_request = http_generator.create_get_request(url_info.path)
        self.tor_client.send_relay_data(get_request)
        await self.socket_wrapper.websocket.send("Sent relay data cell")
        res = self.tor_client.receive_data()
        await self.socket_wrapper.websocket.send("Received relay data cell")
        await self.socket_wrapper.websocket.send(res.decode())
