from src.cell import Cell

class CellSequence:
    def __init__(self, deltas):
        last_coordinates = deltas[0]
        self.positions = [deltas[0]]

        for delta in deltas[1:]:
            last_q, last_r, last_s = last_coordinates
            q_delta, r_delta, s_delta = delta
            coordinates = (last_q + q_delta, last_r + r_delta, last_s + s_delta)
            self.positions.append(coordinates)
            last_coordinates = coordinates
