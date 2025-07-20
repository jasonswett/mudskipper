from src.cell import Cell

class CellBuilder:
    def __init__(self, cell_gene):
        self.cell_gene = cell_gene
    
    def cell(self):
        return Cell((0, 0, 0), 1, (0, 255, 0))