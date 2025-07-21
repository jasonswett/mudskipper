from src.cell_gene import CellGene

class CellGeneFactory:
    def cell(self, placement_delta_gene=None, movement_delta_gene=None, cell_type_gene=None):
        starter_cell_gene = CellGene.random()
        gene_value = starter_cell_gene.value
        
        if placement_delta_gene:
            # Replace the placement_delta section
            gene_value = placement_delta_gene + gene_value[CellGene.GENE_SECTION_LENGTHS['placement_delta']:]
        
        if cell_type_gene:
            # Replace the cell_type section
            start = CellGene.GENE_SECTION_LENGTHS['placement_delta']
            gene_value = gene_value[:start] + cell_type_gene
        
        return CellGene(gene_value)
