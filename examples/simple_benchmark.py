#!/usr/bin/env python3
"""
Simple SPICE Model Benchmark Example

This example demonstrates how to use the spice-model-benchmark library
to run a comprehensive benchmark on a SPICE model with minimal code.

Requirements:
- Install the package: pip install -e .
- Have NGSPICE installed and available in PATH
- Have a SPICE model file (e.g., from a PDK)

Usage:
    python examples/simple_benchmark.py path/to/your/model.inc
"""

import sys
from pathlib import Path

# Import the benchmark function
from spice_model_benchmark import benchmark_spice_model


def main():
    """Run a simple benchmark example."""

    # Check if model file is provided as command line argument
    if len(sys.argv) != 2:
        print("Usage: python examples/simple_benchmark.py <model_file>")
        print("\nExample:")
        print("  python examples/simple_benchmark.py models/ngspice-cmos/FreePDK45/nom.inc")
        print("\nOr if you have your own model:")
        print("  python examples/simple_benchmark.py my_custom_model.inc")
        sys.exit(1)

    model_file = sys.argv[1]

    # Check if model file exists
    if not Path(model_file).exists():
        print(f"Error: Model file '{model_file}' does not exist.")
        sys.exit(1)

    print("SPICE Model Benchmark - Simple Example")
    print("=" * 40)
    print(f"Model file: {model_file}")
    print("This will run DC, Transient, AC, and Noise analysis...")
    print()

    # Run the benchmark with default settings
    success = benchmark_spice_model(
        model_file=model_file,
        output_dir="benchmark_results",  # Custom output directory
        modes=["dc", "transient", "ac", "noise"],  # Run all analyses
        dpi=300,  # High-quality plots
        log_level="INFO"  # Informative logging
    )

    if success:
        print("\n✓ Benchmark completed successfully!")
        print("Check the 'benchmark_results' directory for:")
        print("  - REPORT.md: Comprehensive verification report")
        print("  - plots/: Generated visualization plots")
        print("  - data/: Raw simulation data")
        print("\nYou can view the results with:")
        print("  open benchmark_results/REPORT.md")
        print("  # or")
        print("  ls benchmark_results/plots/")
    else:
        print("\n✗ Benchmark failed. Check the logs above for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
