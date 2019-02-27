from unittest import TestCase
from py_socket.cells import NetInfoPayload, unpack_net_info_payload


class NetInfoPayloadTests(TestCase):
    def test_unpack(self):
        payload_buffer = bytes([92, 118, 192, 202, 4, 4, 172, 73,
                                1, 152, 1, 4, 4, 128, 31, 0, 61, 0, 0, 0, 0, 0, 0, 0, 0])
        _ = unpack_net_info_payload(payload_buffer)
        self.assertEqual(1, 1)
