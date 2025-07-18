import pygame
import Box2D
import math
from src.cell_hexagon import CellHexagon
from src.organism_rendering import OrganismRendering
from src.screen import Screen

ORGANISM_CELL_RADIUS = 3
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

def main():
    pygame.init()
    screen = Screen(800, 600)
    display = pygame.display.set_mode(screen.size())
    pygame.display.set_caption("Mudskipper")
    clock = pygame.time.Clock()

    world = Box2D.b2World(gravity=(0, 0))
    cell_hexagon = CellHexagon(0, 0, ORGANISM_CELL_RADIUS, GREEN)
    organism_rendering = OrganismRendering(world, cell_hexagon, screen.center())

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        display.fill(BLACK)
        
        for screen_vertices in organism_rendering.screen_vertices():
            pygame.draw.polygon(display, cell_hexagon.color, screen_vertices, width=2)
        
        pygame.display.flip()
        clock.tick(60)
        
        # Step the physics simulation
        world.Step(1.0/60, 6, 2)
    
    pygame.quit()

if __name__ == "__main__":
    main()
