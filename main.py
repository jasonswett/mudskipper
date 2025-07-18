import pygame
import Box2D
import math
from cell_hexagon import CellHexagon

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PPM = 20.0  # Pixels per meter for Box2D conversion

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Mudskipper - Hexagon")
    clock = pygame.time.Clock()
    
    # Create Box2D world
    world = Box2D.b2World(gravity=(0, 0))
    
    # Create hexagon body
    body_def = Box2D.b2BodyDef()
    body_def.type = Box2D.b2_staticBody
    body_def.position = (SCREEN_WIDTH / 2 / PPM, SCREEN_HEIGHT / 2 / PPM)
    
    hexagon_body = world.CreateBody(body_def)

    # Create hexagon for Box2D (in meters, centered at origin)
    box2d_hexagon = CellHexagon(0, 0, 3)  # 3 meters radius
    
    hexagon_shape = Box2D.b2PolygonShape(vertices=box2d_hexagon.vertices())
    hexagon_body.CreateFixture(shape=hexagon_shape, density=1.0)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Clear screen
        screen.fill(BLACK)
        
        # Draw the Box2D hexagon
        for fixture in hexagon_body.fixtures:
            shape = fixture.shape
            vertices = []
            for vertex in shape.vertices:
                # Convert Box2D coordinates to screen coordinates
                x = hexagon_body.position.x * PPM + vertex[0] * PPM
                y = SCREEN_HEIGHT - (hexagon_body.position.y * PPM + vertex[1] * PPM)
                vertices.append((x, y))
            
            # Draw green outline
            pygame.draw.polygon(screen, GREEN, vertices, width=2)
        
        pygame.display.flip()
        clock.tick(60)
        
        # Step the physics simulation
        world.Step(1.0/60, 6, 2)
    
    pygame.quit()

if __name__ == "__main__":
    main()
