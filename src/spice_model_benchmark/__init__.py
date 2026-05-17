"""
SPICE Model Benchmark System

A comprehensive benchmarking system for SPICE models, allowing for the automated
verification and validation of semiconductor device models with a focus on MOSFETs.
"""

import os
from pathlib import Path
from typing import Optional, Union, List
from .mosfet_simulation import MOSFETSimulation
from .logger import Logger
from .simulation_runner import SimulationRunner
from .data_reader import DataReader
from .plot_generator import PlotGenerator
from .verification_manager import VerificationManager

__version__ = "1.0.0"
__all__ = [
    "MOSFETSimulation",
    "Logger",
    "SimulationRunner",
    "DataReader",
    "PlotGenerator",
    "VerificationManager",
    "benchmark_spice_model",
    "cli",
]


def benchmark_spice_model(
    model_file: Union[str, Path],
    output_dir: Union[str, Path] = "spice_benchmark_results",
    modes: Optional[List[str]] = None,
    dpi: int = 300,
    log_level: str = "INFO",
    dc_circuit: Optional[Union[str, Path]] = None,
    transient_circuit: Optional[Union[str, Path]] = None,
    noise_circuit: Optional[Union[str, Path]] = None,
    ac_circuit: Optional[Union[str, Path]] = None,
) -> bool:
    """
    Run comprehensive SPICE model benchmarking with a single model file.

    This function provides a simplified interface for benchmarking SPICE models.
    It can automatically use default circuit files or accept custom circuit files.

    Args:
        model_file: Path to the SPICE model file (.inc, .lib, or .model file)
        output_dir: Directory to save results (default: "spice_benchmark_results")
        modes: List of analysis modes to run. Options: ['dc', 'transient', 'ac', 'noise']
               If None, runs all modes.
        dpi: Resolution for generated plots (default: 300)
        log_level: Logging level ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
        dc_circuit: Path to custom DC analysis circuit file (optional)
        transient_circuit: Path to custom transient analysis circuit file (optional)
        noise_circuit: Path to custom noise analysis circuit file (optional)
        ac_circuit: Path to custom AC analysis circuit file (optional)

    Returns:
        bool: True if benchmarking completed successfully, False otherwise

    Example:
        >>> from spice_model_benchmark import benchmark_spice_model
        >>> success = benchmark_spice_model("my_model.inc")
        >>> if success:
        ...     print("Benchmarking completed successfully!")

    Note:
        If custom circuit files are not provided, the function will look for default
        circuit files in the 'netlists/' directory relative to the current working
        directory, or use built-in default circuits.
    """
    # Convert paths to Path objects
    model_file = Path(model_file)
    output_dir = Path(output_dir)

    # Set default modes if not specified
    if modes is None:
        modes = ['dc', 'transient', 'ac', 'noise']

    # Locate netlists directory early (needed for circuit adaptation during conversion).
    candidate_netlists_dirs = [
        Path.cwd() / "netlists",
        Path(__file__).resolve().parent.parent / "netlists",
    ]
    default_circuit_dir = next((p for p in candidate_netlists_dirs if p.exists()), None)

    if dc_circuit is None and default_circuit_dir is not None:
        default_dc = default_circuit_dir / "dc_circuit.cir"
        dc_circuit = str(default_dc) if default_dc.exists() else None

    if transient_circuit is None and default_circuit_dir is not None:
        default_transient = default_circuit_dir / "transient_circuit.cir"
        transient_circuit = str(default_transient) if default_transient.exists() else None

    if noise_circuit is None and default_circuit_dir is not None:
        default_noise = default_circuit_dir / "noise_circuit.cir"
        noise_circuit = str(default_noise) if default_noise.exists() else None

    if ac_circuit is None and default_circuit_dir is not None:
        default_ac = default_circuit_dir / "ac_circuit.cir"
        ac_circuit = str(default_ac) if default_ac.exists() else None

    # Check if required circuit files exist (or were resolved).
    missing_circuits = []
    if 'dc' in modes and (not dc_circuit or not Path(dc_circuit).exists()):
        missing_circuits.append(f"DC circuit: {dc_circuit or '<not found>'}")
    if 'transient' in modes and (not transient_circuit or not Path(transient_circuit).exists()):
        missing_circuits.append(f"Transient circuit: {transient_circuit or '<not found>'}")
    if 'noise' in modes and (not noise_circuit or not Path(noise_circuit).exists()):
        missing_circuits.append(f"Noise circuit: {noise_circuit or '<not found>'}")
    if 'ac' in modes and (not ac_circuit or not Path(ac_circuit).exists()):
        missing_circuits.append(f"AC circuit: {ac_circuit or '<not found>'}")

    if missing_circuits:
        print(f"Error: Missing required circuit files:")
        for circuit in missing_circuits:
            print(f"  - {circuit}")
        if default_circuit_dir is None:
            print("\nHint: could not locate a 'netlists/' folder from the current working directory.")
            print("      Run from your repo root (where netlists/ exists) or pass --dc-circuit/--ac-circuit, etc.")
        else:
            print(f"\nHint: resolved netlists directory: {default_circuit_dir}")
        print("\nPlease ensure circuit files exist or provide custom circuit files.")
        return False

    # Create simulation instance
    simulation = MOSFETSimulation(
        dc_circuit_file=dc_circuit,
        transient_circuit_file=transient_circuit,
        noise_circuit_file=noise_circuit,
        ac_circuit_file=ac_circuit,
        output_dir=str(output_dir),
        dpi=dpi,
        log_level=log_level,
    )

    # Run the benchmark
    return simulation.run(modes=modes)
