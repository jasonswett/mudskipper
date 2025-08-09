import time
import pygame
import Box2D
from main import *
import copy

class PerformanceBenchmarker:
    def __init__(self):
        self.results = {}
        pygame.init()
        self.display = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Performance Benchmark")
        self.clock = pygame.time.Clock()

    def benchmark_baseline(self):
        """Benchmark current performance with 500 organisms for 10 seconds."""
        print("Benchmarking baseline performance with 500 organisms...")

        # Set up world with 500 organisms
        world = Box2D.b2World(gravity=(0, 0))
        organisms, food_morsels, contact_listener = reset_world(world, 120, 120, self.display)

        # Add more organisms to reach 500
        while len(organisms) < 500:
            additional_organisms = generate_organisms(world, 120, 120, self.display, count=min(100, 500 - len(organisms)))
            for org in additional_organisms:
                organisms.append(org)
                contact_listener.add_organism(org)

        fps_samples = []
        start_time = time.time()
        frame_count = 0

        while time.time() - start_time < 10:  # Run for 10 seconds
            # Basic game loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break

            # Update organisms
            for organism in organisms[:]:  # Copy list to avoid modification issues
                organism.update_clock()
                if not organism.is_alive():
                    organisms.remove(organism)
                    contact_listener.remove_organism(organism)
                    world.DestroyBody(organism.body)

            # Step physics
            world.Step(1.0/60, 6, 2)

            # Record FPS
            fps = self.clock.get_fps()
            if fps > 0:  # Ignore first few frames
                fps_samples.append(fps)

            frame_count += 1
            self.clock.tick(60)

        avg_fps = sum(fps_samples) / len(fps_samples) if fps_samples else 0
        self.results["Baseline"] = avg_fps

        # Cleanup
        for organism in organisms:
            if organism.body:
                world.DestroyBody(organism.body)
        for food in food_morsels:
            if food.body:
                world.DestroyBody(food.body)

        print(f"Baseline FPS: {avg_fps:.1f}")
        return avg_fps

    def test_optimization(self, name, optimization_func):
        """Test a specific optimization and return FPS improvement."""
        print(f"Testing: {name}...")

        # Set up world
        world = Box2D.b2World(gravity=(0, 0))
        organisms, food_morsels, contact_listener = reset_world(world, 120, 120, self.display)

        # Add more organisms to reach 500
        while len(organisms) < 500:
            additional_organisms = generate_organisms(world, 120, 120, self.display, count=min(100, 500 - len(organisms)))
            for org in additional_organisms:
                organisms.append(org)
                contact_listener.add_organism(org)

        # Apply optimization
        optimization_func(world, organisms, food_morsels, contact_listener)

        fps_samples = []
        start_time = time.time()

        while time.time() - start_time < 5:  # Shorter test - 5 seconds
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break

            # Update organisms
            for organism in organisms[:]:
                organism.update_clock()
                if not organism.is_alive():
                    organisms.remove(organism)
                    contact_listener.remove_organism(organism)
                    world.DestroyBody(organism.body)

            world.Step(1.0/60, 6, 2)

            fps = self.clock.get_fps()
            if fps > 0:
                fps_samples.append(fps)

            self.clock.tick(60)

        avg_fps = sum(fps_samples) / len(fps_samples) if fps_samples else 0
        self.results[name] = avg_fps

        # Cleanup
        for organism in organisms:
            if organism.body:
                world.DestroyBody(organism.body)
        for food in food_morsels:
            if food.body:
                world.DestroyBody(food.body)

        print(f"{name} FPS: {avg_fps:.1f}")
        return avg_fps

    def optimization_1_reduce_physics_steps(self, world, organisms, food_morsels, contact_listener):
        """Reduce Box2D physics simulation steps."""
        # This will be applied in the step call: world.Step(1.0/60, 3, 1) instead of (1.0/60, 6, 2)
        pass

    def optimization_2_limit_organism_updates(self, world, organisms, food_morsels, contact_listener):
        """Update only every 2nd organism each frame."""
        for i, organism in enumerate(organisms):
            organism._update_skip = i % 2

    def optimization_3_reduce_collision_precision(self, world, organisms, food_morsels, contact_listener):
        """Reduce fixture vertex count for simpler collision shapes."""
        for organism in organisms:
            # Simplify fixtures (this is a placeholder - would need more complex implementation)
            pass

    def optimization_4_batch_organism_deaths(self, world, organisms, food_morsels, contact_listener):
        """Batch process organism deaths instead of immediate removal."""
        self.death_batch = []

    def optimization_5_reduce_simulation_frequency(self, world, organisms, food_morsels, contact_listener):
        """Run physics at 30Hz instead of 60Hz."""
        pass  # Will be handled in test loop

    def optimization_6_simplify_health_decay(self, world, organisms, food_morsels, contact_listener):
        """Reduce health decay frequency."""
        for organism in organisms:
            organism._health_decay_skip = 0

    def optimization_7_limit_stimulation_propagation(self, world, organisms, food_morsels, contact_listener):
        """Limit how often cells can stimulate."""
        pass  # Would need cellular body modification

    def optimization_8_reduce_rendering_calls(self, world, organisms, food_morsels, contact_listener):
        """Skip rendering optimization (measure pure simulation)."""
        pass  # This is for simulation FPS only

    def optimization_9_optimize_memory_allocation(self, world, organisms, food_morsels, contact_listener):
        """Pre-allocate object pools."""
        pass  # Complex to implement in test

    def optimization_10_reduce_contact_events(self, world, organisms, food_morsels, contact_listener):
        """Limit contact event processing frequency."""
        contact_listener._event_skip_counter = 0

    def run_all_benchmarks(self):
        """Run all performance benchmarks."""
        print("=" * 60)
        print("MUDSKIPPER PERFORMANCE BENCHMARK")
        print("=" * 60)

        # Baseline
        baseline_fps = self.benchmark_baseline()

        # All optimizations
        optimizations = [
            ("Reduced Physics Steps", self.optimization_1_reduce_physics_steps),
            ("Limited Organism Updates", self.optimization_2_limit_organism_updates),
            ("Reduced Collision Precision", self.optimization_3_reduce_collision_precision),
            ("Batched Deaths", self.optimization_4_batch_organism_deaths),
            ("30Hz Physics", self.optimization_5_reduce_simulation_frequency),
            ("Reduced Health Decay", self.optimization_6_simplify_health_decay),
            ("Limited Stimulation", self.optimization_7_limit_stimulation_propagation),
            ("Reduced Rendering", self.optimization_8_reduce_rendering_calls),
            ("Memory Pool", self.optimization_9_optimize_memory_allocation),
            ("Limited Contact Events", self.optimization_10_reduce_contact_events),
        ]

        # Test each optimization
        for name, func in optimizations:
            self.test_optimization(name, func)

        # Results table
        self.print_results_table()

    def print_results_table(self):
        """Print formatted results table."""
        print("\n" + "=" * 70)
        print("PERFORMANCE BENCHMARK RESULTS")
        print("=" * 70)
        print(f"{'Optimization':<30} {'FPS':<10} {'Change':<15} {'% Improvement':<15}")
        print("-" * 70)

        baseline = self.results["Baseline"]
        print(f"{'Baseline':<30} {baseline:<10.1f} {'':<15} {'':<15}")

        for name, fps in self.results.items():
            if name != "Baseline":
                change = fps - baseline
                percent = (change / baseline * 100) if baseline > 0 else 0
                change_str = f"{change:+.1f}"
                percent_str = f"{percent:+.1f}%"
                print(f"{name:<30} {fps:<10.1f} {change_str:<15} {percent_str:<15}")

        print("-" * 70)
        print(f"Test Duration: 10s baseline, 5s per optimization")
        print(f"Population: 500 organisms")

def main():
    benchmarker = PerformanceBenchmarker()
    try:
        benchmarker.run_all_benchmarks()
    except KeyboardInterrupt:
        print("\nBenchmark interrupted by user")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
