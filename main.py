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
from src.food_morsel import FoodMorsel

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
ORGANISM_COUNT = 20

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

def create_food_morsels(world, screen, count=200):
    food_morsels = []
    for _ in range(count):
        x = random.uniform(2, screen.width - 2)
        y = random.uniform(2, screen.height - 2)
        food_morsel = FoodMorsel(world, (x, y))
        food_morsels.append(food_morsel)
    return food_morsels

def main():
    pygame.init()
    screen = Screen(60, 35) # unit: meters
    display = pygame.display.set_mode(screen.size_in_pixels())
    pygame.display.set_caption("Mudskipper")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)
    world = Box2D.b2World(gravity=(0, 0))
    organisms = draw_organisms(world, screen, display)
    food_morsels = create_food_morsels(world, screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    organisms.clear()
                    organisms = draw_organisms(world, screen, display)
                    food_morsels = create_food_morsels(world, screen)

        display.fill(BLACK)

        for organism in organisms:
            organism.update_clock()
            organism_rendering = OrganismRendering(organism, screen)

            for cell_rendering in organism_rendering.cell_renderings():
                pygame.draw.polygon(display, cell_rendering['fill_color'], cell_rendering['vertices'])
                pygame.draw.polygon(display, cell_rendering['border_color'], cell_rendering['vertices'], width=2)

        # Draw food morsels
        for food_morsel in food_morsels:
            food_pixel_x = Screen.to_pixels(food_morsel.position[0])
            food_pixel_y = Screen.to_pixels(food_morsel.position[1])
            food_radius_pixels = Screen.to_pixels(food_morsel.radius)
            pygame.draw.circle(display, GREEN, (int(food_pixel_x), int(food_pixel_y)), int(food_radius_pixels))

        organism_text = f"Organisms: {len(organisms)}"
        organism_surface = font.render(organism_text, False, WHITE)
        display.blit(organism_surface, (10, 10))
        
        food_text = f"Food: {len(food_morsels)}"
        food_surface = font.render(food_text, False, WHITE)
        display.blit(food_surface, (10, 30))

        pygame.display.flip()
        clock.tick(60)
        
        # Step the physics simulation
        world.Step(1.0/60, 6, 2)
    
    pygame.quit()

if __name__ == "__main__":
    main()
