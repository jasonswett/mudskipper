import pytest

from src.cell_gene import CellGene

def test_cell_gene_initialization():
    assert CellGene("000").delta() == (0, 0, 0)
    assert CellGene("001").delta() == (0, -1, 1)
    assert CellGene("010").delta() == (1, -1, 0)
    assert CellGene("011").delta() == (1, 0, -1)
    assert CellGene("100").delta() == (0, 1, -1)
    assert CellGene("101").delta() == (-1, 1, 0)
    assert CellGene("110").delta() == (-1, 0, 1)

def test_cell_type():
    assert CellGene("00000").cell_type() == "default"
    assert CellGene("00001").cell_type() == "default"
    assert CellGene("00010").cell_type() == "default"
    assert CellGene("00011").cell_type() == "pulser"
