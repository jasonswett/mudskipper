import pygame
import Box2D
import math

from src.cell import Cell
from src.cell_gene import CellGene
from src.cellular_body_builder import CellularBodyBuilder

from src.organism import Organism
from src.organism_rendering import OrganismRendering
from src.screen import Screen

ORGANISM_CELL_RADIUS = 1
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
ORGANISM_COUNT = 3

def main():
    pygame.init()
    screen = Screen(40, 30) # unit: meters
    display = pygame.display.set_mode(screen.size_in_pixels())
    pygame.display.set_caption("Mudskipper")
    clock = pygame.time.Clock()
    world = Box2D.b2World(gravity=(0, 0))

    organisms = []

    for i in range(ORGANISM_COUNT):
        cell_genes = [
            CellGene("00011"),
            CellGene("00100"),
            CellGene("01000"),
            CellGene("10000"),
        ]

        cellular_body_builder = CellularBodyBuilder(cell_genes)
        cellular_body = cellular_body_builder.cellular_body()
        x, y = screen.center()
        organisms.append(Organism(world, cellular_body, (x - 10 + i * 10, y)))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        display.fill(BLACK)

        for organism in organisms:
            organism.update_clock()
            organism_rendering = OrganismRendering(organism, screen)

            for cell_rendering in organism_rendering.cell_renderings():
                pygame.draw.polygon(display, cell_rendering['fill_color'], cell_rendering['vertices'])
                pygame.draw.polygon(display, cell_rendering['border_color'], cell_rendering['vertices'], width=2)
        
        pygame.display.flip()
        clock.tick(60)
        
        # Step the physics simulation
        world.Step(1.0/60, 6, 2)
    
    pygame.quit()

if __name__ == "__main__":
    main()
