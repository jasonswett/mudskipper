import Box2D

class FoodMorsel:
    def __init__(self, world, position, radius=0.2):
        self.world = world
        self.position = position
        self.radius = radius
        self.eaten = False

        # Create dynamic Box2D body
        body_def = Box2D.b2BodyDef()
        body_def.type = Box2D.b2_dynamicBody
        body_def.position = position
        self.body = world.CreateBody(body_def)

        # Create fixture
        circle = Box2D.b2CircleShape(radius=radius)
        self.body.CreateFixture(shape=circle, density=1.0)
