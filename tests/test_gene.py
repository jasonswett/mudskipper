import pytest
from src.gene import Gene

def test_gene_initialization_with_length():
    gene = Gene(6)
    assert len(gene.value) == 6

def test_gene_initialization_with_value():
    gene = Gene("101")
    assert gene.value == "101"
