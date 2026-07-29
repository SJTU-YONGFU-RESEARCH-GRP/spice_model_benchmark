"""Strict, simulator-neutral rendering of the canonical benchmark plot set.

Every curve is read from an explicitly named simulator result.  Missing or
invalid input is an error; this module never substitutes another file and
never synthesizes a waveform.
"""

import hashlib
import json
import math
import re
import shutil
from pathlib import Path

import numpy as np

from .data_reader import DataReader
from .logger import Logger
from .plot_generator import PlotGenerator


PLOTS_BY_MODE = {
    "dc": (
        "dc_iv_characteristics.png",
        "dc_kcl_verification.png",
        "dc_temperature_analysis.png",
    ),
    "ac": (
        "ac_cv_characteristics.png",
        "ac_cv_components.png",
        "ac_v_multifreq_characteristics.png",
        "ac_cv_characteristics_per_gate_area.png",
        "ac_cv_components_per_gate_area.png",
        "ac_cv_sparameter_analysis.png",
        "ac_cv_nqs_effects.png",
        "ac_charge_conservation.png",
    ),
    "transient": (
        "trans_large_signal_transient.png",
        "trans_switching_response.png",
        "trans_delay_effect.png",
        "trans_power_dissipation.png",
        "trans_energy_consumption.png",
        "trans_quasi_static_time.png",
        "trans_quasi_static_iv.png",
        "trans_charge_conservation.png",
        "trans_total_charge.png",
    ),
    "noise": (
        "noise_thermal_noise.png",
        "noise_flicker_noise.png",
        "noise_shot_noise.png",
        "noise_thermal_noise_vds_comparison.png",
        "noise_vs_temperature.png",
        "noise_components.png",
    ),
}


def _spice_number(text):
    value = text.strip().lower()
    try:
        return float(value)
    except ValueError:
        pass
    for suffix, multiplier in (
        ("meg", 1e6), ("f", 1e-15), ("p", 1e-12), ("n", 1e-9),
        ("u", 1e-6), ("m", 1e-3), ("k", 1e3), ("g", 1e9),
        ("t", 1e12),
    ):
        if value.endswith(suffix):
            return float(value[:-len(suffix)]) * multiplier
    raise ValueError(f"invalid SPICE number: {text}")


def _gate_area_um2(ac_netlist):
    text = Path(ac_netlist).read_text(errors="replace")
    for line in text.splitlines():
        if not re.match(r"(?i)^\s*m(?:1|_iv)\b", line):
            continue
        width = re.search(r"(?i)\bw\s*=\s*(\S+)", line)
        length = re.search(r"(?i)\bl\s*=\s*(\S+)", line)
        if width and length:
            area = (
                _spice_number(width.group(1))
                * _spice_number(length.group(1))
                / 1e-12
            )
            if math.isfinite(area) and area > 0:
                return area
    raise ValueError(f"cannot determine MOS gate area from {ac_netlist}")


def _numeric_rows(path, minimum=2):
    path = Path(path)
    if not path.is_file() or path.stat().st_size == 0:
        raise ValueError(f"required simulator data is missing: {path}")
    rows = []
    for line in path.read_text(errors="replace").splitlines():
        fields = line.strip().split()
        try:
            row = [float(item) for item in fields]
        except ValueError:
            continue
        if row and all(math.isfinite(item) for item in row):
            rows.append(row)
    if len(rows) < minimum:
        raise ValueError(
            f"simulator data has fewer than {minimum} numeric rows: {path}"
        )
    return rows


def _arrays(label, values, minimum=2):
    if values is None:
        raise ValueError(f"{label}: reader returned no data")
    arrays = tuple(values) if isinstance(values, tuple) else (values,)
    for index, item in enumerate(arrays):
        if item is None:
            raise ValueError(f"{label}: array {index} is missing")
        array = np.asarray(item, dtype=float)
        if array.size < minimum or not np.all(np.isfinite(array)):
            raise ValueError(f"{label}: array {index} is invalid")
    return arrays


def _write_per_area_cv(data_dir, area_um2):
    rows = _numeric_rows(data_dir / "cv_data.txt")
    if any(len(row) < 8 for row in rows):
        raise ValueError("cv_data.txt must contain all measured CV components")
    output = data_dir / "ac_cv_caps_1MHz_per_gate_area.csv"
    lines = [
        "Vg,Cgg_fF_per_um2,Cgs_fF_per_um2,Cgd_fF_per_um2,"
        "Cgb_fF_per_um2,W_um,L_um,Area_um2"
    ]
    for row in rows:
        vg, cgg, cgb, cgs, cgd = row[0], row[4], row[5], row[6], row[7]
        lines.append(
            ",".join(
                f"{item:.12g}"
                for item in (
                    vg,
                    cgg * 1e15 / area_um2,
                    cgs * 1e15 / area_um2,
                    cgd * 1e15 / area_um2,
                    cgb * 1e15 / area_um2,
                    float("nan"),
                    float("nan"),
                    area_um2,
                )
            )
        )
    output.write_text("\n".join(lines) + "\n")
    return output


def _integrate_currents(time, currents):
    charges = [np.zeros_like(np.asarray(item, dtype=float)) for item in currents]
    for index in range(1, len(time)):
        step = time[index] - time[index - 1]
        for charge, current in zip(charges, currents):
            charge[index] = (
                charge[index - 1]
                + 0.5 * (current[index] + current[index - 1]) * step
            )
    return charges


def _common_noise_grid(*spectra):
    """Interpolate measured spectra only within their shared frequency range."""
    lower = max(float(np.min(item[0])) for item in spectra)
    upper = min(float(np.max(item[0])) for item in spectra)
    reference_frequency = np.asarray(spectra[0][0], dtype=float)
    common = reference_frequency[
        (reference_frequency >= lower) & (reference_frequency <= upper)
    ]
    if len(common) < 2:
        raise ValueError("noise component spectra have no common frequency grid")
    values = []
    for frequency, density in spectra:
        frequency = np.asarray(frequency, dtype=float)
        density = np.asarray(density, dtype=float)
        order = np.argsort(frequency)
        values.append(
            np.interp(
                np.log10(common),
                np.log10(frequency[order]),
                density[order],
            )
        )
    return common, values


def render_canonical_plots(output_dir, modes, dpi=120, log_level="INFO"):
    """Render selected canonical plots and persist per-plot provenance."""
    output_dir = Path(output_dir).resolve()
    data_dir = output_dir / "data"
    netlist_dir = output_dir / "netlist"
    plots_dir = output_dir / "plots"
    legacy_plot_dir = output_dir / "plot"
    for directory in (plots_dir, legacy_plot_dir):
        if directory.exists():
            shutil.rmtree(directory)
    plots_dir.mkdir(parents=True)

    logger = Logger(log_level=log_level)
    reader = DataReader(logger, output_dir=str(output_dir))
    plotter = PlotGenerator(str(output_dir), dpi=dpi, logger=logger)
    provenance = {}

    def sha256(path):
        hasher = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def sources(plot_names, filenames, transformation="direct plot"):
        relative_sources = ["data/" + item for item in filenames]
        payload = {
            "sources": relative_sources,
            "sourceSha256": {
                relative: sha256(output_dir / relative)
                for relative in relative_sources
            },
            "transformation": transformation,
            "syntheticDataUsed": False,
        }
        for plot_name in plot_names:
            provenance[plot_name] = payload

    if "dc" in modes:
        for temperature in (-40, 0, 25, 50, 100, 150):
            _numeric_rows(data_dir / f"iv_data_{temperature}.txt")
        _numeric_rows(data_dir / "bias_point_data.txt")
        dc = _arrays("DC IV", reader.read_dc_iv_data(str(output_dir)))
        vds, vgs, ids, ig, source_current, bulk_current, _ = dc
        temperature = _arrays(
            "DC temperature", reader.read_dc_temperature_data(str(output_dir))
        )[0]
        plotter.plot_dc_iv_characteristics(output_dir, vds, vgs, ids)
        plotter.plot_dc_kcl_verification(
            output_dir, ids, ig, source_current, bulk_current
        )
        plotter.plot_dc_temperature_analysis(output_dir, temperature, ids)
        dc_sources = [
            f"iv_data_{item}.txt" for item in (-40, 0, 25, 50, 100, 150)
        ]
        sources(PLOTS_BY_MODE["dc"], dc_sources)

    if "ac" in modes:
        for filename in (
            "cv_data.txt", "cmatrix_data.txt", "sparams_data.txt",
            "nqs_effects.txt", "charge_conservation.txt",
        ):
            _numeric_rows(data_dir / filename)
        ac_netlists = list(netlist_dir.glob("ac.*"))
        if len(ac_netlists) != 1:
            raise ValueError(
                "expected one archived AC netlist, found %d"
                % len(ac_netlists)
            )
        area_file = _write_per_area_cv(
            data_dir, _gate_area_um2(ac_netlists[0])
        )
        plotter.plot_ac_cv_characteristics(output_dir)

        sparams = _arrays(
            "S parameters", reader.read_sparameter_data(str(output_dir))
        )
        if np.allclose(
            np.column_stack((sparams[1], sparams[3], sparams[5], sparams[7])),
            0.0,
            rtol=0.0,
            atol=0.0,
        ):
            raise ValueError("S-parameter magnitudes are all zero")
        plotter.plot_ac_sparameter_analysis(
            output_dir,
            freq=sparams[0],
            s11_mag=sparams[1],
            s12_mag=sparams[3],
            s21_mag=sparams[5],
            s22_mag=sparams[7],
        )

        nqs = _arrays(
            "NQS effects", reader.read_nqs_effects_data(str(output_dir))
        )
        if np.allclose(nqs[3], 0.0, rtol=0.0, atol=0.0):
            raise ValueError("NQS phase difference is all zero")
        plotter.plot_ac_nqs_effects(
            output_dir,
            freq=nqs[0],
            vg_phase=nqs[1],
            id_phase=nqs[2],
            phase_diff=nqs[3],
        )

        charge = _arrays(
            "AC charge conservation",
            reader.read_charge_conservation_data(str(output_dir)),
        )
        time, gate, ig, drain_current, source_current, bulk_current = charge
        currents = (ig, drain_current, source_current, bulk_current)
        total_current = sum(currents)
        charges = _integrate_currents(time, currents)
        total_charge = sum(charges)
        plotter.plot_ac_charge_conservation(
            output_dir,
            time,
            gate,
            *currents,
            total_current,
            *charges,
            total_charge,
        )
        sources(
            PLOTS_BY_MODE["ac"][:5],
            ["cv_data.txt", area_file.name],
            "direct CV plot; per-area curves divide measured capacitance "
            "by MOS W*L from netlist/ac.*",
        )
        sources(
            ("ac_cv_sparameter_analysis.png",),
            ["sparams_data.txt"],
            "Y-to-S conversion from two measured complex port excitations",
        )
        sources(
            ("ac_cv_nqs_effects.png",),
            ["nqs_effects.txt"],
            "measured complex gate-voltage/drain-current phase",
        )
        sources(
            ("ac_charge_conservation.png",),
            ["charge_conservation.txt"],
            "trapezoidal integration of measured terminal currents",
        )

    if "transient" in modes:
        transient_files = (
            "tran_large_signal.txt",
            "tran_switching.txt",
            "tran_switching_power.txt",
            "tran_delay.txt",
            "tran_power_27C.txt",
            "tran_power_100C.txt",
            "tran_quasi_static.txt",
            "tran_charge.txt",
        )
        for filename in transient_files:
            _numeric_rows(data_dir / filename)
        large_signal = _arrays(
            "large-signal transient",
            reader.read_trans_large_signal_transient_data(str(output_dir)),
        )
        plotter.plot_trans_large_signal_transient(
            output_dir, *large_signal
        )
        switching = _arrays(
            "switching transient",
            reader.read_trans_switching_response_data(str(output_dir)),
        )
        switching_power = _arrays(
            "switching power",
            reader.read_trans_switching_power_data(str(output_dir)),
        )
        if (
            len(switching[0]) != len(switching_power[0])
            or not np.allclose(
                switching[0],
                switching_power[0],
                rtol=1e-9,
                atol=1e-18,
            )
        ):
            raise ValueError(
                "switching waveform and power use different time grids"
            )
        plotter.plot_trans_switching_response(
            output_dir, *switching, switching_power[1]
        )
        delay = _arrays(
            "delay transient",
            reader.read_trans_delay_effect_data(str(output_dir)),
        )
        plotter.plot_trans_delay_effect(output_dir, *delay)
        power_27 = _arrays(
            "27C transient power",
            reader.read_trans_power_dissipation_data(str(output_dir), 27),
        )
        power_100 = _arrays(
            "100C transient power",
            reader.read_trans_power_dissipation_data(str(output_dir), 100),
        )
        plotter.plot_trans_power_dissipation(
            output_dir, *power_27, *power_100
        )
        energy_27 = _arrays(
            "27C transient energy",
            reader.read_trans_energy_consumption_data(str(output_dir), 27),
        )
        energy_100 = _arrays(
            "100C transient energy",
            reader.read_trans_energy_consumption_data(str(output_dir), 100),
        )
        plotter.plot_trans_energy_consumption(
            output_dir, *energy_27, *energy_100
        )
        quasi_static = _arrays(
            "quasi-static transient",
            reader.read_trans_quasi_static_data(str(output_dir)),
        )
        plotter.plot_trans_quasi_static(output_dir, *quasi_static)
        transient_charge = _arrays(
            "transient terminal charge",
            reader.read_trans_charge_conservation_data(str(output_dir)),
        )
        charge_time, charge_gate, *charge_currents = transient_charge
        charge_total_current = sum(charge_currents)
        terminal_charges = _integrate_currents(
            charge_time, charge_currents
        )
        charge_total = sum(terminal_charges)
        plotter.plot_trans_charge_conservation(
            output_dir,
            charge_time,
            charge_gate,
            *charge_currents,
            charge_total_current,
            *terminal_charges,
            charge_total,
        )
        sources(
            ("trans_large_signal_transient.png",),
            ["tran_large_signal.txt"],
        )
        sources(
            ("trans_switching_response.png",),
            ["tran_switching.txt", "tran_switching_power.txt"],
        )
        sources(("trans_delay_effect.png",), ["tran_delay.txt"])
        sources(
            ("trans_power_dissipation.png",),
            ["tran_power_27C.txt", "tran_power_100C.txt"],
        )
        sources(
            ("trans_energy_consumption.png",),
            ["tran_power_27C.txt", "tran_power_100C.txt"],
            "cumulative trapezoidal integration of measured power",
        )
        sources(
            ("trans_quasi_static_time.png", "trans_quasi_static_iv.png"),
            ["tran_quasi_static.txt"],
        )
        sources(
            ("trans_charge_conservation.png", "trans_total_charge.png"),
            ["tran_charge.txt"],
            "plots use the existing transient-current integration result; "
            "terminal and total-charge artifacts are kept distinct",
        )

    if "noise" in modes:
        thermal_names = [
            f"thermal_noise_vgs{vgs}_vds{vds}.txt"
            for vgs, vds in (
                ("0.3", "0.3"), ("0.3", "0.6"), ("0.3", "0.9"),
                ("0.3", "1.2"), ("0.6", "0.3"), ("0.6", "0.6"),
            )
        ]
        temperature_names = [
            f"noise_temp{temperature}.txt"
            for temperature in (-40, 0, 27, 50, 100, 150)
        ]
        for filename in (
            *thermal_names, "flicker_noise.txt", "shot_noise.txt",
            *temperature_names,
        ):
            rows = _numeric_rows(data_dir / filename)
            if all(
                abs(item) == 0.0
                for row in rows
                for item in row[1:]
            ):
                raise ValueError(f"noise result is all zero: {filename}")
        thermal = _arrays(
            "thermal noise",
            reader.read_thermal_noise_data(
                str(output_dir), vgs=0.6, vds=0.6
            )[:2],
        )
        flicker = _arrays(
            "flicker noise",
            reader.read_flicker_noise_data(str(output_dir)),
        )
        shot = _arrays(
            "shot noise", reader.read_shot_noise_data(str(output_dir))
        )
        for label, spectrum in (
            ("thermal noise", thermal),
            ("flicker noise", flicker),
            ("shot noise", shot),
        ):
            if np.allclose(spectrum[1], 0.0, rtol=0.0, atol=0.0):
                raise ValueError(f"{label} density is all zero")
        temperature_values, temperature_data = (
            reader.read_temperature_noise_data(str(output_dir))
        )
        if temperature_values is None or temperature_data is None:
            raise ValueError("temperature noise: reader returned no data")
        if set(temperature_values) != {-40, 0, 27, 50, 100, 150}:
            raise ValueError("temperature noise: incomplete temperature set")
        for temperature in temperature_values:
            spectrum = _arrays(
                f"temperature noise {temperature}",
                temperature_data[temperature],
            )
            if np.allclose(spectrum[1], 0.0, rtol=0.0, atol=0.0):
                raise ValueError(
                    f"temperature noise {temperature} density is all zero"
                )
        component_frequency, component_values = _common_noise_grid(
            thermal, flicker, shot
        )
        thermal_by_bias = reader.read_all_thermal_noise_data(
            str(output_dir)
        )
        if len(thermal_by_bias) != len(thermal_names):
            raise ValueError("not all thermal-noise bias sweeps were parsed")
        plotter.plot_noise_spectrum(
            output_dir,
            *thermal,
            "Thermal Noise Spectrum",
            "noise_thermal_noise",
        )
        plotter.plot_noise_spectrum(
            output_dir,
            *flicker,
            "Flicker Noise Spectrum",
            "noise_flicker_noise",
        )
        plotter.plot_noise_spectrum(
            output_dir,
            *shot,
            "Shot Noise Spectrum",
            "noise_shot_noise",
        )
        plotter.plot_multiple_noise_spectra(
            output_dir,
            thermal_by_bias,
            "Thermal Noise vs. Bias Conditions",
            "noise_thermal_noise_vds_comparison",
        )
        plotter.plot_noise_vs_temperature(
            output_dir, temperature_values, temperature_data
        )
        plotter.plot_noise_components(
            output_dir, component_frequency, *component_values
        )
        sources(
            ("noise_thermal_noise.png",),
            ["thermal_noise_vgs0.6_vds0.6.txt"],
        )
        sources(
            ("noise_flicker_noise.png",), ["flicker_noise.txt"]
        )
        sources(("noise_shot_noise.png",), ["shot_noise.txt"])
        sources(
            ("noise_thermal_noise_vds_comparison.png",), thermal_names
        )
        sources(
            ("noise_vs_temperature.png",), temperature_names,
            "temperature comparison of measured noise spectra",
        )
        sources(
            ("noise_components.png",),
            [
                "thermal_noise_vgs0.6_vds0.6.txt",
                "flicker_noise.txt",
                "shot_noise.txt",
            ],
            "log-frequency interpolation within the common measured range, "
            "then sum of measured component spectra",
        )

    expected = {
        name for mode in modes for name in PLOTS_BY_MODE[mode]
    }
    actual = {path.name for path in plots_dir.glob("*.png")}
    if actual != expected:
        raise ValueError(
            "canonical plot set mismatch: missing=%s extra=%s"
            % (sorted(expected - actual), sorted(actual - expected))
        )
    dimensions = {}
    image_hashes = {}
    from PIL import Image
    for path in plots_dir.glob("*.png"):
        with Image.open(path) as image:
            dimensions[path.name] = list(image.size)
        image_hashes[path.name] = sha256(path)
    (data_dir / "plot_provenance.json").write_text(
        json.dumps(
            {
                "schemaVersion": 2,
                "plots": provenance,
                "dimensions": dimensions,
                "imageSha256": image_hashes,
                "syntheticDataUsed": False,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    return provenance
