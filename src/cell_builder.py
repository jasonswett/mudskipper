from src.cell_factory import CellFactory

class CellBuilder:
    DEFAULT_RADIUS = 0.4

    def __init__(self, cell_gene, position):
        self.cell_gene = cell_gene
        self.position = position

    def cell(self):
        return CellFactory.create(
            self.cell_gene.cell_type(),
            self.position,
            self.DEFAULT_RADIUS,
            self.cell_gene.border_color(),
            self.cell_gene.fill_color(),
            self.cell_gene.movement_deltas()
        )
