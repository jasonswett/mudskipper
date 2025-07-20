import math

class Cell:
    def __init__(self, coordinates, radius, color):
        self.x, self.y, self.z = coordinates
        self.radius = radius
        self.color = color

    def vertices(self):
        center_x = math.sqrt(3) * self.x + math.sqrt(3)/2 * self.y
        center_y = 3/2 * self.y

        vertices = []
        for i in range(6):
            angle = (math.pi / 3) * i
            x = center_x + math.cos(angle)
            y = center_y + math.sin(angle)
            vertices.append((x, y))
        return vertices
