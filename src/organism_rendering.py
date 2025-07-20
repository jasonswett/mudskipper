from .screen import Screen

class OrganismRendering:
    def __init__(self, organism, screen):
        self.organism = organism
        self.screen = screen

    def cell_renderings(self):
        cell_renderings = []
        for cell in self.organism.cells:
            vertices = []
            for vertex in cell.vertices():
                vertices.append((self.vertex_x(vertex), self.vertex_y(vertex)))
            cell_renderings.append({
                'vertices': vertices,
                'border_color': cell.border_color,
                'fill_color': cell.fill_color
            })
        return cell_renderings

    def vertex_x(self, vertex):
        return Screen.to_pixels(self.organism.body.position.x) + Screen.to_pixels(vertex[0])

    def vertex_y(self, vertex):
        return Screen.to_pixels(self.organism.body.position.y) + Screen.to_pixels(vertex[1])
