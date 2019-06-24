from struct import pack, unpack


class RelayPayload:
    PAYLOAD_LEN = 509
    RELAY_COMMAND_SIZE = 1
    RECOGNIZED_SIZE = 2
    STREAM_ID_SIZE = 2
    DIGEST_SIZE = 4
    LENGTH_SIZE = 2
    DATA_SIZE = (PAYLOAD_LEN - (RELAY_COMMAND_SIZE + RECOGNIZED_SIZE +
                                STREAM_ID_SIZE + DIGEST_SIZE + LENGTH_SIZE))

    def __init__(
        self,
        relay_command: int,
        recognized: int = 0,
        stream_id: int = 0,
        digest: int = 0,
        length: int = 0,
        data: bytes = None,
    ):
        self.relay_command = relay_command
        self.recognized = recognized
        self.stream_id = stream_id
        self.digest = digest
        self.length = length
        self.data = data


def unpack_relay_payload(buffer: bytes) -> RelayPayload:
    relay_payload = RelayPayload(
        *unpack(f'>BSSLS{RelayPayload.DATA_SIZE}s', buffer[:RelayPayload.PAYLOAD_LEN]))
    return relay_payload


def pack_relay_payload(payload: RelayPayload) -> bytes:
    buffer = pack(f'>BSSLS{RelayPayload.DATA_SIZE}s', payload.relay_command, payload.recognized,
                  payload.stream_id, payload.digest, payload.length, payload.data)
    return buffer
