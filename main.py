import pygame
import Box2D
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PPM = 20.0  # Pixels per meter for Box2D conversion

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

def create_hexagon_vertices(center_x, center_y, radius):
    vertices = []
    for i in range(6):
        angle = (math.pi / 3) * i
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        vertices.append((x, y))
    return vertices

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
    
    # Create hexagon shape
    hexagon_vertices = create_hexagon_vertices(0, 0, 3)  # 3 meters radius in Box2D units
    hexagon_shape = Box2D.b2PolygonShape(vertices=hexagon_vertices)
    hexagon_body.CreateFixture(shape=hexagon_shape, density=1.0)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Clear screen
        screen.fill(BLACK)
        
        # Draw hexagon
        for fixture in hexagon_body.fixtures:
            shape = fixture.shape
            vertices = []
            for vertex in shape.vertices:
                x = hexagon_body.position.x * PPM + vertex[0] * PPM
                y = SCREEN_HEIGHT - (hexagon_body.position.y * PPM + vertex[1] * PPM)
                vertices.append((x, y))
            
            # Draw filled black hexagon
            pygame.draw.polygon(screen, BLACK, vertices)
            # Draw green outline
            pygame.draw.polygon(screen, GREEN, vertices, width=2)
        
        pygame.display.flip()
        clock.tick(60)
        
        # Step the physics simulation
        world.Step(1.0/60, 6, 2)
    
    pygame.quit()

if __name__ == "__main__":
    main()
