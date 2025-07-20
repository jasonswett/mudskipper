from src.cell import Cell

class CellSequence:
    DEFAULT_CELL_RADIUS = 1
    DEFAULT_CELL_COLOR = (0, 255, 0)

    def __init__(self, deltas):
        last_coordinates = deltas[0]
        root_cell = Cell(last_coordinates, self.DEFAULT_CELL_RADIUS, self.DEFAULT_CELL_COLOR)
        self.cells = [root_cell]

        for delta in deltas[1:]:
            last_x, last_y, last_z = last_coordinates
            x_delta, y_delta, z_delta = delta
            coordinates = (last_x + x_delta, last_y + y_delta, last_z + z_delta)
            cell = Cell(coordinates, self.DEFAULT_CELL_RADIUS, self.DEFAULT_CELL_COLOR)
            self.cells.append(cell)
            last_coordinates = coordinates
