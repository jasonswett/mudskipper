import math

class Cell:
    STIMULATION_COLOR = (255, 255, 0)
    REFRACTORY_PERIOD = 5

    def __init__(self, position, radius, border_color, fill_color):
        self.position = position
        self.q, self.r, self.s = position
        self.radius = radius
        self.border_color = border_color
        self.fill_color = fill_color
        self.original_fill_color = fill_color
        self.clock_tick_count = 0
        self.ticks_left_before_unstimulated = 0

    def update_clock(self, _):
        self.clock_tick_count += 1
        if self.ticks_left_before_unstimulated > 0:
            self.fill_color = self.STIMULATION_COLOR
            self.ticks_left_before_unstimulated -= 1
        else:
            self.fill_color = self.original_fill_color

    def stimulate(self):
        self.ticks_left_before_unstimulated = self.REFRACTORY_PERIOD

    def vertices(self):
        vertices = []
        for i in range(6):
            angle = (math.pi / 3) * i
            x = self.center_x() + math.cos(angle)
            y = self.center_y() + math.sin(angle)
            vertices.append((x, y))
        return vertices

    def center_x(self):
        return (3/2 * self.q) * self.radius

    def center_y(self):
        return (math.sqrt(3)/2 * self.q + math.sqrt(3) * self.r) * self.radius
