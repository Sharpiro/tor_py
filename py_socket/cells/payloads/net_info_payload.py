class NetInfoPayload:
    TIMESTAMP_SIZE = 4
    ADDRESS_TYPE_SIZE = 1
    ADDRESS_SIZE = 4
    PAYLOAD_SIZE = TIMESTAMP_SIZE + ADDRESS_TYPE_SIZE + ADDRESS_SIZE

    timestamp: int = 0
    address_type: int = 0
    address: int = 0

    def __repr__(self):
        return "(timestamp: {0}, address_type: {1}, address: {2})".format(self.timestamp, self.address_type, self.address)