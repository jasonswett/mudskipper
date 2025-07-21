from src.cell_gene import CellGene

class Genome:
    def __init__(self, size):
        self.size = size

    def cell_genes(self):
        cell_genes = []
        for i in range(self.size):
            cell_genes.append(CellGene.random())
        return cell_genes
