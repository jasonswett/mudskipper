class Camera:
    def __init__(self, world_width, world_height, viewport_width, viewport_height):
        self.x = 0
        self.y = 0
        self.world_width = world_width
        self.world_height = world_height
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height

    def move(self, dx, dy):
        # Keep camera within world bounds
        self.x = max(0, min(self.world_width - self.viewport_width, self.x + dx))
        self.y = max(0, min(self.world_height - self.viewport_height, self.y + dy))

    def world_to_screen(self, world_x, world_y):
        """Convert world coordinates to screen coordinates."""
        screen_x = world_x - self.x
        screen_y = world_y - self.y
        return screen_x, screen_y

    def is_visible(self, world_x, world_y, margin=2):
        """Check if a world position is visible in the viewport."""
        return (self.x - margin <= world_x <= self.x + self.viewport_width + margin and
                self.y - margin <= world_y <= self.y + self.viewport_height + margin)
