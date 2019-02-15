from sockets.my_socket import SocketInfo

class TorClient:
    socket_info: SocketInfo = None

    def __init__(self, socket_info: SocketInfo):
        self.socket_info = socket_info

    def send_versions(self):
        fake_versions_cell = bytes([0, 0]) + bytes([7]) + bytes([0, 2]) + bytes([0, 3])
        self.socket_info.socket.send(fake_versions_cell)
        # self.my_socket.socket.receive(100)
        # mySocket.receive()


'''
struct fixed_cell
{
    uint16 circuti_id
    uint8 command
    uint8[509] payload
}

struct variable_cell
{
    uint16 circuti_id
    uint8 command
    uint16 payload_length
    uint8[payload_length] payload
}
'''
