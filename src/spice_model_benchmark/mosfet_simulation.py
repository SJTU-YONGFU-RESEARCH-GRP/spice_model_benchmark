import os
import sys
import argparse
import json
from pathlib import Path
from datetime import datetime
import numpy as np
from scipy import integrate

from .logger import Logger
from .simulation_runner import SimulationRunner
from .data_reader import DataReader
from .plot_generator import PlotGenerator
from .verification_manager import VerificationManager

class MOSFETSimulation:
    """Main class for MOSFET simulation and verification.
    
    This class handles the complete MOSFET simulation workflow including:
    - Simulation setup and execution
    - DC, AC, Noise and Transient analysis
    - Results verification and reporting
    """
    def __init__(self, dc_circuit_file, transient_circuit_file, noise_circuit_file, 
                 ac_circuit_file, output_dir='results', dpi=300, log_level='INFO'):

        # Store the circuit file paths directly
        self.dc_circuit_file = dc_circuit_file
        self.transient_circuit_file = transient_circuit_file
        self.noise_circuit_file = noise_circuit_file
        self.ac_circuit_file = ac_circuit_file
                
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
            'dc_operating_point_analysis': None,
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
            'large_signal_caps': None,
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
            self.logger.info("Starting MOSFET simulation and analysis")
            
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
                    self.logger.error(f"{circ_type} circuit file not found: {circ_file}")
                    return False
            
            # Run simulations based on selected modes
            if not self.simulation_runner.run_simulations_by_mode(modes):
                self.logger.error("SPICE simulation failed")
                return False
            
            # Verify circuit files
            self.logger.info("Verifying simulation setup")
            setup_results = {}

            # Do a single verification for ngspice and DC circuit
            self.logger.info("Verifying ngspice installation and DC circuit setup")
            dc_result = self.verification_manager.verify_simulation_setup(self.dc_circuit_file)
            setup_results["ngspice_installed"] = dc_result['ngspice_installed']
            setup_results["dc_netlist_exists"] = dc_result['netlist_exists']
            setup_results["dc_details"] = dc_result['details']

            # Verify other circuit files if they exist
            for circ_file, circ_type in circuit_files:
                if circ_file != self.dc_circuit_file:  # Skip DC circuit as it's already verified
                    self.logger.info(f"Verifying {circ_type} circuit setup")
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
                v_ds, v_gs, i_ds, i_g, i_s, i_b, power = self.data_reader.read_dc_iv_data(self.output_dir)

                # Read temperature                 
                temp = self.data_reader.read_dc_temperature_data(self.output_dir)

                # Read bias point data
                bias_vds, bias_vgs, bias_ids, bias_ig, bias_is, bias_ib = self.data_reader.read_dc_bias_point_data(self.output_dir)

                # Verify DC Operating Point Analysis
                if v_ds is not None and v_gs is not None and i_ds is not None:
                    plot_generator.plot_dc_iv_characteristics(self.output_dir, v_ds, v_gs, i_ds)
                    # Store IV characteristics data in results
                    self.results['dc_operating_point_analysis'] = {
                        'data_ready': True,
                        'vds_range': f"{min(v_ds):.2f}V to {max(v_ds):.2f}V" if v_ds is not None else "Not available",
                        'vgs_range': f"{min(v_gs):.2f}V to {max(v_gs):.2f}V" if v_gs is not None else "Not available",
                        'ids_range': f"{min(i_ds):.2e}A to {max(i_ds):.2e}A" if i_ds is not None else "Not available",
                        'details': {
                            'v_ds': v_ds.tolist() if v_ds is not None else None,
                            'v_gs': v_gs.tolist() if v_gs is not None else None,
                            'i_ds': i_ds.tolist() if i_ds is not None else None,
                            'i_g': i_g.tolist() if i_g is not None else None,
                            'i_s': i_s.tolist() if i_s is not None else None,
                            'i_b': i_b.tolist() if i_b is not None else None
                        }
                    }
                                    
                if all(x is not None for x in [i_ds, i_g, i_s, i_b]):
                    plot_generator.plot_dc_kcl_verification(self.output_dir, i_ds, i_g, i_s, i_b)
                
                dc_operating_point_result = self.verification_manager.verify_dc_operating_point_analysis(v_ds, v_gs, i_ds, i_g, i_s, i_b, temp)
                if not dc_operating_point_result['data_ready']:
                    raise ValueError("DC Operating Point Analysis failed")
                self.results['dc_operating_point_analysis'] = dc_operating_point_result

                # Verify bias point analysis
                bias_results = self.verification_manager.verify_bias_point_analysis(
                    bias_vds, bias_vgs, bias_ids, bias_ig, bias_is, bias_ib, temp[0] if temp is not None else 27
                )
                self.results['bias_point_analysis'] = bias_results

                # Verify temperature analysis
                if temp is not None and i_ds is not None:
                    plot_generator.plot_dc_temperature_analysis(self.output_dir, temp, i_ds)

                temp_results = self.verification_manager.verify_temperature_analysis(temp, i_ds)
                if not temp_results['temp_sweep'] or not temp_results['device_behavior']:
                    raise ValueError("Temperature analysis verification failed")
                self.results['temperature_analysis'] = temp_results
                
                # Calculate power for thermodynamic analysis
                power = np.abs(v_ds * i_ds) if v_ds is not None and i_ds is not None else None
                thermo_results = self.verification_manager.verify_thermodynamic_analysis(power, temp, i_ds)
                if not thermo_results['power_measurements']:
                    raise ValueError("Power measurements verification failed")
                self.results['thermodynamic_analysis'] = thermo_results
            
            if 'ac' in modes:
                # Read AC data files
                vg, cv_ig, cv_is, cv_ib, cgg = self.data_reader.read_cv_data(self.output_dir)
                cm_vg, c_matrix = self.data_reader.read_capacitance_matrix_data(self.output_dir)
                freq, s11_mag, s11_phase, s12_mag, s12_phase, s21_mag, s21_phase, s22_mag, s22_phase = self.data_reader.read_sparameter_data(self.output_dir)
                nqs_freq, vg_phase, id_phase, phase_diff = self.data_reader.read_nqs_effects_data(self.output_dir)
                time, vg, ig, id, is_, ib = self.data_reader.read_charge_conservation_data(self.output_dir)

                # AC-integral large-signal capacitance extraction (from cv_data.txt columnar table)
                try:
                    vg_cv, caps_cv = self.data_reader.read_cv_table_data(self.output_dir, freq_tag="1MHz")
                    if vg_cv is not None and caps_cv is not None:
                        vg_cv = np.asarray(vg_cv, dtype=float)
                        order = np.argsort(vg_cv)
                        vg_sorted = vg_cv[order]
                        dv = float(vg_sorted[-1] - vg_sorted[0]) if vg_sorted.size >= 2 else 0.0

                        def _ls_cap_from_cv(cap_arr: np.ndarray) -> float:
                            cap_sorted = np.asarray(cap_arr, dtype=float)[order]
                            if vg_sorted.size < 2 or dv == 0.0:
                                return float('nan')
                            q = float(np.trapezoid(cap_sorted, vg_sorted))
                            return q / dv

                        ls_caps_f = {name: _ls_cap_from_cv(arr) for name, arr in caps_cv.items()}

                        # Also compute cumulative Qg(Vg) if Cgg available
                        qg_c = None
                        if "Cgg" in caps_cv:
                            cgg_sorted = np.asarray(caps_cv["Cgg"], dtype=float)[order]
                            qg = np.zeros_like(vg_sorted, dtype=float)
                            for i in range(1, vg_sorted.size):
                                dv_i = vg_sorted[i] - vg_sorted[i - 1]
                                qg[i] = qg[i - 1] + 0.5 * (cgg_sorted[i] + cgg_sorted[i - 1]) * dv_i
                            qg_c = qg

                        # Persist to <out>/data/
                        data_dir = Path(self.output_dir) / "data"
                        data_dir.mkdir(parents=True, exist_ok=True)

                        summary_path = data_dir / "ac_ls_caps_from_cv_integral.csv"
                        with open(summary_path, "w", encoding="utf-8") as f:
                            f.write("cap,ac_int_F,ac_int_fF\n")
                            for cap_name in ["Cgg", "Cgs", "Cgd", "Cgb"]:
                                if cap_name in ls_caps_f:
                                    v = float(ls_caps_f[cap_name])
                                    f.write(f"{cap_name},{v:.16g},{v*1e15:.12g}\n")
                            f.write(f"Vg_start,{vg_sorted[0]:.16g},\n")
                            f.write(f"Vg_stop,{vg_sorted[-1]:.16g},\n")
                            f.write(f"dVg,{dv:.16g},\n")

                        if qg_c is not None:
                            q_path = data_dir / "ac_qg_from_cv_integral.csv"
                            with open(q_path, "w", encoding="utf-8") as f:
                                f.write("Vg,Qg_C\n")
                                for v, q in zip(vg_sorted.tolist(), qg_c.tolist()):
                                    f.write(f"{v:.16g},{q:.16g}\n")

                        self.results['ac_integrated_large_signal_caps'] = {
                            'data_ready': True,
                            'freq_tag': '1MHz',
                            'vg_start': float(vg_sorted[0]),
                            'vg_stop': float(vg_sorted[-1]),
                            'dv': dv,
                            'ls_caps_f': {k: float(v) for k, v in ls_caps_f.items()},
                            'outputs': {
                                'summary_csv': str(summary_path.relative_to(self.output_dir)),
                                'qg_csv': str((data_dir / 'ac_qg_from_cv_integral.csv').relative_to(self.output_dir)) if qg_c is not None else None,
                            },
                        }
                except Exception as e:
                    self.logger.warning(f"AC-integral LS cap extraction skipped: {e}")
                
                # Generate CV plots
                if vg is not None and cgg is not None:
                    plot_generator.plot_ac_cv_characteristics(self.output_dir)
                    # Store CV characteristics data in results
                    self.results['cv_characteristics'] = {
                        'data_ready': True,
                        'vg_range': f"{min(vg):.2f}V to {max(vg):.2f}V" if vg is not None else "Not available",
                        'cgg_range': f"{min(cgg):.2e}F to {max(cgg):.2e}F" if cgg is not None else "Not available",
                        'freq_range': f"{min(freq):.2e}Hz to {max(freq):.2e}Hz" if freq is not None else "Not available",
                        'details': {
                            'vg': vg.tolist() if vg is not None else None,
                            'cgg': cgg.tolist() if cgg is not None else None,
                            'freq': freq.tolist() if freq is not None else None,
                            'vg_phase': vg_phase.tolist() if vg_phase is not None else None,
                            'id_phase': id_phase.tolist() if id_phase is not None else None
                        }
                    }

                # Store full 4x4 small-signal capacitance matrix (if available)
                if cm_vg is not None and c_matrix is not None:
                    self.results['capacitance_matrix'] = {
                        'data_ready': True,
                        'terminal_order': ['g', 'd', 's', 'b'],
                        'definition': 'I = j*omega*C*V, so C_ij = -Im(Y_ij)/omega',
                        'vg': cm_vg.tolist(),
                        'c_matrix': c_matrix.tolist(),
                    }
                
                # Generate S-parameter plots
                if all(x is not None for x in [freq, s11_mag, s21_mag, s12_mag, s22_mag]):
                    plot_generator.plot_ac_sparameter_analysis(self.output_dir, freq, s11_mag, s21_mag, s12_mag, s22_mag)
                    # Store S-parameter data in results
                    self.results['sparameter_analysis'] = {
                        'data_ready': True,
                        'freq_range': f"{min(freq):.2e}Hz to {max(freq):.2e}Hz" if freq is not None else "Not available",
                        's11_range': f"{min(s11_mag):.2e} to {max(s11_mag):.2e}" if s11_mag is not None else "Not available",
                        's21_range': f"{min(s21_mag):.2e} to {max(s21_mag):.2e}" if s21_mag is not None else "Not available",
                        'isolation': f"{min(s12_mag):.2e} to {max(s12_mag):.2e}" if s12_mag is not None else "Not available",
                        'details': {
                            'freq': freq.tolist() if freq is not None else None,
                            's11_mag': s11_mag.tolist() if s11_mag is not None else None,
                            's21_mag': s21_mag.tolist() if s21_mag is not None else None,
                            's12_mag': s12_mag.tolist() if s12_mag is not None else None,
                            's22_mag': s22_mag.tolist() if s22_mag is not None else None
                        }
                    }
                
                # Generate NQS effects plots
                if all(x is not None for x in [nqs_freq, vg_phase, id_phase, phase_diff]):
                    plot_generator.plot_ac_nqs_effects(self.output_dir, nqs_freq, vg_phase, id_phase, phase_diff)
                    # Store NQS effects data in results
                    self.results['nqs_effects'] = {
                        'data_ready': True,
                        'max_phase_shift': f"{max(phase_diff):.2f}°" if phase_diff is not None else "Not available",
                        'freq_range': f"{min(nqs_freq):.2e}Hz to {max(nqs_freq):.2e}Hz" if nqs_freq is not None else "Not available",
                        'details': {
                            'freq': nqs_freq.tolist() if nqs_freq is not None else None,
                            'vg_phase': vg_phase.tolist() if vg_phase is not None else None,
                            'id_phase': id_phase.tolist() if id_phase is not None else None,
                            'phase_diff': phase_diff.tolist() if phase_diff is not None else None
                        }
                    }
                
                # Read charge conservation data
                if time is not None:
                    # Calculate total current and integrated charge
                    i_total = ig + id + is_ + ib

                    # Integrate currents to get charges - use numpy.cumsum with trapezoidal weights
                    q_gate = np.zeros_like(ig)
                    q_drain = np.zeros_like(id)
                    q_source = np.zeros_like(is_)
                    q_bulk = np.zeros_like(ib)
                    for i in range(1, len(time)):
                        q_gate[i] = q_gate[i-1] + 0.5 * (ig[i] + ig[i-1]) * (time[i] - time[i-1])
                        q_drain[i] = q_drain[i-1] + 0.5 * (id[i] + id[i-1]) * (time[i] - time[i-1])
                        q_source[i] = q_source[i-1] + 0.5 * (is_[i] + is_[i-1]) * (time[i] - time[i-1])
                        q_bulk[i] = q_bulk[i-1] + 0.5 * (ib[i] + ib[i-1]) * (time[i] - time[i-1])
                    q_total = q_gate + q_drain + q_source + q_bulk

                    # Generate charge conservation plots
                    self.plot_generator.plot_ac_charge_conservation(self.output_dir, time, vg, ig, id, is_, ib, i_total, q_gate, q_drain, q_source, q_bulk, q_total)
                    # Verify charge conservation
                    charge_results = self.verification_manager.verify_ac_charge_conservation(time, vg, ig, id, is_, ib, i_total, q_gate, q_drain, q_source, q_bulk, q_total)
                    # Calculate conservation error as in reference
                    conservation_error = np.max(np.abs(q_total - q_total[0])) / np.max(np.abs(q_total)) * 100 if np.max(np.abs(q_total)) != 0 else 0.0
                    self.results['charge_conservation'] = {
                        **charge_results,
                        'conservation_error': f"{conservation_error:.16f}%"
                    }
                
                # Verify CV characteristics
                if vg is not None and cgg is not None:
                    cgg_min = np.min(cgg)
                    cgg_max = np.max(cgg)
                    max_idx = np.argmax(cgg)
                    max_vg = vg[max_idx]
                    cv_results = self.verification_manager.verify_cv_characteristics(vg, cgg, freq, vg_phase, id_phase)
                    if not cv_results['data_ready']:
                        raise ValueError("CV characteristics verification failed")
                        
                    # Get charge conservation error if available
                    cc_error = self.results.get('charge_conservation', {}).get('conservation_error', None)
                    if cc_error is not None:
                        cv_results['charge_conservation_error'] = cc_error
                    else:
                        cv_results['charge_conservation_error'] = "N/A%"

                    self.results['cv_characteristics'] = {
                        **cv_results,
                        'cgg_range': f"{cgg_min*1e15:.2f}fF to {cgg_max*1e15:.2f}fF",
                        'max_value_at': f"{max_vg:.2f}V",
                        'freq_range': f"{min(freq):.2e}Hz to {max(freq):.2e}Hz" if freq is not None and len(freq) > 0 else "N/A"
                    }
                # Verify S-parameter analysis
                if all(x is not None for x in [freq, s11_mag, s21_mag, s12_mag, s22_mag]):
                    sparam_results = self.verification_manager.verify_sparameter_analysis(freq, s11_mag, s21_mag, s12_mag, s22_mag)
                    if not sparam_results['data_ready']:
                        raise ValueError("S-parameter analysis verification failed")
                    self.results['sparameter_analysis'] = sparam_results
                
                # Verify NQS effects
                if all(x is not None for x in [nqs_freq, vg_phase, id_phase, phase_diff]):
                    nqs_results = self.verification_manager.verify_nqs_effects(nqs_freq, vg_phase, id_phase, phase_diff)
                    if not nqs_results['data_ready']:
                        raise ValueError("NQS effects verification failed")
                    self.results['nqs_effects'] = nqs_results
            
            if 'transient' in modes:
                # Read and verify transient analysis data
                
                # 1. Large signal transient analysis
                time_ls, vgate_ls, vdrain_ls, idrain_ls = self.data_reader.read_trans_large_signal_transient_data(self.output_dir)

                if all(x is not None for x in [time_ls, vgate_ls, vdrain_ls, idrain_ls]):
                    plot_generator.plot_trans_large_signal_transient(self.output_dir, time_ls, vgate_ls, vdrain_ls, idrain_ls)
                    ls_results = self.verification_manager.verify_trans_large_signal_transient(time_ls, vgate_ls, vdrain_ls, idrain_ls)
                    self.results['large_signal_transient'] = ls_results
                
                # 2. Switching response analysis
                time_sw, vin_sw, vout_sw, idrain_sw = self.data_reader.read_trans_switching_response_data(self.output_dir)
                time_sw_pwr, power_sw = self.data_reader.read_trans_switching_power_data(self.output_dir)
                
                if all(x is not None for x in [time_sw, vin_sw, vout_sw, idrain_sw, time_sw_pwr, power_sw]):
                    plot_generator.plot_trans_switching_response(self.output_dir, time_sw, vin_sw, vout_sw, idrain_sw, power_sw)
                    sw_results = self.verification_manager.verify_trans_switching_simulations(
                        time_sw, vin_sw, vout_sw, idrain_sw, power_sw
                    )
                    self.results['switching_simulations'] = sw_results
                
                # 3. Delay effect analysis
                time_delay, vin_delay, v_mid1, v_mid2, vout_delay = self.data_reader.read_trans_delay_effect_data(self.output_dir)
                if all(x is not None for x in [time_delay, vin_delay, v_mid1, v_mid2, vout_delay]):
                    plot_generator.plot_trans_delay_effect(self.output_dir, time_delay, vin_delay, v_mid1, v_mid2, vout_delay)
                    delay_results = self.verification_manager.verify_trans_delay_effect(time_delay, vin_delay, v_mid1, v_mid2, vout_delay)
                    self.results['delay_effect'] = delay_results
                
                # 4. Power dissipation analysis
                time_27c, power_27c = self.data_reader.read_trans_power_dissipation_data(self.output_dir, temperature=27)
                time_100c, power_100c = self.data_reader.read_trans_power_dissipation_data(self.output_dir, temperature=100)
                if all(x is not None for x in [time_27c, power_27c, time_100c, power_100c]):
                    plot_generator.plot_trans_power_dissipation(self.output_dir, time_27c, power_27c, time_100c, power_100c)
                    power_results = self.verification_manager.verify_trans_power_dissipation(time_27c, power_27c, time_100c, power_100c)
                    self.results['power_dissipation'] = power_results
                    
                    # Read and plot energy consumption data
                    time_27c_energy, energy_27c = self.data_reader.read_trans_energy_consumption_data(self.output_dir, temperature=27)
                    time_100c_energy, energy_100c = self.data_reader.read_trans_energy_consumption_data(self.output_dir, temperature=100)
                    if all(x is not None for x in [time_27c_energy, energy_27c, time_100c_energy, energy_100c]):
                        plot_generator.plot_trans_energy_consumption(self.output_dir, time_27c_energy, energy_27c, time_100c_energy, energy_100c)
                
                # 5. Quasi-static analysis
                time_qs, vgate_qs, vdrain_qs, idrain_qs = self.data_reader.read_trans_quasi_static_data(self.output_dir)
                if all(x is not None for x in [time_qs, vgate_qs, vdrain_qs, idrain_qs]):
                    plot_generator.plot_trans_quasi_static(self.output_dir, time_qs, vgate_qs, vdrain_qs, idrain_qs)
                    qs_results = self.verification_manager.verify_trans_quasi_static(time_qs, vgate_qs, vdrain_qs, idrain_qs)
                    self.results['quasi_static'] = qs_results

                # 6. Large-signal capacitance extraction from transient charge test (gate step)
                time_cap, vg_cap, ig_cap, id_cap, is_cap, ib_cap = self.data_reader.read_trans_charge_conservation_data(self.output_dir)
                if all(x is not None for x in [time_cap, vg_cap, ig_cap, id_cap, is_cap, ib_cap]):
                    # Integrate terminal currents to obtain terminal charges
                    qg = np.zeros_like(ig_cap)
                    qd = np.zeros_like(id_cap)
                    qs = np.zeros_like(is_cap)
                    qb = np.zeros_like(ib_cap)
                    for i_idx in range(1, len(time_cap)):
                        dt = time_cap[i_idx] - time_cap[i_idx - 1]
                        qg[i_idx] = qg[i_idx - 1] + 0.5 * (ig_cap[i_idx] + ig_cap[i_idx - 1]) * dt
                        qd[i_idx] = qd[i_idx - 1] + 0.5 * (id_cap[i_idx] + id_cap[i_idx - 1]) * dt
                        qs[i_idx] = qs[i_idx - 1] + 0.5 * (is_cap[i_idx] + is_cap[i_idx - 1]) * dt
                        qb[i_idx] = qb[i_idx - 1] + 0.5 * (ib_cap[i_idx] + ib_cap[i_idx - 1]) * dt

                    # Estimate VDD from gate voltage waveform
                    vdd_est = float(np.max(vg_cap)) if vg_cap is not None else 0.0
                    if vdd_est > 0.0:
                        v_low_thr = 0.1 * vdd_est
                        v_high_thr = 0.9 * vdd_est

                        # Rising edge: 0 -> VDD
                        low_indices = np.where(vg_cap <= v_low_thr)[0]
                        high_indices = np.where(vg_cap >= v_high_thr)[0]
                        if low_indices.size > 0 and high_indices.size > 0:
                            i_start = low_indices[0]
                            i_end = high_indices[0]
                            dv = vg_cap[i_end] - vg_cap[i_start]
                            if abs(dv) > 0.0:
                                cgs_rise = -(qs[i_end] - qs[i_start]) / dv
                                cgd_rise = -(qd[i_end] - qd[i_start]) / dv
                                cgb_rise = -(qb[i_end] - qb[i_start]) / dv
                            else:
                                cgs_rise = cgd_rise = cgb_rise = None
                        else:
                            cgs_rise = cgd_rise = cgb_rise = None

                        # Falling edge: VDD -> 0
                        low_indices_end = np.where(vg_cap <= v_low_thr)[0]
                        high_indices_end = np.where(vg_cap >= v_high_thr)[0]
                        if low_indices_end.size > 0 and high_indices_end.size > 0:
                            i_start_fall = high_indices_end[-1]
                            i_end_fall = low_indices_end[-1]
                            if i_end_fall > i_start_fall:
                                dv_fall = vg_cap[i_end_fall] - vg_cap[i_start_fall]
                                if abs(dv_fall) > 0.0:
                                    cgs_fall = -(qs[i_end_fall] - qs[i_start_fall]) / dv_fall
                                    cgd_fall = -(qd[i_end_fall] - qd[i_start_fall]) / dv_fall
                                    cgb_fall = -(qb[i_end_fall] - qb[i_start_fall]) / dv_fall
                                else:
                                    cgs_fall = cgd_fall = cgb_fall = None
                            else:
                                cgs_fall = cgd_fall = cgb_fall = None
                        else:
                            cgs_fall = cgd_fall = cgb_fall = None

                        # Store large-signal capacitance results (transient current-integration method)
                        self.results['large_signal_caps'] = {
                            'definition_tran': 'large-signal ΔQ/ΔV from gate step transient (0→VDD and VDD→0)',
                            'vdd_est_tran': vdd_est,
                            'cgs_rise': cgs_rise,
                            'cgd_rise': cgd_rise,
                            'cgb_rise': cgb_rise,
                            'cgs_fall': cgs_fall,
                            'cgd_fall': cgd_fall,
                            'cgb_fall': cgb_fall,
                        }

                        caps = self.results['large_signal_caps']
                        caps_file = self.output_dir / 'large_signal_caps.txt'
                        try:
                            with open(caps_file, 'w') as f:
                                # Transient current-integration method (5.2)
                                f.write("[Transient gate-step method (current integration, 5.2)]\n")
                                definition_tran = caps.get('definition_tran', '')
                                vdd_tran = caps.get('vdd_est_tran', None)
                                f.write(f"definition_tran: {definition_tran}\n")
                                f.write(f"vdd_est_tran: {vdd_tran}\n")
                                for key in ['cgs_rise', 'cgd_rise', 'cgb_rise', 'cgs_fall', 'cgd_fall', 'cgb_fall']:
                                    val = caps.get(key, None)
                                    if val is None:
                                        f.write(f"{key}: None\n")
                                    else:
                                        f.write(f"{key}: {val:.6e} F ({val*1e15:.3f} fF)\n")
                        except Exception as e:
                            self.logger.error(f"Failed to write large_signal_caps file: {e}")
            
            if 'noise' in modes:
                # Read and verify noise analysis data
                
                # 1. Thermal noise
                thermal_freq, thermal_noise, thermal_temp, thermal_temps = self.data_reader.read_thermal_noise_data(self.output_dir)
                # 2. Flicker noise
                flicker_freq, flicker_noise = self.data_reader.read_flicker_noise_data(self.output_dir)
                # 3. Shot noise
                shot_freq, shot_noise = self.data_reader.read_shot_noise_data(self.output_dir)
                # 4. Temperature-dependent noise
                temps, temp_noise = self.data_reader.read_temperature_noise_data(self.output_dir)
                
                if all(x is not None for x in [thermal_freq, thermal_noise, flicker_freq, flicker_noise]):
                    # Plot noise spectra individually
                    plot_generator.plot_noise_spectrum(self.output_dir, thermal_freq, thermal_noise, 
                                                   'Thermal Noise Spectrum', 'noise_thermal_noise')
                    plot_generator.plot_noise_spectrum(self.output_dir, flicker_freq, flicker_noise, 
                                                   'Flicker Noise Spectrum', 'noise_flicker_noise')
                    
                    if shot_freq is not None and shot_noise is not None:
                        plot_generator.plot_noise_spectrum(self.output_dir, shot_freq, shot_noise,
                                                      'Shot Noise Spectrum', 'noise_shot_noise')
                    
                    # Plot thermal noise comparison
                    thermal_data_dict = self.data_reader.read_all_thermal_noise_data(self.output_dir)
                    if thermal_data_dict and len(thermal_data_dict) > 1:
                        plot_generator.plot_multiple_noise_spectra(
                            self.output_dir, 
                            thermal_data_dict, 
                            'Thermal Noise vs. Bias Conditions', 
                            'noise_thermal_noise_vds_comparison'
                        )
                    
                    # Plot all components together
                    plot_generator.plot_noise_components(self.output_dir, thermal_freq, thermal_noise, 
                                                     flicker_noise, shot_noise if shot_noise is not None else None)
                    
                    # Plot temperature dependence if available
                    if temps is not None and temp_noise is not None:
                        plot_generator.plot_noise_vs_temperature(self.output_dir, temps, temp_noise)
                    
                    # Verify noise analysis results
                    noise_results = self.verification_manager.verify_noise_analysis(
                        thermal_freq, thermal_data_dict if thermal_data_dict and len(thermal_data_dict) > 0 else thermal_noise, 
                        flicker_noise, shot_noise, temp_noise, temps)
                    self.results['noise_analysis'] = noise_results
            
            # Update verification checklist
            self.verification_manager.update_verification_checklist(self.results, modes=modes)
            self.logger.info("MOSFET simulation and analysis completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error in MOSFET simulation: {e}")
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
        args.mode = ['dc', 'ac', 'transient', 'noise']
    
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
        print("MOSFET simulation and analysis failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 