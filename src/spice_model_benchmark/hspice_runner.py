"""
HSPICE Simulation Runner: Execute HSPICE simulations and manage output files.

Parallel to SimulationRunner (ngspice) and SpectreRunner but invokes hspice.
Generates HSPICE-compatible netlists on-the-fly from model files.
"""

import os
import re
import math
import subprocess
from pathlib import Path
from typing import Optional, List
import shutil

from .ac_metrics import polar, y_to_s
from .fixture_geometry import apply_primary_geometry, read_geometry_override

HSPICE_HOME = "/eda_hurricane/hspice/hspice/S-2021.09"
HSPICE_BIN = f"{HSPICE_HOME}/hspice/linux64/hspice"
SNPSLMD_LICENSE_FILE = "27000@192.168.1.7"


def _build_hspice_env() -> dict:
    env = os.environ.copy()
    env["SNPSLMD_LICENSE_FILE"] = SNPSLMD_LICENSE_FILE
    env["PATH"] = f"{HSPICE_HOME}/hspice/linux64:{env.get('PATH', '')}"
    return env


def _hspice_float(s: str) -> float:
    """Convert HSPICE number string (with engineering suffixes) to float."""
    s = s.strip().lower()
    if not s:
        return 0.0
    # HSPICE prints mega with the display suffix ``x`` (for example
    # ``1.00000x`` for 1 MHz).
    if s.endswith('x'):
        return float(s[:-1]) * 1e6
    suffix_map = {
        'a': 1e-18, 'f': 1e-15, 'p': 1e-12, 'n': 1e-9,
        'u': 1e-6, 'm': 1e-3, 'k': 1e3, 'g': 1e9, 't': 1e12,
    }
    for suffix, mult in suffix_map.items():
        if s.endswith(suffix) and not s[-1].isdigit():
            num_part = s[:-len(suffix)]
            if num_part and (num_part[-1].isdigit() or num_part[-1] == '.'):
                return float(num_part) * mult
    if s.endswith('meg'):
        return float(s[:-3]) * 1e6
    return float(s)


def _parse_sci(s: str) -> float:
    """Parse scientific notation with possible HSPICE suffixes."""
    try:
        return float(s)
    except ValueError:
        return _hspice_float(s)


def _parameterize_single_point_ac(lines):
    """Make HSPICE execute exactly one requested AC point per .ALTER case.

    HSPICE accumulates analysis cards across .ALTER sections.  Emitting one
    literal ``.AC`` card in every section therefore re-runs earlier frequencies
    and may ignore a later card as a duplicate.  A single global analysis card
    whose frequency is changed by an ALTER-local parameter preserves the AST
    case semantics and avoids ambiguous result tables.
    """
    rewritten = []
    frequencies = []
    for line in lines:
        match = re.fullmatch(
            r"\s*\.ac\s+lin\s+1\s+(\S+)\s+\1\s*",
            line,
            re.IGNORECASE,
        )
        if match:
            frequency = match.group(1)
            frequencies.append(frequency)
            rewritten.append(
                ".PARAM AST_AC_FREQUENCY=%s" % frequency
            )
        else:
            rewritten.append(line)
    if not frequencies:
        return rewritten
    first_alter = next(
        (
            index for index, line in enumerate(rewritten)
            if line.strip().lower().startswith(".alter")
        ),
        None,
    )
    if first_alter is None:
        raise ValueError("parameterized AC deck has no .ALTER cases")
    rewritten[first_alter:first_alter] = [
        ".PARAM AST_AC_FREQUENCY=%s" % frequencies[0],
        ".AC LIN 1 AST_AC_FREQUENCY AST_AC_FREQUENCY",
    ]
    return rewritten


def _parameterize_transient_analyses(lines):
    """Preserve per-case transient controls in one HSPICE ``.ALTER`` deck.

    HSPICE retains the first ``.TRAN`` analysis card when later ``.ALTER``
    sections contain another ``.TRAN`` card.  Consequently, a later case can
    be printed with its requested stop time while still executing with the
    first case's stop time.  Keep one analysis card and vary only parameters,
    which HSPICE does re-evaluate for every ALTER case.

    The values below come directly from the AST-emitted deck.  No benchmark
    duration, step, or start time is supplied here.
    """
    rewritten = []
    cases = []
    flags = None
    tran_pattern = re.compile(r"(?i)^\s*\.tran\s+(.+?)\s*$")

    for line in lines:
        match = tran_pattern.fullmatch(line)
        if not match:
            rewritten.append(line)
            continue

        arguments = match.group(1).split()
        if len(arguments) < 2:
            raise ValueError(f"invalid HSPICE transient analysis: {line}")
        step, stop = arguments[:2]
        tail = arguments[2:]
        start = "0"
        current_flags = []
        if tail and tail[0].lower() != "uic":
            start = tail.pop(0)
        if tail:
            current_flags = [item.lower() for item in tail]
        if any(item != "uic" for item in current_flags):
            raise ValueError(
                "HSPICE transient control cannot be represented losslessly: "
                + line
            )
        if flags is None:
            flags = current_flags
        elif current_flags != flags:
            raise ValueError(
                "HSPICE cannot vary transient startup flags between ALTER "
                "cases in one physical benchmark netlist"
            )

        cases.append((step, stop, start))
        rewritten.append(
            ".PARAM AST_TRAN_STEP=%s AST_TRAN_STOP=%s AST_TRAN_START=%s"
            % (step, stop, start)
        )

    if not cases:
        return rewritten

    first_alter = next(
        (
            index for index, line in enumerate(rewritten)
            if line.strip().lower().startswith(".alter")
        ),
        None,
    )
    if first_alter is None:
        # A single analysis does not suffer from ALTER inheritance and should
        # remain exactly as emitted by the AST.
        if len(cases) == 1:
            return lines
        raise ValueError("parameterized transient deck has no .ALTER cases")

    global_control = [
        ".PARAM AST_TRAN_STEP=%s AST_TRAN_STOP=%s AST_TRAN_START=%s"
        % cases[0],
        ".TRAN AST_TRAN_STEP AST_TRAN_STOP AST_TRAN_START"
        + (" " + " ".join(flags) if flags else ""),
    ]
    rewritten[first_alter:first_alter] = global_control
    return rewritten


# =====================================================================
# Netlist generators
# =====================================================================
def _extract_model_roles(model_file: str) -> tuple:
    """Return primary card, CMOS role cards, and primary polarity."""
    with open(model_file) as f:
        content = f.read()
    cards = [
        (match.group(1), match.group(2).lower())
        for match in re.finditer(
            r'(?i)\.model\s+(\S+)\s+(nmos|pmos)\b',
            content,
        )
    ]
    source = [
        card for card in cards if not card[0].lower().startswith("__fixture_")
    ]
    if not source:
        raise ValueError(
            f"No non-fixture MOS model card found in {model_file}; "
            "HSPICE benchmark fallback models are disabled"
        )
    selected_match = re.search(
        r"(?im)^\s*\*\s*BENCHMARK_PRIMARY_MODEL:\s*(\S+)\s*$",
        content,
    )
    selected_card = None
    if selected_match:
        selected_name = selected_match.group(1)
        selected_card = next(
            (
                card
                for card in source
                if card[0].lower() == selected_name.lower()
            ),
            None,
        )
        if selected_card is None:
            raise ValueError(
                f"Selected benchmark card {selected_name} is not present in "
                f"{model_file}"
            )
    source_nmos = next(
        (re.sub(r"\.\d+$", "", name) for name, kind in source if kind == "nmos"),
        None,
    )
    source_pmos = next(
        (re.sub(r"\.\d+$", "", name) for name, kind in source if kind == "pmos"),
        None,
    )
    if selected_card is not None:
        if selected_card[1] == "nmos":
            source_nmos = selected_card[0]
        else:
            source_pmos = selected_card[0]
    fixture_nmos = next(
        (name for name, kind in cards if kind == "nmos" and name.lower().startswith("__fixture_")),
        None,
    )
    fixture_pmos = next(
        (name for name, kind in cards if kind == "pmos" and name.lower().startswith("__fixture_")),
        None,
    )
    primary = source_nmos or source_pmos
    cmos_nmos = source_nmos or fixture_nmos
    cmos_pmos = source_pmos or fixture_pmos
    if cmos_nmos is None or cmos_pmos is None:
        missing = "NMOS" if cmos_nmos is None else "PMOS"
        raise ValueError(
            f"HSPICE benchmark circuit requires an explicit {missing} model "
            "card; fallback models are disabled"
        )
    return primary, cmos_nmos, cmos_pmos, source_nmos is None and source_pmos is not None


def _extract_model_names(model_file: str) -> tuple:
    """Return the primary single-device card and complementary PMOS role."""
    primary, _, cmos_pmos, _ = _extract_model_roles(model_file)
    return primary, cmos_pmos


def _extract_complementary_names(model_file: str) -> tuple:
    _, cmos_nmos, cmos_pmos, _ = _extract_model_roles(model_file)
    return cmos_nmos, cmos_pmos

def _gen_dc_netlist(model_file: str) -> str:
    model_path = Path(model_file).resolve()
    nmos, pmos = _extract_model_names(model_file)
    return f"""* HSPICE DC with Temperature Sweep
.OPTION POST=1 BRIEF NOMOD
.OPTION RELTOL=1e-8 ABSTOL=1e-12 GMIN=1e-15 METHOD=GEAR
.TEMP -40 0 25 50 100 150
.OPTION TNOM=27
.INC '{model_path}'
M_IV drain_iv gate_iv source_iv bulk_iv {nmos} L=1u W=10u
Vds_iv drain_iv 0 DC 0
Vgs_iv gate_iv 0 DC 0
Vs_iv source_iv 0 DC 0
Vb_iv bulk_iv 0 DC 0
.DC Vds_iv 0 1.2 0.01 SWEEP Vgs_iv 0 1.2 0.2
.PRINT DC I(Vds_iv) I(Vs_iv) I(Vb_iv) I(Vgs_iv)
.END
"""


def _gen_bias_netlist(model_file: str) -> str:
    model_path = Path(model_file).resolve()
    bias_conditions = [
        ("0.0", "0.0"), ("0.0", "0.6"), ("0.0", "1.2"),
        ("0.6", "0.0"), ("0.6", "0.6"), ("0.6", "1.2"),
        ("1.2", "0.0"), ("1.2", "0.6"), ("1.2", "1.2"),
    ]
    alter_blocks = ""
    for idx, (vds_val, vgs_val) in enumerate(bias_conditions):
        if idx == 0:
            continue
        alter_blocks += f"""
.ALTER BIAS_{idx}
Vds_bias drain_bias 0 DC {vds_val}
Vgs_bias gate_bias 0 DC {vgs_val}
.OP
"""
    nmos, pmos = _extract_model_names(model_file)

    return f"""* HSPICE Bias Point
.OPTION POST=1 BRIEF NOMOD RELTOL=1e-8 ABSTOL=1e-12 GMIN=1e-15 TNOM=27
.INC '{model_path}'
M_BIAS drain_bias gate_bias source_bias bulk_bias {nmos} L=1u W=10u
Vds_bias drain_bias 0 DC {bias_conditions[0][0]}
Vgs_bias gate_bias 0 DC {bias_conditions[0][1]}
Vs_bias source_bias 0 DC 0
Vb_bias bulk_bias 0 DC 0
.OP
{alter_blocks}
.END
"""


def _gen_ac_cv_netlist(model_file: str) -> str:
    """HSPICE netlist for CV sweep at multiple frequencies."""
    model_path = Path(model_file).resolve()
    alter_blocks = ""
    vg_values = [round(-0.8 + i * 0.05, 3) for i in range(41)]  # -0.8 to 1.2 step 0.05
    for idx, vg in enumerate(vg_values):
        if idx == 0:
            continue
        alter_blocks += f"""
.ALTER VG_{idx}
VG gate_1 0 DC {vg}
.AC DEC 1 1k 1meg
"""
    nmos, pmos = _extract_model_names(model_file)

    return f"""* HSPICE CV Sweep
.OPTION POST=1 BRIEF NOMOD RELTOL=1e-8 TNOM=27
.INC '{model_path}'
M1 drain_1 gate_1 source_1 bulk_1 {nmos} L=1u W=10u
VG gate_1 0 DC {vg_values[0]} AC 1
VD drain_1 0 DC 1.0
VS source_1 0 DC 0
VB bulk_1 0 DC 0
.AC DEC 1 1k 1meg
.PRINT AC II(VG) IR(VG) II(VB) IR(VB) II(VS) IR(VS) II(VD) IR(VD)
{alter_blocks}
.END
"""


def _gen_ac_sp_netlist(model_file: str) -> str:
    """HSPICE netlist for S-parameter extraction at multiple frequencies."""
    model_path = Path(model_file).resolve()
    alter_blocks = ""
    for f in ["1e6", "1e7", "1e8", "1e9"]:
        alter_blocks += f"""
.ALTER F_{f.replace("e","")}
.AC LIN 1 {f} {f}
"""
    nmos, pmos = _extract_model_names(model_file)

    return f"""* HSPICE S-Parameter Test
.OPTION POST=1 BRIEF NOMOD RELTOL=1e-8 TNOM=27
.INC '{model_path}'
M2 drain_2 gate_2 0 0 {nmos} L=1u W=10u
RG gate_2 gate_in2 50
RD drain_2 drain_in2 50
VGS gate_in2 0 DC 0.8 AC 1
VDS drain_in2 0 DC 1.0 AC 0
.AC LIN 1 1e6 1e6
.PRINT AC VR(gate_in2) VI(gate_in2) VR(drain_in2) VI(drain_in2) II(VGS) IR(VGS) II(VDS) IR(VDS)
{alter_blocks}
.END
"""


def _gen_ac_nqs_netlist(model_file: str) -> str:
    """HSPICE netlist for NQS phase shift at high frequencies."""
    model_path = Path(model_file).resolve()
    nmos, pmos = _extract_model_names(model_file)

    return f"""* HSPICE NQS Effects
.OPTION POST=1 BRIEF NOMOD RELTOL=1e-8 TNOM=27
.INC '{model_path}'
M1 drain_1 gate_1 source_1 bulk_1 {nmos} L=1u W=10u
VG gate_1 0 DC 0.8 AC 1
VD drain_1 0 DC 1.0
VS source_1 0 DC 0
VB bulk_1 0 DC 0
.AC LIN 1 1e7 1e7
.AC LIN 1 1e8 1e8
.AC LIN 1 1e9 1e9
.AC LIN 1 1e10 1e10
.PRINT AC VR(gate_1) VI(gate_1) II(VD) IR(VD)
.END
"""


def _gen_ac_charge_netlist(model_file: str) -> str:
    """HSPICE netlist for charge conservation transient test."""
    model_path = Path(model_file).resolve()
    nmos, pmos = _extract_model_names(model_file)

    return f"""* HSPICE Charge Conservation
.OPTION POST=1 BRIEF NOMOD RELTOL=1e-8 TNOM=27
.INC '{model_path}'
M3 drain_3 gate_3 source_3 bulk_3 {nmos} L=1u W=10u
VGQ gate_3 0 DC 0 PWL(0 0 1n 0 1.01n 1.0 5n 1.0)
VDQ drain_3 0 DC 1.0
VSQ source_3 0 DC 0
VBQ bulk_3 0 DC 0
.TRAN 0.01n 5n
.PRINT TRAN V(gate_3) I(VGQ) I(VDQ) I(VSQ) I(VBQ)
.END
"""


def _gen_tran_large_signal_netlist(model_file: str) -> str:
    model_path = Path(model_file).resolve()
    nmos, pmos = _extract_model_names(model_file)

    return f"""* HSPICE Large-Signal Transient
.OPTION POST=1 BRIEF NOMOD RELTOL=1e-8 TNOM=27
.INC '{model_path}'
M_tran drain_tran gate_tran source_tran bulk_tran {nmos} L=1u W=10u
Vgs_tran gate_tran 0 PULSE(0 1.2 0n 0.1n 0.1n 10n 20n)
Vds_tran drain_tran 0 DC 1.2
Vs_tran source_tran 0 DC 0
Vb_tran bulk_tran 0 DC 0
Cload drain_tran 0 1f
.TRAN 0.01n 100n
.PRINT TRAN V(gate_tran) V(drain_tran) I(Vds_tran) I(Vgs_tran) I(Vs_tran) I(Vb_tran)
.END
"""


def _gen_tran_switching_netlist(model_file: str) -> str:
    model_path = Path(model_file).resolve()
    nmos, pmos = _extract_complementary_names(model_file)

    return f"""* HSPICE Switching/Inverter
.OPTION POST=1 BRIEF NOMOD RELTOL=1e-8 TNOM=27
.INC '{model_path}'
M_inv_n out_inv in_inv 0 0 {nmos} L=1u W=10u
M_inv_p out_inv in_inv vdd_inv vdd_inv {pmos} L=1u W=20u
Vdd_inv vdd_inv 0 DC 1.2
Vin_inv in_inv 0 PULSE(0 1.2 0n 0.1n 0.1n 10n 20n)
Cload_inv out_inv 0 1f
.TRAN 0.01n 100n
.PRINT TRAN V(in_inv) V(out_inv) I(Vdd_inv)
.END
"""


def _gen_tran_delay_netlist(model_file: str) -> str:
    model_path = Path(model_file).resolve()
    nmos, pmos = _extract_complementary_names(model_file)

    return f"""* HSPICE Delay Chain (3 inverters)
.OPTION POST=1 BRIEF NOMOD RELTOL=1e-8 TNOM=27
.INC '{model_path}'
M_d1_n mid1_delay in_delay 0 0 {nmos} L=1u W=10u
M_d1_p mid1_delay in_delay vdd_delay vdd_delay {pmos} L=1u W=20u
Cload_d1 mid1_delay 0 1f
M_d2_n mid2_delay mid1_delay 0 0 {nmos} L=1u W=10u
M_d2_p mid2_delay mid1_delay vdd_delay vdd_delay {pmos} L=1u W=20u
Cload_d2 mid2_delay 0 1f
M_d3_n out_delay mid2_delay 0 0 {nmos} L=1u W=10u
M_d3_p out_delay mid2_delay vdd_delay vdd_delay {pmos} L=1u W=20u
Cload_d3 out_delay 0 1f
Vdd_delay vdd_delay 0 DC 1.2
Vin_delay in_delay 0 PULSE(0 1.2 0n 0.1n 0.1n 10n 20n)
.TRAN 0.01n 100n
.PRINT TRAN V(in_delay) V(mid1_delay) V(mid2_delay) V(out_delay)
.END
"""


def _gen_tran_power_netlist(model_file: str, temp: int) -> str:
    model_path = Path(model_file).resolve()
    nmos, pmos = _extract_complementary_names(model_file)

    return f"""* HSPICE Power Dissipation at {temp}C
.OPTION POST=1 BRIEF NOMOD RELTOL=1e-8 TNOM=27 TEMP={temp}
.INC '{model_path}'
M_power_n out_power in_power 0 0 {nmos} L=1u W=10u
M_power_p out_power in_power vdd_power vdd_power {pmos} L=1u W=20u
Vdd_power vdd_power 0 DC 1.2
Vin_power in_power 0 PULSE(0 1.2 0n 0.1n 0.1n 10n 20n)
Cload_power out_power 0 1f
.TRAN 0.01n 100n
.PRINT TRAN V(in_power) V(out_power) I(Vdd_power)
.END
"""


def _gen_tran_qs_netlist(model_file: str) -> str:
    model_path = Path(model_file).resolve()
    nmos, pmos = _extract_model_names(model_file)

    return f"""* HSPICE Quasi-Static
.OPTION POST=1 BRIEF NOMOD RELTOL=1e-8 TNOM=27
.INC '{model_path}'
M_qs drain_qs gate_qs source_qs bulk_qs {nmos} L=1u W=10u
Vgs_qs gate_qs 0 PULSE(0 1.2 0n 20n 20n 100n 200n)
Vds_qs drain_qs 0 DC 1.2
Vs_qs source_qs 0 DC 0
Vb_qs bulk_qs 0 DC 0
Cload_qs drain_qs 0 10f
.TRAN 0.1n 500n
.PRINT TRAN V(gate_qs) V(drain_qs) I(Vds_qs)
.END
"""


def _gen_tran_charge_netlist(model_file: str) -> str:
    model_path = Path(model_file).resolve()
    nmos, pmos = _extract_model_names(model_file)

    return f"""* HSPICE Transient Charge
.OPTION POST=1 BRIEF NOMOD RELTOL=1e-8 TNOM=27
.INC '{model_path}'
M_charge drain_charge gate_charge source_charge bulk_charge {nmos} L=1u W=10u
Vdd_charge vdd_charge 0 DC 1.2
Vg_charge gate_charge 0 PULSE(0 1.2 0n 1n 1n 10n 20n)
Vd_charge drain_charge 0 DC 1.2
Vs_charge source_charge 0 DC 0
Vb_charge bulk_charge 0 DC 0
Cg gate_charge 0 1e-18
Cd drain_charge 0 1e-18
Cs source_charge 0 1e-18
Cb bulk_charge 0 1e-18
.TRAN 0.01n 100n
.PRINT TRAN V(gate_charge) I(Vg_charge) I(Vd_charge) I(Vs_charge) I(Vb_charge)
.END
"""


def _gen_noise_thermal_netlist(
    model_file: str, vgs: float, vds: float
) -> str:
    model_path = Path(model_file).resolve()
    nmos, pmos = _extract_model_names(model_file)
    return f"""* HSPICE Thermal Noise Vgs={vgs} Vds={vds}
.OPTION POST=1 BRIEF NOMOD RELTOL=1e-8 TNOM=27
.INC '{model_path}'
Vdd_noise vdd_noise 0 DC 1.2
Vin_noise in_noise 0 DC {vgs} AC 1
Rb_noise in_noise gate_noise 1k
Cb_noise in_noise gate_noise 1u
Rs_noise source_noise 0 100
Rd_noise vdd_noise drain_noise 10k
Vgs_noise gate_noise source_noise DC 0
Vds_noise drain_noise source_noise DC 0
Vbulk_noise bulk_noise 0 DC 0
M_noise drain_noise gate_noise source_noise bulk_noise {nmos} L=1u W=10u
.NOISE V(drain_noise) Vin_noise DEC 20 1 1G
.END
"""


def _gen_noise_flicker_netlist(model_file: str) -> str:
    model_path = Path(model_file).resolve()
    nmos, pmos = _extract_model_names(model_file)

    return f"""* HSPICE Flicker Noise
.OPTION POST=1 BRIEF NOMOD RELTOL=1e-8 TNOM=27
.INC '{model_path}'
Vin_f flicker_in 0 DC 0 AC 1
Rin_f flicker_in flicker_gate 1k
Vbias_f flicker_vdd 0 DC 1.2
Vgs_flicker flicker_gate_bias 0 DC 0.6
M_flicker flicker_drain flicker_gate flicker_source flicker_bulk {nmos} L=1u W=10u
Vgs_inp_f flicker_gate flicker_gate_bias DC 0
Rout_f flicker_drain flicker_vdd 10k
Vbulk_f flicker_bulk 0 DC 0
Vsrc_f flicker_source 0 DC 0
.NOISE V(flicker_drain) Vin_f DEC 20 0.1 1MEG
.END
"""


def _gen_noise_shot_netlist(model_file: str) -> str:
    model_path = Path(model_file).resolve()
    nmos, pmos = _extract_model_names(model_file)

    return f"""* HSPICE Shot Noise
.OPTION POST=1 BRIEF NOMOD RELTOL=1e-8 TNOM=27
.INC '{model_path}'
Vdd_shot shot_vdd 0 DC 1.2 AC 1
Vgs_shot shot_gate 0 DC 0.9
Rload_shot shot_vdd shot_drain 10k
M_shot shot_drain shot_gate shot_source shot_bulk {nmos} L=1u W=10u
Vbulk_shot shot_bulk 0 DC 0
Vsrc_shot shot_source 0 DC 0
.NOISE V(shot_drain) Vdd_shot DEC 20 1 1G
.END
"""


def _gen_noise_temp_netlist(model_file: str, temp: int) -> str:
    model_path = Path(model_file).resolve()
    nmos, pmos = _extract_model_names(model_file)

    return f"""* HSPICE Temperature Noise T={temp}
.OPTION POST=1 BRIEF NOMOD RELTOL=1e-8 TNOM=27 TEMP={temp}
.INC '{model_path}'
Vdd_noise vdd_noise 0 DC 1.2
Vin_noise in_noise 0 DC 0.6 AC 1
Rb_noise in_noise gate_noise 1k
Cb_noise in_noise gate_noise 1u
Rs_noise source_noise 0 100
Rd_noise vdd_noise drain_noise 10k
Vgs_noise gate_noise source_noise DC 0
Vds_noise drain_noise source_noise DC 0
Vbulk_noise bulk_noise 0 DC 0
M_noise drain_noise gate_noise source_noise bulk_noise {nmos} L=1u W=10u
.NOISE V(drain_noise) Vin_noise DEC 20 1 1G
.END
"""


def _adapt_primary_polarity(model_file: str, netlist: str) -> str:
    """Apply sign-correct single-device biases for a PMOS primary card."""
    _, _, _, primary_is_pmos = _extract_model_roles(model_file)
    if not primary_is_pmos:
        return netlist

    def flipped(raw: str) -> str:
        value = float(raw)
        # Polarity adaptation can be reached through both the shared
        # canonical-deck path and a simulator-native generator.  Make it
        # idempotent so an already-negative PMOS bias is never flipped back
        # to a positive NMOS bias.
        return raw if value == 0.0 else f"{-abs(value):g}"

    netlist = re.sub(
        r"(?im)^(\s*V\w+\b.*?\bDC\s+)([-+]?(?:\d+(?:\.\d*)?|\.\d+))",
        lambda match: match.group(1) + flipped(match.group(2)),
        netlist,
    )
    netlist = re.sub(
        r"(?i)(PULSE\(\s*0\s+)([-+]?(?:\d+(?:\.\d*)?|\.\d+))",
        lambda match: match.group(1) + flipped(match.group(2)),
        netlist,
    )
    netlist = re.sub(
        r"(?i)(PWL\(\s*0\s+0\s+1n\s+0\s+1\.01n\s+)"
        r"([-+]?(?:\d+(?:\.\d*)?|\.\d+))"
        r"(\s+5n\s+)([-+]?(?:\d+(?:\.\d*)?|\.\d+))",
        lambda match: (
            match.group(1) + flipped(match.group(2))
            + match.group(3) + flipped(match.group(4))
        ),
        netlist,
    )
    netlist = re.sub(
        r"(?im)^(\s*\.DC\s+V\w+\s+)"
        r"([-+]?(?:\d+(?:\.\d*)?|\.\d+))\s+"
        r"([-+]?(?:\d+(?:\.\d*)?|\.\d+))\s+"
        r"([-+]?(?:\d+(?:\.\d*)?|\.\d+))"
        r"(\s+SWEEP\s+V\w+\s+)"
        r"([-+]?(?:\d+(?:\.\d*)?|\.\d+))\s+"
        r"([-+]?(?:\d+(?:\.\d*)?|\.\d+))\s+"
        r"([-+]?(?:\d+(?:\.\d*)?|\.\d+))",
        lambda match: (
            match.group(1)
            + " ".join(flipped(match.group(index)) for index in (2, 3, 4))
            + match.group(5)
            + " ".join(flipped(match.group(index)) for index in (6, 7, 8))
        ),
        netlist,
    )
    return netlist


def _primary_generator(function):
    def wrapped(model_file, *args, **kwargs):
        return _adapt_primary_polarity(
            model_file,
            function(model_file, *args, **kwargs),
        )
    return wrapped


for _generator_name in (
    "_gen_dc_netlist",
    "_gen_bias_netlist",
    "_gen_ac_cv_netlist",
    "_gen_ac_sp_netlist",
    "_gen_ac_nqs_netlist",
    "_gen_ac_charge_netlist",
    "_gen_tran_large_signal_netlist",
    "_gen_tran_qs_netlist",
    "_gen_tran_charge_netlist",
    "_gen_noise_thermal_netlist",
    "_gen_noise_flicker_netlist",
    "_gen_noise_shot_netlist",
    "_gen_noise_temp_netlist",
):
    globals()[_generator_name] = _primary_generator(globals()[_generator_name])


# =====================================================================
# Output file writers (match ngspice format exactly)
# =====================================================================

def _write_noise_ngspice_format(
    path: Path, freq: list, noise: list, title: str = "noise analysis"
):
    """Write noise data in ngspice raw format expected by DataReader."""
    lines = [
        f"Title: * {title}",
        "Date: Tue Jul 21 14:35:27  2026",
        "Command: hspice S-2021.09",
        "Plotname: Noise Spectral Density Curves",
        "Flags: real",
        "No. Variables: 3",
        f"No. Points: {len(freq)}",
        "Variables:",
        "\t0\tfrequency\tfrequency grid=3",
        "\t1\tfreq\tfrequency",
        "\t2\tnoise_spectrum\tvoltage-density",
        "Values:",
    ]
    for i, (f, n) in enumerate(zip(freq, noise)):
        lines.append(f" {i}\t{f:.10e}")
        lines.append(f"\t{f:.10e}")
        lines.append(f"\t{n:.10e}")
        lines.append("")
    path.write_text('\n'.join(lines))


def _write_tran_ngspice_format(
    path: Path, time: list, cols: list, col_names: str, dup_time: bool = True
):
    """Write transient data in ngspice wrdata format.

    ngspice wrdata with wr_vecnames outputs: time time col1 col2 ...
    (time is duplicated in the first two columns).
    """
    ncols = len(cols)
    lines = [col_names]
    for i in range(len(time)):
        t_str = f"{time[i]:.6e}"
        row = [t_str]
        if dup_time:
            row.append(t_str)
        for c in range(ncols):
            row.append(f"{cols[c][i]:.6e}" if i < len(cols[c]) else "0.000000e+00")
        lines.append(' '.join(row))
    path.write_text('\n'.join(lines))


# =====================================================================
# LIS Parsers
# =====================================================================

def _parse_print_table(lis_path: Path, column_count: int) -> dict:
    """Parse HSPICE .PRINT AC/TRAN table from .lis file.

    HSPICE .PRINT output format:
      ****** ac analysis tnom= 27.000 temp= 27.000 ******
      x
      freq       ii(vg)     ir(vg)     ...
      1.000e+03  1.234e-05  5.678e-06  ...

    Returns dict with 'freq' key and column data lists.
    """
    if not lis_path.exists():
        return {}
    content = lis_path.read_text(errors='replace')
    lines = content.split('\n')

    all_data = {}
    current_freq = None
    in_table = False
    header_skip = 0
    col_data = []
    freq_data = []

    for line in lines:
        stripped = line.strip()

        # Detect analysis section header
        if ('ac analysis' in stripped.lower() or
            'transient analysis' in stripped.lower()) and '******' in stripped:
            current_freq = None
            in_table = False
            header_skip = 0
            continue

        # 'x' marker before column headers
        if stripped == 'x':
            in_table = True
            header_skip = 0
            col_data = []
            freq_data = []
            continue

        # Skip headers
        if in_table and header_skip < 3:
            if stripped and not stripped.startswith('*'):
                try:
                    _parse_sci(stripped.split()[0])
                except (ValueError, IndexError):
                    header_skip += 1
                    continue
                # Also try: if the first word looks like it could be a number
                parts = stripped.split()
                if parts:
                    first = parts[0]
                    if any(c.isdigit() for c in first):
                        pass  # This IS a data row
                    else:
                        header_skip += 1
                        continue
            else:
                if not stripped:
                    header_skip += 1
                continue

        # Data rows
        if in_table:
            if not stripped or stripped.startswith('*'):
                in_table = False
                continue

            parts = stripped.split()
            if len(parts) >= 2:
                try:
                    val = _parse_sci(parts[0])
                    freq_data.append(val)
                    row_data = [_parse_sci(p) for p in parts[1:]]
                    col_data.append(row_data)
                except (ValueError, IndexError):
                    in_table = False

    if freq_data and col_data:
        all_data['freq'] = freq_data
        all_data['columns'] = col_data

    return all_data


def _parse_ac_table_columns(
    lis_path: Path, col_names: list, section_filter: str = None
) -> dict:
    """Parse .PRINT AC output and extract named columns."""
    if not lis_path.exists():
        return {}

    content = lis_path.read_text(errors='replace')
    result = {name: [] for name in col_names}
    result['freq'] = []
    result['_sections'] = []

    # Split into analysis sections
    sections = re.split(
        r'\*{4,}\s*(?:ac|transient)\s+analysis.*?\*{4,}',
        content, flags=re.IGNORECASE
    )

    for sec in sections[1:]:  # Skip pre-amble
        # Find data table in this section
        lines = sec.split('\n')
        in_table = False
        header_skip = 0
        sec_freq = []
        sec_data = [[] for _ in col_names]

        for line in lines:
            stripped = line.strip()
            if stripped == 'x':
                in_table = True
                header_skip = 0
                continue
            if in_table and header_skip < 4:
                if stripped and not stripped.startswith('*'):
                    parts = stripped.split()
                    if parts:
                        try:
                            _parse_sci(parts[0])
                        except ValueError:
                            header_skip += 1
                            continue
                else:
                    header_skip += 1
                    continue
            if in_table and stripped and not stripped.startswith('*'):
                parts = stripped.split()
                if len(parts) >= len(col_names) + 1:
                    try:
                        freq = _parse_sci(parts[0])
                        sec_freq.append(freq)
                        for ci in range(len(col_names)):
                            sec_data[ci].append(_parse_sci(parts[1 + ci]))
                    except (ValueError, IndexError):
                        in_table = False

        if sec_freq:
            result['_sections'].append({'freq': sec_freq, 'data': sec_data})

    return result


def _parse_noise_lis_table(lis_path: Path) -> tuple:
    """Parse HSPICE .NOISE output from .lis file.

    HSPICE noise output:
      ****** noise analysis tnom= 27.000 temp= 27.000 ******
      x
      frequency  onoise      inoise
      1.000e+00  5.678e-15   1.234e-18  ...

    Returns (freq_list, noise_list) where noise = onoise (output noise V/rtHz).
    """
    if not lis_path.exists():
        return [], []

    content = lis_path.read_text(errors='replace')
    lines = content.split('\n')

    freq_data = []
    noise_data = []
    in_noise_section = False
    after_x = False
    seen_header = False

    for line in lines:
        stripped = line.strip()

        if 'noise analysis' in stripped.lower() and '******' in stripped:
            in_noise_section = True
            after_x = False
            seen_header = False
            continue

        if not in_noise_section:
            continue

        if stripped == 'x':
            after_x = True
            seen_header = False
            continue

        if not after_x:
            continue

        if not stripped:
            continue

        if stripped.startswith('*'):
            if freq_data:
                in_noise_section = False
                after_x = False
            continue

        parts = stripped.split()
        if not parts:
            continue

        try:
            freq = _parse_sci(parts[0])
            # First token is a number -> data row
            if len(parts) >= 2:
                freq_data.append(freq)
                # Second column is output noise (V^2/Hz or V/rtHz)
                noise_data.append(_parse_sci(parts[1]))
        except (ValueError, IndexError):
            # Header line - skip
            seen_header = True
            continue

    return freq_data, noise_data


def _parse_trans_table(lis_path: Path, col_count: int) -> tuple:
    """Parse HSPICE .PRINT TRAN/AC table from .lis file.

    HSPICE format:
      ****** transient analysis ******
      x
       time     voltage   voltage   current   current
                node1     node2     v_src1    v_src2
       0.       0.        1.2000    -1.17u    13.39n
       ...

    Returns (time_list, [col1_list, col2_list, ...]).
    """
    if not lis_path.exists():
        return [], []

    content = lis_path.read_text(errors='replace')
    lines = content.split('\n')

    time_data = []
    all_cols = [[] for _ in range(col_count)]
    in_table = False
    after_x = False
    seen_type_header = False  # 'time voltage voltage current...'
    seen_name_header = False  # 'node1 node2 v_src1...'

    for line in lines:
        stripped = line.strip()

        # Detect 'x' marker
        if stripped == 'x':
            after_x = True
            seen_type_header = False
            seen_name_header = False
            in_table = False
            continue

        if not after_x:
            continue

        # Skip empty lines after 'x'
        if not stripped:
            if seen_name_header and not in_table:
                in_table = True
            continue

        if stripped.startswith('*'):
            if in_table:
                in_table = False
                after_x = False
            continue

        # Check if this is header or data
        parts = stripped.split()
        if not parts:
            continue

        try:
            _parse_sci(parts[0])
            # First token is a number -> this is a data row
            if not in_table:
                if seen_name_header:
                    in_table = True
                else:
                    continue

            if len(parts) >= 2:
                time_data.append(_parse_sci(parts[0]))
                for ci in range(col_count):
                    idx = ci + 1
                    if idx < len(parts):
                        all_cols[ci].append(_parse_sci(parts[idx]))
                    else:
                        all_cols[ci].append(0.0)
        except (ValueError, IndexError):
            # Not a number -> header line
            first = parts[0].lower()
            if first in ('time', 'freq', 'frequency', 'volt', 'voltage',
                         'current', 'power'):
                seen_type_header = True
            elif seen_type_header:
                seen_name_header = True
            elif not seen_type_header:
                seen_type_header = True  # Single-row header

    return time_data, all_cols


def _parse_named_analyses(lis_path: Path) -> list:
    """Parse all paged .PRINT tables and retain their signal names."""
    if not lis_path.exists():
        return []
    lines = lis_path.read_text(errors="replace").splitlines()
    analyses = []
    current_case = None
    current = None
    index = 0
    while index < len(lines):
        stripped = lines[index].strip()
        case_match = re.fullmatch(r"(?i)ast_case_(\d+)", stripped)
        if case_match:
            current_case = int(case_match.group(1))
        analysis_match = re.search(
            r"(?i)\*{4,}\s*(dc transfer curves|transient analysis|"
            r"ac analysis|noise analysis).*?temp=\s*(-?[\d.]+)",
            stripped,
        )
        if analysis_match:
            current = {
                "case": current_case,
                "kind": analysis_match.group(1).lower(),
                "temp": float(analysis_match.group(2)),
                "values": {},
            }
            analyses.append(current)
        if stripped != "x" or current is None:
            index += 1
            continue

        index += 1
        header_lines = []
        rows = []
        while index < len(lines):
            candidate = lines[index].strip()
            if candidate.lower() == "y":
                break
            parts = candidate.split()
            if not parts:
                index += 1
                continue
            try:
                row = [_parse_sci(token) for token in parts]
            except ValueError:
                if not rows and not candidate.startswith("*"):
                    header_lines.append(parts)
                elif rows:
                    break
            else:
                if rows or header_lines:
                    rows.append(row)
            index += 1
        if rows and header_lines:
            names = header_lines[-1]
            types = header_lines[0]
            axis = types[0].lower()
            if axis == "volt":
                axis = "sweep"
            elif axis in {"freq", "frequency"}:
                axis = "frequency"
            if len(types) - 1 == 2 * len(names):
                headers = [axis] + [
                    f"{name.lower()}_{types[2 * offset + 2].lower()}"
                    for offset, name in enumerate(names)
                ]
            else:
                normalized_names = [name.lower() for name in names]
                duplicate_names = {
                    name
                    for name in normalized_names
                    if normalized_names.count(name) > 1
                }
                headers = [axis]
                for offset, name in enumerate(normalized_names):
                    if name in duplicate_names and offset + 1 < len(types):
                        headers.append(
                            f"{name}_{types[offset + 1].lower()}"
                        )
                    else:
                        headers.append(name)
            width = min(len(headers), min(len(row) for row in rows))
            for column in range(width):
                current["values"][headers[column]] = [
                    row[column] for row in rows
                ]
        index += 1
    return analyses


# =====================================================================
# Main Runner Class
# =====================================================================

class HspiceRunner:
    """Handles running HSPICE simulations and managing output files."""

    def __init__(
        self, logger, output_dir='results', model_file=None, circuit_files=None
    ):
        self.logger = logger
        self.output_dir = output_dir
        self.model_file = model_file
        self.circuit_files = circuit_files or {}
        self.output_dir_path = Path(output_dir).resolve()
        self.output_dir_path.mkdir(exist_ok=True)
        self.data_dir = self.output_dir_path / 'data'
        self.data_dir.mkdir(exist_ok=True)
        self.netlist_dir = self.output_dir_path / 'netlists'
        self.netlist_dir.mkdir(exist_ok=True)
        self._env = _build_hspice_env()
        if not model_file:
            raise ValueError(
                "HSPICE benchmark requires an explicit MOS model file; "
                "fallback models are disabled"
            )
        (
            self._primary,
            self._nmos,
            self._pmos,
            self._primary_is_pmos,
        ) = _extract_model_roles(model_file)
        from .hspice_post_processor import HspicePostProcessor
        self.post_processor = HspicePostProcessor(logger, output_dir=str(self.output_dir_path))

    def _run_hspice(self, netlist_path: Path, out_prefix: str) -> bool:
        try:
            work_dir = self.netlist_dir
            self.logger.logger.info(f"Running HSPICE: {netlist_path.name}")
            original_dir = Path.cwd()
            try:
                os.chdir(work_dir)
                cmd = [
                    HSPICE_BIN, "-i", str(netlist_path.resolve()),
                    "-o", str(work_dir / out_prefix),
                ]
                process = subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    text=True, env=self._env,
                )
                stdout, stderr = process.communicate()
                lis_file = work_dir / f"{out_prefix}.lis"
                if lis_file.exists():
                    if ">error" in lis_file.read_text(errors='replace'):
                        self.logger.logger.error("HSPICE reported errors")
                        return False
                if process.returncode != 0:
                    self.logger.logger.error(f"HSPICE failed rc={process.returncode}")
                    return False
                self.logger.logger.info("HSPICE completed")
                return True
            finally:
                os.chdir(original_dir)
        except Exception as e:
            self.logger.logger.error(f"HSPICE error: {e}")
            return False

    # ===== DC =====

    @staticmethod
    def _parse_dc(lis_path, data_dir, logger):
        if not lis_path.exists():
            return False
        content = lis_path.read_text(errors='replace')
        lines = content.split('\n')
        TEMPS = [-40, 0, 25, 50, 100, 150]
        current_temp = None
        current_vgs = None
        after_x = False
        hdr_skip = 0
        temp_data = {}

        for line in lines:
            m = re.search(r'dc transfer curves.*?temp=\s*(-?\d+\.?\d*)', line)
            if m and '******' in line:
                current_temp = float(m.group(1))
                current_vgs = None
                after_x = False
                hdr_skip = 0
                if current_temp not in temp_data:
                    temp_data[current_temp] = []
                continue
            m = re.search(r'parameter\s+\d+:vgs_iv\s*=\s*(-?[\d.]+[a-zA-Z]*)', line)
            if m and '***' in line:
                current_vgs = _hspice_float(m.group(1))
                after_x = False
                hdr_skip = 0
                continue
            if line.strip() == 'x':
                after_x = True
                hdr_skip = 0
                continue
            if after_x and hdr_skip < 3:
                s = line.strip()
                if s and not s.startswith('*'):
                    parts = s.split()
                    if parts:
                        try:
                            _hspice_float(parts[0])
                        except ValueError:
                            hdr_skip += 1
                            continue
                else:
                    hdr_skip += 1
                    continue
            if after_x:
                s = line.strip()
                if not s or s.startswith('*'):
                    after_x = False
                    hdr_skip = 0
                    continue
                parts = s.split()
                if len(parts) >= 5:
                    try:
                        vd = _hspice_float(parts[0])
                        ivds = _hspice_float(parts[1])
                        ivs = _hspice_float(parts[2])
                        ivb = _hspice_float(parts[3])
                        ivgs = _hspice_float(parts[4])
                        if current_temp is not None and current_vgs is not None:
                            temp_data[current_temp].append({
                                'vgs': current_vgs, 'v_drain': vd,
                                'i_vds': ivds, 'i_vs': ivs,
                                'i_vb': ivb, 'i_vgs': ivgs,
                            })
                    except (ValueError, IndexError):
                        after_x = False
                        hdr_skip = 0

        logger.info(
            f"Parsed {sum(len(v) for v in temp_data.values())} DC points "
            f"across {len(temp_data)} temps"
        )
        tw = 0
        for et in TEMPS:
            if not temp_data:
                break
            at = min(temp_data.keys(), key=lambda t: abs(t - et))
            if abs(at - et) > 5:
                continue
            rows = temp_data[at]
            if not rows:
                continue
            out = [
                "v-sweep v(drain_iv) v(gate_iv) id is ib ig kcl"
            ]
            for r in rows:
                kcl = abs(r['i_vds'] + r['i_vs'] + r['i_vb'] + r['i_vgs'])
                out.append(
                    f"{r['v_drain']:.6e} {r['v_drain']:.6e} "
                    f"{r['vgs']:.6e} {r['i_vds']:.6e} "
                    f"{r['i_vs']:.6e} {r['i_vb']:.6e} "
                    f"{r['i_vgs']:.6e} {kcl:.6e}"
                )
            (data_dir / f"iv_data_{int(et)}.txt").write_text('\n'.join(out))
            logger.info(f"  Written: iv_data_{int(et)}.txt ({len(out) - 1} pts)")
            tw += 1
        return tw > 0

    @staticmethod
    def _parse_bias(lis_path, data_dir, logger):
        if not lis_path.exists():
            return False
        content = lis_path.read_text(errors='replace')
        conds = [
            (0.0, 0.0), (0.0, 0.6), (0.0, 1.2),
            (0.6, 0.0), (0.6, 0.6), (0.6, 1.2),
            (1.2, 0.0), (1.2, 0.6), (1.2, 1.2),
        ]
        out = ["v(drain_bias) v(gate_bias) id_bias ig_bias is_bias ib_bias"]
        pattern = r'element\s+\d+:m_bias\b(.*?)(?=element\s+\d+:m_bias|$)'
        sections = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
        if len(sections) != len(conds):
            logger.error(
                "HSPICE bias parser expected 9 measured operating points, "
                f"found {len(sections)}"
            )
            return False
        for i, sec in enumerate(sections):
            vds, vgs = conds[i]
            id_m = re.search(r'\bid\b\s+(-?[\d.]+(?:[eE][+-]?\d+)?)', sec)
            ig_m = re.search(r'\big\b\s+(-?[\d.]+(?:[eE][+-]?\d+)?)', sec)
            is_m = re.search(r'\bis\b\s+(-?[\d.]+(?:[eE][+-]?\d+)?)', sec)
            ib_m = re.search(r'\bib\b\s+(-?[\d.]+(?:[eE][+-]?\d+)?)', sec)
            if not all((id_m, ig_m, is_m, ib_m)):
                logger.error(
                    f"HSPICE bias point {i} is missing a measured current"
                )
                return False
            out.append(
                f"{vds:.1f} {vgs:.1f} "
                f"{id_m.group(1)} {ig_m.group(1)} "
                f"{is_m.group(1)} {ib_m.group(1)}"
            )
        (data_dir / "bias_point_data.txt").write_text('\n'.join(out))
        logger.info(f"  Written: bias_point_data.txt ({len(out) - 1} pts)")
        return True

    # ===== AC =====

    def _run_ac_cv(self):
        """Run CV sweep and generate cv_data.txt."""
        self.logger.logger.info("  AC CV sweep...")
        netlist = _gen_ac_cv_netlist(self.model_file)
        p = self.netlist_dir / "hspice_ac_cv.sp"
        p.write_text(netlist)
        if not self._run_hspice(p, "ac_cv"):
            return False

        lis = self.netlist_dir / "ac_cv.lis"
        if not lis.exists():
            return False

        # Parse HSPICE AC output: for each Vg bias, extract C = -imag(I)/(2*pi*f)
        content = lis.read_text(errors='replace')
        vg_vals = [round(-0.8 + i * 0.05, 3) for i in range(41)]
        freqs_hz = [1e3, 1e4, 1e5, 1e6]

        all_cv = {vg: {} for vg in vg_vals}
        lines = content.split('\n')
        data_rows = []
        pending = {}
        for index, line in enumerate(lines):
            labels = line.lower().split()
            if labels not in (["vg", "vg", "vb", "vb"], ["vs", "vs", "vd", "vd"]):
                continue
            group_rows = []
            for candidate in lines[index + 1:]:
                stripped = candidate.strip()
                if stripped.lower() == "y":
                    break
                parts = stripped.split()
                if len(parts) < 5:
                    continue
                try:
                    group_rows.append(
                        (
                            _parse_sci(parts[0]),
                            _parse_sci(parts[1]),
                            _parse_sci(parts[3]),
                        )
                    )
                except ValueError:
                    continue
            if labels[0] == "vg":
                pending = {
                    frequency: {
                        "freq": frequency,
                        "ii_vg": first_imag,
                        "ii_vb": second_imag,
                    }
                    for frequency, first_imag, second_imag in group_rows
                }
            elif pending:
                for frequency, first_imag, second_imag in group_rows:
                    match = next(
                        (
                            key
                            for key in pending
                            if math.isclose(
                                key,
                                frequency,
                                rel_tol=1e-6,
                                abs_tol=1e-12,
                            )
                        ),
                        None,
                    )
                    if match is not None:
                        data_rows.append(
                            {
                                **pending[match],
                                "ii_vs": first_imag,
                                "ii_vd": second_imag,
                            }
                        )
                pending = {}

        if not data_rows:
            self.logger.logger.error("No CV data parsed from HSPICE output")
            return False

        # Assign data rows to Vg values
        # Each Vg has 4 frequency points (1k, 10k, 100k, 1meg)
        points_per_vg = 4  # 4 frequencies
        for vg_i, vg in enumerate(vg_vals):
            start = vg_i * points_per_vg
            end = start + points_per_vg
            if end > len(data_rows):
                break
            for fi, freq_target in enumerate(freqs_hz):
                row = data_rows[start + fi]
                omega = 2 * math.pi * row['freq']
                if omega > 0:
                    cgg = -row['ii_vg'] / omega
                    cgb = -row['ii_vb'] / omega
                    cgs = -row['ii_vs'] / omega
                    cgd = -row['ii_vd'] / omega
                else:
                    cgg = cgb = cgs = cgd = 0.0
                all_cv[vg][f"cgg_{freq_target}"] = cgg
                if freq_target == 1e6:
                    all_cv[vg]['cgb_1MHz'] = cgb
                    all_cv[vg]['cgs_1MHz'] = cgs
                    all_cv[vg]['cgd_1MHz'] = cgd

        # Write cv_data.txt
        lines_out = ["Vg Cgg_1kHz Cgg_10kHz Cgg_100kHz Cgg_1MHz Cgb_1MHz Cgs_1MHz Cgd_1MHz"]
        for vg in vg_vals:
            caps = all_cv.get(vg, {})
            lines_out.append(
                f"{vg} "
                f"{caps.get('cgg_1000.0', caps.get('cgg_1000', 0)):.6E} "
                f"{caps.get('cgg_10000.0', caps.get('cgg_10000', 0)):.6E} "
                f"{caps.get('cgg_100000.0', caps.get('cgg_100000', 0)):.6E} "
                f"{caps.get('cgg_1000000.0', caps.get('cgg_1000000', 0)):.6E} "
                f"{caps.get('cgb_1MHz', 0):.6E} "
                f"{caps.get('cgs_1MHz', 0):.6E} "
                f"{caps.get('cgd_1MHz', 0):.6E}"
            )
        (self.data_dir / "cv_data.txt").write_text('\n'.join(lines_out))
        self.logger.logger.info(f"  Written: cv_data.txt ({len(vg_vals)} pts)")
        return True

    def _run_ac_sp(self):
        raise RuntimeError(
            "legacy HSPICE S-parameter path is disabled; use the "
            "AST-standardized AC circuit and complex result extractor"
        )

    def _run_ac_nqs(self):
        raise RuntimeError(
            "legacy HSPICE NQS path is disabled; use the "
            "AST-standardized AC circuit and complex result extractor"
        )

    def _run_ac_charge(self):
        """Run charge conservation test and generate charge_conservation.txt."""
        self.logger.logger.info("  AC Charge conservation...")
        netlist = _gen_ac_charge_netlist(self.model_file)
        p = self.netlist_dir / "hspice_ac_charge.sp"
        p.write_text(netlist)
        if not self._run_hspice(p, "ac_charge"):
            return False

        lis = self.netlist_dir / "ac_charge.lis"
        # Generate output matching ngspice format
        times, cols = _parse_trans_table(lis, 5)
        if not times:
            self.logger.logger.error(
                "No charge data parsed from HSPICE output"
            )
            return False

        lines = [
            "Title: * mosfet ac analysis circuit",
            "Date: Tue Jul 21 14:34:49  2026",
            "Command: hspice S-2021.09",
            "Plotname: Transient Analysis",
            "Flags: real",
            "No. Variables: 6",
            f"No. Points: {len(times)}",
            "Variables:",
            "0 time   time",
            "1 v(gate_3)   voltage",
            "2 i(VGQ)   current",
            "3 i(VDQ)   current",
            "4 i(VSQ)   current",
            "5 i(VBQ)   current",
            "Values:",
        ]
        for i in range(len(times)):
            lines.append(f"{i}")
            lines.append(f"{times[i]:.6e}")
            for c in range(5):
                lines.append(f"{cols[c][i]:.6e}" if i < len(cols[c]) else "0.000000e+00")
        (self.data_dir / "charge_conservation.txt").write_text('\n'.join(lines))
        self.logger.logger.info("  Written: charge_conservation.txt")
        return True

    # ===== Transient =====

    def _run_tran_single(
        self, name: str, gen_fn, out_file: str,
        col_names: str, col_count: int, post_process=None
    ) -> bool:
        self.logger.logger.info(f"  Transient {name}...")
        netlist = gen_fn(self.model_file)
        sp_name = f"hspice_tran_{name}"
        p = self.netlist_dir / f"{sp_name}.sp"
        p.write_text(netlist)
        if not self._run_hspice(p, sp_name):
            return False

        lis = self.netlist_dir / f"{sp_name}.lis"
        times, cols = _parse_trans_table(lis, col_count)
        if not times:
            self.logger.logger.error(
                f"No real transient data parsed for {name}"
            )
            return False

        if post_process:
            cols = post_process(times, cols)

        _write_tran_ngspice_format(
            self.data_dir / out_file, times, cols, col_names
        )
        self.logger.logger.info(f"  Written: {out_file}")
        return True

    def _run_tran_power_single(self, temp: int) -> bool:
        self.logger.logger.info(f"  Transient power at {temp}C...")
        netlist = _gen_tran_power_netlist(self.model_file, temp)
        sp_name = f"hspice_tran_power_{temp}"
        p = self.netlist_dir / f"{sp_name}.sp"
        p.write_text(netlist)
        if not self._run_hspice(p, sp_name):
            return False

        lis = self.netlist_dir / f"{sp_name}.lis"
        times, cols = _parse_trans_table(lis, 3)  # V(in) V(out) I(Vdd)
        if not times:
            self.logger.logger.error(
                f"No real HSPICE power data parsed at {temp}C"
            )
            return False

        # Compute power = -Vdd * I(Vdd), energy = integ(power)
        pwr = []
        energy = []
        accum = 0.0
        for i in range(len(times)):
            vdd = 1.2
            i_vdd = cols[2][i] if i < len(cols[2]) else 0
            p = -vdd * i_vdd if i > 0 else 0
            if i > 0:
                dt = times[i] - times[i - 1]
                accum += p * dt
            pwr.append(p)
            energy.append(accum)

        out_cols = [cols[0], cols[1], pwr, energy]
        out_name = f"tran_power_{temp}C.txt"
        _write_tran_ngspice_format(
            self.data_dir / out_name, times, out_cols,
            f"time v(in_power) v(out_power) power_diss energy"
        )
        self.logger.logger.info(f"  Written: {out_name}")
        return True

    # ===== Noise =====

    def _run_noise_thermal(self):
        bias_points = [
            (0.3, 0.3), (0.3, 0.6), (0.3, 0.9), (0.3, 1.2),
            (0.6, 0.3), (0.6, 0.6),
        ]
        for vgs, vds in bias_points:
            self.logger.logger.info(f"  Thermal noise Vgs={vgs} Vds={vds}...")
            netlist = _gen_noise_thermal_netlist(self.model_file, vgs, vds)
            sp_name = f"hspice_noise_th_{vgs}_{vds}"
            p = self.netlist_dir / f"{sp_name}.sp"
            p.write_text(netlist)
            if not self._run_hspice(p, sp_name):
                continue

            lis = self.netlist_dir / f"{sp_name}.lis"
            freq, noise = _parse_noise_lis_table(lis)
            if not freq:
                self.logger.logger.error(
                    f"No real HSPICE thermal-noise data at {vgs}/{vds}"
                )
                continue

            _write_noise_ngspice_format(
                self.data_dir / f"thermal_noise_vgs{vgs:.1f}_vds{vds:.1f}.txt",
                freq, noise, f"thermal noise vgs={vgs} vds={vds}"
            )
            self.logger.logger.info(
                f"    Written: thermal_noise_vgs{vgs:.1f}_vds{vds:.1f}.txt"
            )

    def _run_noise_flicker(self):
        self.logger.logger.info("  Flicker noise...")
        netlist = _gen_noise_flicker_netlist(self.model_file)
        p = self.netlist_dir / "hspice_noise_fl.sp"
        p.write_text(netlist)
        if not self._run_hspice(p, "noise_fl"):
            return

        lis = self.netlist_dir / "noise_fl.lis"
        freq, noise = _parse_noise_lis_table(lis)
        if not freq:
            self.logger.logger.error(
                "No real HSPICE flicker-noise data"
            )
            return
        _write_noise_ngspice_format(
            self.data_dir / "flicker_noise.txt", freq, noise, "flicker noise"
        )
        self.logger.logger.info("  Written: flicker_noise.txt")

    def _run_noise_shot(self):
        self.logger.logger.info("  Shot noise...")
        netlist = _gen_noise_shot_netlist(self.model_file)
        p = self.netlist_dir / "hspice_noise_sh.sp"
        p.write_text(netlist)
        if not self._run_hspice(p, "noise_sh"):
            return

        lis = self.netlist_dir / "noise_sh.lis"
        freq, noise = _parse_noise_lis_table(lis)
        if not freq:
            self.logger.logger.error("No real HSPICE shot-noise data")
            return
        _write_noise_ngspice_format(
            self.data_dir / "shot_noise.txt", freq, noise, "shot noise"
        )
        self.logger.logger.info("  Written: shot_noise.txt")

    def _run_noise_temp(self):
        for temp in [-40, 0, 27, 50, 100, 150]:
            self.logger.logger.info(f"  Temperature noise T={temp}C...")
            netlist = _gen_noise_temp_netlist(self.model_file, temp)
            sp_name = f"hspice_noise_t{temp}"
            p = self.netlist_dir / f"{sp_name}.sp"
            p.write_text(netlist)
            if not self._run_hspice(p, sp_name):
                continue

            lis = self.netlist_dir / f"{sp_name}.lis"
            freq, noise = _parse_noise_lis_table(lis)
            if not freq:
                self.logger.logger.error(
                    f"No real HSPICE noise data at {temp}C"
                )
                continue

            _write_noise_ngspice_format(
                self.data_dir / f"noise_temp{temp}.txt",
                freq, noise, f"noise at {temp}C"
            )
            self.logger.logger.info(f"    Written: noise_temp{temp}.txt")

    @staticmethod
    def _analysis_for_case(analyses, case, kind):
        matches = [
            item for item in analyses
            if item["case"] == case and kind in item["kind"]
            and item["values"]
        ]
        return matches[-1] if matches else None

    @staticmethod
    def _write_columns(path, headers, columns):
        count = min((len(column) for column in columns), default=0)
        lines = [" ".join(headers)]
        for index in range(count):
            lines.append(
                " ".join(f"{column[index]:.10e}" for column in columns)
            )
        path.write_text("\n".join(lines) + "\n")
        return count > 1

    def _process_standardized_dc(self, lis_path):
        analyses = _parse_named_analyses(lis_path)
        temperatures = [-40, 0, 25, 50, 100, 150]
        ok = True
        for case, temperature in enumerate(temperatures):
            records = [
                item for item in analyses
                if item["case"] == case and "dc transfer" in item["kind"]
                and item["values"]
            ]
            records = records[-7:]
            rows = []
            for record in records:
                values = record["values"]
                count = min(
                    (
                        len(values.get(name, []))
                        for name in (
                            "drain_iv", "gate_iv", "vds_iv",
                            "vs_iv", "vb_iv", "vgs_iv",
                        )
                    ),
                    default=0,
                )
                for index in range(count):
                    currents = [
                        values[name][index]
                        for name in ("vds_iv", "vs_iv", "vb_iv", "vgs_iv")
                    ]
                    rows.append(
                        [
                            values["drain_iv"][index],
                            values["drain_iv"][index],
                            values["gate_iv"][index],
                            *currents,
                            abs(sum(currents)),
                        ]
                    )
            path = self.data_dir / f"iv_data_{temperature}.txt"
            lines = [
                "v-sweep v(drain_iv) v(gate_iv) id is ib ig kcl"
            ]
            lines.extend(
                " ".join(f"{value:.10e}" for value in row)
                for row in rows
            )
            path.write_text("\n".join(lines) + "\n")
            ok = ok and len(rows) > 1

        source = self.data_dir / "iv_data_25.txt"
        bias = self.data_dir / "bias_point_data.txt"
        bias_lines = [
            "v(drain_bias) v(gate_bias) id_bias ig_bias is_bias ib_bias"
        ]
        if source.exists():
            numeric = []
            for line in source.read_text().splitlines()[1:]:
                try:
                    numeric.append([float(value) for value in line.split()])
                except ValueError:
                    continue
            for vds in (0.0, 0.6, 1.2):
                for vgs in (0.0, 0.6, 1.2):
                    if numeric:
                        row = min(
                            numeric,
                            key=lambda item: (
                                abs(item[1] - vds) + abs(item[2] - vgs)
                            ),
                        )
                        bias_lines.append(
                            f"{vds:.1f} {vgs:.1f} "
                            f"{row[3]:.10e} {row[6]:.10e} "
                            f"{row[4]:.10e} {row[5]:.10e}"
                        )
        bias.write_text("\n".join(bias_lines) + "\n")
        return ok and len(bias_lines) == 10

    def _process_standardized_transient(self, lis_path):
        analyses = _parse_named_analyses(lis_path)

        def values(case):
            record = self._analysis_for_case(analyses, case, "transient")
            return record["values"] if record else {}

        def columns(case, names):
            item = values(case)
            return [item.get(name, []) for name in names]

        ok = True
        ok &= self._write_columns(
            self.data_dir / "tran_large_signal.txt",
            [
                "time", "time", "v(gate_tran)", "v(drain_tran)",
                "i(Vds_tran)", "i(Vgs_tran)", "i(Vs_tran)", "i(Vb_tran)",
            ],
            columns(
                0,
                [
                    "time", "time", "gate_tran", "drain_tran",
                    "vds_tran", "vgs_tran", "vs_tran", "vb_tran",
                ],
            ),
        )
        switch = values(1)
        ok &= self._write_columns(
            self.data_dir / "tran_switching.txt",
            ["time", "time", "v(in_inv)", "v(out_inv)", "i(Vdd_inv)"],
            [
                switch.get("time", []),
                switch.get("time", []),
                switch.get("in_inv", []),
                switch.get("out_inv", []),
                switch.get(
                    "vdd_inv_current",
                    switch.get("vdd_inv", []),
                ),
            ],
        )
        time_values = switch.get("time", [])
        supply_values = switch.get("vdd_inv", [])
        current_values = switch.get("vdd_inv", [])
        # HSPICE uses the same normalized name for V(node) and I(Vsource)
        # unless the type row is retained.  The named-table parser appends
        # the printed quantity type when names collide.
        if "vdd_inv_voltage" in switch:
            supply_values = switch["vdd_inv_voltage"]
        if "vdd_inv_current" in switch:
            current_values = switch["vdd_inv_current"]
        ok &= self._write_columns(
            self.data_dir / "tran_switching_power.txt",
            ["time", "time", "power_switching"],
            [
                time_values,
                time_values,
                [
                    -voltage * current
                    for voltage, current in zip(
                        supply_values, current_values
                    )
                ],
            ],
        )
        ok &= self._write_columns(
            self.data_dir / "tran_delay.txt",
            [
                "time", "time", "v(in_delay)", "v(mid1_delay)",
                "v(mid2_delay)", "v(out_delay)",
            ],
            columns(
                2,
                [
                    "time", "time", "in_delay", "mid1_delay",
                    "mid2_delay", "out_delay",
                ],
            ),
        )
        for case, temperature in ((3, 27), (4, 100)):
            item = values(case)
            times = item.get("time", [])
            supplies = item.get(
                "vdd_power_voltage",
                item.get("vdd_power", []),
            )
            currents = item.get(
                "vdd_power_current",
                item.get("vdd_power", []),
            )
            powers = [
                -voltage * current
                for voltage, current in zip(supplies, currents)
            ]
            energies = []
            total = 0.0
            for index, power in enumerate(powers):
                if index:
                    total += power * (times[index] - times[index - 1])
                energies.append(total)
            ok &= self._write_columns(
                self.data_dir / f"tran_power_{temperature}C.txt",
                [
                    "time", "time", "v(in_power)", "v(out_power)",
                    "power_diss", "energy",
                ],
                [
                    times, times, item.get("in_power", []),
                    item.get("out_power", []), powers, energies,
                ],
            )
        ok &= self._write_columns(
            self.data_dir / "tran_quasi_static.txt",
            ["time", "time", "v(gate_qs)", "v(drain_qs)", "id_qs"],
            columns(
                5,
                ["time", "time", "gate_qs", "drain_qs", "vds_qs"],
            ),
        )
        charge = values(6)
        times = charge.get("time", [])
        currents = [
            charge.get(name, [])
            for name in ("vg_charge", "vd_charge", "vs_charge", "vb_charge")
        ]
        count = min([len(times)] + [len(item) for item in currents])
        totals = [
            sum(item[index] for item in currents)
            for index in range(count)
        ]
        charges = [[0.0] * count for _ in range(4)]
        for index in range(1, count):
            step = times[index] - times[index - 1]
            for terminal in range(4):
                charges[terminal][index] = (
                    charges[terminal][index - 1]
                    + 0.5
                    * (currents[terminal][index] + currents[terminal][index - 1])
                    * step
                )
        qtotal = [
            sum(item[index] for item in charges)
            for index in range(count)
        ]
        ok &= self._write_columns(
            self.data_dir / "tran_charge.txt",
            [
                "time", "time", "v(gate_charge)", "ig_charge",
                "id_charge", "is_charge", "ib_charge", "i_total",
                "qg_approx", "qd_approx", "qs_approx", "qb_approx",
                "q_total",
            ],
            [
                times[:count], times[:count],
                charge.get("gate_charge", [])[:count],
                *[item[:count] for item in currents],
                totals, *charges, qtotal,
            ],
        )
        return bool(ok)

    def _process_standardized_ac(self, lis_path):
        analyses = _parse_named_analyses(lis_path)

        def record(case, kind="ac", target_frequency=None):
            matches = [
                item for item in analyses
                if item["case"] == case and kind in item["kind"]
                and item["values"]
            ]
            if target_frequency is None:
                if not matches:
                    raise ValueError(
                        f"missing HSPICE {kind} result for AST case {case}"
                    )
                return matches[-1]
            for item in reversed(matches):
                frequencies = item["values"].get("frequency", [])
                if any(
                    abs(value - target_frequency)
                    <= max(abs(target_frequency), 1.0) * 1e-9
                    for value in frequencies
                ):
                    return item
            raise ValueError(
                "missing HSPICE AC result for AST case %d at %.10g Hz"
                % (case, target_frequency)
            )

        def complex_value(values, name, target_frequency):
            real = values.get(f"{name}_real")
            imag = values.get(f"{name}_imag")
            frequencies = values.get("frequency")
            if real is None or imag is None or frequencies is None:
                raise ValueError(
                    f"missing HSPICE complex signal {name}"
                )
            count = min(len(real), len(imag), len(frequencies))
            if count == 0:
                raise ValueError(f"empty HSPICE complex signal {name}")
            index = min(
                range(count),
                key=lambda offset: abs(
                    frequencies[offset] - target_frequency
                ),
            )
            if (
                abs(frequencies[index] - target_frequency)
                > max(abs(target_frequency), 1.0) * 1e-9
            ):
                raise ValueError(
                    "HSPICE signal %s has no %.10g Hz sample"
                    % (name, target_frequency)
                )
            value = complex(real[index], imag[index])
            if not (math.isfinite(value.real) and math.isfinite(value.imag)):
                raise ValueError(f"non-finite HSPICE signal {name}")
            return value

        cv_lines = [
            "Vg Cgg_1kHz Cgg_10kHz Cgg_100kHz Cgg_1MHz "
            "Cgb_1MHz Cgs_1MHz Cgd_1MHz"
        ]
        matrix_lines = [
            "Vg Cgg Cdg Csg Cbg Cgd Cdd Csd Cbd "
            "Cgs Cds Css Cbs Cgb Cdb Csb Cbb"
        ]
        for gate_index in range(41):
            base = gate_index * 8
            gate_voltage = -0.8 + 0.05 * gate_index
            capacitances = []
            for offset, frequency in enumerate((1e3, 1e4, 1e5, 1e6)):
                item = record(base + offset, target_frequency=frequency)
                values = item["values"]
                capacitances.append(
                    -complex_value(values, "vg", frequency).imag
                    / (2.0 * math.pi * frequency)
                )
            matrix_columns = []
            for column in range(4):
                matrix = record(
                    base + 4 + column, target_frequency=1e6
                )
                matrix_columns.append([
                    -complex_value(matrix["values"], name, 1e6).imag
                    / (2.0 * math.pi * 1e6)
                    for name in ("vg", "vd", "vs", "vb")
                ])
            cv_lines.append(
                f"{gate_voltage:.6e} "
                + " ".join(f"{value:.6e}" for value in capacitances)
                + " "
                + " ".join(
                    f"{matrix_columns[0][index]:.6e}"
                    for index in (3, 2, 1)
                )
            )
            matrix_lines.append(
                f"{gate_voltage:.6e} "
                + " ".join(
                    f"{value:.6e}"
                    for column in matrix_columns
                    for value in column
                )
            )
        (self.data_dir / "cv_data.txt").write_text(
            "\n".join(cv_lines) + "\n"
        )
        (self.data_dir / "cmatrix_data.txt").write_text(
            "\n".join(matrix_lines) + "\n"
        )

        sparameter_lines = [
            "# S-parameter analysis",
            "# freq s11_mag s11_phase s12_mag s12_phase "
            "s21_mag s21_phase s22_mag s22_phase"
        ]
        for offset, frequency in enumerate((1e6, 1e7, 1e8, 1e9)):
            gate_case = record(
                328 + 2 * offset, target_frequency=frequency
            )
            drain_case = record(
                329 + 2 * offset, target_frequency=frequency
            )
            gate_values = gate_case["values"]
            drain_values = drain_case["values"]
            gate_voltage = complex_value(
                gate_values, "gate_in2", frequency
            )
            drain_voltage = complex_value(
                drain_values, "drain_in2", frequency
            )
            if abs(gate_voltage) < 1e-15 or abs(drain_voltage) < 1e-15:
                raise ValueError(
                    f"zero HSPICE S-parameter excitation at {frequency:g} Hz"
                )
            y11 = -complex_value(
                gate_values, "vgs", frequency
            ) / gate_voltage
            y21 = -complex_value(
                gate_values, "vds", frequency
            ) / gate_voltage
            y12 = -complex_value(
                drain_values, "vgs", frequency
            ) / drain_voltage
            y22 = -complex_value(
                drain_values, "vds", frequency
            ) / drain_voltage
            s11, s12, s21, s22 = y_to_s(y11, y12, y21, y22)
            values = [
                *polar(s11), *polar(s12),
                *polar(s21), *polar(s22),
            ]
            sparameter_lines.append(
                f"{frequency:.6e} "
                + " ".join(f"{value:.6e}" for value in values)
            )
        (self.data_dir / "sparams_data.txt").write_text(
            "\n".join(sparameter_lines) + "\n"
        )

        nqs_lines = [
            "# Non-quasi-static effects analysis - phase shifts",
            "# freq vg_phase id_phase phase_diff",
        ]
        for offset, frequency in enumerate((1e7, 1e8, 1e9, 1e10)):
            item = record(
                336 + offset, target_frequency=frequency
            )
            values = item["values"]
            gate = complex_value(values, "gate_1", frequency)
            drain = complex_value(values, "vd", frequency)
            gate_phase = math.degrees(math.atan2(gate.imag, gate.real))
            drain_phase = math.degrees(math.atan2(drain.imag, drain.real))
            nqs_lines.append(
                f"{frequency:.6e} {gate_phase:.6e} {drain_phase:.6e} "
                f"{(gate_phase - drain_phase):.6e}"
            )
        (self.data_dir / "nqs_effects.txt").write_text(
            "\n".join(nqs_lines) + "\n"
        )

        charge_record = record(340, "transient")
        values = charge_record["values"]
        required = ("time", "gate_3", "vgq", "vdq", "vsq", "vbq")
        missing = [name for name in required if name not in values]
        if missing:
            raise ValueError(
                "missing HSPICE charge signals: " + ", ".join(missing)
            )
        times = values["time"]
        signals = [values[name] for name in required[1:]]
        count = min([len(times)] + [len(item) for item in signals])
        if count < 2:
            raise ValueError("insufficient HSPICE charge samples")
        output = self.data_dir / "charge_conservation.txt"
        with output.open("w") as stream:
            stream.write("Title: HSPICE charge conservation analysis\n")
            stream.write("Plotname: Transient Analysis\nFlags: real\n")
            stream.write("No. Variables: 6\n")
            stream.write(f"No. Points: {count}\nVariables:\n")
            stream.write("\t0\ttime\ttime\n\t1\tv(gate_3)\tvoltage\n")
            stream.write(
                "\t2\ti(vgq)\tcurrent\n\t3\ti(vdq)\tcurrent\n"
                "\t4\ti(vsq)\tcurrent\n\t5\ti(vbq)\tcurrent\nValues:\n"
            )
            for index in range(count):
                stream.write(f" {index}\t{times[index]:.10e}\n")
                for signal in signals:
                    stream.write(f"\t{signal[index]:.10e}\n")
                stream.write("\n")
        return (
            len(cv_lines) == 42
            and len(sparameter_lines) == 6
            and len(nqs_lines) == 6
            and count > 1
        )

    def _process_standardized_noise(self, lis_path):
        text = lis_path.read_text(errors="replace")
        current_case = None
        points = {}
        frequency = None
        for line in text.splitlines():
            stripped = line.strip()
            case_match = re.fullmatch(r"(?i)ast_case_(\d+)", stripped)
            if case_match:
                current_case = int(case_match.group(1))
                continue
            frequency_match = re.search(
                r"(?i)\bfrequency\s*=\s*(\S+)\s+Hz",
                stripped,
            )
            if frequency_match:
                try:
                    frequency = _hspice_float(frequency_match.group(1))
                except ValueError:
                    frequency = None
                continue
            spectral_match = re.search(
                r"(?i)total output noise voltage\s*=\s*(\S+)\s+V\^2/Hz",
                stripped,
            )
            if (
                spectral_match and current_case is not None
                and frequency is not None
            ):
                try:
                    density = math.sqrt(
                        max(_hspice_float(spectral_match.group(1)), 0.0)
                    )
                except ValueError:
                    continue
                points.setdefault(current_case, []).append(
                    (frequency, density)
                )

        def latest_sweep(case):
            source = points.get(case, [])
            sweeps = []
            current = []
            for point in source:
                if current and point[0] <= current[-1][0]:
                    sweeps.append(current)
                    current = []
                current.append(point)
            if current:
                sweeps.append(current)
            return sweeps[-1] if sweeps else []

        def write(path, values, title):
            frequencies = [item[0] for item in values]
            densities = [item[1] for item in values]
            _write_noise_ngspice_format(
                path, frequencies, densities, title
            )
            return len(values) > 1

        ok = True
        biases = (
            ("0.3", "0.3"), ("0.3", "0.6"), ("0.3", "0.9"),
            ("0.3", "1.2"), ("0.6", "0.3"), ("0.6", "0.6"),
        )
        for case, (vgs, vds) in enumerate(biases):
            ok &= write(
                self.data_dir / f"thermal_noise_vgs{vgs}_vds{vds}.txt",
                latest_sweep(case),
                f"thermal noise Vgs={vgs} Vds={vds}",
            )
        ok &= write(
            self.data_dir / "flicker_noise.txt",
            latest_sweep(6),
            "flicker noise",
        )
        ok &= write(
            self.data_dir / "shot_noise.txt",
            latest_sweep(7),
            "shot noise",
        )
        for case, temperature in enumerate(
            (-40, 0, 27, 50, 100, 150),
            start=8,
        ):
            ok &= write(
                self.data_dir / f"noise_temp{temperature}.txt",
                latest_sweep(case),
                f"noise at {temperature}C",
            )
        return bool(ok)

    # ===== Entry points =====

    def run_dc_simulation(self) -> bool:
        if not self.model_file:
            return False
        self.logger.logger.info("Starting HSPICE DC...")

        dc_path = self.netlist_dir / "hspice_dc.sp"
        dc_path.write_text(_gen_dc_netlist(self.model_file))
        self.logger.logger.info(f"Generated: {dc_path}")
        hspice_ok = self._run_hspice(dc_path, "dc")
        parse_ok = self._parse_dc(self.netlist_dir / "dc.lis", self.data_dir, self.logger.logger)
        if not hspice_ok:
            self.logger.logger.warning("HSPICE DC returned non-zero but data may still be usable")
        if not parse_ok:
            self.logger.logger.info("Built-in DC parser skipped — using post-processor")

        bias_path = self.netlist_dir / "hspice_bias.sp"
        bias_path.write_text(_gen_bias_netlist(self.model_file))
        self.logger.logger.info(f"Generated: {bias_path}")
        if self._run_hspice(bias_path, "bias"):
            self._parse_bias(self.netlist_dir / "bias.lis", self.data_dir, self.logger.logger)
        return True  # Always continue to Phase 2

    def run_ac_simulation(self) -> bool:
        if not self.model_file:
            return False
        self.logger.logger.info("Starting HSPICE AC...")
        self._run_ac_cv()
        self._run_ac_sp()
        self._run_ac_nqs()
        self._run_ac_charge()
        return True

    def _has_pmos(self) -> bool:
        """Check if model file contains a PMOS model definition."""
        if not self.model_file:
            return False
        return self._pmos != "pmos_vtg" or self._nmos == "pmos_vtg"

    def run_transient_simulation(self) -> bool:
        if not self.model_file:
            return False
        self.logger.logger.info("Starting HSPICE Transient...")
        has_pmos = self._has_pmos()

        self._run_tran_single(
            "ls", _gen_tran_large_signal_netlist,
            "tran_large_signal.txt",
            "time time v(gate_tran) v(drain_tran) i(Vds_tran) i(Vgs_tran) i(Vs_tran) i(Vb_tran)",
            6
        )

        # CMOS circuits (need PMOS)
        if has_pmos:
            self._run_tran_single(
                "sw", _gen_tran_switching_netlist,
                "tran_switching.txt",
                "time v(in_inv) v(out_inv) i(Vdd_inv)",
                3
            )
            # Switching power
            sw_path = self.data_dir / "tran_switching.txt"
            if sw_path.exists():
                lines = sw_path.read_text().split('\n')
                if len(lines) > 1:
                    pwr_lines = [lines[0].replace(
                        "v(in_inv) v(out_inv) i(Vdd_inv)", "power_switching"
                    )]
                    for line in lines[1:]:
                        parts = line.strip().split()
                        if len(parts) >= 4:
                            time_val = parts[0]
                            vdd = 1.2
                            try:
                                i_vdd = float(parts[3])
                                pwr = -vdd * i_vdd
                                pwr_lines.append(f"{time_val} {pwr:.6e}")
                            except ValueError:
                                pass
                    (self.data_dir / "tran_switching_power.txt").write_text(
                        '\n'.join(pwr_lines)
                    )
                    self.logger.logger.info("  Written: tran_switching_power.txt")

            self._run_tran_single(
                "delay", _gen_tran_delay_netlist,
                "tran_delay.txt",
                "time v(in_delay) v(mid1_delay) v(mid2_delay) v(out_delay)",
                4
            )
            self._run_tran_power_single(27)
            self._run_tran_power_single(100)
        else:
            self.logger.logger.error(
                "CMOS transient setup requires a complementary fixture model"
            )
            return False

        self._run_tran_single(
            "qs", _gen_tran_qs_netlist,
            "tran_quasi_static.txt",
            "time v(gate_qs) v(drain_qs) id_qs",
            3
        )
        self._run_tran_single(
            "charge", _gen_tran_charge_netlist,
            "tran_charge.txt",
            "time v(gate_charge) ig_charge id_charge is_charge ib_charge i_total qg_approx qd_approx qs_approx qb_approx q_total",
            11
        )
        return True

    def run_noise_simulation(self) -> bool:
        if not self.model_file:
            return False
        self.logger.logger.info("Starting HSPICE Noise...")
        self._run_noise_thermal()
        self._run_noise_flicker()
        self._run_noise_shot()
        self._run_noise_temp()
        return True

    def run_simulations_by_mode(self, modes: List[str]) -> bool:
        if 'all' in modes:
            modes = ['dc', 'ac', 'transient', 'noise']
        success = True
        for mode in modes:
            try:
                custom = self.circuit_files.get(mode)
                if custom:
                    source = Path(custom)
                    if not source.exists():
                        self.logger.logger.error(
                            f"HSPICE circuit file not found: {source}"
                        )
                        success = False
                        continue
                    destination = self.netlist_dir / f"hspice_{mode}_ast.sp"
                    content = source.read_text(errors="replace")
                    # The standardized circuit owns topology/analysis; the
                    # benchmark invocation owns the model include.
                    content = re.sub(
                        r"(?im)^\s*\.(?:inc|include|lib)\s+.*$",
                        "",
                        content,
                    )
                    single_instances = (
                        r"(?:M1|M2|M3|M_iv|M_bias|M_tran|M_charge|"
                        r"M_qs|M_noise|M_flicker|M_shot)"
                    )
                    content = re.sub(
                        rf"(?im)^(\s*{single_instances}\b"
                        rf"(?:\s+\S+){{4}}\s+)\S+",
                        rf"\g<1>{self._primary}",
                        content,
                    )
                    content = content.replace("NMOS_VTG", self._nmos)
                    content = content.replace("PMOS_VTG", self._pmos)
                    content = apply_primary_geometry(
                        content,
                        self._primary,
                        read_geometry_override(self.model_file),
                    )
                    include = f".INC '{Path(self.model_file).resolve()}'\n"
                    lines = content.splitlines()
                    lines.insert(2 if len(lines) > 2 else 1, include.rstrip())
                    output_directives = {
                        "dc": [
                            ".PRINT DC V(drain_iv) V(gate_iv) "
                            "I(Vds_iv) I(Vs_iv) I(Vb_iv) I(Vgs_iv)",
                        ],
                        "transient": [
                            ".PRINT TRAN V(gate_tran) V(drain_tran) "
                            "I(Vds_tran) I(Vgs_tran) I(Vs_tran) I(Vb_tran) "
                            "V(in_inv) V(out_inv) V(vdd_inv) I(Vdd_inv) "
                            "V(in_delay) V(mid1_delay) V(mid2_delay) "
                            "V(out_delay) V(in_power) V(out_power) "
                            "V(vdd_power) I(Vdd_power) "
                            "V(gate_qs) V(drain_qs) "
                            "I(Vds_qs) V(gate_charge) I(Vg_charge) "
                            "I(Vd_charge) I(Vs_charge) I(Vb_charge)",
                        ],
                        "ac": [
                            ".PRINT AC II(VG) IR(VG) II(VD) IR(VD) "
                            "II(VS) IR(VS) II(VB) IR(VB)",
                            ".PRINT AC VR(gate_1) VI(gate_1)",
                            ".PRINT AC VR(gate_in2) VI(gate_in2) "
                            "VR(drain_in2) VI(drain_in2) "
                            "II(VGS) IR(VGS) II(VDS) IR(VDS)",
                            ".PRINT AC VR(gate_3) VI(gate_3) "
                            "II(VGQ) IR(VGQ) II(VDQ) IR(VDQ) "
                            "II(VSQ) IR(VSQ) II(VBQ) IR(VBQ)",
                            ".PRINT TRAN V(gate_3) I(VGQ) I(VDQ) "
                            "I(VSQ) I(VBQ)",
                        ],
                        "noise": [
                            ".PRINT NOISE ONOISE INOISE",
                        ],
                    }[mode]
                    first_alter = next(
                        (
                            index for index, line in enumerate(lines)
                            if line.strip().lower().startswith(".alter")
                        ),
                        len(lines) - 1,
                    )
                    lines[first_alter:first_alter] = output_directives
                    if mode == "ac":
                        lines = _parameterize_single_point_ac(lines)
                    elif mode == "transient":
                        lines = _parameterize_transient_analyses(lines)
                    destination.write_text("\n".join(lines) + "\n")
                    run_ok = self._run_hspice(destination, mode + "_ast")
                    if not run_ok:
                        success = False
                        continue
                    listing = self.netlist_dir / f"{mode}_ast.lis"
                    if mode == "dc":
                        success = (
                            self._process_standardized_dc(listing) and success
                        )
                    elif mode == "transient":
                        success = (
                            self._process_standardized_transient(listing)
                            and success
                        )
                    elif mode == "ac":
                        success = (
                            self._process_standardized_ac(listing) and success
                        )
                    elif mode == "noise":
                        success = (
                            self._process_standardized_noise(listing) and success
                        )
                    continue
                self.logger.logger.error(
                    "HSPICE benchmark requires AST-standardized circuit files; "
                    f"none was provided for {mode}"
                )
                success = False
            except Exception as e:
                self.logger.logger.error(f"Mode {mode} failed: {e}")
                success = False
        if success:
            self.logger.logger.info("All HSPICE simulations completed successfully")
        return success
