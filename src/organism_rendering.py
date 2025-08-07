from .screen import Screen

class OrganismRendering:
    def __init__(self, organism, screen, camera):
        self.organism = organism
        self.screen = screen
        self.camera = camera

    def cell_renderings(self):
        return self._cell_renderings_with_offset(0, 0)

    def _cell_renderings_with_offset(self, offset_x, offset_y):
        """Generate cell renderings with optional world coordinate offset."""
        cell_renderings = []
        world_vertices = self.vertices()

        for i, fixture_vertices in enumerate(world_vertices):
            screen_vertices = []
            for world_x, world_y in fixture_vertices:
                # Apply offset to world coordinates
                offset_world_x = world_x + offset_x
                offset_world_y = world_y + offset_y

                # Transform to screen coordinates
                screen_x, screen_y = self.camera.world_to_screen(offset_world_x, offset_world_y)
                pixel_x = Screen.to_pixels(screen_x)
                pixel_y = Screen.to_pixels(screen_y)
                screen_vertices.append((pixel_x, pixel_y))

            # Get the corresponding cell for colors
            if i < len(self.organism.cells()):
                cell = self.organism.cells()[i]
                cell_renderings.append({
                    'vertices': screen_vertices,
                    'border_color': self.organism.genome_color(),
                    'fill_color': cell.fill_color
                })
        return cell_renderings

    def vertices(self):
        """Get all organism vertices in world coordinates (no camera transformation)."""
        all_vertices = []
        # Get vertices directly from Box2D fixtures
        for fixture in self.organism.body.fixtures:
            shape = fixture.shape
            fixture_vertices = []

            # Transform each vertex from local to world coordinates
            for vertex in shape.vertices:
                world_vertex = self.organism.body.transform * vertex
                fixture_vertices.append((world_vertex.x, world_vertex.y))

            all_vertices.append(fixture_vertices)
        return all_vertices

    def bounding_rectangle(self):
        """Get the bounding rectangle in world coordinates as (min_x, min_y, max_x, max_y)."""
        points = []
        for vertices in self.vertices():
            points.extend(vertices)

        if not points:
            return (0.0, 0.0, 0.0, 0.0)

        min_x = min(vertex[0] for vertex in points)
        max_x = max(vertex[0] for vertex in points)
        min_y = min(vertex[1] for vertex in points)
        max_y = max(vertex[1] for vertex in points)

        return (min_x, min_y, max_x, max_y)

    def bounding_rectangle_pixels(self):
        world_vertices = self.vertices()

        pixel_points = []
        for fixture_vertices in world_vertices:
            for world_x, world_y in fixture_vertices:
                screen_x, screen_y = self.camera.world_to_screen(world_x, world_y)
                pixel_x = Screen.to_pixels(screen_x)
                pixel_y = Screen.to_pixels(screen_y)
                pixel_points.append((pixel_x, pixel_y))

        min_x = min(point[0] for point in pixel_points)
        max_x = max(point[0] for point in pixel_points)
        min_y = min(point[1] for point in pixel_points)
        max_y = max(point[1] for point in pixel_points)

        return (int(min_x), int(min_y), int(max_x), int(max_y))

    def _get_wrap_offsets(self, world_width, world_height):
        """Calculate all wrap offsets needed for ghost organisms."""
        min_x, min_y, max_x, max_y = self.bounding_rectangle()

        wrap_offsets = []
        wrap_left = min_x < 0
        wrap_right = max_x > world_width
        wrap_bottom = min_y < 0
        wrap_top = max_y > world_height

        # Single-edge wrapping
        if wrap_left:
            wrap_offsets.append((world_width, 0))
        if wrap_right:
            wrap_offsets.append((-world_width, 0))
        if wrap_bottom:
            wrap_offsets.append((0, world_height))
        if wrap_top:
            wrap_offsets.append((0, -world_height))

        # Corner wrapping
        if wrap_left and wrap_bottom:
            wrap_offsets.append((world_width, world_height))
        if wrap_left and wrap_top:
            wrap_offsets.append((world_width, -world_height))
        if wrap_right and wrap_bottom:
            wrap_offsets.append((-world_width, world_height))
        if wrap_right and wrap_top:
            wrap_offsets.append((-world_width, -world_height))

        return wrap_offsets

    def ghost_rendering(self, world_width, world_height):
        """Return ghost cell renderings if organism extends outside world bounds, otherwise empty list."""
        wrap_offsets = self._get_wrap_offsets(world_width, world_height)

        if not wrap_offsets:
            return []

        ghost_renderings = []
        for offset_x, offset_y in wrap_offsets:
            ghost_renderings.extend(self._cell_renderings_with_offset(offset_x, offset_y))

        return ghost_renderings

    def ghost_rendering_with_grid_offset(self, world_width, world_height, grid_offset_x, grid_offset_y):
        """Return ghost cell renderings with additional grid offset for 3x3 display."""
        wrap_offsets = self._get_wrap_offsets(world_width, world_height)

        if not wrap_offsets:
            return []

        ghost_renderings = []
        for offset_x, offset_y in wrap_offsets:
            # Combine wrap offset with grid offset
            total_offset_x = offset_x + grid_offset_x
            total_offset_y = offset_y + grid_offset_y
            ghost_renderings.extend(self._cell_renderings_with_offset(total_offset_x, total_offset_y))

        return ghost_renderings

    def is_completely_outside_world(self, world_width, world_height):
        """Check if organism's bounding rectangle is completely outside world bounds."""
        min_x, min_y, max_x, max_y = self.bounding_rectangle()

        # Check if completely outside on any side
        completely_left = max_x < 0
        completely_right = min_x > world_width
        completely_bottom = max_y < 0
        completely_top = min_y > world_height

        return completely_left or completely_right or completely_bottom or completely_top

    def get_wrap_position(self, world_width, world_height):
        """Get the wrapped position for toroidal teleportation."""
        if not self.is_completely_outside_world(world_width, world_height):
            return None

        current_x, current_y = self.organism.body.position
        new_x, new_y = current_x, current_y

        # Wrap position based on which side we exited
        min_x, min_y, max_x, max_y = self.bounding_rectangle()

        if max_x < 0:  # Completely left
            new_x += world_width
        elif min_x > world_width:  # Completely right
            new_x -= world_width

        if max_y < 0:  # Completely bottom
            new_y += world_height
        elif min_y > world_height:  # Completely top
            new_y -= world_height

        return (new_x, new_y)
