from src.cell import Cell

class CellSequence:
    DEFAULT_CELL_RADIUS = 1
    DEFAULT_CELL_COLOR = (0, 255, 0)

    def __init__(self, deltas):
        last_coordinates = deltas[0]
        root_cell = Cell(last_coordinates, self.DEFAULT_CELL_RADIUS, self.DEFAULT_CELL_COLOR)
        self.cells = [root_cell]

        for delta in deltas[1:]:
            last_q, last_r, last_s = last_coordinates
            q_delta, r_delta, s_delta = delta
            coordinates = (last_q + q_delta, last_r + r_delta, last_s + s_delta)
            cell = Cell(coordinates, self.DEFAULT_CELL_RADIUS, self.DEFAULT_CELL_COLOR)
            self.cells.append(cell)
            last_coordinates = coordinates
