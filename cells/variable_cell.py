from struct import unpack, pack

class VariableCell:
    CICRUIT_ID_SIZE = 2
    COMMAND_SIZE = 1
    PAYLOAD_LENGTH_SIZE = 2
    HEADER_SIZE = CICRUIT_ID_SIZE + COMMAND_SIZE + PAYLOAD_LENGTH_SIZE

    circuit_id: int = 0
    command: int = 0
    payload_length: int = 0
    payload: bytes = []

    def __repr__(self):
        return "(circuit_id: {0}, command: {1}, payload_length: {2}, payload_data: {3})".format(self.circuit_id, self.command, self.payload_length, list(self.payload_data))


class VersionsPayload:
    TIMESTAMP_SIZE = 4
    ADDRESS_TYPE_SIZE = 1
    ADDRESS_SIZE = 4
    PAYLOAD_SIZE = TIMESTAMP_SIZE + ADDRESS_TYPE_SIZE + ADDRESS_SIZE

    timestamp: int = 0
    address_type: int = 0
    address: int = 0

    def __repr__(self):
        return "(timestamp: {0}, address_type: {1}, address: {2})".format(self.timestamp, self.address_type, self.address)


def create_variable_cell(buffer: bytes):
    print(list(buffer))
    variable_cell = VariableCell()
    variable_cell.circuit_id, variable_cell.command, variable_cell.payload_length = unpack(">HBH", buffer[:VariableCell.HEADER_SIZE])
    variable_cell.payload_data = unpack(f">{variable_cell.payload_length}s", buffer[VariableCell.HEADER_SIZE:VariableCell.HEADER_SIZE+variable_cell.payload_length])[0]
    bytes_consumed = VariableCell.HEADER_SIZE + variable_cell.payload_length
    return (variable_cell, bytes_consumed)