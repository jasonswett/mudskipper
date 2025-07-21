from src.cell import Cell

class PulserCell(Cell):
    PULSE_INTERVAL = 100

    def __init__(self, position, radius, border_color, fill_color):
        super().__init__(position, radius, border_color, fill_color)
        self.original_fill_color = fill_color

    def update_clock(self):
        if self.clock_tick_count % self.PULSE_INTERVAL == 0:
            self.stimulate()
        super().update_clock()
