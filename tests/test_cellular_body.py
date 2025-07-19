import pytest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from src.cellular_body import CellularBody
from src.cell_hexagon import CellHexagon

def test_cellular_body_initialization_with_cell_hexagons():
    cell_hexagon = CellHexagon(0, 0, 1, (0, 255, 0))
    cellular_body = CellularBody([cell_hexagon])
    assert len(cellular_body.cells) == 1
