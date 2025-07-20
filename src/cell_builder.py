from src.cell import Cell

class CellBuilder:
    DEFAULT_RADIUS = 1

    def __init__(self, cell_gene, position):
        self.cell_gene = cell_gene
        self.position = position
    
    def cell(self):
        return Cell(self.position, self.DEFAULT_RADIUS, self.cell_gene.border_color(), self.cell_gene.fill_color())
