import pytest

from src.cell_gene import CellGene
from tests.cell_gene_factory import CellGeneFactory

def test_cell_gene_initialization():
    f = CellGeneFactory()
    assert f.cell(delta_gene="000").delta() == (0, 0, 0)
    assert f.cell(delta_gene="001").delta() == (0, -1, 1)
    assert f.cell(delta_gene="010").delta() == (1, -1, 0)
    assert f.cell(delta_gene="011").delta() == (1, 0, -1)
    assert f.cell(delta_gene="100").delta() == (0, 1, -1)
    assert f.cell(delta_gene="101").delta() == (-1, 1, 0)
    assert f.cell(delta_gene="110").delta() == (-1, 0, 1)
    assert f.cell(delta_gene="111").delta() == (0, 0, 0)

def test_cell_type():
    f = CellGeneFactory()
    assert f.cell(cell_type_gene="00").cell_type() == "default"
    assert f.cell(cell_type_gene="01").cell_type() == "default"
    assert f.cell(cell_type_gene="10").cell_type() == "default"
    assert f.cell(cell_type_gene="11").cell_type() == "pulser"
