import asyncio
import datetime
import random
import websockets
import json
import uuid
import secrets


class SocketWrapper:

    def __init__(self, websocket: websockets.WebSocketServerProtocol, id=None):
        self.websocket = websocket
        self.id = id if id != None else secrets.token_hex(32)


async def time(socket: SocketWrapper, path):
    while True:
        now = datetime.datetime.utcnow().isoformat() + "Z"
        await socket.websocket.send(now)
        await asyncio.sleep(3)


async def consumer_handler(socket: SocketWrapper, path):
    async for message in socket.websocket:
        await consumer(socket, message)


async def handler(websocket, path):
    print("user connected...")
    socket = SocketWrapper(websocket)
    consumer_task = asyncio.ensure_future(consumer_handler(socket, path))
    producer_task = asyncio.ensure_future(time(socket, path))
    done, pending = await asyncio.wait([consumer_task, producer_task], return_when=asyncio.FIRST_COMPLETED)
    for task in pending:
        task.cancel()


async def handshake(socket: SocketWrapper, message: str):
    message = {
        "title": "handshake",
        "data": socket.id
    }
    await socket.websocket.send(json.dumps(message))


async def consumer(socket: SocketWrapper, message: str):
    obj = json.loads(message)
    print(obj["title"])
    print(obj["data"])
    if obj["title"] == "handshake":
        await handshake(socket, message)


start_server = websockets.serve(handler, "127.0.0.1", 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
