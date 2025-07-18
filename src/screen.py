class Screen:
    PIXELS_PER_METER = 20.0

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def size_in_pixels(self):
        return (self.width * self.PIXELS_PER_METER, self.height * self.PIXELS_PER_METER)

    def center(self):
        return (self.width / 2, self.height / 2)
