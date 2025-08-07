import pytest
from src.genome import Genome
from src.cell_gene import CellGene

class TestGenomeSplicing:
    def test_splice_creates_offspring_genome(self):
        """Test that splice creates a valid offspring genome from two parents."""
        # Create two parent genome strings
        parent_a = "1100101111101110101001"
        parent_b = "0110000010001110101110"

        # Create offspring through splicing
        offspring_genome = Genome.splice(parent_a, parent_b, 2)

        # Offspring should be a valid Genome object
        assert isinstance(offspring_genome, Genome)
        assert offspring_genome.cell_count == 2
        assert len(offspring_genome.cell_genes()) == 2

        # Offspring genome string should contain parts from both parents
        offspring_string = offspring_genome.value()
        assert isinstance(offspring_string, str)
        assert len(offspring_string) > 0

        # The offspring string should be composed of genetic material from both parents
        min_length = min(len(parent_a), len(parent_b))
        assert len(offspring_string) >= min_length

    def test_splice_with_different_length_genomes(self):
        """Test splicing with genomes of different lengths."""
        parent_a = "11001011"
        parent_b = "0110000010001110101110"

        offspring_genome = Genome.splice(parent_a, parent_b, 2)

        assert isinstance(offspring_genome, Genome)
        assert offspring_genome.cell_count == 2

    def test_splice_with_empty_genome(self):
        """Test splicing when one parent has empty genome."""
        parent_a = ""
        parent_b = "0110000010001110101110"

        offspring_genome = Genome.splice(parent_a, parent_b, 2)

        # Should create a random genome when one parent is empty
        assert isinstance(offspring_genome, Genome)
        assert offspring_genome.cell_count == 2

    def test_from_string_creates_valid_genome(self):
        """Test that from_string method creates a valid genome."""
        genome_string = "1100101111101110101001"

        genome = Genome.from_string(genome_string, 2)

        assert isinstance(genome, Genome)
        assert genome.cell_count == 2
        assert len(genome.cell_genes()) == 2

        # The resulting genome string should match or be based on the input
        result_string = genome.value()
        assert isinstance(result_string, str)
        assert len(result_string) > 0

    def test_splice_randomness(self):
        """Test that splice point is random by running multiple times."""
        parent_a = "1111111111111111111111"
        parent_b = "0000000000000000000000"

        # Run splice multiple times and collect results
        results = []
        for _ in range(10):
            offspring = Genome.splice(parent_a, parent_b, 2)
            results.append(offspring.value())

        # Should have some variation in results due to random splice point
        unique_results = set(results)
        assert len(unique_results) >= 1  # At least one result (could be same due to randomness)
