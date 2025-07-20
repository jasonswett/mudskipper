import pytest
from src.cell_sequence import CellSequence

def test_cell_sequence():
    cell_sequence = CellSequence([
        (0, 0, 0),
        (0, -1, 1),
        (1, -1, 0),
    ])

    positions = cell_sequence.positions
    assert positions[2] == (1, -2, 1)
