class Gene:
    def __init__(self, value_or_length):
        if isinstance(value_or_length, int):
            self.value = [0] * value_or_length
        else:
            self.value = value_or_length