import pytest

from src.cell_gene import CellGene
from tests.cell_gene_factory import CellGeneFactory

def test_cell_gene_initialization():
    f = CellGeneFactory()
    assert f.cell(placement_delta_gene="000").placement_delta() == (0, 0, 0)
    assert f.cell(placement_delta_gene="001").placement_delta() == (0, -1, 1)
    assert f.cell(placement_delta_gene="010").placement_delta() == (1, -1, 0)
    assert f.cell(placement_delta_gene="011").placement_delta() == (1, 0, -1)
    assert f.cell(placement_delta_gene="100").placement_delta() == (0, 1, -1)
    assert f.cell(placement_delta_gene="101").placement_delta() == (-1, 1, 0)
    assert f.cell(placement_delta_gene="110").placement_delta() == (-1, 0, 1)
    assert f.cell(placement_delta_gene="111").placement_delta() == (0, 0, 0)

def test_cell_type():
    f = CellGeneFactory()
    assert f.cell(cell_type_gene="00").cell_type() == "default"
    assert f.cell(cell_type_gene="01").cell_type() == "default"
    assert f.cell(cell_type_gene="10").cell_type() == "default"
    assert f.cell(cell_type_gene="11").cell_type() == "pulser"
