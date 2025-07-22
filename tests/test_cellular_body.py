import pytest
from src.cellular_body import CellularBody
from src.cell import Cell

def test_cellular_body_initialization_with_cell_hexagons():
    white = (255, 255, 255)
    cell_hexagon = Cell((0, 0, 0), 1, white, white, [(0, 0, 0), (0, 0, 0)])
    cellular_body = CellularBody([cell_hexagon])
    assert len(cellular_body.cells) == 1

def test_neighbors_on_initialization():
    cell = Cell((0, 0, 0), 1, (0, 0, 0), (0, 0, 0), [(0, 0, 0), (0, 0, 0)])
    neighbor_cell = Cell((0, 1, -1), 1, (0, 0, 0), (0, 0, 0), [(0, 0, 0), (0, 0, 0)])
    cellular_body = CellularBody([cell, neighbor_cell])
    assert neighbor_cell in cell.neighbors()

def test_is_legal_true():
    white = (255, 255, 255)
    cell_hexagon = Cell((0, 0, 0), 1, white, white, [(0, 0, 0), (0, 0, 0)])
    cellular_body = CellularBody([cell_hexagon])
    assert cellular_body.is_legal()

def test_is_legal_false():
    white = (255, 255, 255)
    cell_hexagon = Cell((0, 0, 0), 1, white, white, [(0, 0, 0), (0, 0, 0)])
    conflicting_cell_hexagon = Cell((0, 0, 0), 1, white, white, [(0, 0, 0), (0, 0, 0)])
    cellular_body = CellularBody([cell_hexagon, conflicting_cell_hexagon])
    assert not cellular_body.is_legal()

def test_neighbors():
    from src.cell_gene import CellGene
    from src.cell_sequence import CellSequence
    from src.cell_builder import CellBuilder

    # Gene format: placement(3) + movement1(3) + movement2(3) + type(2) = 11 bits
    cell_gene_origin = CellGene("00000000011")
    cell_gene_straight_up = CellGene("00100000000")
    cell_gene_down_right = CellGene("01100000000")

    cell_sequence = CellSequence([
        cell_gene_origin.placement_delta(),
        cell_gene_straight_up.placement_delta(),
        cell_gene_down_right.placement_delta(),
    ])

    cell_origin = CellBuilder(cell_gene_origin, cell_sequence.positions[0]).cell()
    cell_straight_up = CellBuilder(cell_gene_straight_up, cell_sequence.positions[1]).cell()
    cell_down_right = CellBuilder(cell_gene_down_right, cell_sequence.positions[2]).cell()

    cells = [
        cell_origin,
        cell_straight_up,
        cell_down_right,
    ]

    cellular_body = CellularBody(cells)
    assert cell_straight_up in cellular_body.neighbors(cell_origin)
    assert cell_down_right in cellular_body.neighbors(cell_origin)

def test_legal_move():
    from tests.test_cell_factory import TestCellFactory
    f = TestCellFactory()
    cell = f.cell(position=(0, 0, 0), movement_deltas=[(0, 0, 0)])

    # mover_cell is straight up and moves to the lower left
    mover_cell = f.cell(position=(0, -1, 1), movement_deltas=[(-1, 1, 0)])

    cellular_body = CellularBody([cell, mover_cell])
    cellular_body.respond_to_cell_stimulation(mover_cell)
    assert mover_cell.position == (-1, 0, 1)

def test_illegal_move_overlap():
    from tests.test_cell_factory import TestCellFactory
    f = TestCellFactory()
    cell = f.cell(position=(0, 0, 0), movement_deltas=[(0, 0, 0)])

    # mover_cell is straight up and moves straight down (first delta causes overlap)
    # but second delta (-1, 1, 0) should succeed, moving to (-1, 0, 1)
    mover_cell = f.cell(position=(0, -1, 1), movement_deltas=[(0, 1, -1), (-1, 1, 0)])

    cellular_body = CellularBody([cell, mover_cell])
    cellular_body.respond_to_cell_stimulation(mover_cell)
    assert mover_cell.position == (-1, 0, 1)

def test_illegal_move_gap():
    from tests.test_cell_factory import TestCellFactory
    f = TestCellFactory()
    cell = f.cell(position=(0, 0, 0), movement_deltas=[(0, 0, 0)])

    # mover_cell is straight up and moves straight up
    mover_cell = f.cell(position=(0, -1, 1), movement_deltas=[(0, -1, -1)])

    cellular_body = CellularBody([cell, mover_cell])
    cellular_body.respond_to_cell_stimulation(mover_cell)
    assert mover_cell.position == (0, -1, 1)
