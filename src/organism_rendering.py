PIXELS_PER_METER = 20.0 # Pixels per meter for Box2D conversion

class OrganismRendering:
    def __init__(self, organism):
        self.organism = organism

    def screen_vertices(self):
        result = []
        for fixture in self.organism.body.fixtures:
            vertices = []
            for vertex in fixture.shape.vertices:
                # vertex is a tuple (x, y)
                x = self.organism.body.position.x * PIXELS_PER_METER + vertex[0] * PIXELS_PER_METER
                y = 600 - (self.organism.body.position.y * PIXELS_PER_METER + vertex[1] * PIXELS_PER_METER)  # Flip Y axis
                vertices.append((x, y))
            result.append(vertices)
        return result
