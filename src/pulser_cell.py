from src.cell import Cell

class PulserCell(Cell):
    PULSE_HEALTH_COST = 20

    def __init__(self, position, radius, border_color, fill_color, movement_deltas):
        super().__init__(position, radius, border_color, fill_color, movement_deltas)
        self.original_fill_color = fill_color

    def update_clock(self):
        # Use the genetically determined pulse interval
        # gene attribute will be set by CellBuilder after creation
        pulse_interval = self.gene.pulse_interval() if hasattr(self, 'gene') else 20

        if self.clock_tick_count % pulse_interval == 0 and self.is_alive():
            self.stimulate(self.original_fill_color)  # Pass own color as stimulation color
            self.health -= self.PULSE_HEALTH_COST
        super().update_clock()
