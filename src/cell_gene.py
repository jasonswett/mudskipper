from src.gene import Gene
import random

class CellGene(Gene):
    LEGAL_placement_deltaS = [
        (0, 0, 0),  # 000, no difference
        (0, -1, 1), # 001, straight up
        (1, -1, 0), # 010, up-right
        (1, 0, -1), # 011, down-right
        (0, 1, -1), # 100, straight down
        (-1, 1, 0), # 101, down-left
        (-1, 0, 1), # 110, up-left
        (0, 0, 0),  # 111, needed for completeness
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

    @staticmethod
    def random():
        placement_delta = CellGene.random_binary_number(3)
        cell_type = CellGene.random_binary_number(2)
        return CellGene(placement_delta + cell_type)

    @staticmethod
    def random_binary_number(bit_count):
        return "".join([str(random.randint(0, 1)) for i in range(bit_count)])

    def placement_delta_section(self):
        return self.value[:3]

    def cell_type_section(self):
        return self.value[3:5]

    def placement_delta(self):
        placement_delta_index = int(self.placement_delta_section(), 2)
        return self.LEGAL_placement_deltaS[placement_delta_index]

    def fill_color(self):
        return self.FILL_COLORS_BY_CELL_TYPE[self.cell_type()]

    def border_color(self):
        return self.BORDER_COLORS_BY_CELL_TYPE[self.cell_type()]

    def cell_type(self):
        if self.cell_type_section() == "11":
            return "pulser"
        else:
            return "default"
