import pygame
import Box2D
import math

from src.cell import Cell
from src.cell_sequence import CellSequence
from src.cell_builder import CellBuilder
from src.cell_gene import CellGene
from src.cellular_body import CellularBody

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
        CellGene("00011"),
        CellGene("00100"),
        CellGene("01000"),
        CellGene("10000"),
    ]

    deltas = [
        cell_gene.delta() for cell_gene in cell_genes
    ]

    cell_sequence = CellSequence(deltas)

    cells = []
    for index, position in enumerate(cell_sequence.positions):
        gene = cell_genes[index]
        cell_builder = CellBuilder(gene, position)
        cells.append(cell_builder.cell())

    cellular_body = CellularBody(cells)

    organism = Organism(world, cellular_body, screen.center())
    organism_rendering = OrganismRendering(organism, screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        organism.update_clock()
        display.fill(BLACK)

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
