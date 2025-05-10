import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
import numpy as np

from src.logger import Logger
from src.simulation_runner import SimulationRunner
from src.data_reader import DataReader
from src.plot_generator import PlotGenerator
from src.verification_manager import VerificationManager

class MOSFETSimulation:
    """Main class for MOSFET simulation and verification.
    
    This class handles the complete MOSFET simulation workflow including:
    - Simulation setup and execution
    - IV characteristics analysis
    - Temperature analysis
    - Thermodynamic analysis
    - Results verification and reporting
    """
    def __init__(self, circuit_file, output_dir='results', dpi=300, log_level='INFO'):
        self.circuit_file = circuit_file
        self.output_dir = output_dir
        self.dpi = dpi
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize components
        self.logger = Logger(log_level=log_level)
        self.simulation_runner = SimulationRunner(circuit_file, self.logger, output_dir)
        self.data_reader = DataReader(self.logger, output_dir)
        self.plot_generator = PlotGenerator(output_dir, dpi, self.logger)
        self.verification_manager = VerificationManager(self.logger, output_dir)
        
        # Initialize results
        self.results = {
            'simulation_setup': None,
            'iv_characteristics': None,
            'temperature_analysis': None,
            'thermodynamic_analysis': None
        }

    def run(self):
        """Run the MOSFET simulation and verification."""
        try:
            # Verify circuit file
            setup_results = self.verification_manager.verify_simulation_setup(self.circuit_file)
            if not setup_results['netlist_exists'] or not setup_results['ngspice_installed']:
                raise ValueError("Circuit file verification failed")
            self.results['simulation_setup'] = setup_results
            
            # Run SPICE simulation
            if not self.simulation_runner.run_simulation():
                raise RuntimeError("SPICE simulation failed")
            
            # Read data files
            vds, vgs, ids, ig, is_, ib, power = self.data_reader.read_iv_data()
            temp = self.data_reader.read_temperature_data()
            
            # Create plot generator
            plot_generator = PlotGenerator(self.output_dir, logger=self.logger)
            
            # Generate plots
            if vds is not None and vgs is not None and ids is not None:
                plot_generator.plot_iv_characteristics(vds, vgs, ids, self.output_dir)
            if temp is not None and ids is not None:
                plot_generator.plot_temperature_analysis(temp, ids)
            if all(x is not None for x in [ids, ig, is_, ib]):
                plot_generator.plot_kcl_verification(ids, ig, is_, ib)
            
            # Verify characteristics
            iv_results = self.verification_manager.verify_iv_characteristics(vds, vgs, ids, ig, is_, ib, temp)
            if not iv_results['data_generated'] or not iv_results['data_read']:
                raise ValueError("IV characteristics verification failed")
            self.results['iv_characteristics'] = iv_results
                
            temp_results = self.verification_manager.verify_temperature_analysis(temp, ids)
            if not temp_results['temp_sweep'] or not temp_results['device_behavior']:
                raise ValueError("Temperature analysis verification failed")
            self.results['temperature_analysis'] = temp_results
            
            # Calculate power for thermodynamic analysis
            power = np.abs(vds * ids) if vds is not None and ids is not None else None
            thermo_results = self.verification_manager.verify_thermodynamic_analysis(power, temp, ids)
            # Only raise error for critical failures (missing power measurements)
            # Energy conservation failure will be reported in the verification checklist
            if not thermo_results['power_measurements']:
                raise ValueError("Power measurements verification failed")
            self.results['thermodynamic_analysis'] = thermo_results
            
            # Update verification checklist
            self.verification_manager.update_verification_checklist(self.results)
            
            self.logger.logger.info("MOSFET simulation completed successfully")
            return True
            
        except Exception as e:
            self.logger.logger.error(f"Error in MOSFET simulation: {e}")
            return False

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Run MOSFET simulation and analyze results')
    parser.add_argument('--circuit', type=str, default='netlists/circuit.cir',
                      help='Path to the SPICE netlist file (default: circuit.cir)')
    parser.add_argument('--output-dir', type=str, default='results',
                      help='Directory to store output files (default: results)')
    parser.add_argument('--log-level', type=str, default='DEBUG',
                      choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                      help='Set the logging level (default: DEBUG)')
    parser.add_argument('--dpi', type=int, default=300,
                      help='DPI for output plots (default: 300)')
    return parser.parse_args()

def main():
    """Main entry point for the MOSFET simulation tool."""
    args = parse_args()
    simulation = MOSFETSimulation(
        circuit_file=args.circuit,
        output_dir=args.output_dir,
        dpi=args.dpi,
        log_level=args.log_level
    )
    
    if not simulation.run():
        sys.exit(1)

if __name__ == "__main__":
    main() 