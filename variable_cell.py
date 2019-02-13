from struct import (unpack)

class VariableCell:
    circuit_id: int = 0
    command: int = 0
    payload_length: int = 0
    payload: bytes = []

    def __repr__(self):
        return "(circuit_id: {0}, command: {1}, payload_length: {2}, payload_data: {3})".format(self.circuit_id, self.command, self.payload_length, list(self.payload_data))

    @staticmethod
    def create(buffer: bytes):
        print(list(buffer))
        variableCell = VariableCell()
        variableCell.circuit_id, variableCell.command, variableCell.payload_length = unpack(
            ">HBH", buffer[:5])
        variableCell.payload_data = unpack(">2s", buffer[5:])[0]
        return variableCell
