import pytest
import Box2D
from src.organism import Organism
from src.cell import Cell

def test_organism_initialization():
    world = Box2D.b2World()
    cell = Cell((1, -1, 0), 10, (0, 255, 0))
    position = (5, 10)
    organism = Organism(world, cell, position)
    
    assert organism.body.position.x == 5
    assert organism.body.position.y == 10
