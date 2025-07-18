from .screen import Screen

class OrganismRendering:
    def __init__(self, organism, screen):
        self.organism = organism
        self.screen = screen

    def screen_vertices(self):
        result = []
        screen_height_pixels = self.screen.height * Screen.PIXELS_PER_METER
        
        for fixture in self.organism.body.fixtures:
            vertices = []
            for vertex in fixture.shape.vertices:
                x = self.organism.body.position.x * Screen.PIXELS_PER_METER + vertex[0] * Screen.PIXELS_PER_METER
                y = screen_height_pixels - (self.organism.body.position.y * Screen.PIXELS_PER_METER + vertex[1] * Screen.PIXELS_PER_METER)  # Flip Y axis
                vertices.append((x, y))
            result.append(vertices)
        return result
