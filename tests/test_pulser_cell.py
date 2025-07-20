import pytest
from src.pulser_cell import PulserCell

def test_clock_tick():
    original_fill_color = (0, 0, 255)
    pulser_cell = PulserCell((0, 0, 0), 1, (0, 0, 0), original_fill_color)

    for i in range(PulserCell.PULSE_INTERVAL):
        pulser_cell.update_clock()
    assert pulser_cell.fill_color == PulserCell.PULSE_COLOR

    pulser_cell.update_clock()
    assert pulser_cell.fill_color == original_fill_color
