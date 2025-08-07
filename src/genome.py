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

    @classmethod
    def from_string(cls, genome_string, cell_count):
        """Create a genome from a genome string."""
        genome = cls.__new__(cls)
        genome.cell_count = cell_count
        genome._cell_genes = []

        # Calculate the length of each cell gene
        cell_gene_length = sum(CellGene.GENE_SECTION_LENGTHS.values())

        # Extract each cell gene from the string
        for i in range(cell_count):
            start = i * cell_gene_length
            end = start + cell_gene_length
            if end <= len(genome_string):
                cell_gene_string = genome_string[start:end]
                cell_gene = CellGene(cell_gene_string)
                genome._cell_genes.append(cell_gene)
            else:
                # If not enough genetic material, fill with random genes
                genome._cell_genes.append(CellGene.random())

        return genome

    @staticmethod
    def splice(genome_string_a, genome_string_b, cell_count):
        """Create offspring genome by splicing two parent genomes at a random point."""
        import random

        # Find the shorter genome length to avoid index errors
        min_length = min(len(genome_string_a), len(genome_string_b))

        if min_length == 0:
            # If one genome is empty, use random genome
            return Genome(cell_count)

        # Choose a random splice point
        splice_point = random.randint(0, min_length - 1)

        # Create offspring genome: first part from parent A, rest from parent B
        offspring_genome_string = genome_string_a[:splice_point] + genome_string_b[splice_point:]

        return Genome.from_string(offspring_genome_string, cell_count)
