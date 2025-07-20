from src.cell import Cell

class CellBuilder:
    def __init__(self, cell_gene, position):
        self.cell_gene = cell_gene
        self.position = position
    
    def cell(self):
        return Cell(self.position, 1, (0, 255, 0), (0, 0, 0))
