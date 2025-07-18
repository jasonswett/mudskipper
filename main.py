import pygame
import Box2D
import math
from cell_hexagon import CellHexagon

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ORGANISM_CELL_RADIUS = 3
PPM = 20.0 # Pixels per meter for Box2D conversion

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Mudskipper - Hexagon")
    clock = pygame.time.Clock()

    world = Box2D.b2World(gravity=(0, 0))

    body_def = Box2D.b2BodyDef()
    body_def.type = Box2D.b2_staticBody
    body_def.position = (SCREEN_WIDTH / 2 / PPM, SCREEN_HEIGHT / 2 / PPM)

    body = world.CreateBody(body_def)

    box2d_hexagon = CellHexagon(0, 0, ORGANISM_CELL_RADIUS)
    
    hexagon_shape = Box2D.b2PolygonShape(vertices=box2d_hexagon.vertices())
    body.CreateFixture(shape=hexagon_shape, density=1.0)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(BLACK)
        
        for fixture in body.fixtures:
            shape = fixture.shape
            vertices = []
            for vertex in shape.vertices:
                # Convert Box2D coordinates to screen coordinates
                x = body.position.x * PPM + vertex[0] * PPM
                y = SCREEN_HEIGHT - (body.position.y * PPM + vertex[1] * PPM)
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
