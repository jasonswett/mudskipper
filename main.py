import pygame
import Box2D
import math
import random

from src.genome import Genome
from src.cell import Cell
from src.cellular_body_builder import CellularBodyBuilder

from src.organism import Organism
from src.organism_rendering import OrganismRendering
from src.screen import Screen

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
ORGANISM_COUNT = 40

def draw_organisms(world, screen, display):
    organisms = []
    remaining_organisms = ORGANISM_COUNT

    while remaining_organisms > 0:
        genome = Genome(2)
        cellular_body_builder = CellularBodyBuilder(genome.cell_genes())
        cellular_body = cellular_body_builder.cellular_body()
        if cellular_body.is_legal():
            print(genome.value())
            # Generate random position within screen bounds
            x = random.uniform(5, screen.width - 5)  # Leave margin from edges
            y = random.uniform(5, screen.height - 5)  # Leave margin from edges
            organisms.append(Organism(world, cellular_body, (x, y)))
            remaining_organisms -= 1

    return organisms

def main():
    pygame.init()
    screen = Screen(60, 35) # unit: meters
    display = pygame.display.set_mode(screen.size_in_pixels())
    pygame.display.set_caption("Mudskipper")
    clock = pygame.time.Clock()
    world = Box2D.b2World(gravity=(0, 0))
    organisms = draw_organisms(world, screen, display)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    organisms.clear()
                    organisms = draw_organisms(world, screen, display)

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
