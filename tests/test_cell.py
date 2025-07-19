import pytest
from src.cell import Cell

def test_cell_initialization():
    green = (0, 255, 0)
    cell = Cell((1, -1, 0), 10, green)
    
    assert cell.x == 1
    assert cell.y == -1
    assert cell.z == 0
    assert cell.radius == 10
    assert cell.color == (0, 255, 0)
