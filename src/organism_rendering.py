import Box2D
PPM = 20.0 # Pixels per meter for Box2D conversion

class OrganismRendering:
    def __init__(self, world, cell_hexagon, position):
        self.cell_hexagon = cell_hexagon
        self.world = world

        body_def = Box2D.b2BodyDef()
        body_def.type = Box2D.b2_staticBody
        body_def.position = (position[0] / PPM, position[1] / PPM)  # Convert pixels to Box2D units

        self.body = world.CreateBody(body_def)

        hexagon_shape = Box2D.b2PolygonShape(vertices=cell_hexagon.vertices())
        self.body.CreateFixture(shape=hexagon_shape, density=1.0)

        self.fixtures = self.body.fixtures

    def screen_vertices(self):
        result = []
        for fixture in self.fixtures:
            vertices = []
            for vertex in fixture.shape.vertices:
                # vertex is a tuple (x, y)
                x = self.body.position.x * PPM + vertex[0] * PPM
                y = 600 - (self.body.position.y * PPM + vertex[1] * PPM)  # Flip Y axis
                vertices.append((x, y))
            result.append(vertices)
        return result
