from .screen import Screen

class OrganismRendering:
    def __init__(self, organism, screen):
        self.organism = organism
        self.screen = screen

    def cell_renderings(self, camera):
        cell_renderings = []
        # Get vertices directly from Box2D fixtures
        for i, fixture in enumerate(self.organism.body.fixtures):
            shape = fixture.shape
            vertices = []

            # Transform each vertex from local to world coordinates, then apply camera
            for vertex in shape.vertices:
                world_vertex = self.organism.body.transform * vertex

                # Apply camera transformation
                screen_x, screen_y = camera.world_to_screen(world_vertex.x, world_vertex.y)
                pixel_x = Screen.to_pixels(screen_x)
                pixel_y = Screen.to_pixels(screen_y)

                vertices.append((pixel_x, pixel_y))

            # Get the corresponding cell for colors
            if i < len(self.organism.cells()):
                cell = self.organism.cells()[i]
                cell_renderings.append({
                    'vertices': vertices,
                    'border_color': cell.border_color,
                    'fill_color': cell.fill_color
                })
        return cell_renderings
