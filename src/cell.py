import math

class Cell:
    def __init__(self, coordinates, radius, color):
        self.x, self.y, self.z = coordinates
        self.radius = radius
        self.color = color

    def vertices(self):
        center_x, center_y = self.cube_to_pixel()
        vertices = []
        for i in range(6):
            angle = (math.pi / 3) * i
            x = center_x + self.radius * math.cos(angle)
            y = center_y + self.radius * math.sin(angle)
            vertices.append((x, y))
        return vertices

    def cube_to_pixel(self):
        """Convert cube coordinates to pixel coordinates"""
        px = self.radius * (math.sqrt(3) * self.x + math.sqrt(3)/2 * self.y)
        py = self.radius * (3/2 * self.y)
        return (px, py)
