from struct import unpack, pack
from py_socket.cells.cell_type import CellType


class Cell:
    CICRUIT_ID_SIZE = 2
    COMMAND_SIZE = 1
    HEADER_SIZE = CICRUIT_ID_SIZE + COMMAND_SIZE
    PAYLOAD_LENGTH = 509
    PACK_FORMAT = "HB" if CICRUIT_ID_SIZE == 2 else "LB"

    circuit_id: int = 0
    command: CellType = 0
    payload: bytes = bytes()

    def __init__(self, circuit_id: int, command: CellType, payload: bytes):
        self.circuit_id = circuit_id
        self.command = command
        self.payload = payload

    def __repr__(self):
        return "(circuit_id: {0}, command: {1}, payload_length: {2}, payload: {3})".format(self.circuit_id, self.command, len(self.payload), list(self.payload))


def unpack_cell(buffer: bytes) -> (Cell, int):
    circuit_id, command = unpack(
        f">{Cell.PACK_FORMAT}", buffer[:Cell.HEADER_SIZE])
    payload = unpack(f">{Cell.PAYLOAD_LENGTH}s",
                     buffer[Cell.HEADER_SIZE:Cell.HEADER_SIZE + Cell.PAYLOAD_LENGTH])[0]
    cell = Cell(circuit_id, CellType(command), payload)
    bytes_consumed = Cell.HEADER_SIZE + Cell.PAYLOAD_LENGTH
    return (cell, bytes_consumed)


def pack_cell(cell: Cell) -> bytes:
    padding_length = 509 - len(cell.payload)
    padded_payload = cell.payload + bytes(padding_length)
    buffer = pack(">HB509s", cell.circuit_id, cell.command.value, padded_payload)
    return buffer
