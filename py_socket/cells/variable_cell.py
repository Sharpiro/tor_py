from struct import unpack, pack
from py_socket.cells.cell_type import CellType

class VariableCell:
    CICRUIT_ID_SIZE = 2
    COMMAND_SIZE = 1
    PAYLOAD_LENGTH_SIZE = 2
    HEADER_SIZE = CICRUIT_ID_SIZE + COMMAND_SIZE + PAYLOAD_LENGTH_SIZE
    PACK_FORMAT = "HBH" if CICRUIT_ID_SIZE == 2 else "LBH"

    circuit_id: int = 0
    command: CellType = 0
    payload_length: int = 0
    payload: bytes = bytes()

    def __init__(self, circuit_id: int, command: CellType, payload: bytes):
        self.circuit_id = circuit_id
        self.command = command
        self.payload_length = len(payload)
        self.payload = payload

    def __repr__(self):
        return "(circuit_id: {0}, command: {1}, payload_length: {2}, payload: {3})".format(self.circuit_id, self.command, self.payload_length, list(self.payload))


def unpack_variable_cell(buffer: bytes) -> (VariableCell, int):
    circuit_id, command, payload_length = unpack(f">{VariableCell.PACK_FORMAT}", buffer[:VariableCell.HEADER_SIZE])
    payload = unpack(f">{payload_length}s", buffer[VariableCell.HEADER_SIZE:VariableCell.HEADER_SIZE + payload_length])[0]
    variable_cell = VariableCell(circuit_id, CellType(command), payload)
    bytes_consumed = VariableCell.HEADER_SIZE + payload_length
    return (variable_cell, bytes_consumed)


def pack_variable_cell(variable_cell: VariableCell) -> bytes:
    headers_buffer = pack(f">{variable_cell.PACK_FORMAT}", variable_cell.circuit_id, variable_cell.command.value, variable_cell.payload_length)
    full_buffer = headers_buffer + variable_cell.payload
    return full_buffer
    