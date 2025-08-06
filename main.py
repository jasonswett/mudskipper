import pygame
import Box2D
import math
import random

from src.genome import Genome
from src.cell import Cell
from src.cellular_body_builder import CellularBodyBuilder

from src.cell_gene import CellGene
from src.cell_builder import CellBuilder
from src.cellular_body import CellularBody

from src.organism import Organism
from src.organism_rendering import OrganismRendering
from src.screen import Screen
from src.food_morsel import FoodMorsel
from src.contact_listener import ContactListener
from src.camera import Camera

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)
ORGANISM_COUNT = 3

def draw_organisms(world, world_width, world_height, display):
    organisms = []
    remaining_organisms = ORGANISM_COUNT

    cell_genes = [
        CellGene("000" + "100" + "100" + "11"),
        CellGene("011" + "100" + "100" + "10"),
        CellGene("001" + "011" + "100" + "10"),
    ]
    positions = [(0, 0, 0), (1, 0, -1), (1, -1, 0)]
    cells = [CellBuilder(cell_gene, position).cell()
             for cell_gene, position in zip(cell_genes, positions)]

    organisms.append(Organism(world, CellularBody(cells), (0.5, 0.5)))

    cell_genes = [
        CellGene("000" + "100" + "100" + "11"),
        CellGene("011" + "100" + "100" + "10"),
    ]
    positions = [(0, 0, 0), (1, 0, -1)]
    cells = [CellBuilder(cell_gene, position).cell()
             for cell_gene, position in zip(cell_genes, positions)]

    organisms.append(Organism(world, CellularBody(cells), (5, 5)))

    return organisms

    # This code is unreachable due to the return above - removing it
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
    world_width, world_height = (20, 20) # meters

    # Display size (viewport window)
    screen = Screen(30, 30) # unit: meters (viewport size)
    display = pygame.display.set_mode(screen.size_in_pixels())
    pygame.display.set_caption("Mudskipper")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)
    world = Box2D.b2World(gravity=(0, 0))
    organisms = draw_organisms(world, world_width, world_height, display)

    # Create camera and center the world on screen
    camera = Camera(world_width, world_height, screen.width, screen.height)
    camera.x = -((screen.width - world_width) / 2)
    camera.y = -((screen.height - world_height) / 2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    organisms.clear()
                    organisms = draw_organisms(world, world_width, world_height, display)

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

        # Draw gray border around the world
        world_x1, world_y1 = camera.world_to_screen(0, 0)
        world_x2, world_y2 = camera.world_to_screen(world_width, world_height)
        world_rect = pygame.Rect(
            Screen.to_pixels(world_x1),
            Screen.to_pixels(world_y1),
            Screen.to_pixels(world_x2 - world_x1),
            Screen.to_pixels(world_y2 - world_y1)
        )
        pygame.draw.rect(display, GRAY, world_rect, 2)

        # Remove dead organisms and draw living ones
        organisms_to_remove = []
        for i, organism in enumerate(organisms):
            organism.update_clock()
            if organism.is_alive():
                org_pos = organism.body.position

                organism_rendering = OrganismRendering(organism, screen, camera)

                # Check if organism needs toroidal teleportation
                wrap_position = organism_rendering.get_wrap_position(world_width, world_height)
                if wrap_position:
                    # Teleport organism to wrapped position
                    organism.body.position = wrap_position
                    # Note: Ghost will automatically disappear since organism is no longer outside bounds

                # Draw main organism
                for cell_rendering in organism_rendering.cell_renderings():
                    pygame.draw.polygon(display, cell_rendering['fill_color'], cell_rendering['vertices'])
                    pygame.draw.polygon(display, cell_rendering['border_color'], cell_rendering['vertices'], width=2)

                # Draw ghost organisms for toroidal world
                ghost_renderings = organism_rendering.ghost_rendering(world_width, world_height)
                for cell_rendering in ghost_renderings:
                    pygame.draw.polygon(display, cell_rendering['fill_color'], cell_rendering['vertices'])
                    pygame.draw.polygon(display, cell_rendering['border_color'], cell_rendering['vertices'], width=2)

                # Draw yellow bounding rectangle using pixel-accurate method
                pixel_x1, pixel_y1, pixel_x2, pixel_y2 = organism_rendering.bounding_rectangle_pixels()
                bounding_rect = pygame.Rect(
                    pixel_x1,
                    pixel_y1,
                    pixel_x2 - pixel_x1,
                    pixel_y2 - pixel_y1
                )
                pygame.draw.rect(display, YELLOW, bounding_rect, 2)
            else:
                world.DestroyBody(organism.body)
                organisms_to_remove.append(organism)

        for organism in organisms_to_remove:
            organisms.remove(organism)

        organism_text = f"Organisms: {len(organisms)}"
        organism_surface = font.render(organism_text, False, WHITE)
        display.blit(organism_surface, (10, 10))

        pygame.display.flip()
        clock.tick(60)

        # Step the physics simulation
        world.Step(1.0/60, 6, 2)

    pygame.quit()

if __name__ == "__main__":
    main()
