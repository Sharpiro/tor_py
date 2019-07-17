import websockets
import secrets


class SocketWrapper:
    def __init__(self, websocket: websockets.WebSocketServerProtocol, id=None):
        self.websocket = websocket
        self.id = id if id != None else secrets.token_hex(32)
