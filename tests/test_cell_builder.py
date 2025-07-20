import pytest
from src.cell_builder import CellBuilder
from src.cell_gene import CellGene

def test_cell_builder_returns_cell():
    gene = CellGene("000000")
    builder = CellBuilder(gene)
    cell = builder.cell()
    assert cell is not None
