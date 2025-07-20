import math

class Cell:
    def __init__(self, position, radius, border_color, fill_color):
        self.position = position
        self.q, self.r, self.s = position
        self.radius = radius
        self.border_color = border_color
        self.fill_color = fill_color
        self.clock_tick_count = 0

    def update_clock(self):
        self.clock_tick_count += 1

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
