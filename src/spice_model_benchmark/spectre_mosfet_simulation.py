"""
Spectre MOSFET Simulation coordinator.

Mirrors MOSFETSimulation class but uses SpectreRunner for simulation execution.
Reuses DataReader, PlotGenerator, and VerificationManager from the ngspice pipeline
since the post-processor generates identical text file outputs.
"""
import os
import numpy as np
from pathlib import Path
from typing import List, Optional

from .logger import Logger
from .spectre_runner import SpectreRunner
from .data_reader import DataReader
from .plot_generator import PlotGenerator
from .verification_manager import VerificationManager


class SpectreMOSFETSimulation:
    """MOSFET simulation and verification using Spectre.

    Replicates the exact same benchmark workflow as MOSFETSimulation
    but invokes the Spectre simulator. The post-processor generates
    identical text data files, so the existing DataReader/PlotGenerator/
    VerificationManager pipeline works unchanged.
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

        # Components – created here, wired inside run()
        self.logger = Logger(log_level=log_level)
        self._data_reader = DataReader(self.logger, output_dir=str(self.output_dir))
        self._plot_generator = PlotGenerator(str(self.output_dir), dpi=dpi, logger=self.logger)
        self._verification_manager = VerificationManager(self.logger, output_dir=str(self.output_dir))
        self._verification_manager.plot_generator = self._plot_generator

        self.results: dict = {}

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    def run(self, modes: Optional[List[str]] = None) -> bool:
        if modes is None:
            modes = ['dc']

        self.logger.logger.info("=" * 60)
        self.logger.logger.info("Spectre MOSFET Simulation & Verification")
        self.logger.logger.info("=" * 60)

        # ---- Phase 1: Run Spectre simulations ----
        self.logger.logger.info("Phase 1: Running Spectre simulations...")
        runner = SpectreRunner(
            self.logger,
            output_dir=str(self.output_dir),
            dc_circuit_file=self.dc_circuit_file,
            transient_circuit_file=self.transient_circuit_file,
            noise_circuit_file=self.noise_circuit_file,
            ac_circuit_file=self.ac_circuit_file,
        )
        if not runner.run_simulations_by_mode(modes):
            self.logger.logger.error("Spectre simulations failed")
            return False

        # ---- Phase 2: data → plot → verify (same pipeline as ngspice) ----
        self.logger.logger.info("Phase 2: Analysing results...")

        # Verify simulation setup
        self.results['simulation_setup'] = \
            self._verification_manager.verify_simulation_setup(self.dc_circuit_file)
        # Override the ngspice version string
        if 'details' in self.results['simulation_setup']:
            self.results['simulation_setup']['details']['ngspice_version'] = 'Spectre 24.1'

        # DC
        if 'dc' in modes:
            self._process_dc()

        # Transient
        if 'transient' in modes:
            self._process_transient()

        # AC
        if 'ac' in modes:
            self._process_ac()

        # Noise
        if 'noise' in modes:
            self._process_noise()

        # ---- Phase 3: Generate verification report ----
        self.logger.logger.info("Phase 3: Generating verification report...")
        self._verification_manager.update_verification_checklist(self.results, modes)

        self.logger.logger.info("Spectre benchmark workflow complete!")
        report_path = self.output_dir / 'REPORT.md'
        self.logger.logger.info(f"Report: {report_path}")
        return True

    # ==================================================================
    # DC processing
    # ==================================================================

    def _process_dc(self):
        """Read DC data, generate plots, and run verification."""
        self.logger.logger.info("Processing DC results...")
        out = str(self.output_dir)
        dr = self._data_reader
        pg = self._plot_generator
        vm = self._verification_manager

        try:
            # Read DC IV data  (spectre post-processor writes identical format)
            v_ds, v_gs, i_ds, i_g, i_s, i_b, power = dr.read_dc_iv_data(out)
            temp = dr.read_dc_temperature_data(out)
            bias_vds, bias_vgs, bias_ids, bias_ig, bias_is, bias_ib = \
                dr.read_dc_bias_point_data(out)

            # Plots
            if v_ds is not None and v_gs is not None and i_ds is not None:
                pg.plot_dc_iv_characteristics(out, v_ds, v_gs, i_ds)

            if all(x is not None for x in [i_ds, i_g, i_s, i_b]):
                pg.plot_dc_kcl_verification(out, i_ds, i_g, i_s, i_b)

            if temp is not None and i_ds is not None:
                pg.plot_dc_temperature_analysis(out, temp, i_ds)

            # Verification
            if v_ds is not None and v_gs is not None and i_ds is not None:
                self.results['dc_operating_point_analysis'] = \
                    vm.verify_dc_operating_point_analysis(v_ds, v_gs, i_ds, i_g, i_s, i_b, temp)

            if all(x is not None for x in [bias_vds, bias_vgs, bias_ids]):
                self.results['bias_point_analysis'] = vm.verify_bias_point_analysis(
                    bias_vds, bias_vgs, bias_ids, bias_ig, bias_is, bias_ib,
                    float(temp[0]) if temp is not None and len(temp) > 0 else 27
                )

            if temp is not None and i_ds is not None:
                self.results['temperature_analysis'] = vm.verify_temperature_analysis(temp, i_ds)

            power_arr = np.abs(v_ds * i_ds) if v_ds is not None and i_ds is not None else None
            if power_arr is not None:
                self.results['thermodynamic_analysis'] = \
                    vm.verify_thermodynamic_analysis(power_arr, temp, i_ds)

            self.logger.logger.info("DC processing complete.")
        except Exception as e:
            self.logger.logger.error(f"DC processing error: {e}")

    # ==================================================================
    # Transient processing
    # ==================================================================

    def _process_transient(self):
        """Read transient data, generate plots, and run verification."""
        self.logger.logger.info("Processing Transient results...")
        out = str(self.output_dir)
        dr = self._data_reader
        pg = self._plot_generator
        vm = self._verification_manager

        try:
            # Large-signal transient: returns (time, vgate, vdrain, idrain)
            ls = dr.read_trans_large_signal_transient_data(out)
            if ls is not None:
                time_ls, v_gate_ls, v_drain_ls, i_ds_ls = ls
                pg.plot_trans_large_signal_transient(out, time_ls, v_gate_ls, v_drain_ls,
                                                     i_ds_ls, None, None, None)
                self.results['transient_large_signal'] = {'data_ready': True}

            # Switching: returns (time, vin, vout, idrain)
            sw = dr.read_trans_switching_response_data(out)
            if sw is not None:
                time_sw, v_in_sw, v_out_sw, i_vdd_sw = sw
                pg.plot_trans_switching_response(out, time_sw, v_in_sw, v_out_sw, i_vdd_sw)
                self.results['transient_switching'] = {'data_ready': True}

            # Delay effect: returns (time, vin, v_mid1, v_mid2, vout)
            de = dr.read_trans_delay_effect_data(out)
            if de is not None:
                time_de, v_in_de, v_m1_de, v_m2_de, v_out_de = de
                pg.plot_trans_delay_effect(out, time_de, v_in_de, v_m1_de, v_m2_de, v_out_de)
                self.results['transient_delay_effect'] = {'data_ready': True}

            # Power dissipation: returns (time, power)
            for temp_tag in ['27C', '100C']:
                pd = dr.read_trans_power_dissipation_data(out, temp_tag)
                if pd is not None:
                    time_pd, power_pd = pd
                    pg.plot_trans_power_dissipation(out, time_pd, None, None,
                                                    power_pd, None, temp_tag)
                    self.results[f'transient_power_{temp_tag}'] = {'data_ready': True}

            # Quasi-static: returns (time, vgate, vdrain, idrain)
            qs = dr.read_trans_quasi_static_data(out)
            if qs is not None:
                time_qs, v_gate_qs, v_drain_qs, id_qs = qs
                pg.plot_trans_quasi_static(out, time_qs, v_gate_qs, v_drain_qs, id_qs)
                self.results['transient_quasi_static'] = {'data_ready': True}

            self.logger.logger.info("Transient processing complete.")
        except Exception as e:
            self.logger.logger.error(f"Transient processing error: {e}")

    # ==================================================================
    # AC processing
    # ==================================================================

    def _process_ac(self):
        """Read AC data, generate plots, and run verification."""
        self.logger.logger.info("Processing AC results...")
        out = str(self.output_dir)
        dr = self._data_reader
        pg = self._plot_generator
        vm = self._verification_manager

        try:
            # CV characteristics
            vg_cv, cv_ig, cv_is, cv_ib, cgg = dr.read_cv_data(out)
            if vg_cv is not None:
                pg.plot_ac_cv_characteristics(out, vg_cv, cv_ig, cv_is, cv_ib, cgg)
                self.results['ac_cv_characteristics'] = \
                    vm.verify_cv_characteristics(vg_cv, cv_ig, cv_is, cv_ib, cgg)

            # S-parameters
            sp = dr.read_sparameter_data(out)
            if sp is not None:
                freq, s11_m, s11_p, s12_m, s12_p, s21_m, s21_p, s22_m, s22_p = sp
                pg.plot_ac_sparameter_analysis(out, freq, s11_m, s11_p, s12_m, s12_p,
                                               s21_m, s21_p, s22_m, s22_p)
                self.results['ac_sparameter_analysis'] = \
                    vm.verify_sparameter_analysis(freq, s11_m, s11_p, s12_m, s12_p,
                                                   s21_m, s21_p, s22_m, s22_p)

            # NQS effects
            nqs = dr.read_nqs_effects_data(out)
            if nqs is not None:
                nqs_freq, vg_ph, id_ph, pd_ = nqs
                pg.plot_ac_nqs_effects(out, nqs_freq, vg_ph, id_ph, pd_)
                self.results['ac_nqs_effects'] = \
                    vm.verify_nqs_effects(nqs_freq, vg_ph, id_ph, pd_)

            # Charge conservation
            cc = dr.read_charge_conservation_data(out)
            if cc is not None:
                t_cc, vg_cc, ig_cc, id_cc, is_cc, ib_cc = cc
                pg.plot_ac_charge_conservation(out, t_cc, vg_cc, ig_cc, id_cc, is_cc, ib_cc)
                self.results['ac_charge_conservation'] = \
                    vm.verify_ac_charge_conservation(
                        t_cc, vg_cc, ig_cc, id_cc, is_cc, ib_cc)

            self.logger.logger.info("AC processing complete.")
        except Exception as e:
            self.logger.logger.error(f"AC processing error: {e}")

    # ==================================================================
    # Noise processing
    # ==================================================================

    def _process_noise(self):
        """Read noise data, generate plots, and run verification."""
        self.logger.logger.info("Processing Noise results...")
        out = str(self.output_dir)
        dr = self._data_reader
        pg = self._plot_generator
        vm = self._verification_manager

        try:
            # Thermal noise at multiple bias points
            for vgs, vds in [(0.3, 0.3), (0.3, 0.6), (0.3, 0.9), (0.3, 1.2),
                              (0.6, 0.3), (0.6, 0.6)]:
                freq_th, noise_th = dr.read_thermal_noise_data(vgs, vds, out)
                if freq_th is not None:
                    pg.plot_noise_spectrum(out, freq_th, noise_th,
                                           f"thermal_vgs{vgs}_vds{vds}")

            # Flicker noise
            freq_fl, noise_fl = dr.read_flicker_noise_data(out)
            if freq_fl is not None:
                pg.plot_noise_spectrum(out, freq_fl, noise_fl, "flicker")

            # Shot noise
            freq_sh, noise_sh = dr.read_shot_noise_data(out)
            if freq_sh is not None:
                pg.plot_noise_spectrum(out, freq_sh, noise_sh, "shot")

            # Temperature-dependent noise
            temp_noise_data = {}
            for t in [-40, 0, 27, 50, 100, 150]:
                freq_tn, noise_tn = dr.read_temperature_noise_data(out, t)
                if freq_tn is not None:
                    temp_noise_data[t] = (freq_tn, noise_tn)
            if temp_noise_data:
                pg.plot_noise_vs_temperature(out, temp_noise_data)

            self.results['noise_analysis'] = vm.verify_noise_analysis()

            self.logger.logger.info("Noise processing complete.")
        except Exception as e:
            self.logger.logger.error(f"Noise processing error: {e}")


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
    """Convenience function: run Spectre benchmark on a model file."""
    if modes is None:
        modes = ['dc']

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
