from struct import pack, unpack
from py_socket.cells.relay_type import RelayType


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
        relay_command: RelayType,
        recognized: int = 0,
        stream_id: int = 0,
        digest: bytes = bytes([0, 0, 0, 0]),
        relay_data: bytes = None,
    ):
        self.relay_command = relay_command
        self.recognized = recognized
        self.stream_id = stream_id
        self.digest = digest
        self.length = len(relay_data)

        if len(relay_data) > RelayPayload.DATA_SIZE:
            raise ValueError(f"Relay data surpassed {RelayPayload.DATA_SIZE}")
        if len(relay_data) < RelayPayload.DATA_SIZE:
            relay_data = relay_data + bytes(RelayPayload.DATA_SIZE - self.length)
        self.data = relay_data


def unpack_relay_payload(buffer: bytes) -> RelayPayload:
    unpacked = unpack(f'>BHH4sH{RelayPayload.DATA_SIZE}s', buffer[:RelayPayload.PAYLOAD_LEN])
    relay_data_len = unpacked[4]
    relay_data = unpacked[5][:relay_data_len]
    modified_tuple = (*unpacked[:4], relay_data)
    relay_payload = RelayPayload(*modified_tuple)
    return relay_payload


def pack_relay_payload(payload: RelayPayload) -> bytes:
    buffer = pack(f'>BHH4sH{RelayPayload.DATA_SIZE}s', payload.relay_command.value, payload.recognized,
                  payload.stream_id, payload.digest, payload.length, payload.data)
    return buffer
