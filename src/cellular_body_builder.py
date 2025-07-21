from src.cellular_body import CellularBody
from src.cell_sequence import CellSequence
from src.cell_builder import CellBuilder

class CellularBodyBuilder:
    def __init__(self, cell_genes):
        self.cell_genes = cell_genes

    def cellular_body(self):
        placement_deltas = [
            cell_gene.placement_delta() for cell_gene in self.cell_genes
        ]

        cell_sequence = CellSequence(placement_deltas)

        cells = []
        for index, position in enumerate(cell_sequence.positions):
            gene = self.cell_genes[index]
            cell_builder = CellBuilder(gene, position)
            cells.append(cell_builder.cell())

        return CellularBody(cells)
