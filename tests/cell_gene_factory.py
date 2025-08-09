from src.cell_gene import CellGene

class CellGeneFactory:
    def cell(self, placement_delta_gene=None, movement_delta_1_gene=None, movement_delta_2_gene=None, cell_type_gene=None):
        starter_cell_gene = CellGene.random()
        gene_value = starter_cell_gene.value

        if placement_delta_gene:
            start = 0
            end = start + CellGene.GENE_SECTION_LENGTHS['placement_delta']
            gene_value = placement_delta_gene + gene_value[end:]

        if movement_delta_1_gene:
            start = CellGene.GENE_SECTION_LENGTHS['placement_delta']
            end = start + CellGene.GENE_SECTION_LENGTHS['movement_delta_1']
            gene_value = gene_value[:start] + movement_delta_1_gene + gene_value[end:]

        if movement_delta_2_gene:
            start = CellGene.GENE_SECTION_LENGTHS['placement_delta'] + CellGene.GENE_SECTION_LENGTHS['movement_delta_1']
            end = start + CellGene.GENE_SECTION_LENGTHS['movement_delta_2']
            gene_value = gene_value[:start] + movement_delta_2_gene + gene_value[end:]

        if cell_type_gene:
            # Calculate start position: placement + 3 movement deltas
            start = (CellGene.GENE_SECTION_LENGTHS['placement_delta'] +
                    CellGene.GENE_SECTION_LENGTHS['movement_delta_1'] +
                    CellGene.GENE_SECTION_LENGTHS['movement_delta_2'] +
                    CellGene.GENE_SECTION_LENGTHS['movement_delta_3'])
            end = start + CellGene.GENE_SECTION_LENGTHS['cell_type']
            gene_value = gene_value[:start] + cell_type_gene + gene_value[end:]

        return CellGene(gene_value)
