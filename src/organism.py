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
            vertices = self.box2d_cell_vertices(cell)
            hexagon_shape = Box2D.b2PolygonShape(vertices=vertices)
            self.body.CreateFixture(shape=hexagon_shape, density=1.0)

    def cells(self):
        return self.cellular_body.cells

    def update_clock(self):
        self.cellular_body.update_clock()
        self.update_fixtures()
    
    def update_fixtures(self):
        """Recreate all fixtures based on current cell positions."""
        # Remove all existing fixtures
        for fixture in self.body.fixtures:
            self.body.DestroyFixture(fixture)
        
        # Create new fixtures based on current cell positions
        for cell in self.cells():
            vertices = self.box2d_cell_vertices(cell)
            hexagon_shape = Box2D.b2PolygonShape(vertices=vertices)
            self.body.CreateFixture(shape=hexagon_shape, density=1.0)
    
    def box2d_cell_vertices(self, cell):
        """Calculate vertices for a cell's hexagon in Box2D local coordinates."""
        vertices = []
        for i in range(6):
            angle = (math.pi / 3) * i
            x = ((3/2 * cell.q) * cell.radius) + cell.radius * math.cos(angle)
            y = ((math.sqrt(3)/2 * cell.q + math.sqrt(3) * cell.r) * cell.radius) + cell.radius * math.sin(angle)
            vertices.append((x, y))
        return vertices

    def nourish(self):
        for cell in self.cells():
            cell.nourish()

    def is_alive(self):
        return any(cell.is_alive() for cell in self.cells())
