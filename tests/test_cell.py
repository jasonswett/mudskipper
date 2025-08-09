import pytest
import math
from src.cell import Cell
from src.cell_factory import CellFactory
from src.screen import Screen

def test_cell_initialization():
    green = (0, 255, 0)
    cell = Cell((1, -1, 0), 10, green, (0, 0, 0), [(0, 1, -1), (0, 0, 0)])

    assert cell.q == 1
    assert cell.r == -1
    assert cell.s == 0
    assert cell.radius == 10
    assert cell.border_color == (0, 255, 0)
    assert cell.movement_deltas[0] == (0, 1, -1)

def test_cell_coordinate_relationships():
    radius = 2
    cell1 = CellFactory.create("default", (0, 0, 0), radius, (0, 255, 0), (0, 0, 0), [(0, 0, 0), (0, 0, 0)])
    cell2 = CellFactory.create("default", (1, 0, -1), radius, (0, 255, 0), (0, 0, 0), [(0, 0, 0), (0, 0, 0)])

    # Calculate centers directly
    def center_x(cell):
        return (3/2 * cell.q) * cell.radius

    def center_y(cell):
        return (math.sqrt(3)/2 * cell.q + math.sqrt(3) * cell.r) * cell.radius

    assert center_x(cell2) - center_x(cell1) == 3
    assert (center_y(cell2) - center_y(cell1)) - 1.732 < 0.001

    # cell3 is straight above cell2
    cell3 = CellFactory.create("default", (1, 1, -2), radius, (0, 255, 0), (0, 0, 0), [(0, 0, 0), (0, 0, 0)])

    assert center_x(cell3) - center_x(cell2) == 0
    assert (center_x(cell3) - center_x(cell1)) - 3.464 < 0.001

def test_stimulation_color():
    from src.cellular_body import CellularBody

    green = (0, 255, 0)
    original_fill_color = (0, 0, 0)
    cell = Cell((1, -1, 0), 1, green, original_fill_color, [(0, 0, 0), (0, 0, 0)])
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
    cell = Cell((1, -1, 0), 1, green, original_fill_color, [(0, 0, 0), (0, 0, 0)])

    cell.stimulate()
    cell.update_clock()

    for i in range(Cell.STIMULATION_DURATION - 1):
        cell.update_clock()
    assert cell.fill_color == Cell.STIMULATION_COLOR

def test_stimulate_neighbor():
    from src.cellular_body import CellularBody
    from src.cell_gene import CellGene

    cell = Cell((0, 0, 0), 1, (0, 0, 0), (0, 0, 0), [(0, 0, 0), (0, 0, 0)])
    neighbor_cell = Cell((0, 1, -1), 1, (0, 0, 0), (0, 0, 0), [(0, 0, 0), (0, 0, 0)])

    # Create a gene with stimulation_propagation_delay = 2 (binary 001 = 1, +1 = 2)
    # Full gene: placement(3) + movement1-3(9) + celltype(2) + pulse(7) + propagation(3) = 24 bits
    test_gene = CellGene('000000000000000000000001')
    cell.gene = test_gene
    neighbor_cell.gene = test_gene

    cellular_body = CellularBody([cell, neighbor_cell])
    cell.stimulate()
    assert neighbor_cell.stimulation_count == 0

    for i in range(Cell.STIMULATION_DURATION - 1):
        cellular_body.update_clock()
    assert neighbor_cell.stimulation_count == 0

    for i in range(cell.gene.stimulation_propagation_delay()):
        cellular_body.update_clock()
    assert neighbor_cell.stimulation_count == 1

def test_refractory_period():
    from src.cellular_body import CellularBody
    cell = Cell((0, 0, 0), 1, (0, 0, 0), (0, 0, 0), [(0, 0, 0), (0, 0, 0)])
    neighbor_cell = Cell((0, 1, -1), 1, (0, 0, 0), (0, 0, 0), [(0, 0, 0), (0, 0, 0)])

    cellular_body = CellularBody([cell, neighbor_cell])
    cell.stimulate()

    # Use default propagation delay (1) for refractory test
    ticks_until_next_stimulation = Cell.STIMULATION_DURATION + 1
    for i in range(ticks_until_next_stimulation * 2):
        cellular_body.update_clock()

    assert cell.stimulation_count == 1
