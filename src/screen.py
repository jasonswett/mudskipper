class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def size(self):
        return (self.width, self.height)

    def center(self):
        return (self.width / 2, self.height / 2)
