from src.cell_gene import CellGene

class Genome:
    def __init__(self, cell_count):
        self.cell_count = cell_count
        self._cell_genes = []
        for i in range(self.cell_count):
            self._cell_genes.append(CellGene.random())

    def cell_genes(self):
        return self._cell_genes

    def value(self):
        return "".join([str(cell_gene.value) for cell_gene in self._cell_genes])
