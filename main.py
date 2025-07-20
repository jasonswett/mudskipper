import pygame
import Box2D
import math

from src.cell import Cell
from src.cell_sequence import CellSequence
from src.cell_gene import CellGene
from src.organism import Organism
from src.organism_rendering import OrganismRendering
from src.screen import Screen

ORGANISM_CELL_RADIUS = 1
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

def main():
    pygame.init()
    screen = Screen(40, 30) # unit: meters
    display = pygame.display.set_mode(screen.size_in_pixels())
    pygame.display.set_caption("Mudskipper")
    clock = pygame.time.Clock()

    world = Box2D.b2World(gravity=(0, 0))

    cell_genes = [
        CellGene("000"),
        CellGene("001"),
        CellGene("010"),
    ]

    deltas = [
        cell_gene.delta() for cell_gene in cell_genes
    ]

    cell_sequence = CellSequence(deltas)

    organism = Organism(world, cell_sequence.cells, screen.center())
    organism_rendering = OrganismRendering(organism, screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        display.fill(BLACK)
        
        for position in organism_rendering.screen_vertex_positions():
            pygame.draw.polygon(display, GREEN, position, width=2)
        
        pygame.display.flip()
        clock.tick(60)
        
        # Step the physics simulation
        world.Step(1.0/60, 6, 2)
    
    pygame.quit()

if __name__ == "__main__":
    main()
