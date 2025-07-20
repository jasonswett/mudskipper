class CellularBody:
    def __init__(self, cells):
        self.cells = cells

    def is_legal(self):
        for i in range(len(self.cells)):
            for j in range(i + 1, len(self.cells)):
                if (self.cells[i].q == self.cells[j].q and
                    self.cells[i].r == self.cells[j].r and
                    self.cells[i].s == self.cells[j].s):
                    return False
        return True

    def neighbors(self, cell):
        neighbors = []

        neighbor_offsets = [
            (1, 0, -1),
            (1, -1, 0),
            (0, -1, 1),
            (-1, 0, 1),
            (-1, 1, 0),
            (0, 1, -1)
        ]
        
        for other_cell in self.cells:
            if other_cell != cell:
                q_diff = other_cell.q - cell.q
                r_diff = other_cell.r - cell.r
                s_diff = other_cell.s - cell.s
                if (q_diff, r_diff, s_diff) in neighbor_offsets:
                    neighbors.append(other_cell)
        return neighbors
