import websockets
import secrets
import json


class SocketWrapper:
    def __init__(self, websocket: websockets.WebSocketServerProtocol, id=""):
        self.websocket = websocket
        self.id = id if id != "" else secrets.token_hex(32)

    async def send_message(self, title: str, data: str):
        message = {
            "title": title,
            "data": data
        }
        await self.websocket.send(json.dumps(message))
