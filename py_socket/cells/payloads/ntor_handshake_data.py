class NtorHandshakeData:
    def __init__(self, eph_my_private_key: bytes, eph_my_public_key: bytes, server_identity_digest: bytes, onion_key: bytes):
        self.handshake_type = 2
        self.eph_my_private_key = eph_my_private_key
        self.eph_my_public_key = eph_my_public_key
        self.server_identity_digest = server_identity_digest
        self.onion_key = onion_key

    def pack(self):
        handshake_type_buffer = bytes([0, self.handshake_type])
        handshake_data = self.server_identity_digest + self.onion_key + self.eph_my_public_key
        handshake_length_buffer = bytes([0, len(handshake_data)])
        payload_buffer = handshake_type_buffer + handshake_length_buffer + handshake_data
        return payload_buffer

    def serialize(self):
        return {
            "handshakeType": self.handshake_type,
            "ephMyPrivateKey": list(self.eph_my_private_key),
            "ephMyPublicKey": list(self.eph_my_public_key),
            "serverIdentityDigest": list(self.server_identity_digest),
            "onionKey": list(self.onion_key)
        }
