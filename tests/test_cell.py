import pytest
from src.cell import Cell


def test_cell_initialization_and_cube_to_pixel_conversion():
    # Create a cell at cube coordinates (1, -1, 0)
    green = (0, 255, 0)
    radius = 10
    cell = Cell((1, -1, 0), radius, green)
    
    # Test that coordinates are properly stored
    assert cell.x == 1
    assert cell.y == -1
    assert cell.z == 0
    assert cell.radius == 10
    assert cell.color == (0, 255, 0)
    
    # Test cube_to_pixel conversion
    px, py = cell.cube_to_pixel()
    
    # Expected calculations:
    # px = radius * (sqrt(3) * x + sqrt(3)/2 * y)
    # px = 10 * (1.732 * 1 + 0.866 * (-1))
    # px = 10 * (1.732 - 0.866) = 10 * 0.866 = 8.66
    
    # py = radius * (3/2 * y)
    # py = 10 * (1.5 * (-1)) = -15
    
    assert abs(px - 8.66) < 0.01  # Allow small floating point error
    assert py == -15