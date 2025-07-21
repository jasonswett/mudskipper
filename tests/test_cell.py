import pytest
import math
from src.cell import Cell
from src.screen import Screen

def test_cell_initialization():
    green = (0, 255, 0)
    cell = Cell((1, -1, 0), 10, green, (0, 0, 0))
    
    assert cell.q == 1
    assert cell.r == -1
    assert cell.s == 0
    assert cell.radius == 10
    assert cell.border_color == (0, 255, 0)

def test_cell_coordinate_relationships():
    radius = 2
    cell1 = Cell((0, 0, 0), radius, (0, 255, 0), (0, 0, 0))
    cell2 = Cell((1, 0, -1), radius, (0, 255, 0), (0, 0, 0))
    assert cell2.center_x() - cell1.center_x() == 3
    assert (cell2.center_y() - cell1.center_y()) - 1.732 < 0.001

    # cell3 is straight above cell2
    cell3 = Cell((1, 1, -2), radius, (0, 255, 0), (0, 0, 0))
    assert cell3.center_x() - cell2.center_x() == 0
    assert (cell3.center_x() - cell1.center_x()) - 3.464 < 0.001

def test_stimulation_color():
    from src.cellular_body import CellularBody

    green = (0, 255, 0)
    original_fill_color = (0, 0, 0)
    cell = Cell((1, -1, 0), 1, green, original_fill_color)
    CellularBody([cell])

    cell.stimulate()
    cell.update_clock()
    assert cell.fill_color == Cell.STIMULATION_COLOR

    for i in range(Cell.STIMULATION_DURATION):
        cell.update_clock()
    assert cell.fill_color == original_fill_color

def test_stimulation_duration():
    green = (0, 255, 0)
    original_fill_color = (0, 0, 0)
    cell = Cell((1, -1, 0), 1, green, original_fill_color)

    cell.stimulate()
    cell.update_clock()

    for i in range(Cell.STIMULATION_DURATION - 1):
        cell.update_clock()
    assert cell.fill_color == Cell.STIMULATION_COLOR

def test_stimulate_neighbor():
    from src.cellular_body import CellularBody
    cell = Cell((0, 0, 0), 1, (0, 0, 0), (0, 0, 0))
    neighbor_cell = Cell((0, 1, -1), 1, (0, 0, 0), (0, 0, 0))

    cellular_body = CellularBody([cell, neighbor_cell])
    cell.stimulate()
    assert neighbor_cell.stimulation_count == 0

    for i in range(Cell.STIMULATION_DURATION - 1):
        cellular_body.update_clock()
    assert neighbor_cell.stimulation_count == 0

    for i in range(Cell.STIMULATION_PROPAGATION_DELAY):
        cellular_body.update_clock()
    assert neighbor_cell.stimulation_count == 1

def test_refractory_period():
    from src.cellular_body import CellularBody
    cell = Cell((0, 0, 0), 1, (0, 0, 0), (0, 0, 0))
    neighbor_cell = Cell((0, 1, -1), 1, (0, 0, 0), (0, 0, 0))

    cellular_body = CellularBody([cell, neighbor_cell])
    cell.stimulate()

    ticks_until_next_stimulation = Cell.STIMULATION_DURATION + Cell.STIMULATION_PROPAGATION_DELAY
    for i in range(ticks_until_next_stimulation * 2):
        cellular_body.update_clock()

    assert cell.stimulation_count == 1
