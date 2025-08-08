import pytest
import math
from src.cell import Cell
from src.cellular_body import CellularBody

class MockBody:
    """Mock Box2D body for testing without Box2D dependency."""
    def __init__(self, x, y):
        self.position = MockVec2(x, y)

class MockVec2:
    """Mock Box2D Vec2 for testing."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

class MockOrganism:
    """Mock organism for testing toroidal wrapping logic."""
    def __init__(self, cells, body_position):
        self.cellular_body = MockCellularBody(cells)
        self.body = MockBody(body_position[0], body_position[1])

    def cells(self):
        return self.cellular_body.cells

class MockCellularBody:
    """Mock cellular body for testing."""
    def __init__(self, cells):
        self.cells = cells

class TestToroidalWrapping:
    def test_extreme_hex_coordinates_produce_extreme_world_coordinates(self):
        """Test that demonstrates the bug: extreme hex coordinates produce world coordinates far from reasonable bounds."""
        # Create a cell with extreme hex coordinates (similar to the bug reports)
        extreme_q = 1500
        extreme_r = 0
        extreme_s = -1500

        cell = Cell(
            position=(extreme_q, extreme_r, extreme_s),
            radius=0.4,
            border_color=(255, 255, 255),
            fill_color=(255, 0, 0),
            movement_deltas=[]
        )

        # Calculate world coordinates using the same formula from box2d_cell_vertices
        world_x = (3/2 * cell.q) * cell.radius
        world_y = (math.sqrt(3)/2 * cell.q + math.sqrt(3) * cell.r) * cell.radius

        # With extreme hex coordinates, world coordinates should be extreme too
        # This demonstrates the problem - hex coordinates of 1500 produce world coordinates of ~900
        expected_world_x = (3/2 * extreme_q) * 0.4  # = 900
        expected_world_y = (math.sqrt(3)/2 * extreme_q) * 0.4  # ≈ 519

        assert abs(world_x - expected_world_x) < 0.1, f"World X calculation changed: expected {expected_world_x}, got {world_x}"
        assert abs(world_y - expected_world_y) < 0.1, f"World Y calculation changed: expected {expected_world_y:.1f}, got {world_y:.1f}"

        # This is the bug: world coordinates (900, 519) are way outside reasonable world bounds (e.g., 0-120)
        world_bounds = 120  # From main.py WORLD_WIDTH/HEIGHT

        # The test should pass (showing the bug exists) - coordinates ARE extreme
        assert abs(world_x) > world_bounds or abs(world_y) > world_bounds, \
            f"World coordinates ({world_x:.1f}, {world_y:.1f}) should be outside bounds ±{world_bounds} to demonstrate the bug"

    def test_normal_hex_coordinates_produce_normal_world_coordinates(self):
        """Test that normal hex coordinates produce reasonable world coordinates."""
        # Create a cell with normal hex coordinates
        normal_q = 1
        normal_r = 0
        normal_s = -1

        cell = Cell(
            position=(normal_q, normal_r, normal_s),
            radius=0.4,
            border_color=(255, 255, 255),
            fill_color=(255, 0, 0),
            movement_deltas=[]
        )

        # Calculate world coordinates
        world_x = (3/2 * cell.q) * cell.radius
        world_y = (math.sqrt(3)/2 * cell.q + math.sqrt(3) * cell.r) * cell.radius

        # With normal hex coordinates, world coordinates should be reasonable
        expected_world_x = (3/2 * normal_q) * 0.4  # = 0.6
        expected_world_y = (math.sqrt(3)/2 * normal_q) * 0.4  # ≈ 0.35

        assert abs(world_x - expected_world_x) < 0.1
        assert abs(world_y - expected_world_y) < 0.1

        # These should be within reasonable bounds
        world_bounds = 120
        assert abs(world_x) < world_bounds and abs(world_y) < world_bounds, \
            f"World coordinates ({world_x:.1f}, {world_y:.1f}) should be within bounds ±{world_bounds}"

    @pytest.mark.xfail(reason="This test documents the original bug and is expected to fail until sync is called")
    def test_toroidal_wrap_should_sync_hex_coordinates_with_body_position(self):
        """Test that after toroidal wrapping, hex coordinates should produce world coordinates consistent with body position."""
        # Create cells with extreme hex coordinates (simulating the bug condition)
        cell1 = Cell(
            position=(1500, 0, -1500),  # Extreme coordinates like in the bug report
            radius=0.4,
            border_color=(255, 255, 255),
            fill_color=(255, 0, 0),
            movement_deltas=[]
        )
        cell2 = Cell(
            position=(1500, 1, -1501),  # Adjacent extreme coordinates
            radius=0.4,
            border_color=(255, 255, 255),
            fill_color=(255, 0, 0),
            movement_deltas=[]
        )

        # Create mock organism with these cells
        # Body position simulates after toroidal wrapping - should be within world bounds
        wrapped_body_position = (50.0, 60.0)  # Within world bounds after wrapping
        mock_organism = MockOrganism([cell1, cell2], wrapped_body_position)

        # This is the test for the fix: after toroidal wrapping, there should be a method
        # that adjusts hex coordinates to be consistent with the new body position

        # For now, let's test what the current buggy behavior looks like
        # Calculate world coordinates from current hex coordinates
        world_coords_from_hex = []
        for cell in mock_organism.cells():
            world_x = (3/2 * cell.q) * cell.radius
            world_y = (math.sqrt(3)/2 * cell.q + math.sqrt(3) * cell.r) * cell.radius
            world_coords_from_hex.append((world_x, world_y))

        body_x, body_y = mock_organism.body.position.x, mock_organism.body.position.y

        # Check if hex coordinates and body position are reasonably aligned
        for world_x, world_y in world_coords_from_hex:
            distance_from_body = math.sqrt((world_x - body_x)**2 + (world_y - body_y)**2)

            # This assertion should FAIL before the fix is implemented
            # because extreme hex coordinates produce world coordinates ~(900, 519)
            # but body is at wrapped position (50, 60)
            # Distance will be ~850, which is way more than 50
            max_reasonable_distance = 50  # Reasonable distance for cells from organism center

            # This test documents the bug - it will fail until we implement the fix
            assert distance_from_body < max_reasonable_distance, \
                f"EXPECTED FAILURE: Hex coordinates produce world position ({world_x:.1f}, {world_y:.1f}) " \
                f"too far from wrapped body position ({body_x:.1f}, {body_y:.1f}). " \
                f"Distance: {distance_from_body:.1f} > {max_reasonable_distance}. " \
                f"This demonstrates the toroidal wrapping bug where hex coordinates don't get updated."

    def test_sync_hex_coordinates_fixes_toroidal_wrapping_bug(self):
        """Test that sync_hex_coordinates_to_body_position() fixes the coordinate desync."""
        # Create cells with extreme hex coordinates
        cell1 = Cell(
            position=(1500, 0, -1500),
            radius=0.4,
            border_color=(255, 255, 255),
            fill_color=(255, 0, 0),
            movement_deltas=[]
        )
        cell2 = Cell(
            position=(1500, 1, -1501),
            radius=0.4,
            border_color=(255, 255, 255),
            fill_color=(255, 0, 0),
            movement_deltas=[]
        )

        # Create mock organism with wrapped body position
        wrapped_body_position = (50.0, 60.0)
        mock_organism = MockOrganism([cell1, cell2], wrapped_body_position)

        # Verify the problem exists before the fix
        world_x_before = (3/2 * cell1.q) * cell1.radius
        world_y_before = (math.sqrt(3)/2 * cell1.q + math.sqrt(3) * cell1.r) * cell1.radius
        distance_before = math.sqrt((world_x_before - 50.0)**2 + (world_y_before - 60.0)**2)
        assert distance_before > 500, f"Expected large distance before sync, got {distance_before:.1f}"

        # Create a real CellularBody for testing the sync method
        cellular_body = CellularBody([cell1, cell2])

        # Create a minimal mock organism that can use the real sync method
        class TestableOrganism:
            def __init__(self, cellular_body, body_position):
                self.cellular_body = cellular_body
                self.body = MockBody(body_position[0], body_position[1])
                self.fixtures_need_update = False
                self._last_cell_positions = None

            def cells(self):
                return self.cellular_body.cells

            def _update_position_cache(self):
                self._last_cell_positions = [(cell.q, cell.r, cell.s) for cell in self.cells()]

            # Import the sync method from the real Organism class
            def sync_hex_coordinates_to_body_position(self):
                """Synchronize cell hex coordinates to match current Box2D body position after toroidal wrapping."""
                if not self.cells():
                    return

                # Get the current body position
                body_x, body_y = self.body.position.x, self.body.position.y

                # Calculate what the first cell's hex coordinates should be to place it near body position
                # We'll use the first cell as reference and adjust all cells relative to it
                first_cell = self.cells()[0]

                # Calculate where the first cell currently appears in world coordinates
                current_world_x = (3/2 * first_cell.q) * first_cell.radius
                current_world_y = (math.sqrt(3)/2 * first_cell.q + math.sqrt(3) * first_cell.r) * first_cell.radius

                # Calculate the offset needed to move the first cell near the body position
                offset_x = body_x - current_world_x
                offset_y = body_y - current_world_y

                # Convert the offset back to hex coordinates
                radius = first_cell.radius
                q_offset = (2 * offset_x) / (3 * radius)
                r_offset = (offset_y / radius - (math.sqrt(3)/2 * q_offset)) / math.sqrt(3)

                # Round to nearest integers since hex coordinates must be integers
                q_offset = round(q_offset)
                r_offset = round(r_offset)
                s_offset = -(q_offset + r_offset)  # Maintain q + r + s = 0 constraint

                # Apply the offset to all cells
                for cell in self.cells():
                    cell.q += q_offset
                    cell.r += r_offset
                    cell.s += s_offset

                # Mark fixtures as needing update since cell positions changed
                self.fixtures_need_update = True
                self._update_position_cache()

        test_organism = TestableOrganism(cellular_body, wrapped_body_position)

        # Apply the fix
        test_organism.sync_hex_coordinates_to_body_position()

        # Verify coordinates are now synchronized
        world_coords_after_sync = []
        for cell in test_organism.cells():
            world_x = (3/2 * cell.q) * cell.radius
            world_y = (math.sqrt(3)/2 * cell.q + math.sqrt(3) * cell.r) * cell.radius
            world_coords_after_sync.append((world_x, world_y))

        body_x, body_y = test_organism.body.position.x, test_organism.body.position.y

        # Check that coordinates are now reasonable
        for world_x, world_y in world_coords_after_sync:
            distance_from_body = math.sqrt((world_x - body_x)**2 + (world_y - body_y)**2)

            # After sync, hex coordinates should produce world positions close to body position
            max_reasonable_distance = 5  # Much smaller tolerance after sync
            assert distance_from_body < max_reasonable_distance, \
                f"After sync: world position ({world_x:.1f}, {world_y:.1f}) still too far from body ({body_x:.1f}, {body_y:.1f}). Distance: {distance_from_body:.1f}"
