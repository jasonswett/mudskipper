import pytest
import Box2D
from unittest.mock import Mock
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

    # Create screen, camera, and organism rendering
    screen = Screen(20, 20)
    from src.camera import Camera
    camera = Camera(10, 10, 20, 20)
    organism_rendering = OrganismRendering(organism, screen, camera)

    # Basic assertion to verify initialization
    assert organism_rendering.organism == organism

def test_bounding_rectangle():
    # Create a mock organism rendering
    mock_organism = Mock()
    screen = Screen(20, 20)
    from src.camera import Camera
    camera = Camera(10, 10, 20, 20)
    organism_rendering = OrganismRendering(mock_organism, screen, camera)

    # Stub vertices() method with hard-coded values
    # Two hexagon fixtures with vertices that create a bounding rectangle
    organism_rendering.vertices = Mock(return_value=[
        # First hexagon centered at (3.0, 4.0) with vertices extending to specific bounds
        [(4.0, 4.0), (3.5, 5.0), (2.5, 5.0), (2.0, 4.0), (2.5, 3.0), (3.5, 3.0)],
        # Second hexagon centered at (6.0, 3.0) with vertices extending the bounds
        [(7.0, 3.0), (6.5, 4.0), (5.5, 4.0), (5.0, 3.0), (5.5, 2.0), (6.5, 2.0)]
    ])

    # Get bounding rectangle
    bounding_rectangle = organism_rendering.bounding_rectangle()

    # Assert the four corners match expected values
    # min_x=2.0, min_y=2.0, max_x=7.0, max_y=5.0
    assert bounding_rectangle == (2.0, 2.0, 7.0, 5.0)  # (min_x, min_y, max_x, max_y)
