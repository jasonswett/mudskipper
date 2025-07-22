import math

class Cell:
    STIMULATION_COLOR = (255, 255, 0)
    STIMULATION_DURATION = 8
    STIMULATION_PROPAGATION_DELAY = 1
    REFRACTORY_PERIOD = 20

    def __init__(self, position, radius, border_color, fill_color, movement_delta):
        self.position = position
        self.q, self.r, self.s = position
        self.radius = radius
        self.border_color = border_color
        self.fill_color = fill_color
        self.original_fill_color = fill_color
        self.movement_delta = movement_delta
        self.clock_tick_count = 0
        self.ticks_left_before_unstimulated = 0
        self.ticks_left_before_stimulation_propagation = 0
        self.stimulation_count = 0
        self.neighbors = []
        self.last_stimulation_tick = -self.REFRACTORY_PERIOD

    def update_clock(self):
        self.clock_tick_count += 1
        if self.ticks_left_before_unstimulated > 0:
            self.fill_color = self.STIMULATION_COLOR
            self.ticks_left_before_unstimulated -= 1
            if self.ticks_left_before_unstimulated == 0:
                self.ticks_left_before_stimulation_propagation = self.STIMULATION_PROPAGATION_DELAY
        else:
            self.fill_color = self.original_fill_color
        if self.ticks_left_before_stimulation_propagation > 0:
            self.ticks_left_before_stimulation_propagation -= 1
            if self.ticks_left_before_stimulation_propagation == 0:
                self.stimulate_neighbors()

    def stimulate(self):
        if self.clock_tick_count - self.last_stimulation_tick < self.REFRACTORY_PERIOD:
            return
        self.stimulation_count += 1
        self.ticks_left_before_unstimulated = self.STIMULATION_DURATION
        self.last_stimulation_tick = self.clock_tick_count

    def stimulate_neighbors(self):
        for neighbor in self.neighbors:
            neighbor.stimulate()

    def move(self):
        print(f"original position: {self.position}")
        q, r, s = self.position
        dq, dr, ds = self.movement_delta
        self.position = (q + dq, r + dr, s + ds)
        self.q, self.r, self.s = self.position
        print(f"new position: {self.position}")

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
