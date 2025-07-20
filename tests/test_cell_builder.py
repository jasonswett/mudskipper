import pytest
from src.cell_builder import CellBuilder
from src.cell_gene import CellGene

def test_cell_builder_returns_cell():
    gene = CellGene("000000")
    position = (0, 0, 0)
    builder = CellBuilder(gene, position)
    cell = builder.cell()
    assert cell is not None
