from struct import pack, unpack


class Created2Payload:
    LENGTH_SIZE = 2
    KEY_SIZE = 32

    def __init__(
        self,
        eph_server_public_key: bytes,
        server_auth: bytes,
    ):
        self.length = len(eph_server_public_key) + len(server_auth)
        self.eph_server_public_key = eph_server_public_key
        self.server_auth = server_auth

    def serialize(self):
        return {
            "ephServerPublicKey": list(self.eph_server_public_key),
            "serverAuth": list(self.server_auth)
        }


def unpack_created2_payload(buffer: bytes) -> Created2Payload:
    actual_handshake_length, *_ = unpack(">H", buffer[:2])
    if actual_handshake_length != Created2Payload.KEY_SIZE * 2:
        raise Exception("Invalid key size")

    padding = len(buffer) - Created2Payload.LENGTH_SIZE - Created2Payload.KEY_SIZE*2
    pub, auth, _ = unpack(f'>32s32s{padding}s', buffer[2:len(buffer)])
    created2_payload = Created2Payload(pub, auth)
    return created2_payload
