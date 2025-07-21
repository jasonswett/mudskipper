from src.cell_gene import CellGene

class CellGeneFactory:
    def cell(self, placement_delta_gene=None, cell_type_gene=None):
        starter_cell_gene = CellGene.random()
        gene_value = starter_cell_gene.value
        
        if placement_delta_gene:
            # Replace the first 3 characters (placement_delta section)
            gene_value = placement_delta_gene + gene_value[3:]
        
        if cell_type_gene:
            # Replace characters at position 3-4 (cell type section)
            gene_value = gene_value[:3] + cell_type_gene
        
        return CellGene(gene_value)
