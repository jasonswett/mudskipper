from .screen import Screen

class OrganismRendering:
    def __init__(self, organism, screen):
        self.organism = organism
        self.screen = screen

    def cell_renderings(self, camera):
        cell_renderings = []
        world_vertices = self.vertices()  # Use the vertices() method

        for i, fixture_vertices in enumerate(world_vertices):
            # Apply camera transformation to world vertices
            screen_vertices = []
            for world_x, world_y in fixture_vertices:
                screen_x, screen_y = camera.world_to_screen(world_x, world_y)
                pixel_x = Screen.to_pixels(screen_x)
                pixel_y = Screen.to_pixels(screen_y)
                screen_vertices.append((pixel_x, pixel_y))

            # Get the corresponding cell for colors
            if i < len(self.organism.cells()):
                cell = self.organism.cells()[i]
                cell_renderings.append({
                    'vertices': screen_vertices,
                    'border_color': cell.border_color,
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

    def bounding_rectangle_pixels(self, camera):
        world_vertices = self.vertices()

        pixel_points = []
        for fixture_vertices in world_vertices:
            for world_x, world_y in fixture_vertices:
                screen_x, screen_y = camera.world_to_screen(world_x, world_y)
                pixel_x = Screen.to_pixels(screen_x)
                pixel_y = Screen.to_pixels(screen_y)
                pixel_points.append((pixel_x, pixel_y))

        min_x = min(point[0] for point in pixel_points)
        max_x = max(point[0] for point in pixel_points)
        min_y = min(point[1] for point in pixel_points)
        max_y = max(point[1] for point in pixel_points)

        return (int(min_x), int(min_y), int(max_x), int(max_y))
