import pytest
from src.cell_builder import CellBuilder
from src.cell_gene import CellGene

def test_cell_builder_returns_cell():
    # Gene needs: placement(3) + movement1(3) + movement2(3) + type(2) = 11 bits
    gene = CellGene("00000000000")
    position = (0, 0, 0)
    builder = CellBuilder(gene, position)
    cell = builder.cell()
    assert cell is not None
