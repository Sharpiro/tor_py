from client import MySocket
from ctypes import (
    Union, Array,
    c_uint8, c_uint32,
    cdll, CDLL
)


class TorSocket:
    def __init__(self, mySocket: MySocket):
        self.my_socket = mySocket

    def send_versions(self):
        print("doing tor stuff...")
        fake_versions_cell = bytes(
            [0, 0]) + bytes([7]) + bytes([0, 2]) + bytes([0, 3])
        self.my_socket.tls_socket.send(fake_versions_cell)
        # self.my_socket.tls_socket.receive(100)
        # mySocket.receive()


class uint8_array(Array):
    _type_ = c_uint8
    _length_ = 4


class u_type(Union):
    _fields_ = ("data", c_uint32), ("chunk", uint8_array)


class Test:
    def __init__(self):
        pass


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
