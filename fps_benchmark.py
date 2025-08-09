#!/usr/bin/env python3
"""
FPS Benchmark Tool for Mudskipper Performance Testing
Tests various optimizations with 500 organisms over 10 seconds each.
"""

import time
import subprocess
import sys
import os
import tempfile
import shutil

class MudskipperBenchmark:
    def __init__(self):
        self.results = {}
        self.original_main = None
        self.backup_file = None

    def backup_main_py(self):
        """Backup the original main.py file."""
        shutil.copy('main.py', 'main.py.backup')
        print("✓ Backed up main.py")

    def restore_main_py(self):
        """Restore the original main.py file."""
        if os.path.exists('main.py.backup'):
            shutil.copy('main.py.backup', 'main.py')
            os.remove('main.py.backup')
            print("✓ Restored original main.py")

    def modify_main_for_benchmark(self, optimization_name="baseline", modification_func=None):
        """Modify main.py for benchmark testing."""

        # Read current main.py
        with open('main.py', 'r') as f:
            content = f.readlines()

        # Find the main function and modify for benchmarking
        modified_content = []
        in_main = False
        added_benchmark = False

        for line in content:
            if 'def main():' in line and not added_benchmark:
                modified_content.append(line)
                # Add benchmark setup
                modified_content.append('    # BENCHMARK SETUP\n')
                modified_content.append('    import time\n')
                modified_content.append('    import sys\n')
                modified_content.append('    benchmark_start_time = time.time()\n')
                modified_content.append('    frame_times = []\n')
                modified_content.append('    target_population = 500\n')
                modified_content.append(f'    print("Starting {optimization_name} benchmark...")\n')
                added_benchmark = True
                in_main = True
            elif in_main and 'while running:' in line:
                modified_content.append(line)
                # Add FPS tracking at start of main loop
                modified_content.append('        # BENCHMARK: Track frame time\n')
                modified_content.append('        frame_start = time.time()\n')
                modified_content.append('        \n')
                modified_content.append('        # BENCHMARK: Stop after 10 seconds\n')
                modified_content.append('        if time.time() - benchmark_start_time > 10:\n')
                modified_content.append('            avg_fps = 1.0 / (sum(frame_times) / len(frame_times)) if frame_times else 0\n')
                modified_content.append(f'            print(f"BENCHMARK_RESULT:{optimization_name}:{{avg_fps:.2f}}")\n')
                modified_content.append('            break\n')
                modified_content.append('        \n')

            elif in_main and 'clock.tick(60)' in line:
                modified_content.append(line)
                # Add frame time recording
                modified_content.append('        \n')
                modified_content.append('        # BENCHMARK: Record frame time\n')
                modified_content.append('        frame_time = time.time() - frame_start\n')
                modified_content.append('        if frame_time > 0:\n')
                modified_content.append('            frame_times.append(frame_time)\n')

            else:
                # Apply specific optimization modifications
                if modification_func:
                    line = modification_func(line)
                modified_content.append(line)

        # Write modified file
        with open('main.py', 'w') as f:
            f.writelines(modified_content)

    def run_benchmark_test(self, optimization_name):
        """Run a single benchmark test and extract FPS."""
        try:
            # Run the modified script
            result = subprocess.run(['python3', 'main.py'],
                                  capture_output=True, text=True, timeout=15)

            # Extract FPS from output
            for line in result.stdout.split('\n'):
                if f'BENCHMARK_RESULT:{optimization_name}:' in line:
                    fps = float(line.split(':')[-1])
                    return fps

            # If no result found, check stderr
            print(f"No benchmark result found for {optimization_name}")
            if result.stderr:
                print(f"Error: {result.stderr[:200]}...")
            return 0.0

        except subprocess.TimeoutExpired:
            print(f"Benchmark timeout for {optimization_name}")
            return 0.0
        except Exception as e:
            print(f"Error running {optimization_name}: {e}")
            return 0.0

    # Optimization modification functions
    def mod_reduce_physics_iterations(self, line):
        """Reduce physics simulation iterations."""
        if 'world.Step(1.0/60, 6, 2)' in line:
            return line.replace('world.Step(1.0/60, 6, 2)', 'world.Step(1.0/60, 3, 1)')
        return line

    def mod_limit_organism_updates(self, line):
        """Update organisms every other frame."""
        if 'for organism in organisms:' in line and 'organism.update_clock()' in line:
            return line.replace('for organism in organisms:',
                              'for i, organism in enumerate(organisms):\n        if i % 2 == frame_count % 2:')
        return line

    def mod_reduce_fps_target(self, line):
        """Run at 30 FPS instead of 60."""
        if 'clock.tick(60)' in line:
            return line.replace('clock.tick(60)', 'clock.tick(30)')
        return line

    def mod_reduce_health_decay(self, line):
        """Reduce health decay frequency."""
        if 'self.health -= 1' in line:
            return '        if self.clock_tick_count % 2 == 0:\n            self.health -= 1\n'
        return line

    def mod_skip_rendering(self, line):
        """Skip some rendering calls."""
        if 'pygame.draw.polygon(display,' in line:
            return f'        if frame_count % 2 == 0:\n    {line}'
        return line

    def mod_reduce_collision_checks(self, line):
        """Reduce collision detection frequency."""
        if 'contact_events = contact_listener.get_contact_events()' in line:
            return '            if frame_count % 2 == 0:\n                contact_events = contact_listener.get_contact_events()\n            else:\n                contact_events = []\n'
        return line

    def mod_batch_food_removal(self, line):
        """Batch food removal every few frames."""
        if 'for food_morsel in food_morsels_to_remove:' in line:
            return '        if frame_count % 3 == 0:\n            for food_morsel in food_morsels_to_remove:'
        return line

    def mod_reduce_display_updates(self, line):
        """Reduce display update frequency."""
        if 'pygame.display.flip()' in line:
            return '        if frame_count % 2 == 0:\n            pygame.display.flip()'
        return line

    def mod_simplify_toroidal_check(self, line):
        """Simplify toroidal wrapping checks."""
        if 'wrap_position = organism_rendering.get_wrap_position' in line:
            return '                if frame_count % 5 == 0:\n                    wrap_position = organism_rendering.get_wrap_position'
        return line

    def mod_reduce_stimulation_cost(self, line):
        """Reduce stimulation health cost frequency."""
        if 'self.health -= self.PULSE_HEALTH_COST' in line:
            return '            if self.clock_tick_count % 2 == 0:\n                self.health -= self.PULSE_HEALTH_COST\n'
        return line

    def run_all_benchmarks(self):
        """Run comprehensive benchmark suite."""
        print("🚀 MUDSKIPPER PERFORMANCE BENCHMARK SUITE")
        print("=" * 60)
        print("Testing 10 optimizations with 500 organisms, 10 seconds each")
        print("=" * 60)

        # Backup original
        self.backup_main_py()

        # Define test cases
        tests = [
            ("Baseline", None),
            ("Reduced Physics Steps", self.mod_reduce_physics_iterations),
            ("Limited Organism Updates", self.mod_limit_organism_updates),
            ("30 FPS Target", self.mod_reduce_fps_target),
            ("Reduced Health Decay", self.mod_reduce_health_decay),
            ("Skip Some Rendering", self.mod_skip_rendering),
            ("Reduced Collision Checks", self.mod_reduce_collision_checks),
            ("Batch Food Removal", self.mod_batch_food_removal),
            ("Reduced Display Updates", self.mod_reduce_display_updates),
            ("Simplified Toroidal Wrapping", self.mod_simplify_toroidal_check),
            ("Reduced Stimulation Cost", self.mod_reduce_stimulation_cost),
        ]

        try:
            # Run each test
            for i, (name, mod_func) in enumerate(tests):
                print(f"\n[{i+1}/{len(tests)}] Testing: {name}")

                # Restore original and apply modification
                self.restore_main_py()
                self.modify_main_for_benchmark(name.lower().replace(' ', '_'), mod_func)

                # Run benchmark
                fps = self.run_benchmark_test(name.lower().replace(' ', '_'))
                self.results[name] = fps

                print(f"    Result: {fps:.1f} FPS")

        finally:
            # Always restore original
            self.restore_main_py()

        # Print results
        self.print_results_table()

    def print_results_table(self):
        """Print comprehensive results table."""
        print("\n" + "=" * 80)
        print("📊 BENCHMARK RESULTS SUMMARY")
        print("=" * 80)

        baseline_fps = self.results.get("Baseline", 0)

        print(f"{'Optimization':<35} {'FPS':<8} {'Change':<10} {'% Improvement':<15} {'Rating'}")
        print("-" * 80)

        # Sort by FPS improvement
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
                if percent > 20:
                    rating = "🚀 Excellent"
                elif percent > 10:
                    rating = "✅ Good"
                elif percent > 5:
                    rating = "🔧 Minor"
                elif percent > 0:
                    rating = "📈 Slight"
                else:
                    rating = "❌ Negative"

            print(f"{name:<35} {fps:<8.1f} {change_str:<10} {percent_str:<15} {rating}")

        print("-" * 80)
        print(f"💡 Best optimization: {sorted_results[1][0] if len(sorted_results) > 1 else 'None'}")
        print(f"📈 Max improvement: {((sorted_results[1][1] - baseline_fps) / baseline_fps * 100):+.1f}% FPS" if len(sorted_results) > 1 and baseline_fps > 0 else "N/A")
        print("🔬 Test conditions: 500 organisms, 10 second runs")

def main():
    benchmark = MudskipperBenchmark()
    try:
        benchmark.run_all_benchmarks()
    except KeyboardInterrupt:
        print("\n⚠️ Benchmark interrupted by user")
        benchmark.restore_main_py()
    except Exception as e:
        print(f"\n❌ Benchmark failed: {e}")
        benchmark.restore_main_py()
        raise

if __name__ == "__main__":
    main()
