import Box2D
PIXELS_PER_METER = 20.0 # Pixels per meter for Box2D conversion

class Organism:
    def __init__(self, world, cell_hexagon, position):
        body_def = Box2D.b2BodyDef()
        body_def.type = Box2D.b2_staticBody
        body_def.position = (position[0] / PIXELS_PER_METER, position[1] / PIXELS_PER_METER)  # Convert pixels to Box2D units
        self.body = world.CreateBody(body_def)

        hexagon_shape = Box2D.b2PolygonShape(vertices=cell_hexagon.vertices())
        self.body.CreateFixture(shape=hexagon_shape, density=1.0)
