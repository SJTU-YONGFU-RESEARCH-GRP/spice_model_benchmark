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
                 model_file: Optional[str] = None,
                 model_name: Optional[str] = None,
                 output_dir: str = 'results_spectre',
                 dpi: int = 300,
                 log_level: str = 'INFO'):

        self.dc_circuit_file = dc_circuit_file
        self.transient_circuit_file = transient_circuit_file
        self.noise_circuit_file = noise_circuit_file
        self.ac_circuit_file = ac_circuit_file
        self.model_file = model_file
        self.model_name = model_name

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
            model_file=self.model_file,
            model_name=self.model_name,
        )
        if not runner.run_simulations_by_mode(modes):
            self.logger.logger.error("Spectre simulations failed")
            return False

        # ---- Phase 2: data → plot → verify (same pipeline as ngspice) ----
        self.logger.logger.info("Phase 2: Analysing results...")

        # Verify simulation setup
        selected_circuits = {
            mode: path
            for mode, path in {
                'dc': self.dc_circuit_file,
                'transient': self.transient_circuit_file,
                'ac': self.ac_circuit_file,
                'noise': self.noise_circuit_file,
            }.items()
            if mode in modes and path is not None
        }
        self.results['simulation_setup'] = \
            self._verification_manager.verify_simulation_setup(
                selected_circuits
            )
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
            # 1. Large-signal transient: (time, vgate, vdrain, idrain)
            ls = dr.read_trans_large_signal_transient_data(out)
            if ls is not None:
                time_ls, vg_ls, vd_ls, id_ls = ls
                pg.plot_trans_large_signal_transient(out, time_ls, vg_ls, vd_ls, id_ls)
                self.results['large_signal_transient'] = \
                    vm.verify_trans_large_signal_transient(time_ls, vg_ls, vd_ls, id_ls)

            # 2. Switching: (time, vin, vout, idrain)
            sw = dr.read_trans_switching_response_data(out)
            if sw is not None:
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
                self.results['switching_simulations'] = \
                    vm.verify_trans_switching_simulations(
                        time_sw,
                        vin_sw,
                        vout_sw,
                        id_sw,
                        power_sw,
                    )

            # 3. Delay effect: (time, vin, vmid1, vmid2, vout)
            de = dr.read_trans_delay_effect_data(out)
            if de is not None:
                time_de, vin_de, vm1_de, vm2_de, vout_de = de
                pg.plot_trans_delay_effect(out, time_de, vin_de, vm1_de, vm2_de, vout_de)
                self.results['delay_effect'] = \
                    vm.verify_trans_delay_effect(time_de, vin_de, vm1_de, vm2_de, vout_de)

            # 4. Power dissipation: (time, power) at two temps
            pd_27 = dr.read_trans_power_dissipation_data(out, 27)
            pd_100 = dr.read_trans_power_dissipation_data(out, 100)
            if pd_27 is not None and pd_100 is not None:
                time_27, pwr_27 = pd_27
                time_100, pwr_100 = pd_100
                pg.plot_trans_power_dissipation(out, time_27, pwr_27, time_100, pwr_100)
                self.results['power_dissipation'] = \
                    vm.verify_trans_power_dissipation(time_27, pwr_27, time_100, pwr_100)

            # 5. Quasi-static: (time, vgate, vdrain, idrain)
            qs = dr.read_trans_quasi_static_data(out)
            if qs is not None:
                time_qs, vg_qs, vd_qs, id_qs = qs
                pg.plot_trans_quasi_static(out, time_qs, vg_qs, vd_qs, id_qs)
                self.results['quasi_static'] = \
                    vm.verify_trans_quasi_static(time_qs, vg_qs, vd_qs, id_qs)

            charge = dr.read_trans_charge_conservation_data(out)
            if charge is not None and all(value is not None for value in charge):
                time_cc, vg_cc, ig_cc, id_cc, is_cc, ib_cc = charge
                qg = np.zeros_like(ig_cc)
                qd = np.zeros_like(id_cc)
                qs_charge = np.zeros_like(is_cc)
                qb = np.zeros_like(ib_cc)
                for index in range(1, len(time_cc)):
                    dt = time_cc[index] - time_cc[index - 1]
                    qg[index] = qg[index - 1] + 0.5 * (ig_cc[index] + ig_cc[index - 1]) * dt
                    qd[index] = qd[index - 1] + 0.5 * (id_cc[index] + id_cc[index - 1]) * dt
                    qs_charge[index] = qs_charge[index - 1] + 0.5 * (is_cc[index] + is_cc[index - 1]) * dt
                    qb[index] = qb[index - 1] + 0.5 * (ib_cc[index] + ib_cc[index - 1]) * dt
                i_total = ig_cc + id_cc + is_cc + ib_cc
                q_total = qg + qd + qs_charge + qb
                pg.plot_trans_charge_conservation(
                    out,
                    time_cc,
                    vg_cc,
                    ig_cc,
                    id_cc,
                    is_cc,
                    ib_cc,
                    i_total,
                    qg,
                    qd,
                    qs_charge,
                    qb,
                    q_total,
                )
                self.results['trans_charge_conservation'] = (
                    vm.verify_trans_charge_conservation(
                        time_cc, vg_cc, ig_cc, id_cc, is_cc, ib_cc,
                        i_total, qg, qd, qs_charge, qb, q_total,
                    )
                )

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
            # CV characteristics: read_cv_data → (vg, cv_ig, cv_is, cv_ib, cgg)
            # plot signature: (output_dir, vg=None, ig=None, freq=None)
            vg_cv, cv_ig, cv_is, cv_ib, cgg = dr.read_cv_data(out)
            sp = dr.read_sparameter_data(out)
            nqs = dr.read_nqs_effects_data(out)
            sp_freq = sp[0] if sp is not None else None
            nqs_freq = nqs[0] if nqs is not None else None
            vg_phase = nqs[1] if nqs is not None else None
            id_phase = nqs[2] if nqs is not None else None
            phase_diff = nqs[3] if nqs is not None else None
            if vg_cv is not None and cgg is not None:
                pg.plot_ac_cv_characteristics(out, vg=vg_cv, ig=cv_ig)
                cv_results = vm.verify_cv_characteristics(
                    vg_cv, cgg, sp_freq, vg_phase, id_phase,
                )
                self.results['cv_characteristics'] = {
                    **cv_results,
                    'cgg_range': f"{np.min(cgg)*1e15:.2f}fF to {np.max(cgg)*1e15:.2f}fF",
                    'max_value_at': f"{vg_cv[np.argmax(cgg)]:.2f}V",
                    'freq_range': (
                        f"{np.min(sp_freq):.2e}Hz to {np.max(sp_freq):.2e}Hz"
                        if sp_freq is not None and len(sp_freq) else "N/A"
                    ),
                }
                table_vg, table_caps = dr.read_cv_table_data(
                    out, freq_tag="1MHz"
                )
                if table_vg is None or table_caps is None:
                    raise ValueError(
                        "measured 1MHz CV component table is required"
                    )
                order = np.argsort(table_vg)
                vg_sorted = np.asarray(table_vg, dtype=float)[order]
                dv = float(vg_sorted[-1] - vg_sorted[0])
                if len(vg_sorted) > 1 and dv != 0.0:
                    # Use the same already-established AC C(V) integral for
                    # every measured component.  This completes result/report
                    # mapping for HSPICE and Spectre without changing the
                    # numerical definition used by ngspice.
                    ls_caps = {
                        name: float(
                            np.trapz(
                                np.asarray(values, dtype=float)[order],
                                vg_sorted,
                            )
                            / dv
                        )
                        for name, values in table_caps.items()
                    }
                    self.results['ac_integrated_large_signal_caps'] = {
                        'data_ready': True,
                        'vg_start': float(vg_sorted[0]),
                        'vg_stop': float(vg_sorted[-1]),
                        'dv': dv,
                        'freq_tag': '1MHz',
                        'ls_caps_f': ls_caps,
                        'outputs': {},
                    }

            # S-parameters: returns 9-tuple
            # plot signature: (output_dir, freq, s11_mag, s21_mag, s12_mag, s22_mag)
            if sp is not None and sp[0] is not None:
                freq, s11_m, s11_p, s12_m, s12_p, s21_m, s21_p, s22_m, s22_p = sp
                if freq is not None and len(freq) > 0:
                    pg.plot_ac_sparameter_analysis(out, freq=freq,
                                                   s11_mag=s11_m, s21_mag=s21_m,
                                                   s12_mag=s12_m, s22_mag=s22_m)
                    self.results['sparameter_analysis'] = {
                        **vm.verify_sparameter_analysis(
                            freq, s11_m, s21_m, s12_m, s22_m,
                        ),
                        'freq_range': f"{np.min(freq):.2e}Hz to {np.max(freq):.2e}Hz",
                        's11_range': f"{np.min(s11_m):.0f}dB to {np.max(s11_m):.0f}dB",
                        's21_range': f"{np.min(s21_m):.0f}dB to {np.max(s21_m):.0f}dB",
                        's12_range': f"{np.min(s12_m):.0f}dB to {np.max(s12_m):.0f}dB",
                        's22_range': f"{np.min(s22_m):.0f}dB to {np.max(s22_m):.0f}dB",
                        'isolation': f">{np.min(np.abs(s21_m-s12_m)):.0f}dB",
                    }

            # NQS effects: returns 4-tuple
            # plot signature: (output_dir, freq, vg_phase, id_phase, phase_diff)
            if nqs is not None and nqs[0] is not None:
                nqs_freq, vg_ph, id_ph, pd_ = nqs
                if nqs_freq is not None and len(nqs_freq) > 0:
                    pg.plot_ac_nqs_effects(out, freq=nqs_freq,
                                           vg_phase=vg_ph, id_phase=id_ph,
                                           phase_diff=pd_)
                    self.results['nqs_effects'] = {
                        **vm.verify_nqs_effects(nqs_freq, vg_ph, id_ph, pd_),
                        'max_phase_shift': f"{np.max(np.abs(pd_)):.2f}°",
                        'freq_range': f"{np.min(nqs_freq):.2e}Hz to {np.max(nqs_freq):.2e}Hz",
                    }

            # Charge conservation: returns 6-tuple
            cc = dr.read_charge_conservation_data(out)
            if cc is not None and cc[0] is not None:
                t_cc, vg_cc, ig_cc, id_cc, is_cc, ib_cc = cc
                i_total = ig_cc + id_cc + is_cc + ib_cc
                charges = [np.zeros_like(i_total) for _ in range(4)]
                currents = (ig_cc, id_cc, is_cc, ib_cc)
                for index in range(1, len(t_cc)):
                    dt = t_cc[index] - t_cc[index - 1]
                    for charge_values, current_values in zip(charges, currents):
                        charge_values[index] = (
                            charge_values[index - 1]
                            + 0.5 * (current_values[index] + current_values[index - 1]) * dt
                        )
                q_total = sum(charges)
                self.results['charge_conservation'] = vm.verify_ac_charge_conservation(
                    t_cc, vg_cc, ig_cc, id_cc, is_cc, ib_cc, i_total,
                    *charges, q_total,
                )

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
            # Thermal noise at main bias point (Vgs=0.6, Vds=0.6)
            th = dr.read_thermal_noise_data(out, vgs=0.6, vds=0.6)
            flicker_freq, flicker_noise = dr.read_flicker_noise_data(out)
            shot_freq, shot_noise = dr.read_shot_noise_data(out)
            temperatures, temp_noise = dr.read_temperature_noise_data(out)
            if th[0] is not None and flicker_freq is not None:
                freq_th, noise_th, _, _ = th
                pg.plot_noise_spectrum(out, freq_th, noise_th,
                                       "Thermal Noise (Vgs=0.6V, Vds=0.6V)",
                                       "thermal_noise")
                thermal_by_bias = dr.read_all_thermal_noise_data(out)
                self.results['noise_analysis'] = vm.verify_noise_analysis(
                    freq_th,
                    thermal_by_bias if thermal_by_bias else noise_th,
                    (flicker_freq, flicker_noise),
                    (shot_freq, shot_noise),
                    temp_noise,
                    temperatures,
                )
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
    model_name: Optional[str] = None,
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
        model_file=model_file,
        model_name=model_name,
    )

    return sim.run(modes=modes)
