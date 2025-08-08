import Box2D
import math

class Organism:
    MINIMUM_STIMULATION_COUNT = 40
    MINIMUM_REPRODUCTION_HEALTH = 200

    def __init__(self, world, cellular_body, position, genome=None):
        body_def = Box2D.b2BodyDef()
        body_def.type = Box2D.b2_dynamicBody
        body_def.position = position
        self.body = world.CreateBody(body_def)
        self.cellular_body = cellular_body
        self._genome = genome
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
        try:
            # Remove all existing fixtures (collect first to avoid iterator invalidation)
            fixtures_to_destroy = list(self.body.fixtures)
            for fixture in fixtures_to_destroy:
                self.body.DestroyFixture(fixture)

            # Create new fixtures based on current cell positions
            for cell in self.cells():
                vertices = self.box2d_cell_vertices(cell)
                hexagon_shape = Box2D.b2PolygonShape(vertices=vertices)
                self.body.CreateFixture(shape=hexagon_shape, density=1.0)
        except AssertionError as e:
            print(f"WARNING: Box2D fixture update failed: {e}")
            print(f"  Organism health: {self.health()}")
            print(f"  Living cells: {sum(1 for cell in self.cells() if cell.is_alive())} / {len(self.cells())}")
            print(f"  Cell positions: {[(cell.q, cell.r, cell.s) for cell in self.cells()]}")
            print(f"  Fixtures before update: {len(fixtures_to_destroy)}")
            print(f"  Organism Box2D position: ({self.body.position.x:.1f}, {self.body.position.y:.1f})")

            # Convert hex positions to world coordinates
            world_positions = []
            for cell in self.cells():
                world_x = (3/2 * cell.q) * cell.radius
                world_y = (math.sqrt(3)/2 * cell.q + math.sqrt(3) * cell.r) * cell.radius
                world_positions.append((world_x, world_y))
            print(f"  Cell world coordinates: {world_positions}")

            print(f"  Organism genome: {self.genome()[:20]}...")
            print("  Organism may not have proper physics.")

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
        if self._genome:
            return self._genome.value()
        else:
            # Fallback to old method if no genome stored
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
        import hashlib

        genome_string = self.genome()

        # Use MD5 hash for better distribution
        hash_bytes = hashlib.md5(genome_string.encode()).digest()

        # Extract RGB from different parts of hash for independence
        r = hash_bytes[0] % 200 + 55  # 55-254 range (avoid too dark/light)
        g = hash_bytes[1] % 200 + 55
        b = hash_bytes[2] % 200 + 55

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

    def sync_hex_coordinates_to_body_position(self):
        """Synchronize cell hex coordinates to match current Box2D body position after toroidal wrapping."""
        if not self.cells():
            return

        # Get the current body position
        body_x, body_y = self.body.position.x, self.body.position.y

        # Calculate what the first cell's hex coordinates should be to place it near body position
        # We'll use the first cell as reference and adjust all cells relative to it
        first_cell = self.cells()[0]

        # Calculate where the first cell currently appears in world coordinates
        current_world_x = (3/2 * first_cell.q) * first_cell.radius
        current_world_y = (math.sqrt(3)/2 * first_cell.q + math.sqrt(3) * first_cell.r) * first_cell.radius

        # Calculate the offset needed to move the first cell near the body position
        offset_x = body_x - current_world_x
        offset_y = body_y - current_world_y

        # Convert the offset back to hex coordinates
        # This is the inverse of the hex-to-world coordinate transformation
        # world_x = (3/2 * q) * radius
        # world_y = (sqrt(3)/2 * q + sqrt(3) * r) * radius

        # Solve for q and r offsets:
        radius = first_cell.radius
        q_offset = (2 * offset_x) / (3 * radius)
        # For r offset, we use: offset_y = (sqrt(3)/2 * q_offset + sqrt(3) * r_offset) * radius
        r_offset = (offset_y / radius - (math.sqrt(3)/2 * q_offset)) / math.sqrt(3)

        # Round to nearest integers since hex coordinates must be integers
        q_offset = round(q_offset)
        r_offset = round(r_offset)
        s_offset = -(q_offset + r_offset)  # Maintain q + r + s = 0 constraint

        # Apply the offset to all cells
        for cell in self.cells():
            cell.q += q_offset
            cell.r += r_offset
            cell.s += s_offset

        # Mark fixtures as needing update since cell positions changed
        self.fixtures_need_update = True
        self._update_position_cache()
