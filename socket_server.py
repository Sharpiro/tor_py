import asyncio
import datetime
import random
import websockets
import json
import uuid
from py_socket.clients import TorClient, TorSocketClient, Node
from socket_wrapper import SocketWrapper
from py_socket.sockets import create_tls_socket

print("reading file...")


async def consumer_handler(socket: SocketWrapper, path: str):
    async for message in socket.websocket:
        obj = json.loads(message)
        print(obj["title"])
        print(obj["data"])
        print("path", path)
        if obj["title"] == "handshake":
            await socket.send_message("handshake", socket.id)
        elif obj["title"] == "tor":
            await do_tor(socket, message)


async def handler(websocket: websockets.WebSocketServerProtocol, path: str):
    print("user connected...")
    socket = SocketWrapper(websocket)
    consumer_task = asyncio.ensure_future(consumer_handler(socket, path))
    _, pending = await asyncio.wait([consumer_task], return_when=asyncio.FIRST_COMPLETED)
    for task in pending:
        task.cancel()


async def do_tor(socket: SocketWrapper, message: str):
    guard_node = Node("128.31.0.61", "f+XpLjonwta50/OeD71k0oFenh2D+rL/P0f2CxhsbFo=",
                      "MIGJAoGBAMOi1FV0CdvtCBXiokmeYjyzs9aeSj3FOVbii64F8kE/+sshO2TbMv1PTjNnC6FeZ0v0AW6i35tWjFdyRzKdC3XPk1bS1A5C5xZupC+/jsPRB3w0GITWalSWLvbNQwuix9v4hS4wKySdypx7JU0KSFt1pbZHOf7OsbnO047w4EApAgMBAAE=")
    exit_node = Node("176.10.99.201", "yOJokRL2ooq99RZPJ04mNDSfQIZtTA78dKp+c096zU0=",
                     "MIGJAoGBAMw558IiHkrZhEHW83ZjEdWj+vFOP0bHTQqHP+NI7umefWc4VMHcjD0JSclaU2QL/B3mbkNNsct1Zc3nF7HV8F4tG1us1caA36p/Wxzgd8vRHwTixvz82II4KLE02OudCmgWg956JhN0lrI/mRj2SMsOfIMsq+V09qFkrM1HzsDZAgMBAAE=")
    guard_node.socket = create_tls_socket(guard_node.ip_addr)
    tor_client = TorClient(guard_node, exit_node)
    tor_socket_client = TorSocketClient(tor_client, socket)
    await tor_socket_client.start()


# start_server = websockets.serve(handler, "127.0.0.1", 5678)
start_server = websockets.serve(handler, "0.0.0.0", 5678)
print("starting socket server...")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

print("do something e z")
