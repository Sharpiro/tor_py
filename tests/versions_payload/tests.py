from unittest import TestCase
from py_socket.cells import VersionsPayload, pack_versions_payload, unpack_versions_payload

class VersionsPayloadTests(TestCase):
    def test_pack(self):
        versions_payload = VersionsPayload([3, 4, 5])
        expected_payload_buffer = [0, 3, 0, 4, 0, 5]
        actual_payload_buffer = pack_versions_payload(versions_payload)
        self.assertListEqual(expected_payload_buffer, list(actual_payload_buffer))
        

    def test_unpack(self):
        versions_payload_buffer = bytes([0, 3, 0, 4, 0, 5])
        expected_versions = [3, 4, 5]
        actual_versions_payload = unpack_versions_payload(versions_payload_buffer)
        self.assertListEqual(expected_versions, actual_versions_payload.versions)
        