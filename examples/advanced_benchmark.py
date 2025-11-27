#!/usr/bin/env python3
"""
Advanced SPICE Model Benchmark Example

This example shows how to use the spice-model-benchmark library
with custom circuit files and advanced configuration options.

Requirements:
- Install the package: pip install -e .
- Have NGSPICE installed and available in PATH
- Have custom circuit files (optional - will use defaults if not provided)
"""

import sys
from pathlib import Path

# Import the benchmark function and other components
from spice_model_benchmark import benchmark_spice_model, MOSFETSimulation


def run_simple_benchmark(model_file: str):
    """Run benchmark with basic configuration."""
    print("Running simple benchmark...")

    success = benchmark_spice_model(
        model_file=model_file,
        output_dir="simple_results",
        modes=["dc", "transient"],  # Only run DC and transient analysis
        dpi=150,  # Lower resolution for faster execution
    )

    return success


def run_advanced_benchmark(model_file: str):
    """Run benchmark with custom circuit files and advanced settings."""
    print("Running advanced benchmark with custom settings...")

    # Check if custom circuit files exist
    custom_circuits = {
        "dc_circuit": "netlists/custom_dc.cir",
        "transient_circuit": "netlists/custom_transient.cir",
        "noise_circuit": "netlists/custom_noise.cir",
        "ac_circuit": "netlists/custom_ac.cir",
    }

    # Use custom circuits if they exist, otherwise use defaults
    circuit_files = {}
    for key, path in custom_circuits.items():
        if Path(path).exists():
            circuit_files[key] = path
            print(f"Using custom {key}: {path}")
        else:
            print(f"Using default {key}")

    success = benchmark_spice_model(
        model_file=model_file,
        output_dir="advanced_results",
        modes=["dc", "transient", "ac", "noise"],
        dpi=600,  # High resolution
        log_level="DEBUG",  # Detailed logging
        **circuit_files
    )

    return success


def run_programmatic_example(model_file: str):
    """Example of using the MOSFETSimulation class directly."""
    print("Running programmatic example with direct class usage...")

    # Create simulation instance with direct control
    simulation = MOSFETSimulation(
        dc_circuit_file="netlists/dc_circuit.cir",
        transient_circuit_file="netlists/transient_circuit.cir",
        noise_circuit_file="netlists/noise_circuit.cir",
        ac_circuit_file="netlists/ac_circuit.cir",
        output_dir="programmatic_results",
        dpi=300,
        log_level="INFO"
    )

    # Run specific analyses
    success = simulation.run(modes=["dc", "transient"])

    return success


def main():
    """Main function demonstrating different usage patterns."""

    if len(sys.argv) != 2:
        print("Usage: python examples/advanced_benchmark.py <model_file>")
        print("\nExample:")
        print("  python examples/advanced_benchmark.py models/ngspice-cmos/FreePDK45/nom.inc")
        sys.exit(1)

    model_file = sys.argv[1]

    if not Path(model_file).exists():
        print(f"Error: Model file '{model_file}' does not exist.")
        sys.exit(1)

    print("SPICE Model Benchmark - Advanced Examples")
    print("=" * 50)
    print(f"Model file: {model_file}")
    print()

    # Example 1: Simple benchmark
    print("Example 1: Simple benchmark")
    print("-" * 30)
    success1 = run_simple_benchmark(model_file)
    print(f"Result: {'✓ Success' if success1 else '✗ Failed'}")
    print()

    # Example 2: Advanced benchmark
    print("Example 2: Advanced benchmark")
    print("-" * 30)
    success2 = run_advanced_benchmark(model_file)
    print(f"Result: {'✓ Success' if success2 else '✗ Failed'}")
    print()

    # Example 3: Programmatic usage
    print("Example 3: Programmatic usage")
    print("-" * 30)
    success3 = run_programmatic_example(model_file)
    print(f"Result: {'✓ Success' if success3 else '✗ Failed'}")
    print()

    # Summary
    all_success = success1 and success2 and success3
    print("Summary:")
    print(f"All examples completed successfully: {'✓ Yes' if all_success else '✗ No'}")
    print("\nCheck the following directories for results:")
    print("  - simple_results/")
    print("  - advanced_results/")
    print("  - programmatic_results/")


if __name__ == "__main__":
    main()
