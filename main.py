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

# World and display constants
WORLD_WIDTH = 20  # meters
WORLD_HEIGHT = 20  # meters
GRID_SIZE = 3  # 3x3 grid
SCREEN_WIDTH = WORLD_WIDTH * GRID_SIZE  # 60 meters
SCREEN_HEIGHT = WORLD_HEIGHT * GRID_SIZE  # 60 meters

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
    world_width, world_height = (WORLD_WIDTH, WORLD_HEIGHT)

    # Display size (viewport window) - 3x3 grid of worlds
    screen = Screen(SCREEN_WIDTH, SCREEN_HEIGHT)
    display = pygame.display.set_mode(screen.size_in_pixels())
    pygame.display.set_caption("Mudskipper")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)
    world = Box2D.b2World(gravity=(0, 0))
    organisms = draw_organisms(world, world_width, world_height, display)

    # Create camera to view the 3x3 grid
    camera = Camera(screen.width, screen.height, screen.width, screen.height)
    camera.x = 0  # Start at top-left of viewport
    camera.y = 0

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

        # Draw 3x3 grid of world borders
        for grid_x in range(GRID_SIZE):
            for grid_y in range(GRID_SIZE):
                # Calculate offset for this grid cell
                offset_x = grid_x * world_width
                offset_y = grid_y * world_height

                # Draw world border for this grid cell
                world_x1, world_y1 = camera.world_to_screen(offset_x, offset_y)
                world_x2, world_y2 = camera.world_to_screen(offset_x + world_width, offset_y + world_height)
                world_rect = pygame.Rect(
                    Screen.to_pixels(world_x1),
                    Screen.to_pixels(world_y1),
                    Screen.to_pixels(world_x2 - world_x1),
                    Screen.to_pixels(world_y2 - world_y1)
                )
                # Center world (1,1) gets gray border, others get white
                border_color = GRAY if grid_x == 1 and grid_y == 1 else WHITE
                pygame.draw.rect(display, border_color, world_rect, 2)

        # Draw organisms in all 9 grid cells
        for grid_x in range(GRID_SIZE):
            for grid_y in range(GRID_SIZE):
                # Calculate offset for this grid cell
                offset_x = grid_x * world_width
                offset_y = grid_y * world_height

                # Draw all organisms in this grid cell
                for organism in organisms:
                    if organism.is_alive():
                        organism_rendering = OrganismRendering(organism, screen, camera)

                        # Draw organism at offset position for this grid cell
                        cell_renderings = organism_rendering._cell_renderings_with_offset(offset_x, offset_y)
                        for cell_rendering in cell_renderings:
                            pygame.draw.polygon(display, cell_rendering['fill_color'], cell_rendering['vertices'])
                            pygame.draw.polygon(display, cell_rendering['border_color'], cell_rendering['vertices'], width=2)

                        # Draw ghost organisms for this grid cell
                        ghost_renderings = organism_rendering.ghost_rendering_with_grid_offset(world_width, world_height, offset_x, offset_y)
                        for ghost_rendering in ghost_renderings:
                            pygame.draw.polygon(display, ghost_rendering['fill_color'], ghost_rendering['vertices'])
                            pygame.draw.polygon(display, ghost_rendering['border_color'], ghost_rendering['vertices'], width=2)

                        # Draw yellow bounding rectangle only in center grid
                        if grid_x == 1 and grid_y == 1:
                            pixel_x1, pixel_y1, pixel_x2, pixel_y2 = organism_rendering.bounding_rectangle_pixels()
                            pixel_x1 += Screen.to_pixels(offset_x)
                            pixel_y1 += Screen.to_pixels(offset_y)
                            pixel_x2 += Screen.to_pixels(offset_x)
                            pixel_y2 += Screen.to_pixels(offset_y)
                            bounding_rect = pygame.Rect(
                                pixel_x1,
                                pixel_y1,
                                pixel_x2 - pixel_x1,
                                pixel_y2 - pixel_y1
                            )
                            pygame.draw.rect(display, YELLOW, bounding_rect, 2)

        # Update organisms and handle toroidal wrapping
        organisms_to_remove = []
        for organism in organisms:
            organism.update_clock()
            if organism.is_alive():
                organism_rendering = OrganismRendering(organism, screen, camera)

                # Check if organism needs toroidal teleportation
                wrap_position = organism_rendering.get_wrap_position(world_width, world_height)
                if wrap_position:
                    # Teleport organism to wrapped position
                    organism.body.position = wrap_position
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
