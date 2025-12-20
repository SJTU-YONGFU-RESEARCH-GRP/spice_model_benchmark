import argparse
import re
import subprocess
from pathlib import Path
from typing import Optional
from typing import Any

import numpy as np
import re


def run_ngspice(netlist_path: Path, cwd: Path) -> str:
    try:
        rel = netlist_path.relative_to(cwd)
    except Exception:
        rel = netlist_path
    cmd = ["ngspice", "-b", str(rel)]
    result = subprocess.run(cmd, cwd=str(cwd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"ngspice failed for {netlist_path} with code {result.returncode}\n"
            f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return result.stdout


_MEAS_PAT = re.compile(r"\b(?P<name>qs|qd|qb)\s*=\s*(?P<val>[-+0-9.eE]+)")


def parse_terminal_charges(stdout: str) -> dict[str, float]:
    out: dict[str, float] = {}
    for m in _MEAS_PAT.finditer(stdout):
        out[m.group("name")] = float(m.group("val"))
    return out


def _is_sky130(pdk_lower: str) -> bool:
    return "sky130" in pdk_lower or "skywater" in pdk_lower


def _is_cadence45(pdk_lower: str) -> bool:
    return "cadence45" in pdk_lower or "gpdk045" in pdk_lower


def _is_cadence14(pdk_lower: str) -> bool:
    return "cadence14" in pdk_lower or "cds_ff_mpt" in pdk_lower


def _is_cadence90(pdk_lower: str) -> bool:
    return "cadence90" in pdk_lower or "gpdk090" in pdk_lower


def _is_cadence180(pdk_lower: str) -> bool:
    return "cadence180" in pdk_lower or "gpdk180" in pdk_lower


def _sky130_include_block() -> str:
    # Mirror the include stack in netlists/sky130_dc_circuit.cir.
    return """.option scale=1E-6
.option TEMP=27
.option TNOM=27

.include "../models/skywater-pdk-libs-sky130_fd_pr/models/parameters/lod.spice"
.include "../models/skywater-pdk-libs-sky130_fd_pr/models/parameters/invariant.spice"
.include "../models/skywater-pdk-libs-sky130_fd_pr/cells/nfet_01v8/sky130_fd_pr__nfet_01v8__mismatch.corner.spice"
.include "../models/skywater-pdk-libs-sky130_fd_pr/cells/pfet_01v8/sky130_fd_pr__pfet_01v8__mismatch.corner.spice"
.include "../models/skywater-pdk-libs-sky130_fd_pr/cells/nfet_01v8/sky130_fd_pr__nfet_01v8__tt.corner.spice"
.include "../models/skywater-pdk-libs-sky130_fd_pr/cells/pfet_01v8/sky130_fd_pr__pfet_01v8__tt.corner.spice"
"""


def _sky130_nmos_netlist_text(L_um: float, W_um: float, vdd: float) -> str:
    return f"""* Gate-cap sweep (Sky130 NMOS) - Cgs/Cgd/Cgb via terminal current integration
.option gmin=1e-15
.option reltol=1e-8
.option abstol=1e-12
.option chgtol=1e-15
.option method=gear

{_sky130_include_block()}

.param L_dut={L_um:.12g}
.param W_dut={W_um:.12g}
.param VDD={vdd:.12g}

* Biases: use Vds=0 to avoid conduction; measure mostly displacement charge
Vg gate 0 PULSE(0 {{VDD}} 0n 0.1n 0.1n 10n 20n)
Vd drain 0 DC 0
Vs source 0 DC 0
Vb bulk 0 DC 0

X1 drain gate source bulk sky130_fd_pr__nfet_01v8 l={{L_dut}} w={{W_dut}}

.control
set filetype=ascii
set nomoremode
tran 0.01n 20n
meas tran qs INTEG i(Vs) from=0n to=10n
meas tran qd INTEG i(Vd) from=0n to=10n
meas tran qb INTEG i(Vb) from=0n to=10n
print qs qd qb
quit
.endc

.end
"""


def _sky130_nmos_bulkstep_netlist_text(L_um: float, W_um: float, vdd: float) -> str:
    return f"""* Bulk-step sweep (Sky130 NMOS) - Csb/Cdb via terminal current integration
.option gmin=1e-15
.option reltol=1e-8
.option abstol=1e-12
.option chgtol=1e-15
.option method=gear

{_sky130_include_block()}

.param L_dut={L_um:.12g}
.param W_dut={W_um:.12g}
.param VDD={vdd:.12g}
.param VBN=-VDD

* Biases: keep channel off (Vg=0), use Vds=0, step bulk 0->-VDD (reverse bias)
Vg gate 0 DC 0
Vd drain 0 DC 0
Vs source 0 DC 0
Vb bulk 0 PULSE(0 {{VBN}} 0n 0.1n 0.1n 10n 20n)

X1 drain gate source bulk sky130_fd_pr__nfet_01v8 l={{L_dut}} w={{W_dut}}

.control
set filetype=ascii
set nomoremode
tran 0.01n 20n
meas tran qs INTEG i(Vs) from=0n to=10n
meas tran qd INTEG i(Vd) from=0n to=10n
meas tran qb INTEG i(Vb) from=0n to=10n
print qs qd qb
quit
.endc

.end
"""


def _sky130_pmos_netlist_text(L_um: float, W_um: float, vdd: float) -> str:
    return f"""* Gate-cap sweep (Sky130 PMOS) - Cgs/Cgd/Cgb via terminal current integration
.option gmin=1e-15
.option reltol=1e-8
.option abstol=1e-12
.option chgtol=1e-15
.option method=gear

{_sky130_include_block()}

.param L_dut={L_um:.12g}
.param W_dut={W_um:.12g}
.param VDD={vdd:.12g}

* Biases: use Vds=0 to avoid conduction; gate steps VDD->0
Vg gate 0 PULSE({{VDD}} 0 0n 0.1n 0.1n 10n 20n)
Vd drain 0 DC {{VDD}}
Vs source 0 DC {{VDD}}
Vb bulk 0 DC {{VDD}}

X1 drain gate source bulk sky130_fd_pr__pfet_01v8 l={{L_dut}} w={{W_dut}}

.control
set filetype=ascii
set nomoremode
tran 0.01n 20n
meas tran qs INTEG i(Vs) from=0n to=10n
meas tran qd INTEG i(Vd) from=0n to=10n
meas tran qb INTEG i(Vb) from=0n to=10n
print qs qd qb
quit
.endc

.end
"""


def _sky130_pmos_bulkstep_netlist_text(L_um: float, W_um: float, vdd: float) -> str:
    return f"""* Bulk-step sweep (Sky130 PMOS) - Csb/Cdb via terminal current integration
.option gmin=1e-15
.option reltol=1e-8
.option abstol=1e-12
.option chgtol=1e-15
.option method=gear

{_sky130_include_block()}

.param L_dut={L_um:.12g}
.param W_dut={W_um:.12g}
.param VDD={vdd:.12g}

* Biases: keep channel off (Vg=0), use Vds=0, step bulk VDD->0 (reverse-to-zero)
Vg gate 0 DC 0
Vd drain 0 DC 0
Vs source 0 DC 0
Vb bulk 0 PULSE({{VDD}} 0 0n 0.1n 0.1n 10n 20n)

X1 drain gate source bulk sky130_fd_pr__pfet_01v8 l={{L_dut}} w={{W_dut}}

.control
set filetype=ascii
set nomoremode
tran 0.01n 20n
meas tran qs INTEG i(Vs) from=0n to=10n
meas tran qd INTEG i(Vd) from=0n to=10n
meas tran qb INTEG i(Vb) from=0n to=10n
print qs qd qb
quit
.endc

.end
"""


_NAME_VAL_PAT = re.compile(r"(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*(?P<val>[^\s]+)")


def _parse_spectre_parameters_block(lines: list[str]) -> dict[str, str]:
    params: dict[str, str] = {}
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith("//"):
            continue
        if line.startswith("+"):
            line = line[1:].strip()
        if line.lower().startswith("parameters"):
            line = line.split(None, 1)[1] if len(line.split(None, 1)) == 2 else ""
        for m in _NAME_VAL_PAT.finditer(line):
            params[m.group("name")] = m.group("val")
    return params


def _parse_spectre_section_params(section_text: str) -> dict[str, str]:
    # Handles both styles:
    # 1) "parameters" then "+ a=..." continuation lines
    # 2) repeated "parameters a=..." lines
    lines = section_text.splitlines()
    # Skip until we hit a parameters line.
    start: Optional[int] = None
    for i, l in enumerate(lines):
        if l.strip().lower().startswith("parameters"):
            start = i
            break
    if start is None:
        return {}

    collected: list[str] = []
    for l in lines[start:]:
        ls = l.strip().lower()
        if ls.startswith("include") or ls.startswith("endsection"):
            break
        if ls.startswith("section") and l is not lines[start]:
            break
        collected.append(l)

    return _parse_spectre_parameters_block(collected)


def _extract_spectre_model_stmt_lines(section_text: str, model_name: str) -> list[str]:
    # Spectre allows model statements without braces:
    #   model foo bsim3v3 type=n
    #   + param=...
    start_pat = re.compile(rf"^\s*model\s+{re.escape(model_name)}\b", re.IGNORECASE)
    stop_pat = re.compile(r"^\s*(model\b|inline\s+subckt\b|subckt\b|ends\b|section\b|endsection\b)", re.IGNORECASE)
    lines = section_text.splitlines()
    start_idx: Optional[int] = None
    for i, line in enumerate(lines):
        if start_pat.search(line):
            start_idx = i
            break
    if start_idx is None:
        raise RuntimeError(f"Failed to find model statement for '{model_name}'")

    out: list[str] = []
    for j in range(start_idx, len(lines)):
        line = lines[j]
        if j > start_idx and stop_pat.search(line) and not line.lstrip().startswith("+"):
            break
        out.append(line)
    return out


def _spectre_model_kv_from_lines(model_lines: list[str], env: dict[str, float]) -> tuple[list[tuple[str, str]], list[str]]:
    kv: dict[str, str] = {}
    unresolved: list[str] = []

    assign_pat = re.compile(r"\b([A-Za-z_]\w*)\s*=")

    def iter_assignments(line: str) -> list[tuple[str, str]]:
        # Parse sequences like: a=1 b = x + y c=3
        # capturing RHS possibly containing spaces/operators until next assignment.
        matches = list(assign_pat.finditer(line))
        if not matches:
            return []
        out: list[tuple[str, str]] = []
        for idx, m in enumerate(matches):
            k = m.group(1)
            rhs_start = m.end()
            rhs_end = matches[idx + 1].start() if idx + 1 < len(matches) else len(line)
            v = line[rhs_start:rhs_end].strip()
            # Strip trailing continuation backslashes or commas if any.
            v = v.rstrip("\\,")
            if v:
                out.append((k, v))
        return out

    for raw in model_lines:
        no_comment = raw.split("//", 1)[0].strip()
        if not no_comment:
            continue
        if no_comment.startswith("+"):
            no_comment = no_comment[1:].strip()
        # Strip leading "model <name> <type>" if present.
        if no_comment.lower().startswith("model "):
            parts = no_comment.split()
            # drop first 3 tokens if they look like: model name bsimX
            if len(parts) >= 3:
                no_comment = " ".join(parts[3:])
        for k, v in iter_assignments(no_comment):
            if k.lower() == "type":
                continue
            if re.search(r"[A-Za-z_]", v):
                ev = _safe_eval_expr(v, env)
                if ev is not None:
                    v = f"{ev:.12g}"
                else:
                    unresolved.append(f"{k}={v}")
                    continue
            kv[k] = v
    return list(kv.items()), unresolved


def _extract_spectre_section(text: str, section_name: str) -> str:
    start_pat = re.compile(rf"^\s*section\s+{re.escape(section_name)}\b", re.IGNORECASE)
    end_pat = re.compile(rf"^\s*endsection\s+{re.escape(section_name)}\b", re.IGNORECASE)
    lines = text.splitlines()
    start_idx: Optional[int] = None
    for i, line in enumerate(lines):
        if start_pat.search(line):
            start_idx = i
            break
    if start_idx is None:
        raise RuntimeError(f"Failed to find spectre section '{section_name}'")
    for j in range(start_idx + 1, len(lines)):
        if end_pat.search(lines[j]):
            return "\n".join(lines[start_idx : j + 1])
    raise RuntimeError(f"Failed to find endsection for '{section_name}'")


def _extract_spectre_model_block(section_text: str, model_name: str, model_type: str) -> list[str]:
    # Returns raw lines inside the '{...}' including possibly the header line content after '{'.
    # Example: model nch bsim4 { ... }
    header_pat = re.compile(
        rf"^\s*model\s+{re.escape(model_name)}\s+{re.escape(model_type)}\s*\{{", re.IGNORECASE
    )
    lines = section_text.splitlines()
    start_idx: Optional[int] = None
    for i, line in enumerate(lines):
        if header_pat.search(line):
            start_idx = i
            break
    if start_idx is None:
        raise RuntimeError(f"Failed to find model '{model_name}' of type '{model_type}'")

    collected: list[str] = []
    depth = 0
    started = False
    for line in lines[start_idx:]:
        # Remove line comments early.
        no_comment = line.split("//", 1)[0]
        if not started:
            # Count braces on the header line; capture remainder after first '{' if any.
            if "{" in no_comment:
                started = True
                depth += no_comment.count("{") - no_comment.count("}")
                tail = no_comment.split("{", 1)[1].strip()
                if tail:
                    collected.append(tail)
                continue
        else:
            depth += no_comment.count("{") - no_comment.count("}")
            # Stop when we've closed the initial '{'.
            if depth <= 0:
                # Capture any content before the closing '}' on this line.
                before = no_comment.rsplit("}", 1)[0].strip()
                if before:
                    collected.append(before)
                break
            collected.append(no_comment)

    if not collected:
        raise RuntimeError(f"Empty model block for '{model_name}'")
    return collected


_SPICE_SUFFIX_SCALE = {
    "f": 1e-15,
    "p": 1e-12,
    "n": 1e-9,
    "u": 1e-6,
    "m": 1e-3,
    "k": 1e3,
    "g": 1e9,
    "t": 1e12,
    "meg": 1e6,
}


def _normalize_spice_numbers(expr: str) -> str:
    # Convert SPICE-style suffix numbers (e.g. 1u, 10n, 3meg) into Python-friendly floats.
    # Only rewrites standalone numeric literals.
    pat = re.compile(
        r"(?<![A-Za-z0-9_\.])"  # not preceded by identifier/number/dot
        r"(?P<num>(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)"
        r"(?P<suf>meg|[fpnumkgt])\b",
        re.IGNORECASE,
    )

    def repl(m: re.Match) -> str:
        num = float(m.group("num"))
        suf = m.group("suf").lower()
        scale = _SPICE_SUFFIX_SCALE.get(suf)
        if scale is None:
            return m.group(0)
        return f"({num * scale:.18g})"

    return pat.sub(repl, expr)


def _safe_eval_expr(expr: str, env: dict[str, float]) -> Optional[float]:
    # Only allow simple arithmetic with names, numbers, and operators.
    if re.search(r"[^0-9A-Za-z_+\-*/().eE\s]", expr):
        return None
    try:
        expr = _normalize_spice_numbers(expr)
        return float(eval(expr, {"__builtins__": {}}, env))
    except Exception:
        return None


def _cadence45_generate_ngspice_model_inc(repo_root: Path, out_path: Path) -> None:
    src = repo_root / "pdk" / "cadence45" / "models" / "spectre" / "gpdk045_mos.scs"
    text = src.read_text(errors="ignore")

    tt_section = _extract_spectre_section(text, "tt")
    mos_section = _extract_spectre_section(text, "mos")

    # Parse typical corner parameter values from section tt.
    tt_params_raw = _parse_spectre_section_params(tt_section)

    # Build numeric env.
    env: dict[str, float] = {}
    for k, v in tt_params_raw.items():
        try:
            env[k] = float(v)
        except Exception:
            # Some values might be expressions; try eval.
            ev = _safe_eval_expr(v, env)
            if ev is not None:
                env[k] = ev

    # Force mismatch-related terms to zero for deterministic typical runs.
    for k in [
        "rn1",
        "rn2",
        "rp1",
        "rp2",
        "toxmis_n",
        "vthmis_n",
        "dlmis_n",
        "dwmis_n",
        "toxmis_p",
        "vthmis_p",
        "dlmis_p",
        "dwmis_p",
    ]:
        env[k] = 0.0

    def convert_model(model_name: str, mos_kind: str) -> list[str]:
        raw_lines = _extract_spectre_model_block(mos_section, model_name, "bsim4")
        kv, unresolved = _spectre_model_kv_from_lines(raw_lines, env)
        if unresolved:
            print(
                "[warn] cadence45: unresolved symbols dropped in model conversion for "
                f"{model_name}: {unresolved[:8]}{'...' if len(unresolved) > 8 else ''}"
            )
        if not any(k.lower() == "level" for k, _ in kv):
            kv.insert(0, ("level", "54"))
        out: list[str] = [f".model {model_name} {mos_kind}"]
        for k, v in kv:
            out.append(f"+ {k}={v}")
        return out

    lines_out: list[str] = []
    lines_out.append("* Auto-generated: ngspice-compatible subset for cadence45 (GPDK045)\n")
    lines_out.append(f"* Source: {src.as_posix()}\n")
    lines_out.append("\n")
    lines_out.extend(convert_model("nch", "nmos"))
    lines_out.append("\n")
    lines_out.extend(convert_model("pch", "pmos"))
    lines_out.append("\n")

    out_path.write_text("\n".join(lines_out))


def _cadence45_include_block(repo_root: Path, gen_dir: Path) -> str:
    inc_path = gen_dir / "gpdk045_ngspice_tt.inc"
    if not inc_path.exists():
        _cadence45_generate_ngspice_model_inc(repo_root, inc_path)
    return f".include \"{inc_path.as_posix()}\"\n"


def _cadence90_generate_ngspice_model_inc(repo_root: Path, out_path: Path) -> None:
    src = repo_root / "pdk" / "cadence90" / "models" / "spectre" / "gpdk090_mos.scs"
    text = src.read_text(errors="ignore")
    tt_section = _extract_spectre_section(text, "TT_s1v")
    mos_section = _extract_spectre_section(text, "s1v_mos")

    params_raw = _parse_spectre_section_params(tt_section)
    env: dict[str, float] = {}
    for k, v in params_raw.items():
        try:
            env[k] = float(v)
        except Exception:
            ev = _safe_eval_expr(v, env)
            if ev is not None:
                env[k] = ev

    # Deterministic, no mismatch.
    env.update(
        {
            "pvt_mc": 0.0,
            "pu0_mc": 0.0,
            "pltw_mc": 0.0,
            "varvt": 0.004,
            "mm_delvt": 0.0,
            "mm_dl": 0.0,
            "mm_dw": 0.0,
            "mm_dtox": 0.0,
            "mm_mu0": 1.0,
        }
    )

    def convert(model_name: str, mos_kind: str) -> list[str]:
        model_lines = _extract_spectre_model_stmt_lines(mos_section, model_name)
        kv, unresolved = _spectre_model_kv_from_lines(model_lines, env)
        if unresolved:
            print(
                "[warn] cadence90: unresolved symbols dropped in model conversion for "
                f"{model_name}: {unresolved[:8]}{'...' if len(unresolved) > 8 else ''}"
            )
        if not any(k.lower() == "level" for k, _ in kv):
            kv.insert(0, ("level", "49"))
        out = [f".model {model_name} {mos_kind}"]
        for k, v in kv:
            out.append(f"+ {k}={v}")
        return out

    lines_out: list[str] = []
    lines_out.append("* Auto-generated: ngspice-compatible subset for cadence90 (GPDK090) TT_s1v\n")
    lines_out.append(f"* Source: {src.as_posix()}\n")
    lines_out.append("\n")
    lines_out.extend(convert("gpdk090_nmos1v_x", "nmos"))
    lines_out.append("\n")
    lines_out.extend(convert("gpdk090_pmos1v_x", "pmos"))
    lines_out.append("\n")
    out_path.write_text("\n".join(lines_out))


def _cadence90_include_block(repo_root: Path, gen_dir: Path) -> str:
    inc_path = gen_dir / "gpdk090_ngspice_tt_s1v.inc"
    if not inc_path.exists():
        _cadence90_generate_ngspice_model_inc(repo_root, inc_path)
    return f".include \"{inc_path.as_posix()}\"\n"


def _cadence90_nmos_netlist_text(repo_root: Path, gen_dir: Path, L_um: float, W_um: float, vdd: float) -> str:
    return f"""* Gate-cap sweep (Cadence90 / GPDK090 NMOS1V TT) - Cgs/Cgd/Cgb
.option temp=27 tnom=27
.option gmin=1e-15
.option reltol=1e-8
.option abstol=1e-12
.option chgtol=1e-15
.option method=gear

{_cadence90_include_block(repo_root, gen_dir)}

.param L_dut={L_um:.12g}u
.param W_dut={W_um:.12g}u
.param VDD={vdd:.12g}

Vg gate 0 PULSE(0 {{VDD}} 0n 0.1n 0.1n 10n 20n)
Vd drain 0 DC 0
Vs source 0 DC 0
Vb bulk 0 DC 0

M1 drain gate source bulk gpdk090_nmos1v_x L={{L_dut}} W={{W_dut}}

.control
set filetype=ascii
set nomoremode
tran 0.01n 20n
meas tran qs INTEG i(Vs) from=0n to=10n
meas tran qd INTEG i(Vd) from=0n to=10n
meas tran qb INTEG i(Vb) from=0n to=10n
print qs qd qb
quit
.endc

.end
"""


def _cadence90_nmos_bulkstep_netlist_text(repo_root: Path, gen_dir: Path, L_um: float, W_um: float, vdd: float) -> str:
    return f"""* Bulk-step sweep (Cadence90 / GPDK090 NMOS1V TT) - Csb/Cdb
.option temp=27 tnom=27
.option gmin=1e-15
.option reltol=1e-8
.option abstol=1e-12
.option chgtol=1e-15
.option method=gear

{_cadence90_include_block(repo_root, gen_dir)}

.param L_dut={L_um:.12g}u
.param W_dut={W_um:.12g}u
.param VDD={vdd:.12g}
.param VBN=-VDD

Vg gate 0 DC 0
Vd drain 0 DC 0
Vs source 0 DC 0
Vb bulk 0 PULSE(0 {{VBN}} 0n 0.1n 0.1n 10n 20n)

M1 drain gate source bulk gpdk090_nmos1v_x L={{L_dut}} W={{W_dut}}

.control
set filetype=ascii
set nomoremode
tran 0.01n 20n
meas tran qs INTEG i(Vs) from=0n to=10n
meas tran qd INTEG i(Vd) from=0n to=10n
meas tran qb INTEG i(Vb) from=0n to=10n
print qs qd qb
quit
.endc

.end
"""


def _cadence90_pmos_netlist_text(repo_root: Path, gen_dir: Path, L_um: float, W_um: float, vdd: float) -> str:
    return f"""* Gate-cap sweep (Cadence90 / GPDK090 PMOS1V TT) - Cgs/Cgd/Cgb
.option temp=27 tnom=27
.option gmin=1e-15
.option reltol=1e-8
.option abstol=1e-12
.option chgtol=1e-15
.option method=gear

{_cadence90_include_block(repo_root, gen_dir)}

.param L_dut={L_um:.12g}u
.param W_dut={W_um:.12g}u
.param VDD={vdd:.12g}

Vg gate 0 PULSE({{VDD}} 0 0n 0.1n 0.1n 10n 20n)
Vd drain 0 DC {{VDD}}
Vs source 0 DC {{VDD}}
Vb bulk 0 DC {{VDD}}

M1 drain gate source bulk gpdk090_pmos1v_x L={{L_dut}} W={{W_dut}}

.control
set filetype=ascii
set nomoremode
tran 0.01n 20n
meas tran qs INTEG i(Vs) from=0n to=10n
meas tran qd INTEG i(Vd) from=0n to=10n
meas tran qb INTEG i(Vb) from=0n to=10n
print qs qd qb
quit
.endc

.end
"""


def _cadence90_pmos_bulkstep_netlist_text(repo_root: Path, gen_dir: Path, L_um: float, W_um: float, vdd: float) -> str:
    return f"""* Bulk-step sweep (Cadence90 / GPDK090 PMOS1V TT) - Csb/Cdb
.option temp=27 tnom=27
.option gmin=1e-15
.option reltol=1e-8
.option abstol=1e-12
.option chgtol=1e-15
.option method=gear

{_cadence90_include_block(repo_root, gen_dir)}

.param L_dut={L_um:.12g}u
.param W_dut={W_um:.12g}u
.param VDD={vdd:.12g}

Vg gate 0 DC 0
Vd drain 0 DC 0
Vs source 0 DC 0
Vb bulk 0 PULSE({{VDD}} 0 0n 0.1n 0.1n 10n 20n)

M1 drain gate source bulk gpdk090_pmos1v_x L={{L_dut}} W={{W_dut}}

.control
set filetype=ascii
set nomoremode
tran 0.01n 20n
meas tran qs INTEG i(Vs) from=0n to=10n
meas tran qd INTEG i(Vd) from=0n to=10n
meas tran qb INTEG i(Vb) from=0n to=10n
print qs qd qb
quit
.endc

.end
"""


def _cadence180_generate_ngspice_model_inc(repo_root: Path, out_path: Path) -> None:
    nmos_src = repo_root / "pdk" / "cadence180" / "models" / "spectre" / "nmos1.scs"
    pmos_src = repo_root / "pdk" / "cadence180" / "models" / "spectre" / "pmos1.scs"
    n_text = nmos_src.read_text(errors="ignore")
    p_text = pmos_src.read_text(errors="ignore")

    n_nom = _extract_spectre_section(n_text, "nom")
    p_nom = _extract_spectre_section(p_text, "nom")
    n_mos = _extract_spectre_section(n_text, "mos")
    p_mos = _extract_spectre_section(p_text, "mos")

    n_params_raw = _parse_spectre_section_params(n_nom)
    p_params_raw = _parse_spectre_section_params(p_nom)

    n_env: dict[str, float] = {}
    for k, v in n_params_raw.items():
        try:
            n_env[k] = float(v)
        except Exception:
            ev = _safe_eval_expr(v, n_env)
            if ev is not None:
                n_env[k] = ev
    p_env: dict[str, float] = {}
    for k, v in p_params_raw.items():
        try:
            p_env[k] = float(v)
        except Exception:
            ev = _safe_eval_expr(v, p_env)
            if ev is not None:
                p_env[k] = ev

    def convert(mos_section: str, model_name: str, mos_kind: str, env: dict[str, float]) -> list[str]:
        raw_lines = _extract_spectre_model_block(mos_section, model_name, "bsim3v3")
        kv, unresolved = _spectre_model_kv_from_lines(raw_lines, env)
        if unresolved:
            print(
                "[warn] cadence180: unresolved symbols dropped in model conversion for "
                f"{model_name}: {unresolved[:8]}{'...' if len(unresolved) > 8 else ''}"
            )
        if not any(k.lower() == "level" for k, _ in kv):
            kv.insert(0, ("level", "49"))
        out = [f".model {model_name} {mos_kind}"]
        for k, v in kv:
            out.append(f"+ {k}={v}")
        return out

    lines_out: list[str] = []
    lines_out.append("* Auto-generated: ngspice-compatible subset for cadence180 (GPDK180) nominal\n")
    lines_out.append(f"* Source: {nmos_src.as_posix()} and {pmos_src.as_posix()}\n")
    lines_out.append("\n")
    lines_out.extend(convert(n_mos, "nmos1_int", "nmos", n_env))
    lines_out.append("\n")
    lines_out.extend(convert(p_mos, "pmos1_int", "pmos", p_env))
    lines_out.append("\n")
    out_path.write_text("\n".join(lines_out))


def _cadence180_include_block(repo_root: Path, gen_dir: Path) -> str:
    inc_path = gen_dir / "gpdk180_ngspice_nom.inc"
    if not inc_path.exists():
        _cadence180_generate_ngspice_model_inc(repo_root, inc_path)
    return f".include \"{inc_path.as_posix()}\"\n"


def _cadence180_nmos_netlist_text(repo_root: Path, gen_dir: Path, L_um: float, W_um: float, vdd: float) -> str:
    return f"""* Gate-cap sweep (Cadence180 / GPDK180 NMOS nominal) - Cgs/Cgd/Cgb
.option temp=27 tnom=27
.option gmin=1e-15
.option reltol=1e-8
.option abstol=1e-12
.option chgtol=1e-15
.option method=gear

{_cadence180_include_block(repo_root, gen_dir)}

.param L_dut={L_um:.12g}u
.param W_dut={W_um:.12g}u
.param VDD={vdd:.12g}

Vg gate 0 PULSE(0 {{VDD}} 0n 0.1n 0.1n 10n 20n)
Vd drain 0 DC 0
Vs source 0 DC 0
Vb bulk 0 DC 0

M1 drain gate source bulk nmos1_int L={{L_dut}} W={{W_dut}}

.control
set filetype=ascii
set nomoremode
tran 0.01n 20n
meas tran qs INTEG i(Vs) from=0n to=10n
meas tran qd INTEG i(Vd) from=0n to=10n
meas tran qb INTEG i(Vb) from=0n to=10n
print qs qd qb
quit
.endc

.end
"""


def _cadence180_nmos_bulkstep_netlist_text(repo_root: Path, gen_dir: Path, L_um: float, W_um: float, vdd: float) -> str:
    return f"""* Bulk-step sweep (Cadence180 / GPDK180 NMOS nominal) - Csb/Cdb
.option temp=27 tnom=27
.option gmin=1e-15
.option reltol=1e-8
.option abstol=1e-12
.option chgtol=1e-15
.option method=gear

{_cadence180_include_block(repo_root, gen_dir)}

.param L_dut={L_um:.12g}u
.param W_dut={W_um:.12g}u
.param VDD={vdd:.12g}
.param VBN=-VDD

Vg gate 0 DC 0
Vd drain 0 DC 0
Vs source 0 DC 0
Vb bulk 0 PULSE(0 {{VBN}} 0n 0.1n 0.1n 10n 20n)

M1 drain gate source bulk nmos1_int L={{L_dut}} W={{W_dut}}

.control
set filetype=ascii
set nomoremode
tran 0.01n 20n
meas tran qs INTEG i(Vs) from=0n to=10n
meas tran qd INTEG i(Vd) from=0n to=10n
meas tran qb INTEG i(Vb) from=0n to=10n
print qs qd qb
quit
.endc

.end
"""


def _cadence180_pmos_netlist_text(repo_root: Path, gen_dir: Path, L_um: float, W_um: float, vdd: float) -> str:
    return f"""* Gate-cap sweep (Cadence180 / GPDK180 PMOS nominal) - Cgs/Cgd/Cgb
.option temp=27 tnom=27
.option gmin=1e-15
.option reltol=1e-8
.option abstol=1e-12
.option chgtol=1e-15
.option method=gear

{_cadence180_include_block(repo_root, gen_dir)}

.param L_dut={L_um:.12g}u
.param W_dut={W_um:.12g}u
.param VDD={vdd:.12g}

Vg gate 0 PULSE({{VDD}} 0 0n 0.1n 0.1n 10n 20n)
Vd drain 0 DC {{VDD}}
Vs source 0 DC {{VDD}}
Vb bulk 0 DC {{VDD}}

M1 drain gate source bulk pmos1_int L={{L_dut}} W={{W_dut}}

.control
set filetype=ascii
set nomoremode
tran 0.01n 20n
meas tran qs INTEG i(Vs) from=0n to=10n
meas tran qd INTEG i(Vd) from=0n to=10n
meas tran qb INTEG i(Vb) from=0n to=10n
print qs qd qb
quit
.endc

.end
"""


def _cadence180_pmos_bulkstep_netlist_text(repo_root: Path, gen_dir: Path, L_um: float, W_um: float, vdd: float) -> str:
    return f"""* Bulk-step sweep (Cadence180 / GPDK180 PMOS nominal) - Csb/Cdb
.option temp=27 tnom=27
.option gmin=1e-15
.option reltol=1e-8
.option abstol=1e-12
.option chgtol=1e-15
.option method=gear

{_cadence180_include_block(repo_root, gen_dir)}

.param L_dut={L_um:.12g}u
.param W_dut={W_um:.12g}u
.param VDD={vdd:.12g}

Vg gate 0 DC 0
Vd drain 0 DC 0
Vs source 0 DC 0
Vb bulk 0 PULSE({{VDD}} 0 0n 0.1n 0.1n 10n 20n)

M1 drain gate source bulk pmos1_int L={{L_dut}} W={{W_dut}}

.control
set filetype=ascii
set nomoremode
tran 0.01n 20n
meas tran qs INTEG i(Vs) from=0n to=10n
meas tran qd INTEG i(Vd) from=0n to=10n
meas tran qb INTEG i(Vb) from=0n to=10n
print qs qd qb
quit
.endc

.end
"""


def _cadence45_nmos_netlist_text(repo_root: Path, gen_dir: Path, L_um: float, W_um: float, vdd: float) -> str:
    return f"""* Gate-cap sweep (Cadence45 / GPDK045 NMOS) - Cgs/Cgd/Cgb via terminal current integration
.option temp=27 tnom=27
.option gmin=1e-15
.option reltol=1e-8
.option abstol=1e-12
.option chgtol=1e-15
.option method=gear

{_cadence45_include_block(repo_root, gen_dir)}

.param L_dut={L_um:.12g}u
.param W_dut={W_um:.12g}u
.param VDD={vdd:.12g}

Vg gate 0 PULSE(0 {{VDD}} 0n 0.1n 0.1n 10n 20n)
Vd drain 0 DC 0
Vs source 0 DC 0
Vb bulk 0 DC 0

M1 drain gate source bulk nch L={{L_dut}} W={{W_dut}}

.control
set filetype=ascii
set nomoremode
tran 0.01n 20n
meas tran qs INTEG i(Vs) from=0n to=10n
meas tran qd INTEG i(Vd) from=0n to=10n
meas tran qb INTEG i(Vb) from=0n to=10n
print qs qd qb
quit
.endc

.end
"""


def _cadence45_nmos_bulkstep_netlist_text(repo_root: Path, gen_dir: Path, L_um: float, W_um: float, vdd: float) -> str:
    return f"""* Bulk-step sweep (Cadence45 / GPDK045 NMOS) - Csb/Cdb via terminal current integration
.option temp=27 tnom=27
.option gmin=1e-15
.option reltol=1e-8
.option abstol=1e-12
.option chgtol=1e-15
.option method=gear

{_cadence45_include_block(repo_root, gen_dir)}

.param L_dut={L_um:.12g}u
.param W_dut={W_um:.12g}u
.param VDD={vdd:.12g}
.param VBN=-VDD

Vg gate 0 DC 0
Vd drain 0 DC 0
Vs source 0 DC 0
Vb bulk 0 PULSE(0 {{VBN}} 0n 0.1n 0.1n 10n 20n)

M1 drain gate source bulk nch L={{L_dut}} W={{W_dut}}

.control
set filetype=ascii
set nomoremode
tran 0.01n 20n
meas tran qs INTEG i(Vs) from=0n to=10n
meas tran qd INTEG i(Vd) from=0n to=10n
meas tran qb INTEG i(Vb) from=0n to=10n
print qs qd qb
quit
.endc

.end
"""


def _cadence45_pmos_netlist_text(repo_root: Path, gen_dir: Path, L_um: float, W_um: float, vdd: float) -> str:
    return f"""* Gate-cap sweep (Cadence45 / GPDK045 PMOS) - Cgs/Cgd/Cgb via terminal current integration
.option temp=27 tnom=27
.option gmin=1e-15
.option reltol=1e-8
.option abstol=1e-12
.option chgtol=1e-15
.option method=gear

{_cadence45_include_block(repo_root, gen_dir)}

.param L_dut={L_um:.12g}u
.param W_dut={W_um:.12g}u
.param VDD={vdd:.12g}

Vg gate 0 PULSE({{VDD}} 0 0n 0.1n 0.1n 10n 20n)
Vd drain 0 DC {{VDD}}
Vs source 0 DC {{VDD}}
Vb bulk 0 DC {{VDD}}

M1 drain gate source bulk pch L={{L_dut}} W={{W_dut}}

.control
set filetype=ascii
set nomoremode
tran 0.01n 20n
meas tran qs INTEG i(Vs) from=0n to=10n
meas tran qd INTEG i(Vd) from=0n to=10n
meas tran qb INTEG i(Vb) from=0n to=10n
print qs qd qb
quit
.endc

.end
"""


def _cadence45_pmos_bulkstep_netlist_text(repo_root: Path, gen_dir: Path, L_um: float, W_um: float, vdd: float) -> str:
    return f"""* Bulk-step sweep (Cadence45 / GPDK045 PMOS) - Csb/Cdb via terminal current integration
.option temp=27 tnom=27
.option gmin=1e-15
.option reltol=1e-8
.option abstol=1e-12
.option chgtol=1e-15
.option method=gear

{_cadence45_include_block(repo_root, gen_dir)}

.param L_dut={L_um:.12g}u
.param W_dut={W_um:.12g}u
.param VDD={vdd:.12g}

Vg gate 0 DC 0
Vd drain 0 DC 0
Vs source 0 DC 0
Vb bulk 0 PULSE({{VDD}} 0 0n 0.1n 0.1n 10n 20n)

M1 drain gate source bulk pch L={{L_dut}} W={{W_dut}}

.control
set filetype=ascii
set nomoremode
tran 0.01n 20n
meas tran qs INTEG i(Vs) from=0n to=10n
meas tran qd INTEG i(Vd) from=0n to=10n
meas tran qb INTEG i(Vb) from=0n to=10n
print qs qd qb
quit
.endc

.end
"""


def _nmos_netlist_text(L_um: float, W_um: float, vdd: float) -> str:
    return f"""* Gate-cap sweep (NMOS) - Cgs/Cgd/Cgb via terminal current integration
.option temp=27 tnom=27
.option gmin=1e-15
.option reltol=1e-8
.option abstol=1e-12
.option chgtol=1e-15
.option method=gear

.inc ../models/FreePDK45/nom.inc

.param L_dut={L_um:.12g}u
.param W_dut={W_um:.12g}u
.param VDD={vdd:.12g}

* Biases: use Vds=0 to avoid conduction; measure mostly displacement charge
Vg gate 0 PULSE(0 {{VDD}} 0n 0.1n 0.1n 10n 20n)
Vd drain 0 DC 0
Vs source 0 DC 0
Vb bulk 0 DC 0

M1 drain gate source bulk NMOS_VTG L={{L_dut}} W={{W_dut}}

.control
set filetype=ascii
set nomoremode
tran 0.01n 20n
meas tran qs INTEG i(Vs) from=0n to=10n
meas tran qd INTEG i(Vd) from=0n to=10n
meas tran qb INTEG i(Vb) from=0n to=10n
print qs qd qb
quit
.endc

.end
"""


def _nmos_bulkstep_netlist_text(L_um: float, W_um: float, vdd: float) -> str:
    return f"""* Bulk-step sweep (NMOS) - Csb/Cdb via terminal current integration
.option temp=27 tnom=27
.option gmin=1e-15
.option reltol=1e-8
.option abstol=1e-12
.option chgtol=1e-15
.option method=gear

.inc ../models/FreePDK45/nom.inc

.param L_dut={L_um:.12g}u
.param W_dut={W_um:.12g}u
.param VDD={vdd:.12g}
.param VBN=-VDD

* Biases: keep channel off (Vg=0), use Vds=0, step bulk 0->-VDD (reverse bias)
Vg gate 0 DC 0
Vd drain 0 DC 0
Vs source 0 DC 0
Vb bulk 0 PULSE(0 {{VBN}} 0n 0.1n 0.1n 10n 20n)

M1 drain gate source bulk NMOS_VTG L={{L_dut}} W={{W_dut}}

.control
set filetype=ascii
set nomoremode
tran 0.01n 20n
meas tran qs INTEG i(Vs) from=0n to=10n
meas tran qd INTEG i(Vd) from=0n to=10n
meas tran qb INTEG i(Vb) from=0n to=10n
print qs qd qb
quit
.endc

.end
"""


def _pmos_netlist_text(L_um: float, W_um: float, vdd: float) -> str:
    return f"""* Gate-cap sweep (PMOS) - Cgs/Cgd/Cgb via terminal current integration
.option temp=27 tnom=27
.option gmin=1e-15
.option reltol=1e-8
.option abstol=1e-12
.option chgtol=1e-15
.option method=gear

.inc ../models/FreePDK45/nom.inc

.param L_dut={L_um:.12g}u
.param W_dut={W_um:.12g}u
.param VDD={vdd:.12g}

* Biases: use Vds=0 to avoid conduction; gate steps VDD->0
Vg gate 0 PULSE({{VDD}} 0 0n 0.1n 0.1n 10n 20n)
Vd drain 0 DC {{VDD}}
Vs source 0 DC {{VDD}}
Vb bulk 0 DC {{VDD}}

M1 drain gate source bulk PMOS_VTG L={{L_dut}} W={{W_dut}}

.control
set filetype=ascii
set nomoremode
tran 0.01n 20n
meas tran qs INTEG i(Vs) from=0n to=10n
meas tran qd INTEG i(Vd) from=0n to=10n
meas tran qb INTEG i(Vb) from=0n to=10n
print qs qd qb
quit
.endc

.end
"""


def _pmos_bulkstep_netlist_text(L_um: float, W_um: float, vdd: float) -> str:
    return f"""* Bulk-step sweep (PMOS) - Csb/Cdb via terminal current integration
.option temp=27 tnom=27
.option gmin=1e-15
.option reltol=1e-8
.option abstol=1e-12
.option chgtol=1e-15
.option method=gear

.inc ../models/FreePDK45/nom.inc

.param L_dut={L_um:.12g}u
.param W_dut={W_um:.12g}u
.param VDD={vdd:.12g}

* Biases: keep channel off (Vg=0), use Vds=0, step bulk VDD->0 (reverse-to-zero)
Vg gate 0 DC 0
Vd drain 0 DC 0
Vs source 0 DC 0
Vb bulk 0 PULSE({{VDD}} 0 0n 0.1n 0.1n 10n 20n)

M1 drain gate source bulk PMOS_VTG L={{L_dut}} W={{W_dut}}

.control
set filetype=ascii
set nomoremode
tran 0.01n 20n
meas tran qs INTEG i(Vs) from=0n to=10n
meas tran qd INTEG i(Vd) from=0n to=10n
meas tran qb INTEG i(Vb) from=0n to=10n
print qs qd qb
quit
.endc

.end
"""


def parse_args():
    p = argparse.ArgumentParser(
        description=(
            "Sweep MOS (L,W) and extract large-signal gate caps Cgs/Cgd/Cgb via TRAN terminal current integration. "
            "Outputs cap_vs_LW.csv and cap_vs_LW_pmos.csv under test_cap_param/results/<pdk_lower>/."
        )
    )
    p.add_argument("--pdk", default="FreePDK45_nom_T27", help="Results label / directory name (default: FreePDK45_nom_T27)")
    p.add_argument(
        "--vdd",
        type=float,
        default=None,
        help="Step amplitude (V). If not set: 1.2 for FreePDK45, 1.8 for Sky130.",
    )
    p.add_argument("--max-L-count", type=int, default=8, help="Number of L points to use from default list (default: 8)")
    p.add_argument("--max-W-count", type=int, default=12, help="Number of W points to use from default list (default: 12)")
    p.add_argument("--skip-pmos", action="store_true", help="Skip PMOS sweep")
    return p.parse_args()


def _subsample_evenly(values: np.ndarray, count: int) -> np.ndarray:
    if count <= 0:
        return values[:0]
    if len(values) <= count:
        return values
    idx = np.linspace(0, len(values) - 1, num=count)
    idx = np.unique(np.round(idx).astype(int))
    # Ensure we always return exactly count points when possible.
    if len(idx) < count:
        extras = [i for i in range(len(values)) if i not in set(idx)]
        idx = np.array(list(idx) + extras[: (count - len(idx))], dtype=int)
    idx = np.sort(idx[:count])
    return values[idx]


def _sky130_model_pairs_common(repo_root: Path):
    """Return (L_candidates_um, W_candidates_um, allowed_pairs) for Sky130.

    The Sky130 pm3 model files encode bin ranges (lmin/lmax/wmin/wmax) that behave like
    a sparse grid of supported (L, W) points. To avoid cross-bin artifacts, we derive
    the bin-center points from BOTH nfet_01v8 and pfet_01v8 and use the intersection.

    Returns:
      L_candidates_um: sorted unique L centers (um)
      W_candidates_um: sorted unique W centers (um)
      allowed_pairs: set of (L_um_round6, W_um_round6) present in both devices
    """

    def parse_pairs(path: Path) -> set[tuple[float, float]]:
        lmin_re = re.compile(r"\blmin\s*=\s*([0-9.+\-eE]+)")
        lmax_re = re.compile(r"\blmax\s*=\s*([0-9.+\-eE]+)")
        wmin_re = re.compile(r"\bwmin\s*=\s*([0-9.+\-eE]+)")
        wmax_re = re.compile(r"\bwmax\s*=\s*([0-9.+\-eE]+)")

        pairs: set[tuple[float, float]] = set()
        for raw in path.read_text(errors="ignore").splitlines():
            m1 = lmin_re.search(raw)
            m2 = lmax_re.search(raw)
            m3 = wmin_re.search(raw)
            m4 = wmax_re.search(raw)
            if not (m1 and m2 and m3 and m4):
                continue
            lmin_um = float(m1.group(1)) * 1e6
            lmax_um = float(m2.group(1)) * 1e6
            wmin_um = float(m3.group(1)) * 1e6
            wmax_um = float(m4.group(1)) * 1e6
            L_um = 0.5 * (lmin_um + lmax_um)
            W_um = 0.5 * (wmin_um + wmax_um)
            pairs.add((round(L_um, 6), round(W_um, 6)))
        return pairs

    nfet = (
        repo_root
        / "models"
        / "skywater-pdk-libs-sky130_fd_pr"
        / "cells"
        / "nfet_01v8"
        / "sky130_fd_pr__nfet_01v8.pm3.spice"
    )
    pfet = (
        repo_root
        / "models"
        / "skywater-pdk-libs-sky130_fd_pr"
        / "cells"
        / "pfet_01v8"
        / "sky130_fd_pr__pfet_01v8.pm3.spice"
    )
    if not (nfet.exists() and pfet.exists()):
        return np.array([], dtype=float), np.array([], dtype=float), set()

    common = parse_pairs(nfet) & parse_pairs(pfet)
    if not common:
        return np.array([], dtype=float), np.array([], dtype=float), set()

    Ls = sorted({L for L, _ in common})
    Ws = sorted({W for _, W in common})
    return np.array(Ls, dtype=float), np.array(Ws, dtype=float), common


def _sky130_model_pairs_by_device(repo_root: Path):
    """Return (pairs_n, pairs_p, all_pairs) for Sky130.

    For Sky130, the pm3 files define many narrow (lmin/lmax/wmin/wmax) windows.
    If we only simulate the window center points, each window contributes a single
    (L, W) point and bin-aware fits become empty (need >=2 points per bin).

    Strategy:
      - For each bin window, pick TWO L points inside [lmin, lmax] near the center.
      - Fix W at the bin center (within [wmin, wmax]).
      - Do this independently for nfet and pfet.

    Returns:
      pairs_n: set of (L_um_round6, W_um_round6) supported by nfet
      pairs_p: set of (L_um_round6, W_um_round6) supported by pfet
      all_pairs: sorted list of union pairs for iteration
    """

    def parse_bins(path: Path) -> list[tuple[float, float, float, float]]:
        lmin_re = re.compile(r"\blmin\s*=\s*([0-9.+\-eE]+)")
        lmax_re = re.compile(r"\blmax\s*=\s*([0-9.+\-eE]+)")
        wmin_re = re.compile(r"\bwmin\s*=\s*([0-9.+\-eE]+)")
        wmax_re = re.compile(r"\bwmax\s*=\s*([0-9.+\-eE]+)")
        out: list[tuple[float, float, float, float]] = []
        for raw in path.read_text(errors="ignore").splitlines():
            m1 = lmin_re.search(raw)
            m2 = lmax_re.search(raw)
            m3 = wmin_re.search(raw)
            m4 = wmax_re.search(raw)
            if not (m1 and m2 and m3 and m4):
                continue
            lmin_um = float(m1.group(1)) * 1e6
            lmax_um = float(m2.group(1)) * 1e6
            wmin_um = float(m3.group(1)) * 1e6
            wmax_um = float(m4.group(1)) * 1e6
            if lmax_um <= lmin_um or wmax_um <= wmin_um:
                continue
            out.append((lmin_um, lmax_um, wmin_um, wmax_um))
        return out

    def sample_pairs(bins: list[tuple[float, float, float, float]]) -> set[tuple[float, float]]:
        pairs: set[tuple[float, float]] = set()
        for (lmin_um, lmax_um, wmin_um, wmax_um) in bins:
            L_mid = 0.5 * (lmin_um + lmax_um)
            W_mid = 0.5 * (wmin_um + wmax_um)
            # Five samples per axis within the bin window.
            # This makes by-bin fits more stable than the 2/3-point case.
            span_L = max(0.0, lmax_um - lmin_um)
            span_W = max(0.0, wmax_um - wmin_um)

            def _five_points(min_v: float, mid_v: float, max_v: float) -> list[float]:
                span = max(0.0, max_v - min_v)
                d = 0.4 * span
                d2 = 0.2 * span
                pts = [
                    max(min_v, min(max_v, mid_v - d)),
                    max(min_v, min(max_v, mid_v - d2)),
                    max(min_v, min(max_v, mid_v)),
                    max(min_v, min(max_v, mid_v + d2)),
                    max(min_v, min(max_v, mid_v + d)),
                ]
                # If window is narrow, fall back to evenly spaced 5 points.
                if len({round(x, 12) for x in pts}) < 5:
                    pts = [min_v + (i / 4.0) * span for i in range(5)]
                # Clamp again for safety.
                return [max(min_v, min(max_v, x)) for x in pts]

            Ls = _five_points(lmin_um, L_mid, lmax_um)
            Ws = _five_points(wmin_um, W_mid, wmax_um)

            # Typical unique samples per bin:
            #  - 5 points varying L at fixed W_mid
            #  - 5 points varying W at fixed L_mid
            # (L_mid, W_mid) overlaps and is de-duplicated by the set.
            for L in Ls:
                pairs.add((round(float(L), 6), round(float(W_mid), 6)))
            for W in Ws:
                pairs.add((round(float(L_mid), 6), round(float(W), 6)))
        return pairs

    nfet = (
        repo_root
        / "models"
        / "skywater-pdk-libs-sky130_fd_pr"
        / "cells"
        / "nfet_01v8"
        / "sky130_fd_pr__nfet_01v8.pm3.spice"
    )
    pfet = (
        repo_root
        / "models"
        / "skywater-pdk-libs-sky130_fd_pr"
        / "cells"
        / "pfet_01v8"
        / "sky130_fd_pr__pfet_01v8.pm3.spice"
    )
    if not (nfet.exists() and pfet.exists()):
        return set(), set(), []

    pairs_n = sample_pairs(parse_bins(nfet))
    pairs_p = sample_pairs(parse_bins(pfet))
    all_pairs = sorted(pairs_n | pairs_p)
    return pairs_n, pairs_p, all_pairs


def main():
    args = parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    netlists_dir = repo_root / "netlists"

    pdk_lower = args.pdk.lower()
    results_dir = repo_root / "test_cap_param" / "results" / pdk_lower
    plots_dir = results_dir / "plots"
    results_dir.mkdir(parents=True, exist_ok=True)
    plots_dir.mkdir(parents=True, exist_ok=True)

    gen_dir = netlists_dir / pdk_lower
    gen_dir.mkdir(parents=True, exist_ok=True)

    vdd = args.vdd
    if vdd is None:
        if _is_sky130(pdk_lower):
            vdd = 1.8
        elif _is_cadence45(pdk_lower):
            vdd = 1.1
        elif _is_cadence90(pdk_lower):
            vdd = 1.0
        elif _is_cadence180(pdk_lower):
            vdd = 1.8
        else:
            vdd = 1.2

    if _is_cadence14(pdk_lower):
        raise RuntimeError(
            "cadence14 models are Spectre BSIM-CMG (FinFET) and are not supported by the installed ngspice. "
            "To run cadence14, use Spectre (or another simulator with BSIM-CMG support), or switch to a BSIM4-based PDK."
        )

    # Default sweep depends on PDK.
    if _is_sky130(pdk_lower):
        # Prefer model-bin-derived points within the global model range.
        # We sample two L points per bin window so bin-aware fits have >=2 points.
        pairs_n, pairs_p, all_pairs = _sky130_model_pairs_by_device(repo_root)
        use_model_pairs = len(all_pairs) >= 16
        if not use_model_pairs:
            # Fallback: conservative global range (still within typical model limits).
            L_list_um = np.linspace(0.15, 20.0, num=40)
            W_list_um = np.linspace(0.42, 7.0, num=60)
            pairs_n = set()
            pairs_p = set()
            all_pairs = []
    else:
        if _is_cadence45(pdk_lower):
            # GPDK045 demo models in this repo have L/W ranges in microns (see lmin/wmin in model file).
            L_list_um = np.linspace(2.0, 20.0, num=40)
            W_list_um = np.linspace(2.0, 50.0, num=60)
        elif _is_cadence90(pdk_lower):
            # GPDK090 (1V devices) default l=0.1u, typical widths up to ~10u+.
            L_list_um = np.linspace(0.1, 2.0, num=40)
            W_list_um = np.linspace(0.4, 40.0, num=60)
        elif _is_cadence180(pdk_lower):
            # GPDK180 typical ranges in models: L>=0.18u, W>=0.4u.
            L_list_um = np.linspace(0.18, 10.0, num=40)
            W_list_um = np.linspace(0.4, 80.0, num=60)
        else:
            # FreePDK45-ish: log-spaced L, linear W
            L_list_um = np.logspace(np.log10(0.045), np.log10(10.0), num=30)
            W_list_um = np.arange(0.1, 5.0 + 0.5 * 0.1, 0.1)

    if not (_is_sky130(pdk_lower) and "use_model_pairs" in locals() and use_model_pairs):
        L_list_um = _subsample_evenly(L_list_um, max(2, int(args.max_L_count)))
        W_list_um = _subsample_evenly(W_list_um, max(2, int(args.max_W_count)))

    records_n = []  # (L, W, Cgs_fF, Cgd_fF, Cgb_fF, Csb_fF, Cdb_fF)
    records_p = []  # (L, W, Cgs_p_fF, Cgd_p_fF, Cgb_p_fF, Csb_p_fF, Cdb_p_fF)

    if _is_sky130(pdk_lower) and "use_model_pairs" in locals() and use_model_pairs:
        iter_pairs = all_pairs
    else:
        iter_pairs = [(float(L), float(W)) for L in L_list_um for W in W_list_um]

    for L_um, W_um in iter_pairs:
        prefix = pdk_lower

        # Sky130: per-device support can differ; skip unsupported points per device.
        if _is_sky130(pdk_lower) and "use_model_pairs" in locals() and use_model_pairs:
            key = (round(float(L_um), 6), round(float(W_um), 6))
            run_nmos = key in pairs_n
            run_pmos = (not args.skip_pmos) and (key in pairs_p)
            if not (run_nmos or run_pmos):
                continue
        else:
            run_nmos = True
            run_pmos = not args.skip_pmos

        nmos_ok = False
        if run_nmos:
            nmos_name = f"{prefix}_gatecaps_nmos_L{L_um:.6g}u_W{W_um:.6g}u.cir"
            nmos_path = gen_dir / nmos_name
            if _is_sky130(pdk_lower):
                nmos_path.write_text(_sky130_nmos_netlist_text(float(L_um), float(W_um), vdd))
            elif _is_cadence45(pdk_lower):
                nmos_path.write_text(_cadence45_nmos_netlist_text(repo_root, gen_dir, float(L_um), float(W_um), vdd))
            elif _is_cadence90(pdk_lower):
                nmos_path.write_text(_cadence90_nmos_netlist_text(repo_root, gen_dir, float(L_um), float(W_um), vdd))
            elif _is_cadence180(pdk_lower):
                nmos_path.write_text(_cadence180_nmos_netlist_text(repo_root, gen_dir, float(L_um), float(W_um), vdd))
            else:
                nmos_path.write_text(_nmos_netlist_text(float(L_um), float(W_um), vdd))

            try:
                stdout = run_ngspice(nmos_path, cwd=netlists_dir)
            except RuntimeError:
                stdout = None

            qsqdqb = parse_terminal_charges(stdout) if stdout is not None else {}
            if not {"qs", "qd", "qb"}.issubset(qsqdqb.keys()):
                # Don't abort this (L,W) entirely; PMOS may still work.
                qsqdqb = None

            if qsqdqb is not None:
                cgs = -(qsqdqb["qs"]) / vdd
                cgd = -(qsqdqb["qd"]) / vdd
                cgb = -(qsqdqb["qb"]) / vdd

                nmos_b_name = f"{prefix}_bulkstep_nmos_L{L_um:.6g}u_W{W_um:.6g}u.cir"
                nmos_b_path = gen_dir / nmos_b_name
                if _is_sky130(pdk_lower):
                    nmos_b_path.write_text(_sky130_nmos_bulkstep_netlist_text(float(L_um), float(W_um), vdd))
                elif _is_cadence45(pdk_lower):
                    nmos_b_path.write_text(
                        _cadence45_nmos_bulkstep_netlist_text(repo_root, gen_dir, float(L_um), float(W_um), vdd)
                    )
                elif _is_cadence90(pdk_lower):
                    nmos_b_path.write_text(
                        _cadence90_nmos_bulkstep_netlist_text(repo_root, gen_dir, float(L_um), float(W_um), vdd)
                    )
                elif _is_cadence180(pdk_lower):
                    nmos_b_path.write_text(
                        _cadence180_nmos_bulkstep_netlist_text(repo_root, gen_dir, float(L_um), float(W_um), vdd)
                    )
                else:
                    nmos_b_path.write_text(_nmos_bulkstep_netlist_text(float(L_um), float(W_um), vdd))
                try:
                    stdout_b = run_ngspice(nmos_b_path, cwd=netlists_dir)
                except RuntimeError:
                    stdout_b = None

                qsqdqb_b = parse_terminal_charges(stdout_b) if stdout_b is not None else {}
                if {"qs", "qd"}.issubset(qsqdqb_b.keys()):
                    csb = -(qsqdqb_b["qs"]) / vdd
                    cdb = -(qsqdqb_b["qd"]) / vdd
                    records_n.append(
                        (
                            float(L_um),
                            float(W_um),
                            cgs * 1e15,
                            cgd * 1e15,
                            cgb * 1e15,
                            csb * 1e15,
                            cdb * 1e15,
                        )
                    )
                    nmos_ok = True

        if not run_pmos:
            continue

        pmos_name = f"{prefix}_gatecaps_pmos_L{L_um:.6g}u_W{W_um:.6g}u.cir"
        pmos_path = gen_dir / pmos_name
        if _is_sky130(pdk_lower):
            pmos_path.write_text(_sky130_pmos_netlist_text(float(L_um), float(W_um), vdd))
        elif _is_cadence45(pdk_lower):
            pmos_path.write_text(_cadence45_pmos_netlist_text(repo_root, gen_dir, float(L_um), float(W_um), vdd))
        elif _is_cadence90(pdk_lower):
            pmos_path.write_text(_cadence90_pmos_netlist_text(repo_root, gen_dir, float(L_um), float(W_um), vdd))
        elif _is_cadence180(pdk_lower):
            pmos_path.write_text(_cadence180_pmos_netlist_text(repo_root, gen_dir, float(L_um), float(W_um), vdd))
        else:
            pmos_path.write_text(_pmos_netlist_text(float(L_um), float(W_um), vdd))

        try:
            stdout_p = run_ngspice(pmos_path, cwd=netlists_dir)
        except RuntimeError:
            continue

        qsqdqb_p = parse_terminal_charges(stdout_p)
        if not {"qs", "qd", "qb"}.issubset(qsqdqb_p.keys()):
            continue
        cgs_p = -(qsqdqb_p["qs"]) / vdd
        cgd_p = -(qsqdqb_p["qd"]) / vdd
        cgb_p = -(qsqdqb_p["qb"]) / vdd

        pmos_b_name = f"{prefix}_bulkstep_pmos_L{L_um:.6g}u_W{W_um:.6g}u.cir"
        pmos_b_path = gen_dir / pmos_b_name
        if _is_sky130(pdk_lower):
            pmos_b_path.write_text(_sky130_pmos_bulkstep_netlist_text(float(L_um), float(W_um), vdd))
        elif _is_cadence45(pdk_lower):
            pmos_b_path.write_text(
                _cadence45_pmos_bulkstep_netlist_text(repo_root, gen_dir, float(L_um), float(W_um), vdd)
            )
        elif _is_cadence90(pdk_lower):
            pmos_b_path.write_text(_cadence90_pmos_bulkstep_netlist_text(repo_root, gen_dir, float(L_um), float(W_um), vdd))
        elif _is_cadence180(pdk_lower):
            pmos_b_path.write_text(_cadence180_pmos_bulkstep_netlist_text(repo_root, gen_dir, float(L_um), float(W_um), vdd))
        else:
            pmos_b_path.write_text(_pmos_bulkstep_netlist_text(float(L_um), float(W_um), vdd))
        try:
            stdout_pb = run_ngspice(pmos_b_path, cwd=netlists_dir)
        except RuntimeError:
            continue

        qsqdqb_pb = parse_terminal_charges(stdout_pb)
        if not {"qs", "qd"}.issubset(qsqdqb_pb.keys()):
            continue
        csb_p = -(qsqdqb_pb["qs"]) / vdd
        cdb_p = -(qsqdqb_pb["qd"]) / vdd

        records_p.append(
            (
                float(L_um),
                float(W_um),
                cgs_p * 1e15,
                cgd_p * 1e15,
                cgb_p * 1e15,
                csb_p * 1e15,
                cdb_p * 1e15,
            )
        )

    if not records_n:
        raise RuntimeError("No NMOS points collected (ngspice/parse failed for all points)")

    n_arr = np.array(records_n, dtype=float)
    out_n = results_dir / "cap_vs_LW.csv"
    header_n = "L_um,W_um,Cgs_fF,Cgd_fF,Cgb_fF,Csb_fF,Cdb_fF"
    np.savetxt(out_n, n_arr, delimiter=",", header=header_n, comments="")

    if records_p:
        p_arr = np.array(records_p, dtype=float)
        out_p = results_dir / "cap_vs_LW_pmos.csv"
        header_p = "L_um,W_um,Cgs_p_fF,Cgd_p_fF,Cgb_p_fF,Csb_p_fF,Cdb_p_fF"
        np.savetxt(out_p, p_arr, delimiter=",", header=header_p, comments="")

    print(f"[OK] Wrote {out_n} ({len(records_n)} points)")
    if records_p:
        print(f"[OK] Wrote {results_dir / 'cap_vs_LW_pmos.csv'} ({len(records_p)} points)")


if __name__ == "__main__":
    main()
