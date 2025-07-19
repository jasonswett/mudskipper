class CellularBody:
    def __init__(self, cells):
        self.cells = cells

    def is_legal(self):
        for i in range(len(self.cells)):
            for j in range(i + 1, len(self.cells)):
                if (self.cells[i].x == self.cells[j].x and
                    self.cells[i].y == self.cells[j].y and
                    self.cells[i].z == self.cells[j].z):
                    return False
        return True
