import pytest
import Box2D
from src.organism import Organism
from src.cell import Cell

def test_organism_initialization():
    world = Box2D.b2World()
    cells = [
        Cell((0, 0, 0), 1, (0, 255, 0), (0, 0, 0)),
        Cell((1, 0, -1), 1, (0, 255, 0), (0, 0, 0))
    ]
    position = (5, 10)
    organism = Organism(world, cells, position)
    
    assert organism.body.position.x == 5
    assert organism.body.position.y == 10
    assert len(organism.body.fixtures) == 2  # Two cells = two fixtures

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

    world = Box2D.b2World()
    organism = Organism(world, cells, (0, 0))
    assert cell_straight_up in organism.neighbors(cell_origin)
    assert cell_down_right in organism.neighbors(cell_origin)
