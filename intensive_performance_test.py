#!/usr/bin/env python3
"""
Intensive Performance Test Suite for Mudskipper
Tests 10 optimizations without FPS limits to measure true performance impact.
"""

import pygame
import Box2D
import time
import random

from src.genome import Genome
from src.cellular_body_builder import CellularBodyBuilder
from src.organism import Organism
from src.food_morsel import FoodMorsel
from src.contact_listener import ContactListener

class IntensivePerformanceTest:
    def __init__(self):
        self.results = {}
        pygame.init()

    def create_test_world(self, organism_count=500):
        """Create a test world with specified number of organisms."""
        world = Box2D.b2World(gravity=(0, 0))

        # Create organisms
        organisms = []
        for _ in range(organism_count):
            while True:
                genome = Genome()
                cellular_body_builder = CellularBodyBuilder(genome.cell_genes())
                cellular_body = cellular_body_builder.cellular_body()

                if cellular_body.is_legal():
                    x = random.uniform(10, 110)
                    y = random.uniform(10, 110)
                    organism = Organism(world, cellular_body, (x, y), genome)
                    organisms.append(organism)
                    break

        # Create food
        food_morsels = []
        for _ in range(1000):
            x = random.uniform(0, 120)
            y = random.uniform(0, 120)
            food_morsel = FoodMorsel(world, (x, y))
            food_morsels.append(food_morsel)

        # Create contact listener
        contact_listener = ContactListener(organisms, food_morsels)
        world.contactListener = contact_listener

        return world, organisms, food_morsels, contact_listener

    def cleanup_world(self, world, organisms, food_morsels):
        """Clean up world resources."""
        for organism in organisms:
            if hasattr(organism, 'body') and organism.body:
                world.DestroyBody(organism.body)
        for food in food_morsels:
            if hasattr(food, 'body') and food.body:
                world.DestroyBody(food.body)

    def run_baseline_test(self, duration=5):
        """Run baseline performance test - no FPS limit."""
        print("Running baseline test...")

        world, organisms, food_morsels, contact_listener = self.create_test_world()

        frame_count = 0
        start_time = time.time()

        try:
            while time.time() - start_time < duration:
                # Update organisms
                for organism in organisms[:]:
                    organism.update_clock()
                    if not organism.is_alive():
                        organisms.remove(organism)
                        contact_listener.remove_organism(organism)
                        if organism.body:
                            world.DestroyBody(organism.body)

                # Physics step
                world.Step(1.0/60, 6, 2)

                frame_count += 1

        finally:
            self.cleanup_world(world, organisms, food_morsels)

        total_time = time.time() - start_time
        avg_fps = frame_count / total_time
        return avg_fps

    def test_reduced_physics_steps(self, duration=5):
        """Test with reduced physics simulation precision."""
        print("Testing: Reduced Physics Steps...")

        world, organisms, food_morsels, contact_listener = self.create_test_world()

        frame_count = 0
        start_time = time.time()

        try:
            while time.time() - start_time < duration:
                for organism in organisms[:]:
                    organism.update_clock()
                    if not organism.is_alive():
                        organisms.remove(organism)
                        contact_listener.remove_organism(organism)
                        if organism.body:
                            world.DestroyBody(organism.body)

                # Reduced precision: 3 velocity iterations, 1 position iteration
                world.Step(1.0/60, 3, 1)
                frame_count += 1

        finally:
            self.cleanup_world(world, organisms, food_morsels)

        total_time = time.time() - start_time
        return frame_count / total_time

    def test_skip_organism_updates(self, duration=5):
        """Test updating every other organism per frame."""
        print("Testing: Skip Organism Updates...")

        world, organisms, food_morsels, contact_listener = self.create_test_world()

        frame_count = 0
        start_time = time.time()

        try:
            while time.time() - start_time < duration:
                # Update only half the organisms each frame
                for i, organism in enumerate(organisms[:]):
                    if i % 2 == frame_count % 2:
                        organism.update_clock()
                        if not organism.is_alive():
                            organisms.remove(organism)
                            contact_listener.remove_organism(organism)
                            if organism.body:
                                world.DestroyBody(organism.body)

                world.Step(1.0/60, 6, 2)
                frame_count += 1

        finally:
            self.cleanup_world(world, organisms, food_morsels)

        total_time = time.time() - start_time
        return frame_count / total_time

    def test_30fps_physics(self, duration=5):
        """Test running physics at 30 FPS instead of 60."""
        print("Testing: 30 FPS Physics...")

        world, organisms, food_morsels, contact_listener = self.create_test_world()

        frame_count = 0
        start_time = time.time()

        try:
            while time.time() - start_time < duration:
                for organism in organisms[:]:
                    organism.update_clock()
                    if not organism.is_alive():
                        organisms.remove(organism)
                        contact_listener.remove_organism(organism)
                        if organism.body:
                            world.DestroyBody(organism.body)

                # Run physics every other frame (30Hz)
                if frame_count % 2 == 0:
                    world.Step(2.0/60, 6, 2)  # Double timestep

                frame_count += 1

        finally:
            self.cleanup_world(world, organisms, food_morsels)

        total_time = time.time() - start_time
        return frame_count / total_time

    def test_batch_death_processing(self, duration=5):
        """Test batching organism death processing."""
        print("Testing: Batch Death Processing...")

        world, organisms, food_morsels, contact_listener = self.create_test_world()

        frame_count = 0
        start_time = time.time()
        dead_organisms = []

        try:
            while time.time() - start_time < duration:
                # Update organisms and collect dead ones
                for organism in organisms:
                    organism.update_clock()
                    if not organism.is_alive():
                        dead_organisms.append(organism)

                # Process deaths in batches every 5 frames
                if frame_count % 5 == 0 and dead_organisms:
                    for dead_org in dead_organisms:
                        if dead_org in organisms:
                            organisms.remove(dead_org)
                            contact_listener.remove_organism(dead_org)
                            if dead_org.body:
                                world.DestroyBody(dead_org.body)
                    dead_organisms.clear()

                world.Step(1.0/60, 6, 2)
                frame_count += 1

        finally:
            self.cleanup_world(world, organisms, food_morsels)

        total_time = time.time() - start_time
        return frame_count / total_time

    def test_reduced_collision_frequency(self, duration=5):
        """Test processing collisions less frequently."""
        print("Testing: Reduced Collision Frequency...")

        world, organisms, food_morsels, contact_listener = self.create_test_world()

        frame_count = 0
        start_time = time.time()

        try:
            while time.time() - start_time < duration:
                for organism in organisms[:]:
                    organism.update_clock()
                    if not organism.is_alive():
                        organisms.remove(organism)
                        contact_listener.remove_organism(organism)
                        if organism.body:
                            world.DestroyBody(organism.body)

                # Only process collisions every 3rd frame
                if frame_count % 3 == 0:
                    world.Step(1.0/60, 6, 2)
                else:
                    world.Step(1.0/60, 0, 0)  # No collision resolution

                frame_count += 1

        finally:
            self.cleanup_world(world, organisms, food_morsels)

        total_time = time.time() - start_time
        return frame_count / total_time

    def test_larger_timesteps(self, duration=5):
        """Test using larger physics timesteps."""
        print("Testing: Larger Timesteps...")

        world, organisms, food_morsels, contact_listener = self.create_test_world()

        frame_count = 0
        start_time = time.time()

        try:
            while time.time() - start_time < duration:
                for organism in organisms[:]:
                    organism.update_clock()
                    if not organism.is_alive():
                        organisms.remove(organism)
                        contact_listener.remove_organism(organism)
                        if organism.body:
                            world.DestroyBody(organism.body)

                # Use larger timestep: 1/30 instead of 1/60
                world.Step(1.0/30, 6, 2)
                frame_count += 1

        finally:
            self.cleanup_world(world, organisms, food_morsels)

        total_time = time.time() - start_time
        return frame_count / total_time

    def test_simplified_organism_logic(self, duration=5):
        """Test with simplified organism update logic."""
        print("Testing: Simplified Organism Logic...")

        world, organisms, food_morsels, contact_listener = self.create_test_world()

        frame_count = 0
        start_time = time.time()

        try:
            while time.time() - start_time < duration:
                # Simplified update: only every 3rd frame
                if frame_count % 3 == 0:
                    for organism in organisms[:]:
                        organism.update_clock()
                        if not organism.is_alive():
                            organisms.remove(organism)
                            contact_listener.remove_organism(organism)
                            if organism.body:
                                world.DestroyBody(organism.body)

                world.Step(1.0/60, 6, 2)
                frame_count += 1

        finally:
            self.cleanup_world(world, organisms, food_morsels)

        total_time = time.time() - start_time
        return frame_count / total_time

    def test_contact_event_batching(self, duration=5):
        """Test batching contact event processing."""
        print("Testing: Contact Event Batching...")

        world, organisms, food_morsels, contact_listener = self.create_test_world()

        frame_count = 0
        start_time = time.time()

        try:
            while time.time() - start_time < duration:
                for organism in organisms[:]:
                    organism.update_clock()
                    if not organism.is_alive():
                        organisms.remove(organism)
                        contact_listener.remove_organism(organism)
                        if organism.body:
                            world.DestroyBody(organism.body)

                # Only get contact events every 5th frame
                if frame_count % 5 == 0:
                    contact_events = contact_listener.get_contact_events()
                    # Process events (reproduction logic would go here)

                world.Step(1.0/60, 6, 2)
                frame_count += 1

        finally:
            self.cleanup_world(world, organisms, food_morsels)

        total_time = time.time() - start_time
        return frame_count / total_time

    def test_reduced_organism_count(self, duration=5):
        """Test with fewer active organisms (400 instead of 500)."""
        print("Testing: Reduced Organism Count...")

        world, organisms, food_morsels, contact_listener = self.create_test_world(400)

        frame_count = 0
        start_time = time.time()

        try:
            while time.time() - start_time < duration:
                for organism in organisms[:]:
                    organism.update_clock()
                    if not organism.is_alive():
                        organisms.remove(organism)
                        contact_listener.remove_organism(organism)
                        if organism.body:
                            world.DestroyBody(organism.body)

                world.Step(1.0/60, 6, 2)
                frame_count += 1

        finally:
            self.cleanup_world(world, organisms, food_morsels)

        total_time = time.time() - start_time
        return frame_count / total_time

    def run_all_tests(self):
        """Run complete performance test suite."""
        print("🚀 INTENSIVE MUDSKIPPER PERFORMANCE TEST")
        print("=" * 60)
        print("Testing with 500 organisms (no FPS limit)")
        print("Each test runs for 5 seconds to measure max throughput")
        print("=" * 60)

        # Test definitions
        tests = [
            ("Baseline", self.run_baseline_test),
            ("Reduced Physics Steps", self.test_reduced_physics_steps),
            ("Skip Organism Updates", self.test_skip_organism_updates),
            ("30 FPS Physics", self.test_30fps_physics),
            ("Batch Death Processing", self.test_batch_death_processing),
            ("Reduced Collision Frequency", self.test_reduced_collision_frequency),
            ("Larger Timesteps", self.test_larger_timesteps),
            ("Simplified Organism Logic", self.test_simplified_organism_logic),
            ("Contact Event Batching", self.test_contact_event_batching),
            ("Reduced Organism Count", self.test_reduced_organism_count),
        ]

        # Run tests
        for i, (name, test_func) in enumerate(tests):
            print(f"\n[{i+1}/{len(tests)}] {name}")
            try:
                fps = test_func()
                self.results[name] = fps
                print(f"    Result: {fps:.1f} FPS")
            except Exception as e:
                print(f"    Error: {e}")
                self.results[name] = 0.0

        # Print results table
        self.print_results_table()

    def print_results_table(self):
        """Print comprehensive results table."""
        print("\n" + "=" * 85)
        print("📊 INTENSIVE PERFORMANCE TEST RESULTS")
        print("=" * 85)

        baseline_fps = self.results.get("Baseline", 0)

        print(f"{'Test':<35} {'FPS':<10} {'Change':<10} {'% Improvement':<15} {'Rating'}")
        print("-" * 85)

        # Sort by FPS (highest first)
        sorted_results = sorted(self.results.items(), key=lambda x: x[1], reverse=True)

        for name, fps in sorted_results:
            if name == "Baseline":
                rating = "📊 Baseline"
                change_str = "N/A"
                percent_str = "N/A"
            else:
                change = fps - baseline_fps
                percent = (change / baseline_fps * 100) if baseline_fps > 0 else 0
                change_str = f"{change:+.1f}"
                percent_str = f"{percent:+.1f}%"

                # Rating based on improvement
                if percent > 50:
                    rating = "🚀 Excellent"
                elif percent > 25:
                    rating = "✅ Very Good"
                elif percent > 15:
                    rating = "🔧 Good"
                elif percent > 10:
                    rating = "📈 Decent"
                elif percent > 5:
                    rating = "➕ Minor"
                elif percent > 0:
                    rating = "🔍 Slight"
                else:
                    rating = "❌ Negative"

            print(f"{name:<35} {fps:<10.1f} {change_str:<10} {percent_str:<15} {rating}")

        print("-" * 85)

        # Find best optimization
        if len(sorted_results) > 1:
            best_name, best_fps = sorted_results[0] if sorted_results[0][0] != "Baseline" else sorted_results[1]
            improvement = ((best_fps - baseline_fps) / baseline_fps * 100) if baseline_fps > 0 else 0
            print(f"💡 Best optimization: {best_name}")
            print(f"📈 Max improvement: {improvement:+.1f}% FPS")
        else:
            print("💡 No significant improvements found")

        print("🔬 Test conditions: 5 second runs, no FPS limit, pure simulation speed")

def main():
    test = IntensivePerformanceTest()
    try:
        test.run_all_tests()
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
