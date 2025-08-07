import Box2D
import math

class Organism:
    MINIMUM_STIMULATION_COUNT = 10
    MINIMUM_REPRODUCTION_HEALTH = 500

    def __init__(self, world, cellular_body, position):
        body_def = Box2D.b2BodyDef()
        body_def.type = Box2D.b2_dynamicBody
        body_def.position = position
        self.body = world.CreateBody(body_def)
        self.cellular_body = cellular_body
        self.fixtures_need_update = False  # Track if fixtures need recreation
        self._last_cell_positions = None  # Cache to detect movement

        for cell in self.cells():
            vertices = self.box2d_cell_vertices(cell)
            hexagon_shape = Box2D.b2PolygonShape(vertices=vertices)
            self.body.CreateFixture(shape=hexagon_shape, density=1.0)

        # Store initial positions
        self._update_position_cache()

    def cells(self):
        return self.cellular_body.cells

    def update_clock(self):
        self.cellular_body.update_clock()

        # Check if any cell positions have changed
        if self._have_cells_moved():
            self.fixtures_need_update = True

        # Only update fixtures if they actually need updating
        if self.fixtures_need_update:
            self.update_fixtures()
            self.fixtures_need_update = False

    def update_fixtures(self):
        """Recreate all fixtures based on current cell positions."""
        # Remove all existing fixtures
        for fixture in self.body.fixtures:
            self.body.DestroyFixture(fixture)

        # Create new fixtures based on current cell positions
        for cell in self.cells():
            vertices = self.box2d_cell_vertices(cell)
            hexagon_shape = Box2D.b2PolygonShape(vertices=vertices)
            self.body.CreateFixture(shape=hexagon_shape, density=1.0)

    def box2d_cell_vertices(self, cell):
        """Calculate vertices for a cell's hexagon in Box2D local coordinates."""
        vertices = []
        for i in range(6):
            angle = (math.pi / 3) * i
            x = ((3/2 * cell.q) * cell.radius) + cell.radius * math.cos(angle)
            y = ((math.sqrt(3)/2 * cell.q + math.sqrt(3) * cell.r) * cell.radius) + cell.radius * math.sin(angle)
            vertices.append((x, y))
        return vertices

    def nourish(self):
        for cell in self.cells():
            cell.nourish()

    def is_alive(self):
        return any(cell.is_alive() for cell in self.cells())

    def genome(self):
        return "".join(cell.gene.value for cell in self.cells())

    def stimulation_count(self):
        return sum(cell.stimulation_count for cell in self.cells())

    def can_reproduce(self):
        return self.stimulation_count() >= self.MINIMUM_STIMULATION_COUNT and self.can_afford_reproduction()

    def can_afford_reproduction(self):
        return self.health() >= self.MINIMUM_REPRODUCTION_HEALTH

    def health(self):
        return sum(cell.health for cell in self.cells())

    def subtract_reproduction_cost(self):
        for cell in self.cells():
            cell.subtract_reproduction_cost()

    def genome_color(self):
        """Get a color based on the genome checksum for visual identification."""
        genome_string = self.genome()

        # Create a simple checksum from the genome string
        checksum = 0
        for i, char in enumerate(genome_string):
            checksum += ord(char) * (i + 1)

        # Convert checksum to RGB values
        # Use modulo to keep values in 0-255 range, with some offset for visibility
        r = (checksum % 200) + 55  # 55-254 range
        g = ((checksum >> 8) % 200) + 55
        b = ((checksum >> 16) % 200) + 55

        return (r, g, b)

    def _update_position_cache(self):
        """Cache current cell positions for movement detection."""
        self._last_cell_positions = [(cell.q, cell.r, cell.s) for cell in self.cells()]

    def _have_cells_moved(self):
        """Check if any cells have moved since last update."""
        if self._last_cell_positions is None:
            return True

        current_positions = [(cell.q, cell.r, cell.s) for cell in self.cells()]

        if current_positions != self._last_cell_positions:
            self._update_position_cache()  # Update cache with new positions
            return True

        return False
