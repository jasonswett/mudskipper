from src.gene import Gene

class CellGene(Gene):
    LEGAL_DELTAS = [
        (0, 0, 0),
        (0, -1, 1),
        (1, -1, 0),
        (1, 0, -1),
        (0, 1, -1),
        (-1, 1, 0),
        (-1, 0, 1),
    ]

    def __init__(self, value_or_length):
        super().__init__(value_or_length)

    def delta(self):
        delta_index = int(self.value, 2)
        return self.LEGAL_DELTAS[delta_index]
