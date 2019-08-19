from struct import pack, unpack


class RelayConnectedPayload:
    def __init__(
        self,
        ip_address: str,
        ttl: int
    ):
        self.ip_address = ip_address
        self.ttl = ttl


def unpack_relay_connected_payload(buffer: bytes) -> RelayConnectedPayload:
    ip_bytes, ttl = unpack('>4sI', buffer)
    ip_addr = ".".join(str(i) for i in ip_bytes)
    relay_payload = RelayConnectedPayload(ip_addr, ttl)
    return relay_payload
