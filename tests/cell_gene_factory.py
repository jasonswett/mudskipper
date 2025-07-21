from src.cell_gene import CellGene

class CellGeneFactory:
    def cell(self, placement_delta_gene=None, movement_delta_gene=None, cell_type_gene=None):
        starter_cell_gene = CellGene.random()
        gene_value = starter_cell_gene.value
        
        if placement_delta_gene:
            start = 0
            end = start + CellGene.GENE_SECTION_LENGTHS['placement_delta']
            gene_value = placement_delta_gene + gene_value[end:]
        
        if movement_delta_gene:
            start = CellGene.GENE_SECTION_LENGTHS['placement_delta']
            end = start + CellGene.GENE_SECTION_LENGTHS['movement_delta']
            gene_value = gene_value[:start] + movement_delta_gene + gene_value[end:]
        
        if cell_type_gene:
            start = CellGene.GENE_SECTION_LENGTHS['placement_delta'] + CellGene.GENE_SECTION_LENGTHS['movement_delta']
            gene_value = gene_value[:start] + cell_type_gene
        
        return CellGene(gene_value)
