import pytest
import math
from src.cell import Cell
from src.screen import Screen

def test_cell_initialization():
    green = (0, 255, 0)
    cell = Cell((1, -1, 0), 10, green)
    
    assert cell.q == 1
    assert cell.r == -1
    assert cell.s == 0
    assert cell.radius == 10
    assert cell.color == (0, 255, 0)

def test_cell_coordinate_relationships():
    radius = 2
    cell1 = Cell((0, 0, 0), radius, (0, 255, 0))
    cell2 = Cell((1, 0, -1), radius, (0, 255, 0))
    assert cell2.center_x() - cell1.center_x() == 3
    assert cell2.center_y() - cell1.center_y() == radius * math.sqrt(3) / 2
