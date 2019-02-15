from unittest import TestCase
from py_socket.cells import CellType, VariableCell, pack_variable_cell, unpack_variable_cell

class VariableCellTests(TestCase):
    def test_pack(self):
        payload_buffer = bytes([1, 2, 3, 4, 5])
        variable_cell = VariableCell(0, CellType.versions, payload_buffer)
        expected_buffer = bytes([0, 0]) + bytes([7])+ bytes([0, 5]) + bytes([1, 2, 3, 4, 5])
        actual_buffer = pack_variable_cell(variable_cell)
        self.assertListEqual(list(expected_buffer), list(actual_buffer))
      

    def test_unpack(self):
        variable_cell_buffer = bytes([0, 0]) + bytes([7])+ bytes([0, 5]) + bytes([1, 2, 3, 4, 5])
        variable_cell, bytes_read = unpack_variable_cell(variable_cell_buffer)
        self.assertEqual(0, variable_cell.circuit_id)
        self.assertEqual(7, variable_cell.command.value)
        self.assertEqual(5, variable_cell.payload_length)
        self.assertEqual(variable_cell_buffer[-5:], variable_cell.payload)
        self.assertEqual(10, bytes_read)