import pygame
import Box2D
import math
import random
import time

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
DARK_GRAY = (64, 64, 64)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

WORLD_WIDTH = 40  # meters
WORLD_HEIGHT = 40  # meters
ORGANISM_COUNT = (WORLD_WIDTH * WORLD_HEIGHT) // 15

GRID_SIZE = 3  # 3x3 grid
SCREEN_WIDTH = 50
SCREEN_HEIGHT = 35

STARTING_FOOD_COUNT = 200
MUTATION_RATE = 0.01

def generate_organisms(world, world_width, world_height, display):
    organisms = []
    remaining_organisms = ORGANISM_COUNT

    # This code is unreachable due to the return above - removing it
    while remaining_organisms > 0:
        organisms.append(generate_organism(world, world_width, world_height, display))
        remaining_organisms -= 1

    return organisms

def generate_organism(world, world_width, world_height, display):
    # Keep trying until we get a legal cellular body
    while True:
        genome = Genome(2)
        cellular_body_builder = CellularBodyBuilder(genome.cell_genes())
        cellular_body = cellular_body_builder.cellular_body()

        if cellular_body.is_legal():
            print(genome.value())
            # Generate random position within world bounds
            x = random.uniform(0, world_width)
            y = random.uniform(0, world_height)
            return Organism(world, cellular_body, (x, y))

def generate_offspring(parent_a_genome, parent_b_genome, world, world_width, world_height, position):
    # Keep trying until we get a legal cellular body
    while True:
        # Splice parent genomes
        spliced_genome_string = Genome.splice(parent_a_genome, parent_b_genome, 2).value()

        # Apply mutations
        mutated_genome_string = Genome.mutate(spliced_genome_string, mutation_rate=MUTATION_RATE)

        # Create offspring genome from mutated string
        offspring_genome = Genome.from_string(mutated_genome_string, 2)
        cellular_body_builder = CellularBodyBuilder(offspring_genome.cell_genes())
        cellular_body = cellular_body_builder.cellular_body()

        if cellular_body.is_legal():
            print(f"Offspring genome: {offspring_genome.value()}")
            return Organism(world, cellular_body, position)

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


def reset_world(world, world_width, world_height, display):
    organisms = generate_organisms(world, world_width, world_height, display)
    food_morsels = create_food_morsels(world, world_width, world_height, STARTING_FOOD_COUNT)
    contact_listener = ContactListener(organisms, food_morsels)
    world.contactListener = contact_listener
    return organisms, food_morsels, contact_listener

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

    organisms, food_morsels, contact_listener = reset_world(world, world_width, world_height, display)
    frame_count = 0
    run_number = 1
    run_start_time = time.time()

    # Records for longest run
    longest_run_duration = 0
    longest_run_number = 0

    # Create camera to view the 3x3 grid
    # Camera world size is the full 3x3 grid, viewport is the screen size
    camera = Camera(WORLD_WIDTH * GRID_SIZE, WORLD_HEIGHT * GRID_SIZE, screen.width, screen.height)
    # Start camera at origin
    camera.x = 0
    camera.y = 0

    contact_events = []

    # Display counters (update every 60 frames)
    population_count = len(organisms)
    food_count = len(food_morsels)

    print(f"Starting Run #{run_number} with {len(organisms)} organisms")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Calculate run duration
                    run_duration = time.time() - run_start_time
                    print(f"Run #{run_number} manually restarted after {run_duration:.1f} seconds")

                    # Check if this was the longest run
                    if run_duration > longest_run_duration:
                        longest_run_duration = run_duration
                        longest_run_number = run_number
                        print(f"New longest run record: {run_duration:.1f}s (Run #{run_number})")

                    run_number += 1
                    run_start_time = time.time()
                    organisms.clear()
                    organisms, food_morsels, contact_listener = reset_world(world, world_width, world_height, display)
                    population_count = len(organisms)
                    food_count = len(food_morsels)
                    print(f"Run #{run_number} started with {len(organisms)} organisms")

        frame_count += 1
        if frame_count % 60 == 0:
            print("-----------------------")
            print(f"tick: {frame_count}")

            # Get contact events from contact listener
            contact_events = contact_listener.get_contact_events()

            # Process each contact event
            for contact_event in contact_events:
                organism_a = contact_event['organism_a']
                organism_b = contact_event['organism_b']
                position = contact_event['position']

                print(f"Contact: {organism_a.genome()} + {organism_b.genome()}")

                if organism_a.can_reproduce() and organism_b.can_reproduce():
                    organism_a.subtract_reproduction_cost()
                    organism_b.subtract_reproduction_cost()

                    offspring = generate_offspring(
                        organism_a.genome(),
                        organism_b.genome(),
                        world, world_width, world_height, position
                    )
                    organisms.append(offspring)

            # Flush contact events
            contact_events = []

            # Update display counters
            population_count = len(organisms)
            food_count = len(food_morsels)

        if frame_count % 600 == 0:
            # Replenish food to starting level
            current_food_count = len(food_morsels)
            food_needed = STARTING_FOOD_COUNT - current_food_count
            if food_needed > 0:
                new_food = create_food_morsels(world, world_width, world_height, food_needed)
                food_morsels.extend(new_food)
                print(f"Replenished {food_needed} food morsels (total: {len(food_morsels)})")

        # Update food count every frame for responsiveness
        food_count = len(food_morsels)

        # Check if population is too low - restart if so
        if len(organisms) < 2:
            # Calculate run duration
            run_duration = time.time() - run_start_time
            print(f"Run #{run_number} ended - population fell to {len(organisms)} after {run_duration:.1f} seconds")

            # Check if this was the longest run
            if run_duration > longest_run_duration:
                longest_run_duration = run_duration
                longest_run_number = run_number
                print(f"New longest run record: {run_duration:.1f}s (Run #{run_number})")

            run_number += 1
            run_start_time = time.time()
            print(f"Starting Run #{run_number}")

            # Clear existing organisms and food from physics world
            for organism in organisms:
                world.DestroyBody(organism.body)
            for food_morsel in food_morsels:
                world.DestroyBody(food_morsel.body)

            # Reset everything
            organisms, food_morsels, contact_listener = reset_world(world, world_width, world_height, display)
            frame_count = 0
            population_count = len(organisms)
            food_count = len(food_morsels)
            contact_events = []

            print(f"Run #{run_number} started with {len(organisms)} organisms")
            if longest_run_duration > 0:
                print(f"Longest run so far: {longest_run_duration:.1f}s (Run #{longest_run_number})")

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

        # Calculate which tiles are needed based on what the camera can see
        # Find the leftmost and rightmost world coordinates that are visible
        left_world = camera.x
        right_world = camera.x + screen.width
        top_world = camera.y
        bottom_world = camera.y + screen.height

        # Calculate which tiles we need to cover this visible area
        left_tile = int(left_world // world_width) - 1  # Extra tile on left
        right_tile = int(right_world // world_width) + 1  # Extra tile on right
        top_tile = int(top_world // world_height) - 1  # Extra tile on top
        bottom_tile = int(bottom_world // world_height) + 1  # Extra tile on bottom

        base_tile_x = left_tile
        base_tile_y = top_tile
        tiles_to_draw_x = right_tile - left_tile + 1
        tiles_to_draw_y = bottom_tile - top_tile + 1

        # Draw all necessary tiles to cover the visible area
        for grid_x in range(tiles_to_draw_x):
            for grid_y in range(tiles_to_draw_y):
                # Calculate offset for this grid cell relative to the base tile
                offset_x = (base_tile_x + grid_x) * world_width
                offset_y = (base_tile_y + grid_y) * world_height

                # Draw world border for this grid cell
                world_x1, world_y1 = camera.world_to_screen(offset_x, offset_y)
                world_x2, world_y2 = camera.world_to_screen(offset_x + world_width, offset_y + world_height)
                world_rect = pygame.Rect(
                    Screen.to_pixels(world_x1),
                    Screen.to_pixels(world_y1),
                    Screen.to_pixels(world_x2 - world_x1),
                    Screen.to_pixels(world_y2 - world_y1)
                )
                # All tiles get dark gray borders
                pygame.draw.rect(display, DARK_GRAY, world_rect, 1)

        # Draw organisms in all visible tiles
        for grid_x in range(tiles_to_draw_x):
            for grid_y in range(tiles_to_draw_y):
                # Calculate offset for this grid cell relative to the base tile
                offset_x = (base_tile_x + grid_x) * world_width
                offset_y = (base_tile_y + grid_y) * world_height

                # Check if this tile is visible at all
                tile_left = offset_x
                tile_right = offset_x + world_width
                tile_top = offset_y
                tile_bottom = offset_y + world_height

                # If tile is completely outside camera view, skip it
                if (tile_right < camera.x or tile_left > camera.x + screen.width or
                    tile_bottom < camera.y or tile_top > camera.y + screen.height):
                    continue

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

                        # Draw yellow bounding rectangle only in the main world
                        tile_x = base_tile_x + grid_x
                        tile_y = base_tile_y + grid_y
                        if tile_x == 0 and tile_y == 0:
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
                            # Use red bounding rectangle if organism is touching another organism
                            rect_color = RED if contact_listener.is_organism_touching(organism) else YELLOW
                            pygame.draw.rect(display, rect_color, bounding_rect, 2)

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

        # Draw food morsels in all visible tiles
        for grid_x in range(tiles_to_draw_x):
            for grid_y in range(tiles_to_draw_y):
                # Calculate offset for this grid cell relative to the base tile
                offset_x = (base_tile_x + grid_x) * world_width
                offset_y = (base_tile_y + grid_y) * world_height

                # Draw all food morsels in this grid cell
                for food_morsel in food_morsels:
                    if not food_morsel.eaten:
                        pos = food_morsel.body.position
                        # Apply offset for this grid cell
                        screen_x, screen_y = camera.world_to_screen(pos.x + offset_x, pos.y + offset_y)
                        x = Screen.to_pixels(screen_x)
                        y = Screen.to_pixels(screen_y)
                        radius = Screen.to_pixels(food_morsel.radius)
                        pygame.draw.circle(display, GREEN, (int(x), int(y)), int(radius))

        # Remove eaten food morsels
        food_morsels_to_remove = []
        for food_morsel in food_morsels:
            if food_morsel.eaten:
                world.DestroyBody(food_morsel.body)
                food_morsels_to_remove.append(food_morsel)

        for food_morsel in food_morsels_to_remove:
            food_morsels.remove(food_morsel)

        # Display population, food counts, run number, and timer
        population_text = f"Population: {population_count}"
        population_surface = font.render(population_text, False, WHITE)
        display.blit(population_surface, (10, 10))

        food_text = f"Food: {food_count}"
        food_surface = font.render(food_text, False, WHITE)
        display.blit(food_surface, (10, 35))

        run_text = f"Run: {run_number}"
        run_surface = font.render(run_text, False, WHITE)
        display.blit(run_surface, (10, 60))

        # Current run timer
        current_run_time = time.time() - run_start_time
        timer_text = f"Time: {current_run_time:.1f}s"
        timer_surface = font.render(timer_text, False, WHITE)
        display.blit(timer_surface, (10, 85))

        # Longest run record
        if longest_run_duration > 0:
            record_text = f"Record: {longest_run_duration:.1f}s (Run #{longest_run_number})"
            record_surface = font.render(record_text, False, WHITE)
            display.blit(record_surface, (10, 110))

        pygame.display.flip()
        clock.tick(60)

        # Step the physics simulation
        world.Step(1.0/60, 6, 2)

    pygame.quit()

if __name__ == "__main__":
    main()
