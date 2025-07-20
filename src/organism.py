import Box2D

class Organism:
    def __init__(self, world, cellular_body, position):
        body_def = Box2D.b2BodyDef()
        body_def.type = Box2D.b2_staticBody
        body_def.position = position
        self.body = world.CreateBody(body_def)
        self.cellular_body = cellular_body

        for cell in self.cells():
            hexagon_shape = Box2D.b2PolygonShape(vertices=cell.vertices())
            self.body.CreateFixture(shape=hexagon_shape, density=1.0)

    def cells(self):
        return self.cellular_body.cells

    def update_clock(self):
        for cell in self.cells():
            cell.update_clock(self.cellular_body)
