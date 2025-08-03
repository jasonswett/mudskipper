from .screen import Screen
import math

class OrganismRendering:
    def __init__(self, organism, screen):
        self.organism = organism
        self.screen = screen

    def cell_renderings(self):
        cell_renderings = []
        # Get vertices directly from Box2D fixtures
        for i, fixture in enumerate(self.organism.body.fixtures):
            shape = fixture.shape
            vertices = []

            # Transform each vertex from local to world coordinates
            for vertex in shape.vertices:
                world_vertex = self.organism.body.transform * vertex
                pixel_x = Screen.to_pixels(world_vertex.x)
                pixel_y = Screen.to_pixels(world_vertex.y)
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

    def vertex_x(self, vertex):
        return Screen.to_pixels(self.organism.body.position.x) + Screen.to_pixels(vertex[0])

    def vertex_y(self, vertex):
        return Screen.to_pixels(self.organism.body.position.y) + Screen.to_pixels(vertex[1])

    def cell_center_x(self, cell):
        return (3/2 * cell.q) * cell.radius

    def cell_center_y(self, cell):
        return (math.sqrt(3)/2 * cell.q + math.sqrt(3) * cell.r) * cell.radius

    def cell_vertices(self, cell):
        vertices = []
        for i in range(6):
            angle = (math.pi / 3) * i
            x = self.cell_center_x(cell) + cell.radius * math.cos(angle)
            y = self.cell_center_y(cell) + cell.radius * math.sin(angle)
            vertices.append((x, y))
        return vertices
