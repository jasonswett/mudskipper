import Box2D
import random

class ReflectionParticle:
    def __init__(self, world, position, radius=0.15):
        self.world = world
        self.position = position
        self.radius = radius

        # Create dynamic Box2D body
        body_def = Box2D.b2BodyDef()
        body_def.type = Box2D.b2_dynamicBody
        body_def.position = position
        self.body = world.CreateBody(body_def)

        # Create fixture with photon-like properties
        circle = Box2D.b2CircleShape(radius=radius)
        fixture_def = Box2D.b2FixtureDef()
        fixture_def.shape = circle
        fixture_def.density = 0.001  # Very low mass like a photon
        fixture_def.restitution = 1.0  # Perfect bouncing (elastic collision)
        fixture_def.friction = 0.0  # No friction for smooth bouncing

        self.body.CreateFixture(fixture_def)

        # Set initial random velocity
        initial_speed = 5.0  # Moderate speed
        angle = random.uniform(0, 2 * 3.14159)  # Random direction
        velocity_x = initial_speed * (angle ** 0.5)  # Using angle as pseudo-random
        velocity_y = initial_speed * ((angle + 1) ** 0.5)

        # Normalize to get proper random direction
        import math
        velocity_x = initial_speed * math.cos(angle)
        velocity_y = initial_speed * math.sin(angle)

        self.body.linearVelocity = (velocity_x, velocity_y)
