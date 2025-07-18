import pygame
import Box2D
import math
from src.cell_hexagon import CellHexagon
from src.organism_rendering import OrganismRendering

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ORGANISM_CELL_RADIUS = 3

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Mudskipper - Hexagon")
    clock = pygame.time.Clock()

    world = Box2D.b2World(gravity=(0, 0))
    cell_hexagon = CellHexagon(0, 0, ORGANISM_CELL_RADIUS)
    position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    organism_rendering = OrganismRendering(world, cell_hexagon, position)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(BLACK)
        
        for screen_vertices in organism_rendering.screen_vertices():
            pygame.draw.polygon(screen, GREEN, screen_vertices, width=2)
        
        pygame.display.flip()
        clock.tick(60)
        
        # Step the physics simulation
        world.Step(1.0/60, 6, 2)
    
    pygame.quit()

if __name__ == "__main__":
    main()
