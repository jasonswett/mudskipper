from src.cell_gene import CellGene

class Genome:
    MIN_CELL_COUNT = 2
    MAX_CELL_COUNT = 6

    @classmethod
    def cell_count_prefix_length(cls):
        """Calculate required prefix length based on max cell count."""
        import math
        # We need enough bits to represent (MAX_CELL_COUNT - MIN_CELL_COUNT) additional cells
        additional_cells = cls.MAX_CELL_COUNT - cls.MIN_CELL_COUNT
        return max(1, math.ceil(math.log2(additional_cells + 1))) if additional_cells > 0 else 1

    def __init__(self, max_cell_count=None):
        self.max_cell_count = max_cell_count or self.MAX_CELL_COUNT
        # Start with zeros for cell count prefix
        prefix_length = self.cell_count_prefix_length()
        self.cell_count_prefix = '0' * prefix_length

        # Generate genes for maximum possible cells
        self._cell_genes = []
        for i in range(self.max_cell_count):
            self._cell_genes.append(CellGene.random())

    def effective_cell_count(self):
        """Calculate actual number of cells based on prefix sum."""
        prefix_sum = sum(int(bit) for bit in self.cell_count_prefix)
        return self.MIN_CELL_COUNT + min(prefix_sum, self.MAX_CELL_COUNT - self.MIN_CELL_COUNT)  # Cap at max cells

    def cell_genes(self):
        """Return only the cell genes that should be active."""
        effective_count = self.effective_cell_count()
        return self._cell_genes[:effective_count]

    def value(self):
        """Return full genome string including prefix and all cell genes."""
        cell_genes_string = "".join([str(cell_gene.value) for cell_gene in self._cell_genes])
        return self.cell_count_prefix + cell_genes_string

    @classmethod
    def from_string(cls, genome_string):
        """Create a genome from a genome string."""
        genome = cls.__new__(cls)
        genome.max_cell_count = cls.MAX_CELL_COUNT

        # Extract cell count prefix
        prefix_length = cls.cell_count_prefix_length()
        if len(genome_string) >= prefix_length:
            genome.cell_count_prefix = genome_string[:prefix_length]
        else:
            # If genome string is too short, pad with zeros
            genome.cell_count_prefix = (genome_string + '0' * prefix_length)[:prefix_length]

        # Extract cell genes from remainder of string
        cell_genes_string = genome_string[prefix_length:]
        genome._cell_genes = []

        # Calculate the length of each cell gene
        cell_gene_length = sum(CellGene.GENE_SECTION_LENGTHS.values())

        # Extract each cell gene from the string
        for i in range(genome.max_cell_count):
            start = i * cell_gene_length
            end = start + cell_gene_length
            if end <= len(cell_genes_string):
                cell_gene_string = cell_genes_string[start:end]
                cell_gene = CellGene(cell_gene_string)
                genome._cell_genes.append(cell_gene)
            else:
                # If not enough genetic material, fill with random genes
                genome._cell_genes.append(CellGene.random())

        return genome

    @staticmethod
    def splice(genome_string_a, genome_string_b):
        """Create offspring genome by splicing two parent genomes at a random point."""
        import random

        # Find the shorter genome length to avoid index errors
        min_length = min(len(genome_string_a), len(genome_string_b))

        if min_length == 0:
            # If one genome is empty, return a basic genome string
            prefix_length = Genome.cell_count_prefix_length()
            return '0' * prefix_length + '0' * (Genome.MAX_CELL_COUNT * sum(CellGene.GENE_SECTION_LENGTHS.values()))

        # Choose a random splice point
        splice_point = random.randint(0, min_length - 1)

        # Create offspring genome: first part from parent A, rest from parent B
        offspring_genome_string = genome_string_a[:splice_point] + genome_string_b[splice_point:]

        return offspring_genome_string

    @staticmethod
    def mutate(genome_string, mutation_rate):
        """Apply mutations to a genome string by flipping bits at the given rate."""
        import random

        mutated = []
        for bit in genome_string:
            if random.random() < mutation_rate:
                # Flip the bit
                mutated.append('0' if bit == '1' else '1')
            else:
                mutated.append(bit)

        return ''.join(mutated)
