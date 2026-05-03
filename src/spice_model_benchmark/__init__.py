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
    source_format: Optional[str] = None,
    translator_path: Optional[str] = None,
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
        source_format: Source format override ('auto', 'ngspice', 'hspice', 'spectre').
                       'auto' or None (default) detects from file extension/content.
        translator_path: Path to new-spice-translator project root (auto-detected if None)

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

    # ---- Format conversion (hspice/spectre -> ngspice) ----
    converted_model_path = None
    adapted_circuits = None
    from .format_converter import FormatConverter
    converter = FormatConverter(translator_path=translator_path)

    if source_format is None or source_format.lower() == 'auto':
        source_format = converter.detect_format(model_file)

    if source_format.lower() != 'ngspice':
        print(f"Source format detected/specified: {source_format}")
        print(f"Converting {model_file.name} to ngspice format...")
        try:
            convert_dir = output_dir / '_converted'
            converted_model_path = converter.convert_to_ngspice(
                model_file, source_format=source_format, output_dir=convert_dir,
            )
            print(f"  Converted model: {converted_model_path}")

            # Extract model names and adapt circuit files
            model_names = converter.extract_model_names(converted_model_path)
            print(f"  Model names found: {model_names[:5]}{'...' if len(model_names) > 5 else ''}")

            if default_circuit_dir is not None:
                adapted_circuits = converter.generate_adapted_circuits(
                    original_circuit_dir=default_circuit_dir,
                    converted_model_path=converted_model_path,
                    model_names=model_names,
                    output_dir=convert_dir / 'circuits',
                    source_format=source_format,
                )
                print(f"  Adapted circuits: {list(adapted_circuits.keys())}")
        except Exception as e:
            print(f"Error: Format conversion failed: {e}")
            return False

    # Use adapted circuits if conversion happened
    if adapted_circuits:
        if 'dc' in adapted_circuits and dc_circuit is None:
            dc_circuit = adapted_circuits['dc']
        if 'transient' in adapted_circuits and transient_circuit is None:
            transient_circuit = adapted_circuits['transient']
        if 'noise' in adapted_circuits and noise_circuit is None:
            noise_circuit = adapted_circuits['noise']
        if 'ac' in adapted_circuits and ac_circuit is None:
            ac_circuit = adapted_circuits['ac']

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
        source_format=source_format,
        converted_model_path=str(converted_model_path) if converted_model_path else None,
    )

    # Run the benchmark
    return simulation.run(modes=modes)
