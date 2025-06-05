import os
import sys
import argparse
import json
from pathlib import Path
from datetime import datetime
import numpy as np
from scipy import integrate

from logger import Logger
from simulation_runner import SimulationRunner
from data_reader import DataReader
from plot_generator import PlotGenerator
from verification_manager import VerificationManager

class MOSFETSimulation:
    """Main class for MOSFET simulation and verification.
    
    This class handles the complete MOSFET simulation workflow including:
    - Simulation setup and execution
    - IV characteristics analysis
    - Temperature analysis
    - Thermodynamic analysis
    - Results verification and reporting
    """
    def __init__(self, dc_circuit_file, transient_circuit_file, noise_circuit_file, 
                 ac_circuit_file=None, output_dir='results', dpi=300, log_level='INFO'):
        # Store the circuit file paths directly
        self.dc_circuit_file = dc_circuit_file
        self.transient_circuit_file = transient_circuit_file
        self.noise_circuit_file = noise_circuit_file
        self.ac_circuit_file = ac_circuit_file
        
        # Use the DC circuit as the reference circuit for directory paths
        self.circuit_dir = os.path.dirname(dc_circuit_file)
        
        # Convert output_dir to absolute path if it's not already
        self.output_dir = Path(output_dir).resolve()
        self.dpi = dpi
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize components
        self.logger = Logger(log_level=log_level)
        self.simulation_runner = SimulationRunner(self.logger, output_dir=str(self.output_dir))
        self.data_reader = DataReader(self.logger, output_dir=str(self.output_dir))
        self.plot_generator = PlotGenerator(str(self.output_dir), dpi=dpi, logger=self.logger)
        self.verification_manager = VerificationManager(self.logger, output_dir=str(self.output_dir))
        
        # Set plot generator in verification manager to use for plots
        self.verification_manager.plot_generator = self.plot_generator
        
        # Initialize results
        self.results = {
            'simulation_setup': None,
            'iv_characteristics': None,
            'temperature_analysis': None,
            'thermodynamic_analysis': None,
            'bias_point_analysis': None,
            # Add AC analysis results
            'cv_characteristics': None,
            'sparameter_analysis': None,
            'nqs_effects': None,
            'charge_conservation': None,
            # Add transient analysis results
            'large_signal_transient': None,
            'switching_simulations': None,
            'delay_effect': None,
            'power_dissipation': None,
            'quasi_static': None,
            # Add noise analysis results
            'noise_analysis': None
        }

    def run(self, modes=['all']):
        """Run the MOSFET simulation and analysis.
        
        Args:
            modes: List of simulation modes to run. Can be 'dc', 'transient', 'ac', 'noise'.
                  Default is ['all'] which runs all modes.
        """
        try:
            self.logger.logger.info("Starting MOSFET simulation and analysis")
            
            # Create plot generator and data reader
            plot_generator = PlotGenerator(str(self.output_dir), self.dpi, self.logger)
            self.data_reader = DataReader(self.logger, str(self.output_dir))
            self.verification_manager = VerificationManager(self.logger, str(self.output_dir))
            
            # Set the plot generator in the verification manager for proper plot generation
            self.verification_manager.plot_generator = plot_generator
            
            # Initialize simulation runner with the circuit files
            self.simulation_runner = SimulationRunner(
                self.logger, 
                str(self.output_dir),
                dc_circuit_file=self.dc_circuit_file,
                transient_circuit_file=self.transient_circuit_file,
                noise_circuit_file=self.noise_circuit_file,
                ac_circuit_file=self.ac_circuit_file
            )
            
            # Verify circuit files exist based on selected modes
            circuit_files = []
            if 'dc' in modes:
                circuit_files.append((self.dc_circuit_file, "DC"))
            if 'transient' in modes:
                circuit_files.append((self.transient_circuit_file, "Transient"))
            if 'noise' in modes:
                circuit_files.append((self.noise_circuit_file, "Noise"))
            if 'ac' in modes:
                circuit_files.append((self.ac_circuit_file, "AC"))
            
            for circ_file, circ_type in circuit_files:
                if not os.path.exists(circ_file):
                    self.logger.logger.error(f"{circ_type} circuit file not found: {circ_file}")
                    return False
            
            # Run simulations based on selected modes
            if not self.simulation_runner.run_simulations_by_mode(modes):
                self.logger.logger.error("SPICE simulation failed")
                return False
            
            # Verify circuit files
            self.logger.logger.info("Verifying simulation setup")
            setup_results = {}

            # Do a single verification for ngspice and DC circuit
            self.logger.logger.info("Verifying ngspice installation and DC circuit setup")
            dc_result = self.verification_manager.verify_simulation_setup(self.dc_circuit_file)
            setup_results["ngspice_installed"] = dc_result['ngspice_installed']
            setup_results["dc_netlist_exists"] = dc_result['netlist_exists']
            setup_results["dc_details"] = dc_result['details']

            # Verify other circuit files if they exist
            for circ_file, circ_type in circuit_files:
                if circ_file != self.dc_circuit_file:  # Skip DC circuit as it's already verified
                    self.logger.logger.info(f"Verifying {circ_type} circuit setup")
                    result = self.verification_manager.verify_simulation_setup(circ_file)
                    setup_results[f"{circ_type.lower()}_netlist_exists"] = result['netlist_exists']
                    setup_results[f"{circ_type.lower()}_details"] = result['details']

            # Store common verification results
            setup_results["netlist_exists"] = all(result['netlist_exists'] for result in [
                self.verification_manager.verify_simulation_setup(circ_file) 
                for circ_file, _ in circuit_files
            ])
            setup_results["simulation_runs"] = True  # Will be updated by simulation runner
            setup_results["details"] = {
                "netlist_path": ", ".join([str(Path(circ_file).absolute()) for circ_file, _ in circuit_files]),
                "ngspice_version": dc_result['details']['ngspice_version'],
                "simulation_status": "Ready to run"
            }
            self.results['simulation_setup'] = setup_results
            
            # Run analysis based on selected modes
            if 'dc' in modes:
                # Read DC data files
                vds, vgs, ids, ig, is_, ib, power = self.data_reader.read_iv_data()
                temp = self.data_reader.read_temperature_data()
                
                # Read bias point data
                bias_vds, bias_vgs, bias_ids, bias_ig, bias_is, bias_ib = self.data_reader.read_bias_point_data()
                
                # Generate IV plots
                if vds is not None and vgs is not None and ids is not None:
                    plot_generator.plot_iv_characteristics(vds, vgs, ids, self.output_dir)
                    # Store IV characteristics data in results
                    self.results['iv_characteristics'] = {
                        'data_generated': True,
                        'data_read': True,
                        'vds_range': f"{min(vds):.2f}V to {max(vds):.2f}V" if vds is not None else "Not available",
                        'vgs_range': f"{min(vgs):.2f}V to {max(vgs):.2f}V" if vgs is not None else "Not available",
                        'ids_range': f"{min(ids):.2e}A to {max(ids):.2e}A" if ids is not None else "Not available",
                        'details': {
                            'vds': vds.tolist() if vds is not None else None,
                            'vgs': vgs.tolist() if vgs is not None else None,
                            'ids': ids.tolist() if ids is not None else None,
                            'ig': ig.tolist() if ig is not None else None,
                            'is': is_.tolist() if is_ is not None else None,
                            'ib': ib.tolist() if ib is not None else None
                        }
                    }
                if temp is not None and ids is not None:
                    plot_generator.plot_temperature_analysis(temp, ids)
                if all(x is not None for x in [ids, ig, is_, ib]):
                    plot_generator.plot_kcl_verification(ids, ig, is_, ib)
                
                # Verify characteristics
                iv_results = self.verification_manager.verify_iv_characteristics(vds, vgs, ids, ig, is_, ib, temp)
                if not iv_results['data_generated'] or not iv_results['data_read']:
                    raise ValueError("IV characteristics verification failed")
                self.results['iv_characteristics'] = iv_results
                
                # Verify temperature analysis
                temp_results = self.verification_manager.verify_temperature_analysis(temp, ids)
                if not temp_results['temp_sweep'] or not temp_results['device_behavior']:
                    raise ValueError("Temperature analysis verification failed")
                self.results['temperature_analysis'] = temp_results
                
                # Calculate power for thermodynamic analysis
                power = np.abs(vds * ids) if vds is not None and ids is not None else None
                thermo_results = self.verification_manager.verify_thermodynamic_analysis(power, temp, ids)
                if not thermo_results['power_measurements']:
                    raise ValueError("Power measurements verification failed")
                self.results['thermodynamic_analysis'] = thermo_results
                
                # Verify bias point analysis
                bias_results = self.verification_manager.verify_bias_point_analysis(
                    bias_vds, bias_vgs, bias_ids, bias_ig, bias_is, bias_ib, temp[0] if temp is not None else 27
                )
                self.results['bias_point_analysis'] = bias_results
            
            if 'ac' in modes:
                # Read CV data
                vg, cv_ig, cv_is, cv_ib, cgg = self.data_reader.read_cv_data()
                
                # Read high-frequency data
                freq, s11_mag, s11_phase, s12_mag, s12_phase, s21_mag, s21_phase, s22_mag, s22_phase = self.data_reader.read_sparameter_data()
                nqs_freq, vg_phase, id_phase, phase_diff = self.data_reader.read_nqs_effects_data()
                
                # Generate CV plots
                if vg is not None:
                    plot_generator.plot_cv_characteristics()
                
                # Verify CV characteristics
                if vg is not None:
                    cv_results = self.verification_manager.verify_cv_characteristics(vg, cgg, freq, vg_phase, id_phase)
                    self.results['cv_characteristics'] = cv_results
                
                # Verify S-parameter and high-frequency behavior
                if freq is not None and s11_mag is not None and s21_mag is not None and s12_mag is not None and s22_mag is not None:
                    plot_generator.plot_sparameter_analysis(freq, s11_mag, s21_mag, s12_mag, s22_mag)
                    sparam_results = self.verification_manager.verify_sparameter_analysis(
                        freq, s11_mag, s21_mag, s12_mag, s22_mag
                    )
                    self.results['sparameter_analysis'] = sparam_results
                
                # Verify non-quasi-static effects
                if nqs_freq is not None and vg_phase is not None and id_phase is not None:
                    plot_generator.plot_nqs_effects(nqs_freq, vg_phase, id_phase, phase_diff)
                    nqs_results = self.verification_manager.verify_nqs_effects(
                        nqs_freq, vg_phase, id_phase, phase_diff
                    )
                    self.results['nqs_effects'] = nqs_results
            
            if 'transient' in modes:
                # Read and verify transient analysis data
                
                # 1. Large signal transient analysis
                time_ls, vgate_ls, vdrain_ls, idrain_ls = self.data_reader.read_large_signal_transient_data()
                if all(x is not None for x in [time_ls, vgate_ls, vdrain_ls, idrain_ls]):
                    plot_generator.plot_large_signal_transient(time_ls, vgate_ls, vdrain_ls, idrain_ls)
                    ls_results = self.verification_manager.verify_large_signal_transient(time_ls, vgate_ls, vdrain_ls, idrain_ls)
                    self.results['large_signal_transient'] = ls_results
                
                # 2. Switching response analysis
                time_sw, vin_sw, vout_sw, idrain_sw = self.data_reader.read_switching_response_data()
                time_sw_pwr, power_sw = self.data_reader.read_switching_power_data()
                
                if all(x is not None for x in [time_sw, vin_sw, vout_sw, idrain_sw, time_sw_pwr, power_sw]):
                    plot_generator.plot_switching_response(time_sw, vin_sw, vout_sw, idrain_sw, power_sw)
                    sw_results = self.verification_manager.verify_switching_simulations(
                        time_sw, vin_sw, vout_sw, idrain_sw, power_sw
                    )
                    self.results['switching_simulations'] = sw_results
                
                # 3. Delay effect analysis
                time_delay, vin_delay, v_mid1, v_mid2, vout_delay = self.data_reader.read_delay_effect_data()
                if all(x is not None for x in [time_delay, vin_delay, v_mid1, v_mid2, vout_delay]):
                    plot_generator.plot_delay_effect(time_delay, vin_delay, v_mid1, v_mid2, vout_delay)
                    delay_results = self.verification_manager.verify_delay_effect(time_delay, vin_delay, v_mid1, v_mid2, vout_delay)
                    self.results['delay_effect'] = delay_results
                
                # 4. Power dissipation analysis
                time_27c, power_27c = self.data_reader.read_power_dissipation_data(temperature=27)
                time_100c, power_100c = self.data_reader.read_power_dissipation_data(temperature=100)
                if all(x is not None for x in [time_27c, power_27c, time_100c, power_100c]):
                    plot_generator.plot_power_dissipation(time_27c, power_27c, time_100c, power_100c)
                    power_results = self.verification_manager.verify_power_dissipation(time_27c, power_27c, time_100c, power_100c)
                    self.results['power_dissipation'] = power_results
                    
                    # Read and plot energy consumption data
                    time_27c_energy, energy_27c = self.data_reader.read_energy_consumption_data(temperature=27)
                    time_100c_energy, energy_100c = self.data_reader.read_energy_consumption_data(temperature=100)
                    if all(x is not None for x in [time_27c_energy, energy_27c, time_100c_energy, energy_100c]):
                        plot_generator.plot_energy_consumption(time_27c_energy, energy_27c, time_100c_energy, energy_100c)
                
                # 5. Quasi-static analysis
                time_qs, vgate_qs, vdrain_qs, idrain_qs = self.data_reader.read_quasi_static_data()
                if all(x is not None for x in [time_qs, vgate_qs, vdrain_qs, idrain_qs]):
                    plot_generator.plot_quasi_static(time_qs, vgate_qs, vdrain_qs, idrain_qs)
                    qs_results = self.verification_manager.verify_quasi_static(time_qs, vgate_qs, vdrain_qs, idrain_qs)
                    self.results['quasi_static'] = qs_results
            
            if 'noise' in modes:
                # Read and verify noise analysis data
                
                # 1. Thermal noise
                thermal_freq, thermal_noise, thermal_temp, thermal_temps = self.data_reader.read_thermal_noise_data()
                # 2. Flicker noise
                flicker_freq, flicker_noise = self.data_reader.read_flicker_noise_data()
                # 3. Shot noise
                shot_freq, shot_noise = self.data_reader.read_shot_noise_data()
                # 4. Temperature-dependent noise
                temps, temp_noise = self.data_reader.read_temperature_noise_data()
                
                if all(x is not None for x in [thermal_freq, thermal_noise, flicker_freq, flicker_noise]):
                    # Plot noise spectra individually
                    plot_generator.plot_noise_spectrum(thermal_freq, thermal_noise, 
                                                   'Thermal Noise Spectrum', 'thermal_noise')
                    plot_generator.plot_noise_spectrum(flicker_freq, flicker_noise, 
                                                   'Flicker Noise Spectrum', 'flicker_noise')
                    
                    if shot_freq is not None and shot_noise is not None:
                        plot_generator.plot_noise_spectrum(shot_freq, shot_noise,
                                                      'Shot Noise Spectrum', 'shot_noise')
                    
                    # Plot thermal noise comparison
                    thermal_data_dict = self.data_reader.read_all_thermal_noise_data()
                    if thermal_data_dict and len(thermal_data_dict) > 1:
                        plot_generator.plot_multiple_noise_spectra(
                            thermal_data_dict, 
                            'Thermal Noise vs. Bias Conditions', 
                            'thermal_noise_vds_comparison'
                        )
                    
                    # Plot all components together
                    plot_generator.plot_noise_components(thermal_freq, thermal_noise, 
                                                     flicker_noise, shot_noise if shot_noise is not None else None)
                    
                    # Plot temperature dependence if available
                    if temps is not None and temp_noise is not None:
                        plot_generator.plot_noise_vs_temperature(temps, temp_noise)
                    
                    # Verify noise analysis results
                    noise_results = self.verification_manager.verify_noise_analysis(
                        thermal_freq, thermal_data_dict if thermal_data_dict and len(thermal_data_dict) > 0 else thermal_noise, 
                        flicker_noise, shot_noise, temp_noise, temps)
                    self.results['noise_analysis'] = noise_results
            
            # Update verification checklist
            self.verification_manager.update_verification_checklist(self.results, modes=modes)
            exit()
            self.logger.logger.info("MOSFET simulation and analysis completed successfully")
            return True
            
        except Exception as e:
            self.logger.logger.error(f"Error in MOSFET simulation: {e}")
            import traceback
            traceback.print_exc()
            return False

def parse_args():
    parser = argparse.ArgumentParser(description='MOSFET Simulation and Analysis')
    parser.add_argument('--mode', type=str, nargs='+', default=['all'],
                        choices=['all', 'dc', 'transient', 'ac', 'noise'],
                        help='Simulation modes to run (default: all). Can specify multiple modes.')
    parser.add_argument('--dc-circuit', type=str, default='netlists/dc_circuit.cir',
                        help='Path to DC circuit file (default: netlists/dc_circuit.cir)')
    parser.add_argument('--transient-circuit', type=str, default='netlists/transient_circuit.cir',
                        help='Path to transient circuit file (default: netlists/transient_circuit.cir)')
    parser.add_argument('--noise-circuit', type=str, default='netlists/noise_circuit.cir',
                        help='Path to noise circuit file (default: netlists/noise_circuit.cir)')
    parser.add_argument('--ac-circuit', type=str, default='netlists/ac_circuit.cir',
                        help='Path to AC circuit file (default: netlists/ac_circuit.cir)')
    parser.add_argument('--output-dir', type=str, default='results',
                        help='Output directory (default: results)')
    parser.add_argument('--dpi', type=int, default=300,
                        help='DPI for output plots (default: 300)')
    parser.add_argument('--log-level', type=str, default='INFO',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='Logging level (default: INFO)')
    
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Convert 'all' to list of all modes
    if 'all' in args.mode:
        args.mode = ['dc', 'transient', 'ac', 'noise']
    
    simulation = MOSFETSimulation(
        dc_circuit_file=args.dc_circuit,
        transient_circuit_file=args.transient_circuit,
        noise_circuit_file=args.noise_circuit,
        ac_circuit_file=args.ac_circuit,
        output_dir=args.output_dir,
        dpi=args.dpi,
        log_level=args.log_level
    )
    
    # Pass modes to run method
    success = simulation.run(modes=args.mode)
    
    if success:
        print("MOSFET simulation and analysis completed successfully.")
    else:
        print("MOSFET simulation and analysis failed.")
        sys.exit(1)

if __name__ == "__main__":
    main() 