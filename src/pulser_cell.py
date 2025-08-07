from src.cell import Cell

class PulserCell(Cell):
    PULSE_INTERVAL = 20
    PULSE_HEALTH_COST = 20

    def __init__(self, position, radius, border_color, fill_color, movement_deltas):
        super().__init__(position, radius, border_color, fill_color, movement_deltas)
        self.original_fill_color = fill_color

    def update_clock(self):
        if self.clock_tick_count % self.PULSE_INTERVAL == 0 and self.is_alive():
            self.stimulate()
            self.health -= self.PULSE_HEALTH_COST
        super().update_clock()
