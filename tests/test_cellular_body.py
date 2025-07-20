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

def test_neighbors():
    from src.cell_gene import CellGene
    from src.cell_sequence import CellSequence
    from src.cell_builder import CellBuilder

    cell_gene_origin = CellGene("00011")
    cell_gene_straight_up = CellGene("00100")
    cell_gene_down_right = CellGene("01100")

    cell_sequence = CellSequence([
        cell_gene_origin.delta(),
        cell_gene_straight_up.delta(),
        cell_gene_down_right.delta(),
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
