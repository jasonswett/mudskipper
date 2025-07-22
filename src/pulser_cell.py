from src.cell import Cell

class PulserCell(Cell):
    PULSE_INTERVAL = 40

    def __init__(self, position, radius, border_color, fill_color, movement_deltas):
        super().__init__(position, radius, border_color, fill_color, movement_deltas)
        self.original_fill_color = fill_color

    def update_clock(self):
        if self.clock_tick_count % self.PULSE_INTERVAL == 0:
            self.stimulate()
        super().update_clock()
