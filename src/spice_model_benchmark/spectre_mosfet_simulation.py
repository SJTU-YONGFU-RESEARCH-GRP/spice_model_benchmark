"""
Spectre MOSFET Simulation coordinator.

Mirrors MOSFETSimulation class but uses SpectreRunner for simulation execution.
Reuses DataReader, PlotGenerator, and VerificationManager from the ngspice pipeline
since the post-processor generates identical text file outputs.
"""
import os
import sys
from pathlib import Path
from typing import List, Optional

from .logger import Logger
from .spectre_runner import SpectreRunner
from .data_reader import DataReader
from .plot_generator import PlotGenerator
from .verification_manager import VerificationManager


class SpectreMOSFETSimulation:
    """Main class for MOSFET simulation using Spectre.

    Replicates the exact same benchmark workflow as MOSFETSimulation
    but uses the Spectre simulator instead of ngspice.
    The post-processor ensures output data files are identical in format.
    """

    def __init__(self,
                 dc_circuit_file: Optional[str] = None,
                 transient_circuit_file: Optional[str] = None,
                 noise_circuit_file: Optional[str] = None,
                 ac_circuit_file: Optional[str] = None,
                 output_dir: str = 'results_spectre',
                 dpi: int = 300,
                 log_level: str = 'INFO'):

        self.dc_circuit_file = dc_circuit_file
        self.transient_circuit_file = transient_circuit_file
        self.noise_circuit_file = noise_circuit_file
        self.ac_circuit_file = ac_circuit_file

        self.output_dir = Path(output_dir).resolve()
        self.dpi = dpi

        os.makedirs(self.output_dir, exist_ok=True)

        # Initialize components
        self.logger = Logger(log_level=log_level)
        self.simulation_runner = SpectreRunner(
            self.logger,
            output_dir=str(self.output_dir),
            dc_circuit_file=dc_circuit_file,
            transient_circuit_file=transient_circuit_file,
            noise_circuit_file=noise_circuit_file,
            ac_circuit_file=ac_circuit_file,
        )
        self.data_reader = DataReader(self.logger, output_dir=str(self.output_dir))
        self.plot_generator = PlotGenerator(str(self.output_dir), dpi=dpi, logger=self.logger)
        self.verification_manager = VerificationManager(self.logger, output_dir=str(self.output_dir))

        # Set plot generator in verification manager
        self.verification_manager.plot_generator = self.plot_generator

        self.results = {
            'simulation_setup': None,
            'dc_operating_point_analysis': None,
            'temperature_analysis': None,
            'thermodynamic_analysis': None,
            'transient_large_signal': None,
            'transient_switching': None,
            'transient_delay_effect': None,
            'transient_power_dissipation': None,
            'transient_quasi_static': None,
            'ac_cv_characteristics': None,
            'ac_sparameter_analysis': None,
            'ac_nqs_effects': None,
            'ac_charge_conservation': None,
            'noise_analysis': None,
        }

    def run(self, modes: Optional[List[str]] = None) -> bool:
        """Run the Spectre simulation and verification workflow.

        Args:
            modes: List of simulation modes. Default: ['dc']
        """
        if modes is None:
            modes = ['dc']

        self.logger.logger.info("=" * 60)
        self.logger.logger.info("Spectre MOSFET Simulation & Verification")
        self.logger.logger.info("=" * 60)

        # Phase 1: Run Spectre simulations
        self.logger.logger.info("Phase 1: Running Spectre simulations...")
        if not self.simulation_runner.run_simulations_by_mode(modes):
            self.logger.logger.error("Spectre simulations failed")
            return False

        # Phase 2: Read data and generate plots/reports
        self.logger.logger.info("Phase 2: Reading data and generating reports...")

        # Verify simulation setup
        self.results['simulation_setup'] = self.verification_manager.verify_simulation_setup(
            self.dc_circuit_file
        )

        # Process DC mode
        if 'dc' in modes or 'all' in modes:
            self.logger.logger.info("Processing DC results...")
            try:
                self.results['dc_operating_point_analysis'] = \
                    self.verification_manager.verify_dc_operating_point_analysis()
                self.results['temperature_analysis'] = \
                    self.verification_manager.verify_temperature_analysis()
                self.results['thermodynamic_analysis'] = \
                    self.verification_manager.verify_thermodynamic_analysis()
            except Exception as e:
                self.logger.logger.error(f"DC processing failed: {e}")
                self.logger.logger.warning("Continuing with partial DC results...")

        # Phase 3: Generate verification report
        self.logger.logger.info("Phase 3: Generating verification report...")
        self.verification_manager.update_verification_checklist(self.results, modes)

        self.logger.logger.info("Spectre benchmark workflow complete!")
        report_path = self.output_dir / 'REPORT.md'
        self.logger.logger.info(f"Report: {report_path}")

        return True


def benchmark_spice_model_spectre(
    model_file: str,
    output_dir: str = "spectre_benchmark_results",
    modes: Optional[List[str]] = None,
    dpi: int = 300,
    log_level: str = "INFO",
    dc_circuit: Optional[str] = None,
    transient_circuit: Optional[str] = None,
    noise_circuit: Optional[str] = None,
    ac_circuit: Optional[str] = None,
) -> bool:
    """Convenience function: run Spectre benchmark on a model file.

    Uses default spectre netlists from netlists/spectre/ directory.

    Args:
        model_file: Path to the model file to benchmark
        output_dir: Directory for results
        modes: List of modes to run (default: ['dc'])
        dpi: Plot resolution
        log_level: Logging level
        dc_circuit: Custom DC circuit file
        transient_circuit: Custom transient circuit file
        noise_circuit: Custom noise circuit file
        ac_circuit: Custom AC circuit file

    Returns:
        bool: True if benchmark completed successfully
    """
    if modes is None:
        modes = ['dc']

    # Use default spectre netlists
    default_netlist_dir = Path(__file__).parent.parent.parent / 'netlists' / 'spectre'

    def _resolve(custom_path: Optional[str], default_name: str) -> Optional[str]:
        if custom_path:
            return custom_path
        default_path = default_netlist_dir / default_name
        if default_path.exists():
            return str(default_path)
        return None

    sim = SpectreMOSFETSimulation(
        dc_circuit_file=_resolve(dc_circuit, 'dc_circuit.scs'),
        transient_circuit_file=_resolve(transient_circuit, 'transient_circuit.scs'),
        noise_circuit_file=_resolve(noise_circuit, 'noise_circuit.scs'),
        ac_circuit_file=_resolve(ac_circuit, 'ac_circuit.scs'),
        output_dir=output_dir,
        dpi=dpi,
        log_level=log_level,
    )

    return sim.run(modes=modes)
