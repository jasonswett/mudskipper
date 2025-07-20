import pytest
import Box2D
from src.organism import Organism
from src.cell import Cell
from src.cellular_body import CellularBody

def test_organism_initialization():
    world = Box2D.b2World()
    cells = [
        Cell((0, 0, 0), 1, (0, 255, 0), (0, 0, 0)),
        Cell((1, 0, -1), 1, (0, 255, 0), (0, 0, 0))
    ]
    position = (5, 10)
    cellular_body = CellularBody(cells)
    organism = Organism(world, cellular_body, position)
    
    assert organism.body.position.x == 5
    assert organism.body.position.y == 10
    assert len(organism.body.fixtures) == 2  # Two cells = two fixtures
