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
            cell.update_clock(self)

    def neighbors(self, cell):
        neighbors = []

        neighbor_offsets = [
            (1, 0, -1),
            (1, -1, 0),
            (0, -1, 1),
            (-1, 0, 1),
            (-1, 1, 0),
            (0, 1, -1)
        ]
        
        for other_cell in self.cells():
            if other_cell != cell:
                q_diff = other_cell.q - cell.q
                r_diff = other_cell.r - cell.r
                s_diff = other_cell.s - cell.s
                if (q_diff, r_diff, s_diff) in neighbor_offsets:
                    neighbors.append(other_cell)
        return neighbors
