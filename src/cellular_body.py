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
