import pytest
from src.cellular_body import CellularBody
from src.cell import Cell

def test_cellular_body_initialization_with_cell_hexagons():
    white = (255, 255, 255)
    cell_hexagon = Cell((0, 0, 0), 1, white, white)
    cellular_body = CellularBody([cell_hexagon])
    assert len(cellular_body.cells) == 1

def test_is_legal_true():
    white = (255, 255, 255)
    cell_hexagon = Cell((0, 0, 0), 1, white, white)
    cellular_body = CellularBody([cell_hexagon])
    assert cellular_body.is_legal()

def test_is_legal_false():
    white = (255, 255, 255)
    cell_hexagon = Cell((0, 0, 0), 1, white, white)
    conflicting_cell_hexagon = Cell((0, 0, 0), 1, white, white)
    cellular_body = CellularBody([cell_hexagon, conflicting_cell_hexagon])
    assert not cellular_body.is_legal()
