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
from src.contact_listener import ContactListener
from src.camera import Camera

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
ORGANISM_COUNT = 50

def draw_organisms(world, world_width, world_height, display):
    organisms = []
    remaining_organisms = ORGANISM_COUNT

    while remaining_organisms > 0:
        genome = Genome(2)
        cellular_body_builder = CellularBodyBuilder(genome.cell_genes())
        cellular_body = cellular_body_builder.cellular_body()
        if cellular_body.is_legal():
            print(genome.value())
            # Generate random position within world bounds
            x = random.uniform(0, world_width)
            y = random.uniform(0, world_height)
            organisms.append(Organism(world, cellular_body, (x, y)))
            remaining_organisms -= 1

    return organisms

def create_food_morsels(world, world_width, world_height, count=200):
    food_morsels = []
    for _ in range(count):
        x = random.uniform(0, world_width)
        y = random.uniform(0, world_height)
        food_morsel = FoodMorsel(world, (x, y))
        food_morsels.append(food_morsel)
    return food_morsels

def create_walls(world, world_width, world_height):
    thickness = 1.0

    # Bottom wall
    world.CreateStaticBody(
        position=(world_width/2, thickness/2),
        shapes=Box2D.b2PolygonShape(box=(world_width/2, thickness/2))
    )

    # Top wall
    world.CreateStaticBody(
        position=(world_width/2, world_height - thickness/2),
        shapes=Box2D.b2PolygonShape(box=(world_width/2, thickness/2))
    )

    # Left wall
    world.CreateStaticBody(
        position=(thickness/2, world_height/2),
        shapes=Box2D.b2PolygonShape(box=(thickness/2, world_height/2))
    )

    # Right wall
    world.CreateStaticBody(
        position=(world_width - thickness/2, world_height/2),
        shapes=Box2D.b2PolygonShape(box=(thickness/2, world_height/2))
    )


def main():
    pygame.init()
    # World size (physics simulation area)
    world_width, world_height = (30, 20) # meters

    # Display size (viewport window)
    screen = Screen(40, 30) # unit: meters (viewport size)
    display = pygame.display.set_mode(screen.size_in_pixels())
    pygame.display.set_caption("Mudskipper")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)
    world = Box2D.b2World(gravity=(0, 0))
    create_walls(world, world_width, world_height)
    organisms = draw_organisms(world, world_width, world_height, display)
    food_morsels = create_food_morsels(world, world_width, world_height)
    world.contactListener = ContactListener(organisms, food_morsels)

    # Create camera
    camera = Camera(world_width, world_height, screen.width, screen.height)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    organisms.clear()
                    organisms = draw_organisms(world, world_width, world_height, display)
                    food_morsels = create_food_morsels(world, world_width, world_height)
                    world.contactListener = ContactListener(organisms, food_morsels)

        # Continuous camera movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            camera.move(-0.5, 0)
        if keys[pygame.K_RIGHT]:
            camera.move(0.5, 0)
        if keys[pygame.K_UP]:
            camera.move(0, -0.5)
        if keys[pygame.K_DOWN]:
            camera.move(0, 0.5)

        display.fill(BLACK)

        # Remove dead organisms and draw living ones
        organisms_to_remove = []
        for organism in organisms:
            organism.update_clock()
            if organism.is_alive():
                organism_rendering = OrganismRendering(organism, screen)
                for cell_rendering in organism_rendering.cell_renderings(camera):
                    pygame.draw.polygon(display, cell_rendering['fill_color'], cell_rendering['vertices'])
                    pygame.draw.polygon(display, cell_rendering['border_color'], cell_rendering['vertices'], width=2)
            else:
                world.DestroyBody(organism.body)
                organisms_to_remove.append(organism)

        for organism in organisms_to_remove:
            organisms.remove(organism)

        # Remove eaten food and draw remaining food
        food_morsels_to_remove = []
        for food_morsel in food_morsels:
            if food_morsel.eaten:
                world.DestroyBody(food_morsel.body)
                food_morsels_to_remove.append(food_morsel)
            else:
                pos = food_morsel.body.position
                screen_x, screen_y = camera.world_to_screen(pos.x, pos.y)
                x = Screen.to_pixels(screen_x)
                y = Screen.to_pixels(screen_y)
                radius = Screen.to_pixels(food_morsel.radius)
                pygame.draw.circle(display, GREEN, (int(x), int(y)), int(radius))

        for food_morsel in food_morsels_to_remove:
            food_morsels.remove(food_morsel)

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
