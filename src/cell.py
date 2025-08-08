from src.cellular_body import CellularBody

class Cell:
    STIMULATION_COLOR = (255, 255, 0)
    STIMULATION_DURATION = 8
    STIMULATION_PROPAGATION_DELAY = 1
    DEATH_COLOR = (128, 128, 128)
    REFRACTORY_PERIOD = 20
    STARTING_HEALTH = 400
    MAX_HEALTH = 5000
    FOOD_MORSEL_HEALTH_VALUE = 500
    REPRODUCTION_COST = 200

    def __init__(self, position, radius, border_color, fill_color, movement_deltas):
        self.position = position
        self.q, self.r, self.s = position
        self.radius = radius
        self.border_color = border_color
        self.fill_color = fill_color
        self.original_fill_color = fill_color
        self.movement_deltas = movement_deltas
        self.clock_tick_count = 0
        self.ticks_left_before_unstimulated = 0
        self.ticks_left_before_stimulation_propagation = 0
        self.stimulation_count = 0
        self.last_stimulation_tick = -self.REFRACTORY_PERIOD
        self.cellular_body = CellularBody([])
        self.health = self.STARTING_HEALTH

    def update_clock(self):
        if self.health <= 0:
            return

        self.clock_tick_count += 1

        self.health -= 1
        if self.health <= 0:
            self.die()

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
        if not(self.is_alive()):
            return

        self.cellular_body.respond_to_cell_stimulation(self)

        if self.clock_tick_count - self.last_stimulation_tick < self.REFRACTORY_PERIOD:
            return
        self.stimulation_count += 1
        self.ticks_left_before_unstimulated = self.STIMULATION_DURATION
        self.last_stimulation_tick = self.clock_tick_count

    def stimulate_neighbors(self):
        for neighbor in self.neighbors():
            neighbor.stimulate()

    def neighbors(self):
        return self.cellular_body.neighbors(self)

    def move(self, delta):
        q, r, s = self.position
        dq, dr, ds = delta
        new_q = q + dq
        new_r = r + dr
        new_s = s + ds

        # Clamp hex coordinates to prevent extreme values that cause Box2D issues
        # Based on world size of 120x120, reasonable hex coordinate range is about ±150
        MAX_HEX_COORD = 150
        new_q = max(-MAX_HEX_COORD, min(MAX_HEX_COORD, new_q))
        new_r = max(-MAX_HEX_COORD, min(MAX_HEX_COORD, new_r))
        new_s = max(-MAX_HEX_COORD, min(MAX_HEX_COORD, new_s))

        # Ensure q + r + s = 0 constraint is maintained after clamping
        # If clamping broke the constraint, adjust the coordinate that changed least
        coord_sum = new_q + new_r + new_s
        if coord_sum != 0:
            # Find which coordinate was clamped least (has most room to adjust)
            q_room = MAX_HEX_COORD - abs(new_q)
            r_room = MAX_HEX_COORD - abs(new_r)
            s_room = MAX_HEX_COORD - abs(new_s)

            if q_room >= r_room and q_room >= s_room:
                new_q -= coord_sum
            elif r_room >= s_room:
                new_r -= coord_sum
            else:
                new_s -= coord_sum

        self.position = (new_q, new_r, new_s)
        self.q, self.r, self.s = self.position
        # Note: Position change will be detected by organism's _have_cells_moved() check

    def die(self):
        self.fill_color = self.DEATH_COLOR
        self.border_color = self.DEATH_COLOR

    def is_alive(self):
        return self.health > 0

    def nourish(self):
        health_after_eating = self.health + self.FOOD_MORSEL_HEALTH_VALUE
        self.health = min(health_after_eating, self.MAX_HEALTH)

    def subtract_reproduction_cost(self):
        self.health -= self.REPRODUCTION_COST

    def get_health_faded_color(self, base_color):
        """Get a color that fades to light gray as health declines."""
        # Calculate health percentage (0.0 to 1.0)
        health_percentage = max(0, min(1, self.health / self.STARTING_HEALTH))

        # Ghost gray color (light gray)
        ghost_gray = (200, 200, 200)

        # Interpolate between base color and ghost gray
        r = int(base_color[0] * health_percentage + ghost_gray[0] * (1 - health_percentage))
        g = int(base_color[1] * health_percentage + ghost_gray[1] * (1 - health_percentage))
        b = int(base_color[2] * health_percentage + ghost_gray[2] * (1 - health_percentage))

        return (r, g, b)
