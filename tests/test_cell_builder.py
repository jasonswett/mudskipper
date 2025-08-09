import pytest
from src.cell_builder import CellBuilder
from src.cell_gene import CellGene

def test_cell_builder_returns_cell():
    # Gene needs: placement(3) + movement1-3(9) + type(2) + pulse(7) + propagation(3) = 24 bits
    gene = CellGene("000000000000000000000000")
    position = (0, 0, 0)
    builder = CellBuilder(gene, position)
    cell = builder.cell()
    assert cell is not None
