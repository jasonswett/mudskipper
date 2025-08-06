import pytest
import Box2D
from src.organism_rendering import OrganismRendering
from src.organism import Organism
from src.cellular_body import CellularBody
from src.cell import Cell
from src.screen import Screen

def test_organism_rendering_initialization():
    # Create a simple organism for testing
    world = Box2D.b2World(gravity=(0, 0))
    cell = Cell((0, 0, 0), 0.8, (255, 0, 0), (255, 100, 100), [])
    cellular_body = CellularBody([cell])
    organism = Organism(world, cellular_body, (5, 5))

    # Create screen and organism rendering
    screen = Screen(20, 20)
    organism_rendering = OrganismRendering(organism, screen)

    # Basic assertion to verify initialization
    assert organism_rendering.organism == organism
