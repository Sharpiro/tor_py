from struct import pack, unpack


class NetInfoPayload:
    TIMESTAMP_SIZE = 4
    ADDRESS_TYPE_SIZE = 1
    ADDRESS_LENGTH_SIZE = 1
    ADDRESS_SIZE = 4
    NUMBER_OF_MY_ADDRESSES_SIZE = 1
    PAYLOAD_SIZE = (TIMESTAMP_SIZE + ADDRESS_TYPE_SIZE * 2 +
                    ADDRESS_LENGTH_SIZE * 2 + ADDRESS_SIZE * 2 +
                    NUMBER_OF_MY_ADDRESSES_SIZE)

    def __init__(
        self,
        timestamp: int = 0,
        other_address_type: int = 0,
        other_address_length: int = 0,
        other_address: bytes = None,
        my_addresses_amount: int = 0,
        my_address_type: int = 0,
        my_address_length: int = 0,
        my_address: bytes = None
    ):
        self.timestamp = timestamp
        self.other_address_type = other_address_type
        self.other_address_length = other_address_length
        self.other_address = other_address
        self.my_addresses_amount = my_addresses_amount
        self.my_address_type = my_address_type
        self.my_address_length = my_address_length
        self.my_address = my_address

    def __repr__(self):
        return ("(timestamp: {0}, other_address_type: {1}, other_address_length: {2})"
                "derp"
                ).format(self.timestamp, self.other_address_type, self.other_address)


def unpack_net_info_payload(buffer: bytes) -> NetInfoPayload:
    net_info_payload = NetInfoPayload(
        *unpack('>LBB4sBBB4s', buffer[:NetInfoPayload.PAYLOAD_SIZE]))
    return net_info_payload


def pack_net_info_payload(payload: NetInfoPayload) -> bytes:
    buffer = pack('>LBB4sBBB4s', payload.timestamp, payload.other_address_type,
                  payload.other_address_length, payload.other_address, payload.my_addresses_amount,
                  payload.my_address_type, payload.my_address_length, payload.my_address)
    return buffer
