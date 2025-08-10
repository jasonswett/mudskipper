import pytest
from src.pulser_cell import PulserCell
from src.cellular_body import CellularBody
from src.cell_gene import CellGene

def test_clock_tick():
    original_fill_color = (0, 0, 255)
    pulser_cell = PulserCell((0, 0, 0), 1, (0, 0, 0), original_fill_color, [(0, 0, 0)])
    cellular_body = CellularBody([pulser_cell])

    # Create a gene with a specific pulse interval for testing
    # Using a gene that sets pulse interval to 20 (binary 0010011 = 19, +1 = 20)
    # Full gene: placement(3) + movement1-3(9) + celltype(2) + pulse(7) + propagation(3) = 24 bits
    test_gene = CellGene('000000000110010011001000')
    pulser_cell.gene = test_gene

    pulse_interval = pulser_cell.gene.pulse_interval()

    for i in range(pulse_interval + 1):
        pulser_cell.update_clock()
    assert pulser_cell.fill_color == original_fill_color  # Pulser cell should light up with its own color (blue)

    for i in range(pulser_cell.STIMULATION_DURATION):
        pulser_cell.update_clock()
    assert pulser_cell.fill_color == original_fill_color
