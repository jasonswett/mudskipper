class CellularBody:
    def __init__(self, cells):
        self.cells = cells

    def is_legal(self):
        for i in range(len(self.cells)):
            for j in range(i + 1, len(self.cells)):
                if (self.cells[i].center_x == self.cells[j].center_x and 
                    self.cells[i].center_y == self.cells[j].center_y):
                    return False
        return True
