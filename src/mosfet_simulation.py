import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
import numpy as np

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
                 output_dir='results', dpi=300, log_level='INFO'):
        # Store the circuit file paths directly
        self.dc_circuit_file = dc_circuit_file
        self.transient_circuit_file = transient_circuit_file
        self.noise_circuit_file = noise_circuit_file
        
        # Use the DC circuit as the reference circuit for directory paths
        self.circuit_dir = os.path.dirname(dc_circuit_file)
        
        self.output_dir = output_dir
        self.dpi = dpi
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize components
        self.logger = Logger(log_level=log_level)
        self.simulation_runner = SimulationRunner(
            self.logger, 
            output_dir,
            dc_circuit_file=self.dc_circuit_file,
            transient_circuit_file=self.transient_circuit_file,
            noise_circuit_file=self.noise_circuit_file
        )
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
            'charge_conservation': None,
            # Add noise analysis results
            'noise_analysis': None
        }

    def run(self):
        """Run the MOSFET simulation and analysis."""
        try:
            self.logger.logger.info("Starting MOSFET simulation and analysis")
            
            # Create plot generator and data reader
            plot_generator = PlotGenerator(self.output_dir, self.dpi, self.logger)
            self.data_reader = DataReader(self.logger, self.output_dir)
            self.verification_manager = VerificationManager(self.logger, self.output_dir)
            
            # Initialize simulation runner with the circuit files
            self.simulation_runner = SimulationRunner(
                self.logger, 
                self.output_dir,
                dc_circuit_file=self.dc_circuit_file,
                transient_circuit_file=self.transient_circuit_file,
                noise_circuit_file=self.noise_circuit_file
            )
            
            # Verify circuit files exist
            for circ_file, circ_type in [
                (self.dc_circuit_file, "DC"),
                (self.transient_circuit_file, "Transient"),
                (self.noise_circuit_file, "Noise")
            ]:
                if not os.path.exists(circ_file):
                    self.logger.logger.error(f"{circ_type} circuit file not found: {circ_file}")
                    return False
                    
            # Run all simulations (DC, transient, and noise) sequentially
            if not self.simulation_runner.run_all_simulations():
                self.logger.logger.error("SPICE simulation failed")
                return False
            
            # Verify circuit files
            setup_results = {}
            for circ_file, circ_type in [
                (self.dc_circuit_file, "DC"),
                (self.transient_circuit_file, "Transient"),
                (self.noise_circuit_file, "Noise")
            ]:
                result = self.verification_manager.verify_simulation_setup(circ_file)
                setup_results[f"{circ_type.lower()}_netlist_exists"] = result['netlist_exists']
                setup_results[f"{circ_type.lower()}_details"] = result['details']
            
            # Store common ngspice verification
            setup_results["ngspice_installed"] = self.verification_manager.verify_simulation_setup(
                self.dc_circuit_file)['ngspice_installed']
            setup_results["details"] = {"netlist_path": "multiple files"} 
            self.results['simulation_setup'] = setup_results
            
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
            
            # 7. Noise analysis
            self.logger.logger.info("Performing noise analysis")
            
            # Get thermal noise data for different bias points
            thermal_noise_data = {}
            thermal_noise_data_dict = self.data_reader.read_all_thermal_noise_data()
            for bias_key, (freq, noise) in thermal_noise_data_dict.items():
                if freq is not None and noise is not None:
                    thermal_noise_data[bias_key] = noise
            
            # Get flicker noise data
            freq_flicker, flicker_noise = self.data_reader.read_flicker_noise_data()
            
            # Get shot noise data
            freq_shot, shot_noise = self.data_reader.read_shot_noise_data()
            
            # Get temperature noise data
            temps, temp_noise_data = self.data_reader.read_temperature_noise_data()
            
            # Process noise data for temperature dependence
            temp_noise = {}
            if temps is not None and temp_noise_data is not None:
                for temp in temps:
                    freq_temp, noise_temp = temp_noise_data[temp]
                    temp_noise[temp] = noise_temp
            
            # Plot noise data if available
            if thermal_noise_data:
                # Generate plot of thermal noise at different bias points
                bias_data = {}
                for key, (freq, noise) in thermal_noise_data_dict.items():
                    bias_data[key] = (freq, noise)
                
                plot_generator.plot_multiple_noise_spectra(
                    bias_data, 
                    "Thermal Noise vs Bias Conditions", 
                    "thermal_noise_vds_comparison"
                )
            
            if freq_flicker is not None and flicker_noise is not None:
                # Generate flicker noise plot
                plot_generator.plot_noise_spectrum(
                    freq_flicker, 
                    flicker_noise, 
                    "Flicker (1/f) Noise Analysis", 
                    "flicker_noise"
                )
            
            if freq_shot is not None and shot_noise is not None:
                # Generate shot noise plot
                plot_generator.plot_noise_spectrum(
                    freq_shot, 
                    shot_noise, 
                    "Shot Noise Analysis", 
                    "shot_noise"
                )
            
            if temps is not None and temp_noise_data is not None:
                # Extract average noise level at each temperature for plotting
                avg_noise_levels = []
                for temp in temps:
                    freq_temp, noise_temp = temp_noise_data[temp]
                    avg_noise_levels.append(np.mean(noise_temp))
                
                # Generate temperature dependence plot
                plot_generator.plot_noise_vs_temperature(
                    temps, 
                    avg_noise_levels, 
                    "Noise vs Temperature"
                )
            
            # Generate composite noise components plot if all components are available
            if (freq_flicker is not None and flicker_noise is not None and
                freq_shot is not None and shot_noise is not None and
                thermal_noise_data_dict):
                # Take the thermal noise from one bias point as reference
                first_bias = list(thermal_noise_data_dict.keys())[0]
                freq_thermal, thermal_noise_sample = thermal_noise_data_dict[first_bias]
                
                # Only create plot if frequencies match
                if (len(freq_thermal) == len(freq_flicker) == len(freq_shot) and
                    np.allclose(freq_thermal, freq_flicker) and np.allclose(freq_thermal, freq_shot)):
                    plot_generator.plot_noise_components(
                        freq_thermal, 
                        thermal_noise_sample, 
                        flicker_noise, 
                        shot_noise
                    )
            
            # Verify noise analysis data
            freq_to_use = None
            if freq_flicker is not None:
                freq_to_use = freq_flicker
            elif freq_shot is not None:
                freq_to_use = freq_shot
            elif thermal_noise_data_dict:
                # Take frequency array from the first thermal noise dataset
                first_bias = list(thermal_noise_data_dict.keys())[0]
                freq_to_use, _ = thermal_noise_data_dict[first_bias]
            
            # Call verification manager to verify noise analysis
            noise_results = self.verification_manager.verify_noise_analysis(
                freq=freq_to_use,
                thermal_noise=thermal_noise_data if thermal_noise_data else None,
                flicker_noise=flicker_noise if freq_flicker is not None else None,
                shot_noise=shot_noise if freq_shot is not None else None,
                temp_noise=temp_noise if temps is not None else None,
                temperatures=temps
            )
            self.results['noise_analysis'] = noise_results
            
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
    
    # Circuit file options
    circuit_group = parser.add_argument_group('Circuit Files')
    circuit_group.add_argument('--dc-circuit', type=str, default='netlists/dc_circuit.cir',
                      help='Path to the DC analysis circuit file (default: netlists/dc_circuit.cir)')
    circuit_group.add_argument('--transient-circuit', type=str, default='netlists/transient_circuit.cir',
                      help='Path to the transient analysis circuit file (default: netlists/transient_circuit.cir)')
    circuit_group.add_argument('--noise-circuit', type=str, default='netlists/noise_circuit.cir',
                      help='Path to the noise analysis circuit file (default: netlists/noise_circuit.cir)')
    
    # Other options
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
        dc_circuit_file=args.dc_circuit,
        transient_circuit_file=args.transient_circuit,
        noise_circuit_file=args.noise_circuit,
        output_dir=args.output_dir,
        dpi=args.dpi,
        log_level=args.log_level
    )
    
    if not simulation.run():
        sys.exit(1)

if __name__ == "__main__":
    main() 