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
            'thermodynamic_analysis': None,
            'bias_point_analysis': None,
            # Add transient analysis results
            'large_signal_transient': None,
            'switching_simulations': None,
            'delay_effect': None,
            'power_dissipation': None,
            'quasi_static': None,
            'charge_conservation': None
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
            
            # Read bias point data
            bias_vds, bias_vgs, bias_ids, bias_ig, bias_is, bias_ib = self.data_reader.read_bias_point_data()
            
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
            
            # Verify bias point analysis
            bias_results = self.verification_manager.verify_bias_point_analysis(
                bias_vds, bias_vgs, bias_ids, bias_ig, bias_is, bias_ib, temp[0] if temp is not None else 27
            )
            self.results['bias_point_analysis'] = bias_results
                
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
            
            # Read and verify transient analysis data
            
            # 1. Large signal transient analysis
            time_ls, vgate_ls, vdrain_ls, idrain_ls = self.data_reader.read_large_signal_transient_data()
            if all(x is not None for x in [time_ls, vgate_ls, vdrain_ls, idrain_ls]):
                # Generate plot
                plot_generator.plot_large_signal_transient(time_ls, vgate_ls, vdrain_ls, idrain_ls)
                # Verify data
                ls_results = self.verification_manager.verify_large_signal_transient(time_ls, vgate_ls, vdrain_ls, idrain_ls)
                self.results['large_signal_transient'] = ls_results
            else:
                self.logger.logger.warning("Large signal transient data not available for verification")
            
            # 2. Switching response analysis
            time_sw, vin_sw, vout_sw, idrain_sw = self.data_reader.read_switching_response_data()
            time_sw_pwr, power_sw = self.data_reader.read_switching_power_data()
            
            if all(x is not None for x in [time_sw, vin_sw, vout_sw, idrain_sw, time_sw_pwr, power_sw]):
                # Generate plots
                plot_generator.plot_switching_response(time_sw, vin_sw, vout_sw, idrain_sw, power_sw)
                # Verify data
                sw_results = self.verification_manager.verify_switching_simulations(
                    time_sw, vin_sw, vout_sw, idrain_sw, power_sw
                )
                self.results['switching_simulations'] = sw_results
            else:
                self.logger.logger.warning("Switching response data not available for verification")
            
            # 3. Delay effect analysis
            time_delay, vin_delay, v_mid1, v_mid2, vout_delay = self.data_reader.read_delay_effect_data()
            if all(x is not None for x in [time_delay, vin_delay, v_mid1, v_mid2, vout_delay]):
                # Generate plot
                plot_generator.plot_delay_effect(time_delay, vin_delay, v_mid1, v_mid2, vout_delay)
                # Verify data
                delay_results = self.verification_manager.verify_delay_effect(time_delay, vin_delay, v_mid1, v_mid2, vout_delay)
                self.results['delay_effect'] = delay_results
            else:
                self.logger.logger.warning("Delay effect data not available for verification")
            
            # 4. Power dissipation analysis
            time_pwr_27, power_27 = self.data_reader.read_power_dissipation_data(27)
            time_pwr_100, power_100 = self.data_reader.read_power_dissipation_data(100)
            
            if all(x is not None for x in [time_pwr_27, power_27, time_pwr_100, power_100]):
                # Generate power plot
                plot_generator.plot_power_dissipation(
                    time_pwr_27, power_27, time_pwr_100, power_100
                )
                
                # Calculate energy by integrating power over time
                # Calculate time intervals
                dt_27 = np.diff(time_pwr_27, prepend=time_pwr_27[0])
                dt_100 = np.diff(time_pwr_100, prepend=time_pwr_100[0])
                
                # Calculate energy by cumulative integration of power
                energy_27 = np.cumsum(power_27 * dt_27)
                energy_100 = np.cumsum(power_100 * dt_100)
                
                # Generate energy consumption plot
                plot_generator.plot_energy_consumption(
                    time_pwr_27, energy_27, time_pwr_100, energy_100
                )
                
                # Verify data
                pwr_results = self.verification_manager.verify_power_dissipation(
                    time_pwr_27, power_27, time_pwr_100, power_100
                )
                self.results['power_dissipation'] = pwr_results
            else:
                self.logger.logger.warning("Power dissipation data not available for verification")
            
            # 5. Quasi-static analysis
            time_qs, vgate_qs, vdrain_qs, idrain_qs = self.data_reader.read_quasi_static_data()
            if all(x is not None for x in [time_qs, vgate_qs, vdrain_qs, idrain_qs]):
                # Generate plot
                plot_generator.plot_quasi_static(time_qs, vgate_qs, vdrain_qs, idrain_qs)
                # Verify data
                qs_results = self.verification_manager.verify_quasi_static(time_qs, vgate_qs, vdrain_qs, idrain_qs)
                self.results['quasi_static'] = qs_results
            else:
                self.logger.logger.warning("Quasi-static data not available for verification")
            
            # 6. Charge conservation analysis
            time_cc, vgate_cc, vdrain_cc, id_cc, ig_cc, is_cc, ib_cc = self.data_reader.read_charge_conservation_data()
            
            if all(x is not None for x in [time_cc, vgate_cc, vdrain_cc, id_cc, ig_cc, is_cc, ib_cc]):
                # Calculate total current and integrate to get charges
                i_total = id_cc + ig_cc + is_cc + ib_cc
                
                # Calculate charges by integrating currents
                dt = np.diff(time_cc, prepend=time_cc[0])
                q_gate = np.cumsum(ig_cc * dt)
                q_drain = np.cumsum(id_cc * dt)
                q_source = np.cumsum(is_cc * dt)
                q_bulk = np.cumsum(ib_cc * dt)
                q_total = q_gate + q_drain + q_source + q_bulk
                
                # Generate plot
                plot_generator.plot_charge_conservation(
                    time_cc, vgate_cc, ig_cc, id_cc, is_cc, ib_cc, i_total, 
                    q_gate, q_drain, q_source, q_bulk, q_total
                )
                # Verify data
                cc_results = self.verification_manager.verify_charge_conservation(
                    time_cc, vgate_cc, ig_cc, id_cc, is_cc, ib_cc, i_total, 
                    q_gate, q_drain, q_source, q_bulk, q_total
                )
                self.results['charge_conservation'] = cc_results
            else:
                self.logger.logger.warning("Charge conservation data not available for verification")
            
            # Update verification checklist with all results
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