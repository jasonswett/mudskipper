import Box2D
import math

class Organism:
    def __init__(self, world, cellular_body, position):
        body_def = Box2D.b2BodyDef()
        body_def.type = Box2D.b2_dynamicBody
        body_def.position = position
        self.body = world.CreateBody(body_def)
        self.cellular_body = cellular_body

        for cell in self.cells():
            # Calculate vertices locally - same as OrganismRendering.vertices()
            vertices = []
            for i in range(6):
                angle = (math.pi / 3) * i
                x = ((3/2 * cell.q) * cell.radius) + cell.radius * math.cos(angle)
                y = ((math.sqrt(3)/2 * cell.q + math.sqrt(3) * cell.r) * cell.radius) + cell.radius * math.sin(angle)
                vertices.append((x, y))
            
            hexagon_shape = Box2D.b2PolygonShape(vertices=vertices)
            self.body.CreateFixture(shape=hexagon_shape, density=1.0)

    def cells(self):
        return self.cellular_body.cells

    def update_clock(self):
        self.cellular_body.update_clock()
