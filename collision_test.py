import pygame
import Box2D
import math

from src.cell import Cell
from src.cellular_body import CellularBody
from src.organism import Organism
from src.organism_rendering import OrganismRendering
from src.screen import Screen

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

def create_ball(world, position, velocity):
    """Create a bouncing ball in the Box2D world."""
    body_def = Box2D.b2BodyDef()
    body_def.type = Box2D.b2_dynamicBody
    body_def.position = position
    body = world.CreateBody(body_def)
    
    # Create circular fixture
    circle = Box2D.b2CircleShape(radius=0.5)
    fixture_def = Box2D.b2FixtureDef(
        shape=circle,
        density=1.0,
        restitution=0.9,  # Very bouncy
        friction=0.1
    )
    body.CreateFixture(fixture_def)
    body.linearVelocity = velocity
    
    return body

def create_walls(world, screen_width, screen_height):
    """Create walls around the screen edges."""
    thickness = 0.5
    
    # Bottom wall
    bottom_body = world.CreateStaticBody(
        position=(screen_width/2, thickness/2),
        shapes=Box2D.b2PolygonShape(box=(screen_width/2, thickness/2))
    )
    
    # Top wall  
    top_body = world.CreateStaticBody(
        position=(screen_width/2, screen_height - thickness/2),
        shapes=Box2D.b2PolygonShape(box=(screen_width/2, thickness/2))
    )
    
    # Left wall
    left_body = world.CreateStaticBody(
        position=(thickness/2, screen_height/2),
        shapes=Box2D.b2PolygonShape(box=(thickness/2, screen_height/2))
    )
    
    # Right wall
    right_body = world.CreateStaticBody(
        position=(screen_width - thickness/2, screen_height/2),
        shapes=Box2D.b2PolygonShape(box=(thickness/2, screen_height/2))
    )

def main():
    pygame.init()
    screen = Screen(40, 30)  # 40x30 meters
    display = pygame.display.set_mode(screen.size_in_pixels())
    pygame.display.set_caption("Collision Test")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)
    
    # Create Box2D world
    world = Box2D.b2World(gravity=(0, 0))
    
    # Create walls
    create_walls(world, screen.width, screen.height)
    
    # Create a two-celled organism in the center
    cell1 = Cell((0, 0, 0), 2, GREEN, (0, 100, 0), [(0, 0, 0), (0, 0, 0)])
    cell2 = Cell((1, 0, -1), 2, GREEN, (0, 100, 0), [(0, 0, 0), (0, 0, 0)])
    cellular_body = CellularBody([cell1, cell2])
    organism = Organism(world, cellular_body, (screen.width/2, screen.height/2))
    
    # Create multiple bouncing balls
    balls = []
    for i in range(10):
        x = 5 + i * 3
        y = 5 + (i % 3) * 5
        vx = (i + 1) * 3
        vy = (10 - i) * 2
        ball = create_ball(world, (x, y), (vx, vy))
        balls.append(ball)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        display.fill(BLACK)
        
        # Draw organism
        organism_rendering = OrganismRendering(organism, screen)
        for cell_rendering in organism_rendering.cell_renderings():
            pygame.draw.polygon(display, cell_rendering['fill_color'], cell_rendering['vertices'])
            pygame.draw.polygon(display, cell_rendering['border_color'], cell_rendering['vertices'], width=2)
        
        # Draw balls
        for ball in balls:
            ball_pos = ball.position
            ball_pixel_x = Screen.to_pixels(ball_pos.x)
            ball_pixel_y = Screen.to_pixels(ball_pos.y)
            pygame.draw.circle(display, RED, (int(ball_pixel_x), int(ball_pixel_y)), int(Screen.to_pixels(0.5)))
        
        # Display positions
        org_text = f"Organism: ({organism.body.position.x:.2f}, {organism.body.position.y:.2f})"
        org_surface = font.render(org_text, True, WHITE)
        display.blit(org_surface, (10, 10))
        
        # Display cell positions
        y_offset = 35
        for i, cell in enumerate(organism.cells()):
            # Calculate cell center position
            cell_center_x = (3/2 * cell.q) * cell.radius
            cell_center_y = (math.sqrt(3)/2 * cell.q + math.sqrt(3) * cell.r) * cell.radius
            cell_world_x = organism.body.position.x + cell_center_x
            cell_world_y = organism.body.position.y + cell_center_y
            cell_text = f"Cell {i}: ({cell_world_x:.2f}, {cell_world_y:.2f})"
            cell_surface = font.render(cell_text, True, WHITE)
            display.blit(cell_surface, (10, y_offset))
            y_offset += 25
        
        pygame.display.flip()
        clock.tick(60)
        
        # Step physics
        world.Step(1.0/60, 6, 2)
    
    pygame.quit()

if __name__ == "__main__":
    main()