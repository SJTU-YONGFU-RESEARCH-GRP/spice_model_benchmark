#!/usr/bin/env python3

import argparse
import json
import math
import re
import random
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


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
    if len(unit_l) == 1 and unit_l in _UNIT_MULTIPLIERS:
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


def _read_ids_from_output(path: Path) -> float:
    lines = [ln.strip() for ln in path.read_text(encoding="utf-8", errors="ignore").splitlines() if ln.strip()]
    if len(lines) < 2:
        raise RuntimeError(f"Unexpected geometry output format (need >=2 lines): {path}")
    parts = lines[-1].split()
    if len(parts) < 5:
        raise RuntimeError(f"Unexpected geometry output row: {lines[-1]!r}")
    return float(parts[-1])


@dataclass
class SweepPoint:
    w: str
    l: str
    ids: float


@dataclass
class SmallSignalPoint:
    w: str
    l: str
    gm: float
    gds: float


def _check_monotonic_increasing(xs: List[float], ys: List[float], rel_tol: float) -> bool:
    for i in range(1, len(xs)):
        if ys[i] + abs(ys[i]) * rel_tol < ys[i - 1]:
            return False
    return True


def _check_monotonic_decreasing(xs: List[float], ys: List[float], rel_tol: float) -> bool:
    for i in range(1, len(xs)):
        if ys[i] > ys[i - 1] + abs(ys[i - 1]) * rel_tol:
            return False
    return True


def _check_near_linear_through_origin(xs: List[float], ys: List[float], ratio_tol: float) -> Tuple[bool, float, float]:
    ratios = []
    for x, y in zip(xs, ys):
        if x == 0:
            continue
        ratios.append(y / x)
    if not ratios:
        return False, float("nan"), float("nan")
    rmin = min(ratios)
    rmax = max(ratios)
    if rmin == 0:
        return False, rmin, rmax
    return (rmax / rmin) <= ratio_tol, rmin, rmax


def _is_finite(x: float) -> bool:
    return x == x and x not in (float("inf"), float("-inf"))


def _extract_crossing_vgs(vgs: List[float], ids: List[float], target: float) -> float:
    if not vgs or len(vgs) != len(ids):
        return float("nan")
    for i in range(1, len(vgs)):
        lo_i = ids[i - 1]
        hi_i = ids[i]
        if (lo_i - target) * (hi_i - target) <= 0:
            v_lo = vgs[i - 1]
            v_hi = vgs[i]
            if v_hi == v_lo:
                return v_hi
            if lo_i > 0 and hi_i > 0 and target > 0 and lo_i != hi_i:
                x0 = math.log(lo_i)
                x1 = math.log(hi_i)
                xt = math.log(target)
                if x1 != x0:
                    frac = (xt - x0) / (x1 - x0)
                    return v_lo + frac * (v_hi - v_lo)
            if hi_i != lo_i:
                frac = (target - lo_i) / (hi_i - lo_i)
                return v_lo + frac * (v_hi - v_lo)
            return v_hi
    return float("nan")


def _extract_ss_mV_per_dec(vgs: List[float], ids: List[float], id_low: float, id_high: float) -> float:
    if not vgs or len(vgs) != len(ids):
        return float("nan")
    if id_low <= 0 or id_high <= 0 or id_high <= id_low:
        return float("nan")
    xs: List[float] = []
    ys: List[float] = []
    for vg, idv in zip(vgs, ids):
        if idv > 0 and id_low <= idv <= id_high:
            xs.append(math.log10(idv))
            ys.append(vg)
    if len(xs) < 2:
        return float("nan")
    x_mean = sum(xs) / len(xs)
    y_mean = sum(ys) / len(ys)
    sxx = sum((x - x_mean) ** 2 for x in xs)
    if sxx == 0:
        return float("nan")
    sxy = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys))
    slope = sxy / sxx
    return slope * 1e3


def _extract_ss_from_crossings_mV_per_dec(vgs: List[float], ids: List[float], id_low: float, id_high: float) -> float:
    if not vgs or len(vgs) != len(ids):
        return float("nan")
    if id_low <= 0 or id_high <= 0 or id_high <= id_low:
        return float("nan")
    vg_low = _extract_crossing_vgs(vgs, ids, id_low)
    vg_high = _extract_crossing_vgs(vgs, ids, id_high)
    if not _is_finite(vg_low) or not _is_finite(vg_high):
        return float("nan")
    decades = math.log10(id_high / id_low)
    if decades == 0:
        return float("nan")
    return (vg_high - vg_low) * 1e3 / decades


def _quantile(values: List[float], q: float) -> float:
    if not values:
        return float("nan")
    if q <= 0:
        return min(values)
    if q >= 1:
        return max(values)
    xs = sorted(values)
    pos = q * (len(xs) - 1)
    lo = int(pos)
    hi = min(lo + 1, len(xs) - 1)
    if hi == lo:
        return xs[lo]
    frac = pos - lo
    return xs[lo] * (1 - frac) + xs[hi] * frac


def _mean_std(values: List[float]) -> Tuple[float, float]:
    if not values:
        return float("nan"), float("nan")
    mu = sum(values) / len(values)
    if len(values) < 2:
        return mu, 0.0
    var = sum((x - mu) ** 2 for x in values) / (len(values) - 1)
    return mu, var ** 0.5


def _sample_positive_rel_gauss(nom: float, sigma_rel: float, rng: random.Random) -> float:
    if sigma_rel <= 0:
        return max(nom, 0.0)
    for _ in range(50):
        x = nom * (1.0 + rng.gauss(0.0, sigma_rel))
        if x > 0:
            return x
    return max(nom, 1e-30)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Minimal geometry scaling check (MVP)")
    parser.add_argument("--model-file", required=True)
    parser.add_argument("--device-name", required=True)
    parser.add_argument("--from-model-name", default="NMOS_VTG")
    parser.add_argument(
        "--template-netlist",
        default="netlists/geometry_op_circuit.cir",
    )
    parser.add_argument("--output-dir", default="geometry_check_results")

    parser.add_argument("--vds", default="0.6")
    parser.add_argument("--vgs", default="1.2")
    parser.add_argument("--temp", default="27")

    parser.add_argument(
        "--w-sweep",
        nargs="+",
        default=["0.5u", "1u", "2u", "5u"],
    )
    parser.add_argument("--l-fixed", default="0.15u")

    parser.add_argument(
        "--l-sweep",
        nargs="+",
        default=["0.15u", "0.3u", "0.5u", "1u"],
    )
    parser.add_argument("--w-fixed", default="1u")

    parser.add_argument("--w-param", default=None)
    parser.add_argument("--l-param", default=None)

    parser.add_argument("--monotonic-rel-tol", type=float, default=1e-3)
    parser.add_argument("--w-linearity-ratio-tol", type=float, default=1.5)

    parser.add_argument("--mc-samples", type=int, default=0)
    parser.add_argument("--mc-seed", type=int, default=1)
    parser.add_argument("--mc-w-sigma-rel", type=float, default=0.05)
    parser.add_argument("--mc-l-sigma-rel", type=float, default=0.05)
    parser.add_argument("--mc-keep-runs", action="store_true")
    parser.add_argument("--mc-min-success-rate", type=float, default=0.95)

    parser.add_argument("--enable-vth-dibl-ss", action="store_true")
    parser.add_argument("--enable-gm-gds", action="store_true")
    parser.add_argument("--extensions-strict", action="store_true")

    parser.add_argument(
        "--vgs-sweep",
        nargs="+",
        default=["0", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0", "1.1", "1.2"],
    )
    parser.add_argument("--dibl-vds-low", default="0.05")
    parser.add_argument("--dibl-vds-high", default=None)
    parser.add_argument("--vth-id-target", default="1e-7")
    parser.add_argument("--ss-id-low", default="1e-10")
    parser.add_argument("--ss-id-high", default="1e-7")

    parser.add_argument("--gm-dvgs", type=float, default=0.01)
    parser.add_argument("--gds-dvds", type=float, default=0.01)
    parser.add_argument("--gm-linearity-ratio-tol", type=float, default=1.5)

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
    runs_dir = output_dir / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)

    base_template = template_netlist.read_text(encoding="utf-8", errors="ignore")

    def run_point(
        w: str,
        l: str,
        tag: Optional[str] = None,
        run_base_dir: Optional[Path] = None,
        vds: Optional[str] = None,
        vgs: Optional[str] = None,
        temp: Optional[str] = None,
    ) -> SweepPoint:
        tag = _sanitize_tag(tag or f"W{w}_L{l}")
        base = run_base_dir or runs_dir
        run_dir = base / tag
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
            "__W__": w,
            "__L__": l,
            "__VDS__": str(args.vds) if vds is None else str(vds),
            "__VGS__": str(args.vgs) if vgs is None else str(vgs),
            "__TEMP__": str(args.temp) if temp is None else str(temp),
            "__TAG__": tag,
            "__WPARAM__": str(w_param),
            "__LPARAM__": str(l_param),
        }

        rendered = _render_tokens(adapted_path.read_text(encoding="utf-8", errors="ignore"), token_map)
        final_path = run_dir / f"geometry_{tag}.cir"
        final_path.write_text(rendered, encoding="utf-8")

        rc, stdout, stderr = _run_ngspice(final_path, cwd=run_dir)
        (run_dir / "ngspice_stdout.txt").write_text(stdout or "", encoding="utf-8")
        (run_dir / "ngspice_stderr.txt").write_text(stderr or "", encoding="utf-8")
        if rc != 0:
            raise RuntimeError(f"ngspice failed for {tag} (rc={rc}). See logs in {run_dir}")

        out_file = run_dir / f"geometry_op_{tag}.txt"
        if not out_file.exists():
            raise RuntimeError(f"Expected output file not found: {out_file}")

        ids = _read_ids_from_output(out_file)
        return SweepPoint(w=w, l=l, ids=ids)

    w_points: List[SweepPoint] = []
    for w in args.w_sweep:
        w_points.append(run_point(w=w, l=args.l_fixed))

    l_points: List[SweepPoint] = []
    for l in args.l_sweep:
        l_points.append(run_point(w=args.w_fixed, l=l))

    vth_dibl_ss: Optional[Dict[str, object]] = None
    if bool(args.enable_vth_dibl_ss):
        vgs_vals: List[float] = []
        for s in args.vgs_sweep:
            try:
                vgs_vals.append(_parse_eng_value(str(s)))
            except ValueError:
                pass
        vgs_vals = sorted(set(vgs_vals))

        vds_low = str(args.dibl_vds_low)
        vds_high = str(args.dibl_vds_high) if args.dibl_vds_high is not None else str(args.vds)

        idvg_dir = runs_dir / "idvg"
        idvg_dir.mkdir(parents=True, exist_ok=True)

        w_m = _parse_eng_value(args.w_fixed)
        vth_id_nom = _parse_eng_value(args.vth_id_target)
        ss_id_low_nom = _parse_eng_value(args.ss_id_low)
        ss_id_high_nom = _parse_eng_value(args.ss_id_high)

        per_l: List[Dict[str, object]] = []
        for l in sorted(args.l_sweep, key=lambda x: _parse_eng_value(x)):
            l_m = _parse_eng_value(l)
            wl_ratio = (w_m / l_m) if l_m > 0 else float("nan")
            vth_target = vth_id_nom * wl_ratio if _is_finite(wl_ratio) else float("nan")
            ss_id_low_req = ss_id_low_nom
            ss_id_high_req = ss_id_high_nom

            ids_low: List[float] = []
            ids_high: List[float] = []
            for vg in vgs_vals:
                pt_low = run_point(
                    w=str(args.w_fixed),
                    l=str(l),
                    vds=vds_low,
                    vgs=f"{vg:g}",
                    tag=f"idvg_L{l}_VDS{vds_low}_VGS{vg:g}",
                    run_base_dir=idvg_dir,
                )
                ids_low.append(pt_low.ids)
                pt_high = run_point(
                    w=str(args.w_fixed),
                    l=str(l),
                    vds=vds_high,
                    vgs=f"{vg:g}",
                    tag=f"idvg_L{l}_VDS{vds_high}_VGS{vg:g}",
                    run_base_dir=idvg_dir,
                )
                ids_high.append(pt_high.ids)

            vth_low = _extract_crossing_vgs(vgs_vals, ids_low, vth_target)
            vth_high = _extract_crossing_vgs(vgs_vals, ids_high, vth_target)
            dvds = _parse_eng_value(vds_high) - _parse_eng_value(vds_low)
            dibl = ((vth_low - vth_high) / dvds) if (dvds != 0 and _is_finite(vth_low) and _is_finite(vth_high)) else float("nan")

            ids_pos = [x for x in ids_low if x > 0]
            ss_id_low_used = float("nan")
            ss_id_high_used = float("nan")
            ss = float("nan")
            if len(ids_pos) >= 2:
                i_min = min(ids_pos)
                i_max = max(ids_pos)
                ss_id_low_used = max(ss_id_low_req, i_min)
                ss_id_high_used = min(ss_id_high_req, i_max)
                if not _is_finite(ss_id_low_used) or not _is_finite(ss_id_high_used) or ss_id_high_used <= ss_id_low_used:
                    ss_id_low_used = i_min
                    ss_id_high_used = min(i_max, i_min * 1e3)
                if ss_id_high_used > ss_id_low_used and (ss_id_high_used / ss_id_low_used) < 10:
                    ss_id_high_used = min(i_max, ss_id_low_used * 10)

                ss = _extract_ss_from_crossings_mV_per_dec(vgs_vals, ids_low, ss_id_low_used, ss_id_high_used)
                if not _is_finite(ss):
                    ss = _extract_ss_mV_per_dec(vgs_vals, ids_low, ss_id_low_used, ss_id_high_used)

            per_l.append(
                {
                    "w": str(args.w_fixed),
                    "l": str(l),
                    "vds_low": vds_low,
                    "vds_high": vds_high,
                    "vth_target_ids": vth_target,
                    "vth_low": vth_low,
                    "vth_high": vth_high,
                    "dibl": dibl,
                    "ss_mV_per_dec": ss,
                    "ss_id_low": ss_id_low_used,
                    "ss_id_high": ss_id_high_used,
                }
            )

        l_x = [_parse_eng_value(r["l"]) for r in per_l if isinstance(r.get("l"), str)]
        vth_low_y = [float(r["vth_low"]) for r in per_l]
        dibl_y = [float(r["dibl"]) for r in per_l]
        ss_y = [float(r["ss_mV_per_dec"]) for r in per_l]

        vth_lx: List[float] = []
        vth_ly: List[float] = []
        dibl_lx: List[float] = []
        dibl_ly: List[float] = []
        ss_lx: List[float] = []
        ss_ly: List[float] = []
        for lx, vy, dy, sy in zip(l_x, vth_low_y, dibl_y, ss_y):
            if _is_finite(vy):
                vth_lx.append(lx)
                vth_ly.append(vy)
            if _is_finite(dy):
                dibl_lx.append(lx)
                dibl_ly.append(dy)
            if _is_finite(sy):
                ss_lx.append(lx)
                ss_ly.append(sy)

        vth_monotonic_inc_with_l = _check_monotonic_increasing(vth_lx, vth_ly, rel_tol=float(args.monotonic_rel_tol)) if len(vth_lx) >= 2 else False
        dibl_monotonic_dec_with_l = _check_monotonic_decreasing(dibl_lx, dibl_ly, rel_tol=float(args.monotonic_rel_tol)) if len(dibl_lx) >= 2 else False
        ss_monotonic_dec_with_l = _check_monotonic_decreasing(ss_lx, ss_ly, rel_tol=float(args.monotonic_rel_tol)) if len(ss_lx) >= 2 else False
        dibl_non_negative = all((d >= -abs(d) * float(args.monotonic_rel_tol)) for d in dibl_ly) if dibl_ly else False

        vth_dibl_ss = {
            "per_l": per_l,
            "checks": {
                "vth_low_monotonic_increasing_with_l": vth_monotonic_inc_with_l,
                "dibl_monotonic_decreasing_with_l": dibl_monotonic_dec_with_l,
                "ss_monotonic_decreasing_with_l": ss_monotonic_dec_with_l,
                "dibl_non_negative": dibl_non_negative,
            },
        }

    small_signal: Optional[Dict[str, object]] = None
    if bool(args.enable_gm_gds):
        ss_dir = runs_dir / "small_signal"
        ss_dir.mkdir(parents=True, exist_ok=True)

        vgs0 = _parse_eng_value(str(args.vgs))
        vds0 = _parse_eng_value(str(args.vds))
        dvgs = float(args.gm_dvgs)
        dvds = float(args.gds_dvds)

        def calc_small_signal(w: str, l: str) -> SmallSignalPoint:
            if dvgs <= 0 or dvds <= 0:
                return SmallSignalPoint(w=w, l=l, gm=float("nan"), gds=float("nan"))

            if vgs0 - dvgs >= 0:
                ids_p = run_point(
                    w=w,
                    l=l,
                    vgs=f"{(vgs0 + dvgs):g}",
                    vds=f"{vds0:g}",
                    tag=f"gm_W{w}_L{l}_VDS{vds0:g}_VGS{(vgs0 + dvgs):g}",
                    run_base_dir=ss_dir,
                ).ids
                ids_m = run_point(
                    w=w,
                    l=l,
                    vgs=f"{(vgs0 - dvgs):g}",
                    vds=f"{vds0:g}",
                    tag=f"gm_W{w}_L{l}_VDS{vds0:g}_VGS{(vgs0 - dvgs):g}",
                    run_base_dir=ss_dir,
                ).ids
                gm = (ids_p - ids_m) / (2.0 * dvgs)
            else:
                ids_0 = run_point(
                    w=w,
                    l=l,
                    vgs=f"{vgs0:g}",
                    vds=f"{vds0:g}",
                    tag=f"gm_W{w}_L{l}_VDS{vds0:g}_VGS{vgs0:g}",
                    run_base_dir=ss_dir,
                ).ids
                ids_p = run_point(
                    w=w,
                    l=l,
                    vgs=f"{(vgs0 + dvgs):g}",
                    vds=f"{vds0:g}",
                    tag=f"gm_W{w}_L{l}_VDS{vds0:g}_VGS{(vgs0 + dvgs):g}",
                    run_base_dir=ss_dir,
                ).ids
                gm = (ids_p - ids_0) / dvgs

            if vds0 - dvds >= 0:
                ids_p = run_point(
                    w=w,
                    l=l,
                    vgs=f"{vgs0:g}",
                    vds=f"{(vds0 + dvds):g}",
                    tag=f"gds_W{w}_L{l}_VDS{(vds0 + dvds):g}_VGS{vgs0:g}",
                    run_base_dir=ss_dir,
                ).ids
                ids_m = run_point(
                    w=w,
                    l=l,
                    vgs=f"{vgs0:g}",
                    vds=f"{(vds0 - dvds):g}",
                    tag=f"gds_W{w}_L{l}_VDS{(vds0 - dvds):g}_VGS{vgs0:g}",
                    run_base_dir=ss_dir,
                ).ids
                gds = (ids_p - ids_m) / (2.0 * dvds)
            else:
                ids_0 = run_point(
                    w=w,
                    l=l,
                    vgs=f"{vgs0:g}",
                    vds=f"{vds0:g}",
                    tag=f"gds_W{w}_L{l}_VDS{vds0:g}_VGS{vgs0:g}",
                    run_base_dir=ss_dir,
                ).ids
                ids_p = run_point(
                    w=w,
                    l=l,
                    vgs=f"{vgs0:g}",
                    vds=f"{(vds0 + dvds):g}",
                    tag=f"gds_W{w}_L{l}_VDS{(vds0 + dvds):g}_VGS{vgs0:g}",
                    run_base_dir=ss_dir,
                ).ids
                gds = (ids_p - ids_0) / dvds

            return SmallSignalPoint(w=w, l=l, gm=gm, gds=gds)

        ss_w_points: List[SmallSignalPoint] = []
        for w in args.w_sweep:
            ss_w_points.append(calc_small_signal(w=w, l=str(args.l_fixed)))

        ss_l_points: List[SmallSignalPoint] = []
        for l in args.l_sweep:
            ss_l_points.append(calc_small_signal(w=str(args.w_fixed), l=l))

        ss_w_sorted = sorted(ss_w_points, key=lambda p: _parse_eng_value(p.w))
        ss_l_sorted = sorted(ss_l_points, key=lambda p: _parse_eng_value(p.l))

        w_x_ss = [_parse_eng_value(p.w) for p in ss_w_sorted]
        gm_w = [p.gm for p in ss_w_sorted]
        gds_w = [p.gds for p in ss_w_sorted]
        l_x_ss = [_parse_eng_value(p.l) for p in ss_l_sorted]
        gm_l = [p.gm for p in ss_l_sorted]

        gm_positive = all((_is_finite(gm) and gm >= -abs(gm) * float(args.monotonic_rel_tol)) for gm in gm_w + gm_l)
        gds_non_negative = all((_is_finite(gds) and gds >= -abs(gds) * float(args.monotonic_rel_tol)) for gds in gds_w)

        gm_linear, gm_ratio_min, gm_ratio_max = _check_near_linear_through_origin(
            w_x_ss, gm_w, ratio_tol=float(args.gm_linearity_ratio_tol)
        )

        small_signal = {
            "w_sweep": [p.__dict__ for p in ss_w_sorted],
            "l_sweep": [p.__dict__ for p in ss_l_sorted],
            "checks": {
                "gm_positive": gm_positive,
                "gds_non_negative": gds_non_negative,
                "gm_near_linear_with_w": gm_linear,
                "gm_over_w_ratio_min": gm_ratio_min,
                "gm_over_w_ratio_max": gm_ratio_max,
                "gm_dvgs": float(args.gm_dvgs),
                "gds_dvds": float(args.gds_dvds),
                "gm_linearity_ratio_tol": float(args.gm_linearity_ratio_tol),
            },
        }

    mc_result: Optional[Dict[str, object]] = None
    if int(args.mc_samples) > 0:
        rng = random.Random(int(args.mc_seed))
        w_nom = _parse_eng_value(args.w_fixed)
        l_nom = _parse_eng_value(args.l_fixed)
        ids_samples: List[float] = []
        w_samples: List[float] = []
        l_samples: List[float] = []
        failures: List[Dict[str, object]] = []

        mc_dir = runs_dir / "mc"
        mc_dir.mkdir(parents=True, exist_ok=True)

        for i in range(int(args.mc_samples)):
            w_s = _sample_positive_rel_gauss(w_nom, float(args.mc_w_sigma_rel), rng)
            l_s = _sample_positive_rel_gauss(l_nom, float(args.mc_l_sigma_rel), rng)
            tag = f"mc_{i:05d}"
            run_subdir = mc_dir / tag
            try:
                pt = run_point(
                    w=f"{w_s:.6g}",
                    l=f"{l_s:.6g}",
                    tag=tag,
                    run_base_dir=mc_dir,
                )
                ids_samples.append(pt.ids)
                w_samples.append(w_s)
                l_samples.append(l_s)
                if not args.mc_keep_runs:
                    for child in list(run_subdir.iterdir()):
                        if child.is_file():
                            child.unlink(missing_ok=True)
                    # Remove directory if empty
                    try:
                        run_subdir.rmdir()
                    except OSError:
                        pass
            except Exception as e:
                failures.append({"index": i, "w": w_s, "l": l_s, "error": str(e)})
                if not args.mc_keep_runs:
                    # keep failed runs for debugging
                    pass

        success_count = len(ids_samples)
        total = int(args.mc_samples)
        success_rate = (success_count / total) if total > 0 else 0.0

        ids_mean, ids_std = _mean_std(ids_samples)
        mc_result = {
            "samples": total,
            "success": success_count,
            "success_rate": success_rate,
            "w_nom": w_nom,
            "l_nom": l_nom,
            "w_sigma_rel": float(args.mc_w_sigma_rel),
            "l_sigma_rel": float(args.mc_l_sigma_rel),
            "ids_mean": ids_mean,
            "ids_std": ids_std,
            "ids_p05": _quantile(ids_samples, 0.05),
            "ids_p50": _quantile(ids_samples, 0.50),
            "ids_p95": _quantile(ids_samples, 0.95),
            "failures": failures,
            "min_success_rate": float(args.mc_min_success_rate),
            "passed": success_rate >= float(args.mc_min_success_rate),
        }

    w_sorted = sorted(w_points, key=lambda p: _parse_eng_value(p.w))
    l_sorted = sorted(l_points, key=lambda p: _parse_eng_value(p.l))

    w_x = [_parse_eng_value(p.w) for p in w_sorted]
    w_y = [p.ids for p in w_sorted]
    l_x = [_parse_eng_value(p.l) for p in l_sorted]
    l_y = [p.ids for p in l_sorted]

    w_monotonic = _check_monotonic_increasing(w_x, w_y, rel_tol=float(args.monotonic_rel_tol))
    l_monotonic = _check_monotonic_decreasing(l_x, l_y, rel_tol=float(args.monotonic_rel_tol))
    w_linear, w_ratio_min, w_ratio_max = _check_near_linear_through_origin(
        w_x, w_y, ratio_tol=float(args.w_linearity_ratio_tol)
    )

    result = {
        "model_file": str(model_file),
        "device_name": args.device_name,
        "device_style": chosen.style,
        "w_param": w_param,
        "l_param": l_param,
        "bias": {"vds": str(args.vds), "vgs": str(args.vgs), "temp": str(args.temp)},
        "w_sweep": [p.__dict__ for p in w_sorted],
        "l_sweep": [p.__dict__ for p in l_sorted],
        "monte_carlo": mc_result,
        "vth_dibl_ss": vth_dibl_ss,
        "small_signal": small_signal,
        "checks": {
            "ids_monotonic_increasing_with_w": w_monotonic,
            "ids_monotonic_decreasing_with_l": l_monotonic,
            "ids_near_linear_with_w": w_linear,
            "ids_over_w_ratio_min": w_ratio_min,
            "ids_over_w_ratio_max": w_ratio_max,
            "monotonic_rel_tol": float(args.monotonic_rel_tol),
            "w_linearity_ratio_tol": float(args.w_linearity_ratio_tol),
        },
        "paths": {"runs_dir": str(runs_dir)},
    }

    (output_dir / "geometry_results.json").write_text(
        json.dumps(result, indent=2, sort_keys=True),
        encoding="utf-8",
    )

    report_lines: List[str] = []
    report_lines.append("# Geometry Scaling Check (MVP)")
    report_lines.append("")
    report_lines.append(f"Model file: `{model_file}`")
    report_lines.append(f"Device: `{args.device_name}` (style: `{chosen.style}`)")
    report_lines.append(f"Bias: VDS={args.vds}, VGS={args.vgs}, TEMP={args.temp}")
    report_lines.append("")

    report_lines.append("## Checks")
    report_lines.append(f"- Ids monotonic increasing with W: `{w_monotonic}`")
    report_lines.append(f"- Ids monotonic decreasing with L: `{l_monotonic}`")
    report_lines.append(
        f"- Ids near-linear with W (max/min(Id/W) <= {float(args.w_linearity_ratio_tol):g}): `{w_linear}`"
    )
    report_lines.append(f"  - min(Id/W)={w_ratio_min:.6g}, max(Id/W)={w_ratio_max:.6g}")
    report_lines.append("")

    report_lines.append("## W sweep (fixed L)")
    report_lines.append("| W | L | Ids (A) |")
    report_lines.append("|---|---|---------|")
    for p in w_sorted:
        report_lines.append(f"| {p.w} | {p.l} | {p.ids:.6g} |")
    report_lines.append("")

    report_lines.append("## L sweep (fixed W)")
    report_lines.append("| W | L | Ids (A) |")
    report_lines.append("|---|---|---------|")
    for p in l_sorted:
        report_lines.append(f"| {p.w} | {p.l} | {p.ids:.6g} |")
    report_lines.append("")

    report_lines.append("## Artifacts")
    report_lines.append(f"- `geometry_results.json`")
    report_lines.append(f"- Per-run netlists/logs under `{runs_dir}`")

    if vth_dibl_ss is not None:
        report_lines.append("")
        report_lines.append("## Vth/DIBL/SS vs L (MVP)")
        checks = vth_dibl_ss.get("checks", {}) if isinstance(vth_dibl_ss, dict) else {}
        report_lines.append(f"- Vth_low monotonic increasing with L: `{checks.get('vth_low_monotonic_increasing_with_l')}`")
        report_lines.append(f"- DIBL monotonic decreasing with L: `{checks.get('dibl_monotonic_decreasing_with_l')}`")
        report_lines.append(f"- SS monotonic decreasing with L: `{checks.get('ss_monotonic_decreasing_with_l')}`")
        report_lines.append(f"- DIBL non-negative: `{checks.get('dibl_non_negative')}`")
        report_lines.append("")
        report_lines.append("| W | L | VDS_low | VDS_high | Vth_low (V) | Vth_high (V) | DIBL (V/V) | SS (mV/dec) |")
        report_lines.append("|---|---|---------|----------|------------:|-------------:|-----------:|------------:|")
        per_l = vth_dibl_ss.get("per_l", []) if isinstance(vth_dibl_ss, dict) else []
        for r in per_l if isinstance(per_l, list) else []:
            try:
                report_lines.append(
                    "| {w} | {l} | {vds_low} | {vds_high} | {vth_low:.6g} | {vth_high:.6g} | {dibl:.6g} | {ss:.6g} |".format(
                        w=r.get("w"),
                        l=r.get("l"),
                        vds_low=r.get("vds_low"),
                        vds_high=r.get("vds_high"),
                        vth_low=float(r.get("vth_low")),
                        vth_high=float(r.get("vth_high")),
                        dibl=float(r.get("dibl")),
                        ss=float(r.get("ss_mV_per_dec")),
                    )
                )
            except Exception:
                continue

    if small_signal is not None:
        report_lines.append("")
        report_lines.append("## gm/gds vs W/L (MVP)")
        checks = small_signal.get("checks", {}) if isinstance(small_signal, dict) else {}
        report_lines.append(f"- gm positive: `{checks.get('gm_positive')}`")
        report_lines.append(f"- gds non-negative: `{checks.get('gds_non_negative')}`")
        report_lines.append(f"- gm near-linear with W: `{checks.get('gm_near_linear_with_w')}`")
        report_lines.append(f"  - min(gm/W)={checks.get('gm_over_w_ratio_min')}, max(gm/W)={checks.get('gm_over_w_ratio_max')}")
        report_lines.append("")
        report_lines.append("### W sweep (fixed L)")
        report_lines.append("| W | L | gm (S) | gds (S) |")
        report_lines.append("|---|---|--------:|---------:|")
        for p in small_signal.get("w_sweep", []) if isinstance(small_signal, dict) else []:
            try:
                report_lines.append(
                    f"| {p.get('w')} | {p.get('l')} | {float(p.get('gm')):.6g} | {float(p.get('gds')):.6g} |"
                )
            except Exception:
                continue
        report_lines.append("")
        report_lines.append("### L sweep (fixed W)")
        report_lines.append("| W | L | gm (S) | gds (S) |")
        report_lines.append("|---|---|--------:|---------:|")
        for p in small_signal.get("l_sweep", []) if isinstance(small_signal, dict) else []:
            try:
                report_lines.append(
                    f"| {p.get('w')} | {p.get('l')} | {float(p.get('gm')):.6g} | {float(p.get('gds')):.6g} |"
                )
            except Exception:
                continue

    if mc_result is not None:
        report_lines.append("")
        report_lines.append("## Geometry Monte Carlo")
        report_lines.append(f"- Samples: `{mc_result['samples']}`")
        report_lines.append(f"- Success rate: `{mc_result['success_rate']:.3f}`")
        report_lines.append(f"- Passed (success_rate >= {mc_result['min_success_rate']:.3f}): `{mc_result['passed']}`")
        report_lines.append(f"- Ids mean: `{mc_result['ids_mean']:.6g}` A")
        report_lines.append(f"- Ids std: `{mc_result['ids_std']:.6g}` A")
        report_lines.append(f"- Ids p05/p50/p95: `{mc_result['ids_p05']:.6g}` / `{mc_result['ids_p50']:.6g}` / `{mc_result['ids_p95']:.6g}` A")
        report_lines.append(f"- W sigma_rel: `{mc_result['w_sigma_rel']}`; L sigma_rel: `{mc_result['l_sigma_rel']}`")

    (output_dir / "GEOMETRY_REPORT.md").write_text("\n".join(report_lines), encoding="utf-8")

    mc_ok = True
    if mc_result is not None:
        mc_ok = bool(mc_result.get("passed", False))

    ext_ok = True
    if bool(args.extensions_strict):
        if vth_dibl_ss is not None:
            c = vth_dibl_ss.get("checks", {}) if isinstance(vth_dibl_ss, dict) else {}
            ext_ok = ext_ok and bool(c.get("vth_low_monotonic_increasing_with_l", False))
            ext_ok = ext_ok and bool(c.get("dibl_non_negative", False))
        if small_signal is not None:
            c = small_signal.get("checks", {}) if isinstance(small_signal, dict) else {}
            ext_ok = ext_ok and bool(c.get("gm_positive", False))
            ext_ok = ext_ok and bool(c.get("gds_non_negative", False))
            ext_ok = ext_ok and bool(c.get("gm_near_linear_with_w", False))

    ok = bool(w_monotonic and l_monotonic and w_linear and mc_ok and ext_ok)
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
