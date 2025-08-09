from src.gene import Gene
import random

class CellGene(Gene):
    GENE_SECTION_LENGTHS = {
        'placement_delta': 3,
        'movement_delta_1': 3,
        'movement_delta_2': 3,
        'movement_delta_3': 3,
        'cell_type': 2,
        'pulse_interval': 7,
        'stimulation_propagation_delay': 3,
    }

    LEGAL_DELTAS = [
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
        total_cell_gene_length = sum(CellGene.GENE_SECTION_LENGTHS.values())
        return CellGene(CellGene.random_binary_number(total_cell_gene_length))

    @staticmethod
    def random_binary_number(bit_count):
        return "".join([str(random.randint(0, 1)) for i in range(bit_count)])

    def section(self, section_name):
        start = 0
        for name in self.GENE_SECTION_LENGTHS:
            if name == section_name:
                end = start + self.GENE_SECTION_LENGTHS[name]
                return self.value[start:end]
            start += self.GENE_SECTION_LENGTHS[name]

    def placement_delta(self):
        return self.LEGAL_DELTAS[self.int_value('placement_delta')]

    def movement_deltas(self):
        return [
            self.LEGAL_DELTAS[self.int_value('movement_delta_1')],
            self.LEGAL_DELTAS[self.int_value('movement_delta_2')],
            self.LEGAL_DELTAS[self.int_value('movement_delta_3')]
        ]

    def int_value(self, section_name):
        return int(self.section(section_name), 2)

    def fill_color(self):
        return self.FILL_COLORS_BY_CELL_TYPE[self.cell_type()]

    def border_color(self):
        return self.BORDER_COLORS_BY_CELL_TYPE[self.cell_type()]

    def cell_type(self):
        if self.section('cell_type') == "11":
            return "pulser"
        else:
            return "default"

    def pulse_interval(self):
        # Get 7-bit value (0-127) and add 1 for range 1-128
        return self.int_value('pulse_interval') + 1

    def stimulation_propagation_delay(self):
        # Get 3-bit value (0-7) and add 1 for range 1-8
        return self.int_value('stimulation_propagation_delay') + 1
