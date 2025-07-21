from src.cell import Cell
from src.pulser_cell import PulserCell

class CellFactory:
    @staticmethod
    def create(cell_type, position, radius, border_color, fill_color, movement_delta):
        if cell_type == "pulser":
            return PulserCell(position, radius, border_color, fill_color, movement_delta)
        else:
            return Cell(position, radius, border_color, fill_color, movement_delta)