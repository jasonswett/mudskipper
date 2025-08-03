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
    from src.organism_rendering import OrganismRendering
    from src.organism import Organism
    from src.cellular_body import CellularBody
    import Box2D
    
    radius = 2
    cell1 = CellFactory.create("default", (0, 0, 0), radius, (0, 255, 0), (0, 0, 0), [(0, 0, 0), (0, 0, 0)])
    cell2 = CellFactory.create("default", (1, 0, -1), radius, (0, 255, 0), (0, 0, 0), [(0, 0, 0), (0, 0, 0)])
    
    # Create organisms to use OrganismRendering
    world = Box2D.b2World()
    organism1 = Organism(world, CellularBody([cell1]), (0, 0))
    organism2 = Organism(world, CellularBody([cell2]), (0, 0))
    
    rendering1 = OrganismRendering(organism1, None)
    rendering2 = OrganismRendering(organism2, None)
    
    assert rendering2.cell_center_x(cell2) - rendering1.cell_center_x(cell1) == 3
    assert (rendering2.cell_center_y(cell2) - rendering1.cell_center_y(cell1)) - 1.732 < 0.001

    # cell3 is straight above cell2
    cell3 = CellFactory.create("default", (1, 1, -2), radius, (0, 255, 0), (0, 0, 0), [(0, 0, 0), (0, 0, 0)])
    organism3 = Organism(world, CellularBody([cell3]), (0, 0))
    rendering3 = OrganismRendering(organism3, None)
    
    assert rendering3.cell_center_x(cell3) - rendering2.cell_center_x(cell2) == 0
    assert (rendering3.cell_center_x(cell3) - rendering1.cell_center_x(cell1)) - 3.464 < 0.001

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
    cell = Cell((0, 0, 0), 1, (0, 0, 0), (0, 0, 0), [(0, 0, 0), (0, 0, 0)])
    neighbor_cell = Cell((0, 1, -1), 1, (0, 0, 0), (0, 0, 0), [(0, 0, 0), (0, 0, 0)])

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
    cell = Cell((0, 0, 0), 1, (0, 0, 0), (0, 0, 0), [(0, 0, 0), (0, 0, 0)])
    neighbor_cell = Cell((0, 1, -1), 1, (0, 0, 0), (0, 0, 0), [(0, 0, 0), (0, 0, 0)])

    cellular_body = CellularBody([cell, neighbor_cell])
    cell.stimulate()

    ticks_until_next_stimulation = Cell.STIMULATION_DURATION + Cell.STIMULATION_PROPAGATION_DELAY
    for i in range(ticks_until_next_stimulation * 2):
        cellular_body.update_clock()

    assert cell.stimulation_count == 1
