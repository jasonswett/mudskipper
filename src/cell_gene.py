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

    FILL_COLORS_BY_CELL_TYPE = {
        "pulser": (0, 0, 255),
        "default": (0, 0, 0),
    }

    BORDER_COLORS_BY_CELL_TYPE = {
        "pulser": (0, 0, 255),
        "default": (0, 255, 0),
    }

    def __init__(self, value_or_length):
        super().__init__(value_or_length)

    def delta_section(self):
        return self.value[:3]

    def cell_type_section(self):
        return self.value[3:5]

    def delta(self):
        delta_index = int(self.delta_section(), 2)
        return self.LEGAL_DELTAS[delta_index]

    def fill_color(self):
        return self.FILL_COLORS_BY_CELL_TYPE[self.cell_type()]

    def border_color(self):
        return self.BORDER_COLORS_BY_CELL_TYPE[self.cell_type()]

    def cell_type(self):
        if self.cell_type_section() == "11":
            return "pulser"
        else:
            return "default"
