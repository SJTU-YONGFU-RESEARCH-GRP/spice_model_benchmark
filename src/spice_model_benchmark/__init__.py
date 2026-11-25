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
from .circuit_stress_runner import CircuitStressRunner, CircuitStressSpec
from .regression_runner import RegressionRunner, CornerSpec
from .commercial_pdk_benchmark import CommercialPDKBenchmark, CommercialPDKSpec
from .monte_carlo_benchmark import MonteCarloBenchmark
from .veriloga_linter_and_compiler import VerilogALinter, OpenVAFCompiler, VerilogABenchmarkSuite

__version__ = "1.0.0"
__all__ = [
    "MOSFETSimulation",
    "Logger",
    "SimulationRunner",
    "DataReader",
    "PlotGenerator",
    "VerificationManager",
    "CircuitStressRunner",
    "CircuitStressSpec",
    "RegressionRunner",
    "CornerSpec",
    "CommercialPDKBenchmark",
    "CommercialPDKSpec",
    "MonteCarloBenchmark",
    "VerilogALinter",
    "OpenVAFCompiler",
    "VerilogABenchmarkSuite",
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
    device_name: Optional[str] = None,
    evaluate_all: bool = False,
) -> bool:
    """
    Run comprehensive SPICE model benchmarking with a single model file.

    Netlists are dynamically synthesized on the fly from the model file without
    requiring pre-existing circuit template files in a netlists/ directory.

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
        device_name: Specific device model to benchmark (optional)
        evaluate_all: Whether to evaluate all devices discovered in the model file (default: False)

    Returns:
        bool: True if benchmarking completed successfully, False otherwise
    """
    # Convert paths to Path objects
    model_file = Path(model_file)
    output_dir = Path(output_dir)

    # Set default modes if not specified
    if modes is None:
        modes = ['dc', 'transient', 'ac', 'noise']

    # Check if input is a Verilog-A model (.va)
    va_compilation_result = None
    if str(model_file).endswith('.va'):
        from .verilog_a_compiler import VerilogACompiler
        compiler = VerilogACompiler()
        va_compilation_result = compiler.compile(str(model_file), output_dir=str(output_dir))
        if not va_compilation_result.get('success', False):
            print(f"Error: OpenVAF compilation of Verilog-A model failed: {va_compilation_result.get('error', '')}")
            return False

    # Create simulation instance (netlists synthesized on the fly if not explicitly provided)
    simulation = MOSFETSimulation(
        dc_circuit_file=dc_circuit,
        transient_circuit_file=transient_circuit,
        noise_circuit_file=noise_circuit,
        ac_circuit_file=ac_circuit,
        output_dir=str(output_dir),
        dpi=dpi,
        log_level=log_level,
        model_file=model_file,
        device_name=device_name,
        evaluate_all=evaluate_all,
    )

    if va_compilation_result:
        simulation.results['verilog_a_compilation'] = va_compilation_result

    # Run the benchmark
    return simulation.run(modes=modes)
