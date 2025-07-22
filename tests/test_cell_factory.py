from src.cell_builder import CellBuilder
from src.cell import Cell

class TestCellFactory:
    def cell(self, position, movement_deltas):
        # Convert single delta to array if needed
        if not isinstance(movement_deltas, list):
            movement_deltas = [movement_deltas]
        return Cell(
            position,
            CellBuilder.DEFAULT_RADIUS,
            (0, 0, 0),
            (0, 0, 0),
            movement_deltas
        )
