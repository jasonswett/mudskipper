from src.cell import Cell

class CellBuilder:
    DEFAULT_RADIUS = 1
    DEFAULT_COLOR = (0, 255, 0)

    def __init__(self, cell_gene, position):
        self.cell_gene = cell_gene
        self.position = position
    
    def cell(self):
        return Cell(self.position, self.DEFAULT_RADIUS, self.DEFAULT_COLOR)
