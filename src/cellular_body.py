import copy

class CellularBody:
    def __init__(self, cells):
        self.cells = cells
        for cell in self.cells:
            cell.cellular_body = self

    def respond_to_cell_stimulation(self, cell):
        if not(cell in self.cells):
            return

        i = self.cells.index(cell)

        # Round-robin through movement deltas, starting from current movement_index
        attempts = 0
        num_movements = len(cell.movement_deltas)

        while attempts < num_movements:
            delta = cell.movement_deltas[cell.movement_index]

            test_cells = copy.deepcopy(self.cells)
            test_cells[i].move(delta)
            test_body = CellularBody(test_cells)

            if test_body.is_legal():
                cell.move(delta)
                # Advance to next movement for next stimulation
                cell.movement_index = (cell.movement_index + 1) % num_movements
                return

            # Try next movement delta
            cell.movement_index = (cell.movement_index + 1) % num_movements
            attempts += 1

    def update_clock(self):
        for cell in self.cells:
            cell.update_clock()

    def is_legal(self):
        return not self.contains_overlaps() and self.is_contiguous() and self.has_valid_coordinates()

    def has_valid_coordinates(self):
        for cell in self.cells:
            if cell.q + cell.r + cell.s != 0:
                return False
        return True

    def is_contiguous(self):
        if len(self.cells) == 0:
            return True
        if len(self.cells) == 1:
            return True

        # Use BFS to check if all cells are connected
        visited = set()
        queue = [self.cells[0]]
        visited.add(self.cells[0])

        while queue:
            current = queue.pop(0)
            for neighbor in self.neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        # If all cells were visited, the body is contiguous
        return len(visited) == len(self.cells)

    def contains_overlaps(self):
        for i in range(len(self.cells)):
            for j in range(i + 1, len(self.cells)):
                if (self.cells[i].q == self.cells[j].q and
                    self.cells[i].r == self.cells[j].r and
                    self.cells[i].s == self.cells[j].s):
                    return True
        return False

    def neighbors(self, cell):
        neighbors = []

        neighbor_offsets = [
            (1, 0, -1),
            (1, -1, 0),
            (0, -1, 1),
            (-1, 0, 1),
            (-1, 1, 0),
            (0, 1, -1)
        ]

        for other_cell in self.cells:
            if other_cell != cell:
                q_diff = other_cell.q - cell.q
                r_diff = other_cell.r - cell.r
                s_diff = other_cell.s - cell.s
                if (q_diff, r_diff, s_diff) in neighbor_offsets:
                    neighbors.append(other_cell)
        return neighbors
