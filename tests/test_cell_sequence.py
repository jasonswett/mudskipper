import pytest
from src.cell_sequence import CellSequence

def test_cell_sequence():
    cell_sequence = CellSequence([
        (0, 0, 0),
        (1, 0, 0),
        (1, 0, 0),
    ])

    cells = cell_sequence.cells
    assert cells[2].x == 2
    assert cells[2].y == 0
    assert cells[2].z == 0
