import pytest
from gene import Gene

def test_gene_initialization_with_length():
    gene = Gene(6)
    assert len(gene.value) == 6
