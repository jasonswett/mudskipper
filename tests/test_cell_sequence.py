import pytest
from src.cell_sequence import CellSequence

def test_cell_sequence():
    cell_sequence = CellSequence([
        (0, 0, 0),
        (0, -1, 1),
        (1, -1, 0),
    ])

    cells = cell_sequence.cells
    assert cells[2].q == 1
    assert cells[2].r == -2
    assert cells[2].s == 1
