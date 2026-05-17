"""
Command-line interface for SPICE Model Benchmark System.
"""

import argparse
import shlex
import sys
from pathlib import Path
from typing import List, Optional

from . import benchmark_spice_model


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the command-line interface.

    Args:
        args: Command line arguments (defaults to sys.argv[1:])

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    parser = argparse.ArgumentParser(
        description="SPICE Model Benchmark System - Comprehensive MOSFET verification",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run benchmark with default settings
  spice-benchmark model.inc

  # Run only DC analysis with custom output directory
  spice-benchmark model.inc --modes dc --output-dir my_results

  # Run with custom circuit files
  spice-benchmark model.inc \\
    --dc-circuit custom_dc.cir \\
    --transient-circuit custom_transient.cir \\
    --output-dir benchmark_output

  # Run with high-resolution plots and debug logging
  spice-benchmark model.inc --dpi 600 --log-level DEBUG
        """
    )

    parser.add_argument(
        "model_file",
        type=str,
        help="Path to the SPICE model file (.inc, .lib, or .model file)"
    )

    parser.add_argument(
        "--modes",
        type=str,
        nargs="+",
        choices=["dc", "transient", "ac", "noise"],
        default=["dc", "transient", "ac", "noise"],
        help="Analysis modes to run (default: all modes)"
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="spice_benchmark_results",
        help="Output directory for results (default: spice_benchmark_results)"
    )

    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="Resolution for generated plots (default: 300)"
    )

    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Logging level (default: INFO)"
    )

    parser.add_argument(
        "--dc-circuit",
        type=str,
        help="Path to custom DC analysis circuit file"
    )

    parser.add_argument(
        "--transient-circuit",
        type=str,
        help="Path to custom transient analysis circuit file"
    )

    parser.add_argument(
        "--noise-circuit",
        type=str,
        help="Path to custom noise analysis circuit file"
    )

    parser.add_argument(
        "--ac-circuit",
        type=str,
        help="Path to custom AC analysis circuit file"
    )

    parser.add_argument(
        "--source-format",
        type=str,
        choices=["auto", "ngspice", "hspice", "spectre"],
        default="auto",
        help="Source SPICE format (default: auto-detect from file extension/content)"
    )

    parser.add_argument(
        "--translator-path",
        type=str,
        help="Path to new-spice-translator project root (auto-detected if omitted)"
    )

    parser.add_argument(
        "--bridge",
        action="append",
        default=[],
        metavar='"TOOL [ARGS...]"',
        help="Chain to downstream tool after benchmark (e.g. --bridge \"translate --targets hspice\")"
    )

    # Parse arguments
    if args is None:
        args = sys.argv[1:]

    try:
        parsed_args = parser.parse_args(args)
    except SystemExit as e:
        return e.code

    # Validate model file exists
    model_path = Path(parsed_args.model_file)
    if not model_path.exists():
        print(f"Error: Model file '{parsed_args.model_file}' does not exist.")
        return 1

    # Run the benchmark
    print(f"Starting SPICE model benchmark for: {parsed_args.model_file}")
    print(f"Output directory: {parsed_args.output_dir}")
    print(f"Modes: {', '.join(parsed_args.modes)}")
    print("-" * 60)

    success = benchmark_spice_model(
        model_file=parsed_args.model_file,
        output_dir=parsed_args.output_dir,
        modes=parsed_args.modes,
        dpi=parsed_args.dpi,
        log_level=parsed_args.log_level,
        dc_circuit=parsed_args.dc_circuit,
        transient_circuit=parsed_args.transient_circuit,
        noise_circuit=parsed_args.noise_circuit,
        ac_circuit=parsed_args.ac_circuit,
        source_format=parsed_args.source_format if parsed_args.source_format != "auto" else None,
        translator_path=parsed_args.translator_path,
    )

    # --- Bridge chaining ---
    if parsed_args.bridge:
        context = {
            "model_file": parsed_args.model_file,
            "output_dir": parsed_args.output_dir,
        }
        _run_bridges(context, parsed_args.bridge)

    if success:
        print("\n✓ SPICE model benchmark completed successfully!")
        print(f"Results saved to: {parsed_args.output_dir}")
        return 0
    else:
        print("\n✗ SPICE model benchmark failed!")
        return 1


def _run_bridges(context: dict, bridge_directives: list[str]) -> None:
    """Execute bridge directives after benchmarking completes."""
    project_root = Path(__file__).resolve().parents[2]  # src/spice_model_benchmark/cli.py -> project root
    sys.path.insert(0, str(project_root))
    for directive in bridge_directives:
        parts = shlex.split(directive)
        if not parts:
            continue
        name = parts[0]
        bridge_args = parts[1:]
        try:
            mod = __import__(f"bridge.{name}", fromlist=["run"])
            mod.run(context, bridge_args)
        except ImportError:
            print(f"[bridge] Unknown bridge target: {name} (bridge/{name}.py not found)")
        except Exception as e:
            print(f"[bridge] {name} failed: {e}")


if __name__ == "__main__":
    sys.exit(main())
