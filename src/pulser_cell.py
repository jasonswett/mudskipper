from src.cell import Cell

class PulserCell(Cell):
    PULSE_COLOR = (255, 255, 0)
    PULSE_INTERVAL = 50

    def __init__(self, position, radius, border_color, fill_color):
        super().__init__(position, radius, border_color, fill_color)
        self.original_fill_color = fill_color

    def update_clock(self):
        self.clock_tick_count += 1
        if self.clock_tick_count % self.PULSE_INTERVAL == 0:
            self.fill_color = self.PULSE_COLOR
            for neighbor in self.neighbors:
                neighbor.stimulate()
        else:
            self.fill_color = self.original_fill_color
