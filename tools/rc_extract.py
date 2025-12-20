#!/usr/bin/env python3

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


_THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_THIS_DIR))

import generate_spice_netlist as gsn  # type: ignore


_UNIT_MULTIPLIERS: Dict[str, float] = {
    "f": 1e-15,
    "p": 1e-12,
    "n": 1e-9,
    "u": 1e-6,
    "m": 1e-3,
    "k": 1e3,
    "meg": 1e6,
    "g": 1e9,
    "t": 1e12,
}


def _parse_eng_value(s: str) -> float:
    st = str(s).strip()
    m = re.fullmatch(r"([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)\s*([a-zA-Z]+)?", st)
    if not m:
        raise ValueError(f"Cannot parse numeric value: {s!r}")
    base = float(m.group(1))
    unit = (m.group(2) or "").strip()
    if not unit:
        return base
    unit_l = unit.lower()
    if unit_l in _UNIT_MULTIPLIERS:
        return base * _UNIT_MULTIPLIERS[unit_l]
    raise ValueError(f"Unsupported unit suffix {unit!r} in value {s!r}")


def _sanitize_tag(tag: str) -> str:
    out = []
    for ch in tag:
        if ch.isalnum():
            out.append(ch)
        else:
            out.append("_")
    s = "".join(out)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "run"


def _resolve_path(p: str, repo_root: Path) -> Path:
    cand = Path(p)
    if cand.is_absolute():
        return cand
    if cand.exists():
        return cand.resolve()
    alt = repo_root / cand
    if alt.exists():
        return alt.resolve()
    return cand.resolve()


def _render_tokens(text: str, mapping: Dict[str, str]) -> str:
    for k, v in mapping.items():
        text = text.replace(k, v)
    return text


def _run_ngspice(netlist: Path, cwd: Path) -> Tuple[int, str, str]:
    proc = subprocess.Popen(
        ["ngspice", "-b", netlist.name],
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout, stderr = proc.communicate()
    return proc.returncode, stdout, stderr


def _load_rc_step(path: Path) -> Tuple[List[float], List[float], List[float]]:
    lines = [ln.strip() for ln in path.read_text(encoding="utf-8", errors="ignore").splitlines() if ln.strip()]
    if len(lines) < 2:
        raise RuntimeError(f"Unexpected rc_step format: {path}")

    header = lines[0].split()
    if not header:
        raise RuntimeError(f"Empty header in: {path}")

    def find_col(name: str) -> Optional[int]:
        for i, h in enumerate(header):
            if h.strip() == name:
                return i
        return None

    vg_col = find_col("v(gate_rc)")
    id_col = find_col("id")
    time_col = find_col("time")
    if time_col is None:
        time_col = 0

    # Fallback for variations in capitalization
    if vg_col is None:
        for i, h in enumerate(header):
            if "gate_rc" in h.lower():
                vg_col = i
                break
    if id_col is None:
        for i, h in enumerate(header):
            if h.lower() == "id":
                id_col = i
                break

    if vg_col is None or id_col is None:
        raise RuntimeError(f"Cannot locate required columns in header {header!r} for file {path}")

    t: List[float] = []
    vg: List[float] = []
    ids: List[float] = []
    for ln in lines[1:]:
        parts = ln.split()
        if len(parts) <= max(time_col, vg_col, id_col):
            continue
        try:
            t.append(float(parts[time_col]))
            vg.append(float(parts[vg_col]))
            ids.append(float(parts[id_col]))
        except ValueError:
            continue

    if not t:
        raise RuntimeError(f"No numeric samples found in: {path}")
    return t, vg, ids


def _find_tau_63(t: List[float], vg: List[float]) -> float:
    v0 = vg[0]
    v1 = max(vg)
    if v1 == v0:
        return float("nan")
    target = v0 + 0.6321205588 * (v1 - v0)
    for i in range(1, len(t)):
        if (vg[i - 1] - target) * (vg[i] - target) <= 0:
            dt = t[i] - t[i - 1]
            if dt == 0:
                return t[i]
            frac = (target - vg[i - 1]) / (vg[i] - vg[i - 1]) if vg[i] != vg[i - 1] else 0.0
            return t[i - 1] + frac * dt
    return float("nan")


@dataclass
class RcResult:
    tau: float
    ceff: float
    ids_final: float
    r_equiv: float


@dataclass
class RcSweepPoint:
    w: str
    l: str
    tau: float
    ceff: float
    ids_final: float
    r_equiv: float


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="RC extraction prototype (MVP)")
    parser.add_argument("--model-file", required=True)
    parser.add_argument("--device-name", required=True)
    parser.add_argument("--from-model-name", default="NMOS_VTG")
    parser.add_argument("--template-netlist", default="netlists/rc_gate_step_circuit.cir")
    parser.add_argument("--output-dir", default="rc_extract_results")

    parser.add_argument("--w", default="1u")
    parser.add_argument("--l", default="0.15u")

    parser.add_argument("--sweep-mode", choices=["none", "w", "l"], default="none")
    parser.add_argument(
        "--w-sweep",
        nargs="+",
        default=["0.5u", "1u", "2u", "5u"],
    )
    parser.add_argument(
        "--l-sweep",
        nargs="+",
        default=["0.15u", "0.3u", "0.5u", "1u"],
    )
    parser.add_argument("--w-fixed", default=None)
    parser.add_argument("--l-fixed", default=None)

    parser.add_argument("--vds", default="0.6")
    parser.add_argument("--vgs", default="1.2")
    parser.add_argument("--temp", default="27")

    parser.add_argument("--rdrive", default="1k")
    parser.add_argument("--td", default="0")
    parser.add_argument("--tr", default="1p")
    parser.add_argument("--tf", default="1p")
    parser.add_argument("--pw", default="10n")
    parser.add_argument("--per", default="20n")
    parser.add_argument("--tstep", default="1p")
    parser.add_argument("--tstop", default="20n")

    parser.add_argument("--w-param", default=None)
    parser.add_argument("--l-param", default=None)

    args = parser.parse_args(argv)

    repo_root = _THIS_DIR.parent
    model_file = _resolve_path(args.model_file, repo_root)
    template_netlist = _resolve_path(args.template_netlist, repo_root)
    output_dir = Path(args.output_dir).resolve()

    if not model_file.exists():
        raise SystemExit(f"Model file not found: {model_file}")
    if not template_netlist.exists():
        raise SystemExit(f"Template netlist not found: {template_netlist}")

    chosen = gsn.choose_device_from_model_file(model_file, args.device_name)
    chosen = gsn.preprocess_hspice_model_for_ngspice(chosen)

    w_param = args.w_param
    l_param = args.l_param
    if w_param is None or l_param is None:
        if chosen.style == "subckt":
            w_param = w_param or "w"
            l_param = l_param or "l"
        else:
            w_param = w_param or "W"
            l_param = l_param or "L"

    output_dir.mkdir(parents=True, exist_ok=True)

    base_template = template_netlist.read_text(encoding="utf-8", errors="ignore")

    def run_point(w: str, l: str) -> Tuple[RcResult, Path]:
        tag = _sanitize_tag(f"W{w}_L{l}")
        run_dir = output_dir / "runs" / tag
        run_dir.mkdir(parents=True, exist_ok=True)

        tmpl_path = run_dir / "template.cir"
        tmpl_path.write_text(base_template, encoding="utf-8")

        adapted_path = run_dir / "adapted.cir"
        gsn.transform_netlist(
            base_netlist=tmpl_path,
            output_netlist=adapted_path,
            chosen_device=chosen,
            old_model_name=args.from_model_name,
        )

        token_map = {
            "__W__": str(w),
            "__L__": str(l),
            "__VDS__": str(args.vds),
            "__VGS__": str(args.vgs),
            "__TEMP__": str(args.temp),
            "__TAG__": tag,
            "__WPARAM__": str(w_param),
            "__LPARAM__": str(l_param),
            "__RDRIVE__": str(args.rdrive),
            "__TD__": str(args.td),
            "__TR__": str(args.tr),
            "__TF__": str(args.tf),
            "__PW__": str(args.pw),
            "__PER__": str(args.per),
            "__TSTEP__": str(args.tstep),
            "__TSTOP__": str(args.tstop),
        }

        rendered = _render_tokens(adapted_path.read_text(encoding="utf-8", errors="ignore"), token_map)
        final_path = run_dir / f"rc_{tag}.cir"
        final_path.write_text(rendered, encoding="utf-8")

        rc, stdout, stderr = _run_ngspice(final_path, cwd=run_dir)
        (run_dir / "ngspice_stdout.txt").write_text(stdout or "", encoding="utf-8")
        (run_dir / "ngspice_stderr.txt").write_text(stderr or "", encoding="utf-8")
        if rc != 0:
            raise RuntimeError(f"ngspice failed (rc={rc}). See logs in {run_dir}")

        out_file = run_dir / f"rc_step_{tag}.txt"
        if not out_file.exists():
            raise RuntimeError(f"Expected output file not found: {out_file}")

        t, vg, ids = _load_rc_step(out_file)

        tau = _find_tau_63(t, vg)
        rdrive_ohm = _parse_eng_value(args.rdrive)
        ceff = tau / rdrive_ohm if (rdrive_ohm > 0 and tau == tau) else float("nan")

        max_idx = max(range(len(vg)), key=lambda i: vg[i])
        ids_final = ids[max_idx]
        vds = _parse_eng_value(str(args.vds))
        r_equiv = (vds / ids_final) if ids_final > 0 else float("inf")

        return RcResult(tau=tau, ceff=ceff, ids_final=ids_final, r_equiv=r_equiv), run_dir

    if str(args.sweep_mode) == "none":
        res, run_dir = run_point(str(args.w), str(args.l))
        result = {
            "model_file": str(model_file),
            "device_name": args.device_name,
            "device_style": chosen.style,
            "w_param": w_param,
            "l_param": l_param,
            "bias": {"vds": str(args.vds), "vgs": str(args.vgs), "temp": str(args.temp)},
            "w": str(args.w),
            "l": str(args.l),
            "rdrive": str(args.rdrive),
            "tau": res.tau,
            "ceff": res.ceff,
            "ids_final": res.ids_final,
            "r_equiv": res.r_equiv,
            "paths": {"run_dir": str(run_dir)},
        }

        (output_dir / "rc_results.json").write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")

        report: List[str] = []
        report.append("# RC Extraction Prototype (MVP)")
        report.append("")
        report.append(f"Model file: `{model_file}`")
        report.append(f"Device: `{args.device_name}` (style: `{chosen.style}`)")
        report.append(f"Bias: VDS={args.vds}, VGS_step={args.vgs}, TEMP={args.temp}")
        report.append(f"W={args.w}, L={args.l}")
        report.append(f"Rdrive={args.rdrive}")
        report.append("")
        report.append("## Extracted")
        report.append(f"- tau (63.2% gate step): `{res.tau:.6g}` s")
        report.append(f"- Ceff = tau/Rdrive: `{res.ceff:.6g}` F")
        report.append(f"- Ids_final (at end of sim): `{res.ids_final:.6g}` A")
        report.append(f"- R_equiv ≈ VDS/Ids_final: `{res.r_equiv:.6g}` ohm")
        report.append("")
        report.append("## Artifacts")
        report.append(f"- `rc_results.json`")
        report.append(f"- Per-run netlists/logs under `{run_dir}`")

        (output_dir / "RC_REPORT.md").write_text("\n".join(report), encoding="utf-8")
        return 0

    sweep_points: List[RcSweepPoint] = []
    if str(args.sweep_mode) == "w":
        l_fixed = str(args.l_fixed) if args.l_fixed is not None else str(args.l)
        for w in args.w_sweep:
            res, _run = run_point(str(w), l_fixed)
            sweep_points.append(
                RcSweepPoint(w=str(w), l=l_fixed, tau=res.tau, ceff=res.ceff, ids_final=res.ids_final, r_equiv=res.r_equiv)
            )
        sweep_points = sorted(sweep_points, key=lambda p: _parse_eng_value(p.w))
    elif str(args.sweep_mode) == "l":
        w_fixed = str(args.w_fixed) if args.w_fixed is not None else str(args.w)
        for l in args.l_sweep:
            res, _run = run_point(w_fixed, str(l))
            sweep_points.append(
                RcSweepPoint(w=w_fixed, l=str(l), tau=res.tau, ceff=res.ceff, ids_final=res.ids_final, r_equiv=res.r_equiv)
            )
        sweep_points = sorted(sweep_points, key=lambda p: _parse_eng_value(p.l))
    else:
        raise SystemExit(f"Unknown sweep-mode: {args.sweep_mode}")

    sweep_result = {
        "model_file": str(model_file),
        "device_name": args.device_name,
        "device_style": chosen.style,
        "w_param": w_param,
        "l_param": l_param,
        "bias": {"vds": str(args.vds), "vgs": str(args.vgs), "temp": str(args.temp)},
        "rdrive": str(args.rdrive),
        "sweep_mode": str(args.sweep_mode),
        "points": [p.__dict__ for p in sweep_points],
        "paths": {"runs_dir": str(output_dir / "runs")},
    }
    (output_dir / "rc_sweep_results.json").write_text(
        json.dumps(sweep_result, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    report: List[str] = []
    report.append("# RC Extraction Sweep (MVP)")
    report.append("")
    report.append(f"Model file: `{model_file}`")
    report.append(f"Device: `{args.device_name}` (style: `{chosen.style}`)")
    report.append(f"Bias: VDS={args.vds}, VGS_step={args.vgs}, TEMP={args.temp}")
    report.append(f"Rdrive={args.rdrive}")
    report.append(f"Sweep mode: `{args.sweep_mode}`")
    report.append("")
    report.append("## Sweep points")
    report.append("| W | L | tau (s) | Ceff (F) | Ids_final (A) | R_equiv (ohm) |")
    report.append("|---|---|--------:|---------:|-------------:|--------------:|")
    for p in sweep_points:
        report.append(
            f"| {p.w} | {p.l} | {p.tau:.6g} | {p.ceff:.6g} | {p.ids_final:.6g} | {p.r_equiv:.6g} |"
        )
    report.append("")
    report.append("## Artifacts")
    report.append("- `rc_sweep_results.json`")
    report.append(f"- Per-run netlists/logs under `{output_dir / 'runs'}`")

    (output_dir / "RC_SWEEP_REPORT.md").write_text("\n".join(report), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
