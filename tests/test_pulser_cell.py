import pytest
from src.pulser_cell import PulserCell
from src.cellular_body import CellularBody

def test_clock_tick():
    original_fill_color = (0, 0, 255)
    pulser_cell = PulserCell((0, 0, 0), 1, (0, 0, 0), original_fill_color, [(0, 0, 0)])
    cellular_body = CellularBody([pulser_cell])

    for i in range(PulserCell.PULSE_INTERVAL + 1):
        pulser_cell.update_clock()
    assert pulser_cell.fill_color == pulser_cell.STIMULATION_COLOR

    for i in range(pulser_cell.STIMULATION_DURATION):
        pulser_cell.update_clock()
    assert pulser_cell.fill_color == original_fill_color
