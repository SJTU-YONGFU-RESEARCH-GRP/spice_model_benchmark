"""
HSPICE MOSFET Simulation coordinator.

Mirrors MOSFETSimulation and SpectreMOSFETSimulation classes
but uses HspiceRunner for simulation execution.
Reuses DataReader, PlotGenerator, and VerificationManager from the ngspice
pipeline since the runner generates identical text file outputs.
"""

import os
import numpy as np
from pathlib import Path
from typing import List, Optional

from .logger import Logger
from .hspice_runner import HspiceRunner
from .data_reader import DataReader
from .plot_generator import PlotGenerator
from .verification_manager import VerificationManager
from .spectre_mosfet_simulation import SpectreMOSFETSimulation


class HspiceMOSFETSimulation:
    """MOSFET simulation and verification using HSPICE.

    Replicates the same benchmark workflow as MOSFETSimulation
    but invokes HSPICE. The runner generates identical text data files,
    so the existing DataReader/PlotGenerator/VerificationManager
    pipeline works unchanged.
    """

    def __init__(self,
                 model_file: Optional[str] = None,
                 output_dir: str = 'results_hspice',
                 dpi: int = 300,
                 log_level: str = 'INFO',
                 model_name: Optional[str] = None,
                 dc_circuit_file: Optional[str] = None,
                 transient_circuit_file: Optional[str] = None,
                 noise_circuit_file: Optional[str] = None,
                 ac_circuit_file: Optional[str] = None):

        self.model_file = model_file
        self.model_name = model_name
        self.circuit_files = {
            "dc": dc_circuit_file,
            "transient": transient_circuit_file,
            "noise": noise_circuit_file,
            "ac": ac_circuit_file,
        }

        self.output_dir = Path(output_dir).resolve()
        self.dpi = dpi

        os.makedirs(self.output_dir, exist_ok=True)

        self.logger = Logger(log_level=log_level)
        self._data_reader = DataReader(
            self.logger, output_dir=str(self.output_dir)
        )
        self._plot_generator = PlotGenerator(
            str(self.output_dir), dpi=dpi, logger=self.logger
        )
        self._verification_manager = VerificationManager(
            self.logger, output_dir=str(self.output_dir)
        )
        self._verification_manager.plot_generator = self._plot_generator

        self.results: dict = {}

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    def run(self, modes: Optional[List[str]] = None) -> bool:
        if modes is None:
            modes = ['dc']

        self.logger.logger.info("=" * 60)
        self.logger.logger.info("HSPICE MOSFET Simulation & Verification")
        self.logger.logger.info("=" * 60)

        # ---- Phase 1: Run HSPICE simulations ----
        self.logger.logger.info("Phase 1: Running HSPICE simulations...")
        runner = HspiceRunner(
            self.logger,
            output_dir=str(self.output_dir),
            model_file=self.model_file,
            circuit_files=self.circuit_files,
        )
        if not runner.run_simulations_by_mode(modes):
            self.logger.logger.error("HSPICE simulations failed")
            return False

        # ---- Phase 2: data -> plot -> verify ----
        self.logger.logger.info("Phase 2: Analysing results...")

        # Simulation setup verification
        selected_circuits = {
            mode: path
            for mode, path in self.circuit_files.items()
            if mode in modes and path is not None
        }
        self.results['simulation_setup'] = \
            self._verification_manager.verify_simulation_setup(
                selected_circuits
            )
        if 'details' in self.results['simulation_setup']:
            self.results['simulation_setup']['details'][
                'ngspice_version'
            ] = 'HSPICE S-2021.09'

        # DC processing
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
        self._verification_manager.update_verification_checklist(
            self.results, modes
        )

        self.logger.logger.info("HSPICE benchmark workflow complete!")
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
            v_ds, v_gs, i_ds, i_g, i_s, i_b, power = dr.read_dc_iv_data(out)
            temp = dr.read_dc_temperature_data(out)
            bias_vds, bias_vgs, bias_ids, bias_ig, bias_is, bias_ib = \
                dr.read_dc_bias_point_data(out)

            if v_ds is not None and v_gs is not None and i_ds is not None:
                pg.plot_dc_iv_characteristics(out, v_ds, v_gs, i_ds)

            if all(x is not None for x in [i_ds, i_g, i_s, i_b]):
                pg.plot_dc_kcl_verification(out, i_ds, i_g, i_s, i_b)

            if temp is not None and i_ds is not None:
                pg.plot_dc_temperature_analysis(out, temp, i_ds)

            if v_ds is not None and v_gs is not None and i_ds is not None:
                self.results['dc_operating_point_analysis'] = \
                    vm.verify_dc_operating_point_analysis(
                        v_ds, v_gs, i_ds, i_g, i_s, i_b, temp
                    )

            if all(x is not None for x in [bias_vds, bias_vgs, bias_ids]):
                self.results['bias_point_analysis'] = \
                    vm.verify_bias_point_analysis(
                        bias_vds, bias_vgs, bias_ids,
                        bias_ig, bias_is, bias_ib,
                        float(temp[0]) if temp is not None
                        and len(temp) > 0 else 27
                    )

            if temp is not None and i_ds is not None:
                self.results['temperature_analysis'] = \
                    vm.verify_temperature_analysis(temp, i_ds)

            power_arr = np.abs(v_ds * i_ds) if v_ds is not None \
                and i_ds is not None else None
            if power_arr is not None:
                self.results['thermodynamic_analysis'] = \
                    vm.verify_thermodynamic_analysis(
                        power_arr, temp, i_ds
                    )

            self.logger.logger.info("DC processing complete.")
        except Exception as e:
            self.logger.logger.error(f"DC processing error: {e}")

    # ==================================================================
    # Transient processing
    # ==================================================================

    def _process_transient(self):
        self.logger.logger.info("Processing Transient results...")
        out = str(self.output_dir)
        dr = self._data_reader
        pg = self._plot_generator
        vm = self._verification_manager

        try:
            ls = dr.read_trans_large_signal_transient_data(out)
            if ls is not None and ls[0] is not None:
                time_ls, vg_ls, vd_ls, id_ls = ls
                pg.plot_trans_large_signal_transient(out, time_ls, vg_ls, vd_ls, id_ls)
                self.results['transient_large_signal'] = \
                    vm.verify_trans_large_signal_transient(time_ls, vg_ls, vd_ls, id_ls)

            sw = dr.read_trans_switching_response_data(out)
            if sw is not None and sw[0] is not None:
                time_sw, vin_sw, vout_sw, id_sw = sw
                sw_power = dr.read_trans_switching_power_data(out)
                if (
                    sw_power is None
                    or sw_power[0] is None
                    or sw_power[1] is None
                ):
                    raise ValueError(
                        "measured switching-power data is required"
                    )
                _, power_sw = sw_power
                pg.plot_trans_switching_response(
                    out,
                    time_sw,
                    vin_sw,
                    vout_sw,
                    id_sw,
                    power_sw,
                )
                self.results['transient_switching'] = \
                    vm.verify_trans_switching_simulations(
                        time_sw,
                        vin_sw,
                        vout_sw,
                        id_sw,
                        power_sw,
                    )

            de = dr.read_trans_delay_effect_data(out)
            if de is not None and de[0] is not None:
                time_de, vin_de, vm1_de, vm2_de, vout_de = de
                pg.plot_trans_delay_effect(out, time_de, vin_de, vm1_de, vm2_de, vout_de)
                self.results['transient_delay_effect'] = \
                    vm.verify_trans_delay_effect(time_de, vin_de, vm1_de, vm2_de, vout_de)

            pd_27 = dr.read_trans_power_dissipation_data(out, 27)
            pd_100 = dr.read_trans_power_dissipation_data(out, 100)
            if pd_27 is not None and pd_27[0] is not None and \
               pd_100 is not None and pd_100[0] is not None:
                time_27, pwr_27 = pd_27
                time_100, pwr_100 = pd_100
                pg.plot_trans_power_dissipation(out, time_27, pwr_27, time_100, pwr_100)
                self.results['transient_power_dissipation'] = \
                    vm.verify_trans_power_dissipation(time_27, pwr_27, time_100, pwr_100)

            qs = dr.read_trans_quasi_static_data(out)
            if qs is not None and qs[0] is not None:
                time_qs, vg_qs, vd_qs, id_qs = qs
                pg.plot_trans_quasi_static(out, time_qs, vg_qs, vd_qs, id_qs)
                self.results['transient_quasi_static'] = \
                    vm.verify_trans_quasi_static(time_qs, vg_qs, vd_qs, id_qs)

            self.logger.logger.info("Transient processing complete.")
        except Exception as e:
            self.logger.logger.error(f"Transient processing error: {e}")

    # ==================================================================
    # AC processing
    # ==================================================================

    def _process_ac(self):
        self.logger.logger.info("Processing AC results...")
        out = str(self.output_dir)
        dr = self._data_reader
        pg = self._plot_generator
        vm = self._verification_manager

        try:
            vg_cv, cv_ig, cv_is, cv_ib, cgg = dr.read_cv_data(out)
            if vg_cv is not None and cgg is not None:
                pg.plot_ac_cv_characteristics(out, vg=vg_cv, ig=cv_ig)
                self.results['ac_cv_characteristics'] = {'data_ready': True}

            sp = dr.read_sparameter_data(out)
            if sp is not None and sp[0] is not None:
                freq, s11_m, s11_p, s12_m, s12_p, s21_m, s21_p, s22_m, s22_p = sp
                if freq is not None and len(freq) > 0:
                    pg.plot_ac_sparameter_analysis(
                        out, freq=freq, s11_mag=s11_m, s21_mag=s21_m,
                        s12_mag=s12_m, s22_mag=s22_m
                    )
                    self.results['ac_sparameter_analysis'] = {'data_ready': True}

            nqs = dr.read_nqs_effects_data(out)
            if nqs is not None and nqs[0] is not None:
                nqs_freq, vg_ph, id_ph, pd_ = nqs
                if nqs_freq is not None and len(nqs_freq) > 0:
                    pg.plot_ac_nqs_effects(
                        out, freq=nqs_freq, vg_phase=vg_ph,
                        id_phase=id_ph, phase_diff=pd_
                    )
                    self.results['ac_nqs_effects'] = {'data_ready': True}

            self.logger.logger.info("AC processing complete.")
        except Exception as e:
            self.logger.logger.error(f"AC processing error: {e}")

    # ==================================================================
    # Noise processing
    # ==================================================================

    def _process_noise(self):
        self.logger.logger.info("Processing Noise results...")
        out = str(self.output_dir)
        dr = self._data_reader
        pg = self._plot_generator

        try:
            th = dr.read_thermal_noise_data(out, vgs=0.6, vds=0.6)
            if th[0] is not None:
                freq_th, noise_th, _, _ = th
                pg.plot_noise_spectrum(
                    out, freq_th, noise_th,
                    "Thermal Noise (Vgs=0.6V, Vds=0.6V)", "thermal_noise"
                )
                self.results['noise_analysis'] = {'data_ready': True}
            self.logger.logger.info("Noise processing complete.")
        except Exception as e:
            self.logger.logger.error(f"Noise processing error: {e}")


# Both commercial simulators emit the same normalized data schema.  Share the
# complete processing implementation so their REPORT.md result keys and
# verification calculations cannot drift apart again.
HspiceMOSFETSimulation._process_transient = SpectreMOSFETSimulation._process_transient
HspiceMOSFETSimulation._process_ac = SpectreMOSFETSimulation._process_ac
HspiceMOSFETSimulation._process_noise = SpectreMOSFETSimulation._process_noise


def benchmark_spice_model_hspice(
    model_file: str,
    output_dir: str = "hspice_benchmark_results",
    modes: Optional[List[str]] = None,
    dpi: int = 300,
    log_level: str = "INFO",
    model_name: Optional[str] = None,
    dc_circuit: Optional[str] = None,
    transient_circuit: Optional[str] = None,
    noise_circuit: Optional[str] = None,
    ac_circuit: Optional[str] = None,
) -> bool:
    """Convenience function: run HSPICE benchmark on a model file."""
    if modes is None:
        modes = ['dc']

    sim = HspiceMOSFETSimulation(
        model_file=model_file,
        output_dir=output_dir,
        dpi=dpi,
        log_level=log_level,
        model_name=model_name,
        dc_circuit_file=dc_circuit,
        transient_circuit_file=transient_circuit,
        noise_circuit_file=noise_circuit,
        ac_circuit_file=ac_circuit,
    )
    return sim.run(modes=modes)
