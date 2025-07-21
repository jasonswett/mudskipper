from src.cell import Cell
from src.pulser_cell import PulserCell

class CellBuilder:
    DEFAULT_RADIUS = 1

    def __init__(self, cell_gene, position):
        self.cell_gene = cell_gene
        self.position = position
    
    def cell(self):
        cell_class = PulserCell if self.cell_gene.cell_type() == "pulser" else Cell
        return cell_class(self.position, self.DEFAULT_RADIUS, self.cell_gene.border_color(), self.cell_gene.fill_color())
