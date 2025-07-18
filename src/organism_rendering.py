from .screen import Screen

class OrganismRendering:
    def __init__(self, organism, screen):
        self.organism = organism
        self.screen = screen

    def screen_vertex_positions(self):
        positions = []
        for fixture in self.organism.body.fixtures:
            vertices = []
            for vertex in fixture.shape.vertices:
                vertices.append((self.vertex_x(vertex), self.vertex_y(vertex)))
            positions.append(vertices)
        return positions

    def vertex_x(self, vertex):
        return Screen.to_pixels(self.organism.body.position.x) + Screen.to_pixels(vertex[0])

    def vertex_y(self, vertex):
        return self.screen.height_in_pixels() - (Screen.to_pixels(self.organism.body.position.y) + Screen.to_pixels(vertex[1]))
