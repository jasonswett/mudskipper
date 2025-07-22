from src.cell_builder import CellBuilder
from src.cell import Cell

class TestCellFactory:
    def cell(self, position, movement_delta):
        return Cell(
            position,
            CellBuilder.DEFAULT_RADIUS,
            (0, 0, 0),
            (0, 0, 0),
            movement_delta
        )
