#!/usr/bin/env python3
r"""Verify large-signal capacitances from TRAN vs integral of small-signal C(V) from AC.

Goal
- Extract *large-signal* effective capacitances from TRAN by integrating terminal currents
    during a voltage step.
- Extract *small-signal* C(V) from AC as a function of the stepped voltage and compare via
    voltage integration:
        Q_pred = \int C(V) dV,   C_pred = Q_pred/\Delta V

Naming convention (matches this repo's AC CV outputs)
- In netlists/ac_circuit.cir, when the gate is excited (VG AC=1), the script reports:
        Cgs = -Im(i(VS))/ω   (row s, col g)
        Cgd = -Im(i(VD))/ω   (row d, col g)
        Cgb = -Im(i(VB))/ω   (row b, col g)
    So here we verify these three using a *gate step* in TRAN.

- For bulk excitation (VB AC=1), we verify:
        Csb = -Im(i(VS))/ω   (row s, col b)
        Cdb = -Im(i(VD))/ω   (row d, col b)
    using a *bulk step* in TRAN.

Defaults are chosen to avoid forward-biasing body diodes:
- Vb sweep/step is 0 -> -VSTEP (reverse bias for NMOS with body at 0 initially).

Example
  python test_cap_param/verify_ls_caps_vs_ac_integral.py \
      --pdk FreePDK45 --model NMOS_VTG --L 0.045u --W 10u \
      --vg 0.0 --vstep 0.8

Outputs
- Writes intermediate ngspice outputs under:
    test_cap_param/results/ls_caps_vs_ac/
  and prints a comparison table.
"""

from __future__ import annotations

import argparse
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class DeviceSpec:
    pdk: str
    include_path: str
    model: str
    l_str: str
    w_str: str


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _run_ngspice(netlist_rel_to_netlists: Path, *, netlists_dir: Path) -> str:
    cmd = ["ngspice", "-b", str(netlist_rel_to_netlists)]
    result = subprocess.run(
        cmd,
        cwd=str(netlists_dir),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"ngspice failed: {netlist_rel_to_netlists} (code {result.returncode})\n"
            f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    # ngspice sometimes prints useful info to stderr even on success; keep both
    return (result.stdout or "") + ("\n" + result.stderr if result.stderr else "")


_MEAS_RE = re.compile(r"\b(?P<name>[A-Za-z0-9_]+)\s*=\s*(?P<val>[-+0-9.eE]+)")


def _parse_meas(stdout: str, name: str) -> float:
    for m in _MEAS_RE.finditer(stdout):
        if m.group("name").lower() == name.lower():
            return float(m.group("val"))
    raise RuntimeError(f"Measurement '{name}' not found in ngspice output")


def _trapz_integral(x: np.ndarray, y: np.ndarray) -> float:
    order = np.argsort(x)
    # numpy.trapz is deprecated in newer numpy; trapezoid is the direct replacement.
    return float(np.trapezoid(y[order], x[order]))


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _gen_ac_sweep_netlist(
    *,
    dev: DeviceSpec,
    sweep_name: str,
    sweep_source: str,
    v_start: float,
    v_stop: float,
    v_step: float,
    vg: float,
    vd: float,
    vs: float,
    vb: float,
    out_file: str,
    ac_freq_hz: float,
) -> str:
    sweep_source_u = sweep_source.strip().upper()
    if sweep_source_u not in {"VG", "VB"}:
        raise ValueError(f"Unsupported sweep_source={sweep_source!r}; expected 'VG' or 'VB'.")

    if sweep_source_u == "VG":
        header = f'echo "Vg Cgs Cgd Cgb Cgg" > {out_file}'
        body = f"""
  alter VG = vx
  alter @VG[acmag] = 1
  alter @VB[acmag] = 0
  alter @VD[acmag] = 0
  alter @VS[acmag] = 0

  ac lin 1 {ac_freq_hz} {ac_freq_hz}
  let cgs_m = -imag(i(VS))/w
  let cgd_m = -imag(i(VD))/w
  let cgb_m = -imag(i(VB))/w
    let cgg_m = -imag(i(VG))/w
  set cgs_s = $&cgs_m
  set cgd_s = $&cgd_m
  set cgb_s = $&cgb_m
    set cgg_s = $&cgg_m
    echo "$&vx $cgs_s $cgd_s $cgb_s $cgg_s" >> {out_file}
"""
    else:
        header = f'echo "Vb Csb Cdb" > {out_file}'
        body = f"""
  alter VB = vx
  alter @VG[acmag] = 0
  alter @VB[acmag] = 1
  alter @VD[acmag] = 0
  alter @VS[acmag] = 0

  ac lin 1 {ac_freq_hz} {ac_freq_hz}
  let csb_m = -imag(i(VS))/w
  let cdb_m = -imag(i(VD))/w
  set csb_s = $&csb_m
  set cdb_s = $&cdb_m
  echo "$&vx $csb_s $cdb_s" >> {out_file}
"""

    return f"""* AC sweep for LS-vs-AC-integral verification ({sweep_name})
.option temp=27 tnom=27
.option gmin=1e-15 reltol=1e-8 abstol=1e-12 chgtol=1e-15 method=gear

.inc {dev.include_path}

* DUT
M1 d g s b {dev.model} L={dev.l_str} W={dev.w_str}

* Bias sources (DC). We will excite either VG or VB depending on sweep_source.
VG g 0 DC {vg} AC 0
VD d 0 DC {vd} AC 0
VS s 0 DC {vs} AC 0
VB b 0 DC {vb} AC 0

.control
set filetype=ascii
set wr_vecnames=no
set wr_singlescale=yes
set numdgt=10

let w = 2*3.141592653589793*{ac_freq_hz}

{header}

let vx_start = {v_start}
let vx_stop  = {v_stop}
let vx_step  = {v_step}
let npts = floor((vx_stop - vx_start)/vx_step) + 1
let idx = 0

while idx < npts
  let vx = vx_start + idx*vx_step

{body}

  let idx = idx + 1
end

quit
.endc
.end
"""


def _gen_tran_step_netlist(
    *,
    dev: DeviceSpec,
    step_name: str,
    step_source: str,
    v1: float,
    v2: float,
    vg: float,
    vd: float,
    vs: float,
    vb: float,
    tstop: float,
    tstep: float,
    tr: float,
    td: float,
) -> str:
    """Generate TRAN step netlist that measures integrated charges on sources."""

    pulse = f"PULSE({v1} {v2} {td} {tr} {tr} {tstop} {tstop*2})"

    # By default all sources are DC; replace exactly one with the pulse.
    src_vg = f"DC {vg}"
    src_vd = f"DC {vd}"
    src_vs = f"DC {vs}"
    src_vb = f"DC {vb}"
    if step_source == "VG":
        src_vg = pulse
    elif step_source == "VB":
        src_vb = pulse
    else:
        raise ValueError(f"unknown step_source: {step_source} (expected 'VG' or 'VB')")

    return f"""* TRAN step for LS-vs-AC-integral verification ({step_name})
.option temp=27 tnom=27
.option gmin=1e-15 reltol=1e-8 abstol=1e-12 chgtol=1e-15 method=gear

.inc {dev.include_path}

M1 d g s b {dev.model} L={dev.l_str} W={dev.w_str}

VG g 0 {src_vg}
VD d 0 {src_vd}
VS s 0 {src_vs}
VB b 0 {src_vb}

.control
tran {tstep} {tstop}

* Integrated charges (Coulombs)
meas tran qg INTEG i(VG) from=0 to={tstop}
meas tran qd INTEG i(VD) from=0 to={tstop}
meas tran qs INTEG i(VS) from=0 to={tstop}
meas tran qb INTEG i(VB) from=0 to={tstop}

print qg
print qd
print qs
print qb

quit
.endc
.end
"""


def _load_ac_table(path: Path) -> dict[str, np.ndarray]:
    with path.open("r", encoding="utf-8") as f:
        header = f.readline().strip().split()
    raw = np.genfromtxt(path, skip_header=1)
    if raw.ndim == 1:
        raw = raw[None, :]
    cols = {h: i for i, h in enumerate(header)}
    out: dict[str, np.ndarray] = {}
    for h in header:
        out[h] = raw[:, cols[h]]
    return out


def _print_table(rows: list[tuple[str, float, float]]) -> None:
    # rows: (name, tran, ac_pred)
    print("\nCapacitance verification (TRAN vs AC integral)")
    print("  Units: fF")
    print("  Note: sign should match if conventions are consistent")
    print("\n  {:<5s} {:>14s} {:>14s} {:>14s}".format("cap", "tran", "ac_int", "rel_err"))
    for name, tran_ff, ac_ff in rows:
        denom = abs(ac_ff) if abs(ac_ff) > 0 else 1.0
        rel = (tran_ff - ac_ff) / denom
        print("  {:<5s} {:>14.6f} {:>14.6f} {:>+14.3e}".format(name, tran_ff, ac_ff, rel))


def parse_args() -> argparse.Namespace:
    repo_root = _repo_root()
    default_out = repo_root / "test_cap_param" / "results" / "ls_caps_vs_ac"

    p = argparse.ArgumentParser(
        description="Extract LS caps from TRAN and compare to integral of SS caps from AC sweep."
    )
    p.add_argument("--pdk", default="FreePDK45", help="PDK name (default: FreePDK45)")
    p.add_argument(
        "--include",
        default="../models/FreePDK45/nom.inc",
        help="Model include path as seen from netlists/ working directory (default: ../models/FreePDK45/nom.inc)",
    )
    p.add_argument("--model", default="NMOS_VTG", help="SPICE model name (default: NMOS_VTG)")
    p.add_argument("--L", dest="l_str", default="0.045u", help="Device L string (default: 0.045u)")
    p.add_argument("--W", dest="w_str", default="10u", help="Device W string (default: 10u)")

    p.add_argument("--vg", type=float, default=0.0, help="Gate DC bias (V)")
    p.add_argument("--vd", type=float, default=0.0, help="Drain DC bias baseline (V)")
    p.add_argument("--vs", type=float, default=0.0, help="Source DC bias baseline (V)")
    p.add_argument("--vb", type=float, default=0.0, help="Bulk DC bias baseline (V)")

    p.add_argument(
        "--vstep",
        type=float,
        default=0.8,
        help="Step magnitude (V). VG steps to +vstep, VB steps to -vstep by default.",
    )
    p.add_argument("--vb-stop", type=float, default=None, help="Bulk stop voltage for sweep/step (default: -vstep)")
    p.add_argument("--ac-step", type=float, default=0.05, help="AC sweep step (V) (default: 0.05)")
    p.add_argument(
        "--ac-freq",
        type=float,
        default=1e6,
        help="AC extraction frequency in Hz (default: 1e6).",
    )

    p.add_argument("--out-dir", default=str(default_out), help=f"Output directory (default: {default_out})")

    return p.parse_args()


def main() -> int:
    args = parse_args()

    repo_root = _repo_root()
    netlists_dir = repo_root / "netlists"
    work_dir = netlists_dir / "temp_ls_caps_vs_ac"
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    vb_stop = args.vb_stop if args.vb_stop is not None else -float(args.vstep)

    dev = DeviceSpec(
        pdk=args.pdk,
        include_path=args.include,
        model=args.model,
        l_str=args.l_str,
        w_str=args.w_str,
    )

    # -----------------
    # 1) AC sweeps
    # -----------------
    ac_vg_name = "ac_sweep_vg.cir"
    ac_vb_name = "ac_sweep_vb.cir"

    ac_vg_out = "ac_sweep_vg.txt"  # columns: Vg Cgs Cgd Cgb Cgg
    ac_vb_out = "ac_sweep_vb.txt"  # columns: Vb Csb Cdb

    # Sweep ranges are anchored at the specified baselines.
    vg_start = float(args.vg)
    vg_stop = vg_start + float(args.vstep)
    vb_start = float(args.vb)
    vb_stop = float(vb_stop)

    ac_vg = _gen_ac_sweep_netlist(
        dev=dev,
        sweep_name="sweep_VG",
        sweep_source="VG",
        v_start=vg_start,
        v_stop=vg_stop,
        v_step=float(args.ac_step),
        vg=float(args.vg),
        vd=float(args.vd),
        vs=float(args.vs),
        vb=float(args.vb),
        out_file=ac_vg_out,
        ac_freq_hz=float(args.ac_freq),
    )

    ac_vb = _gen_ac_sweep_netlist(
        dev=dev,
        sweep_name="sweep_VB",
        sweep_source="VB",
        v_start=vb_start,
        v_stop=vb_stop,
        v_step=float(args.ac_step) if vb_stop >= vb_start else -float(args.ac_step),
        vg=float(args.vg),
        vd=float(args.vd),
        vs=float(args.vs),
        vb=float(args.vb),
        out_file=ac_vb_out,
        ac_freq_hz=float(args.ac_freq),
    )

    _write(work_dir / ac_vg_name, ac_vg)
    _write(work_dir / ac_vb_name, ac_vb)

    # Run AC sweeps
    for cir_name in [ac_vg_name, ac_vb_name]:
        rel = Path("temp_ls_caps_vs_ac") / cir_name
        stdout = _run_ngspice(rel, netlists_dir=netlists_dir)
        _write(out_dir / f"{cir_name}.log.txt", stdout)

    # Copy data files from netlists/ to out_dir for traceability
    for txt in [ac_vg_out, ac_vb_out]:
        src = netlists_dir / txt
        if src.exists():
            (out_dir / txt).write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    tab_vg = _load_ac_table(out_dir / ac_vg_out)
    tab_vb = _load_ac_table(out_dir / ac_vb_out)

    # Compute AC-integral predicted LS caps along the same paths.
    dv_g = vg_stop - vg_start
    dv_b = vb_stop - vb_start

    cgs_pred = _trapz_integral(tab_vg["Vg"], tab_vg["Cgs"]) / dv_g
    cgd_pred = _trapz_integral(tab_vg["Vg"], tab_vg["Cgd"]) / dv_g
    cgb_pred = _trapz_integral(tab_vg["Vg"], tab_vg["Cgb"]) / dv_g
    cgg_pred = _trapz_integral(tab_vg["Vg"], tab_vg["Cgg"]) / dv_g
    csb_pred = _trapz_integral(tab_vb["Vb"], tab_vb["Csb"]) / dv_b
    cdb_pred = _trapz_integral(tab_vb["Vb"], tab_vb["Cdb"]) / dv_b

    # -----------------
    # 2) TRAN steps
    # -----------------
    tran_vg_name = "tran_step_vg.cir"
    tran_vb_name = "tran_step_vb.cir"

    # Time settings: keep rise time comfortably above timestep to avoid undersampling
    # (undersampling the displacement-current spike will underestimate integrated charge).
    tr = 1e-10     # 100 ps
    tstop = 2e-10  # 200 ps (covers the full rise + short settle)
    tstep = 1e-12  # 1 ps
    td = 0.0

    tran_vg = _gen_tran_step_netlist(
        dev=dev,
        step_name="step_VG",
        step_source="VG",
        v1=vg_start,
        v2=vg_stop,
        vg=float(args.vg),
        vd=float(args.vd),
        vs=float(args.vs),
        vb=float(args.vb),
        tstop=tstop,
        tstep=tstep,
        tr=tr,
        td=td,
    )

    tran_vb = _gen_tran_step_netlist(
        dev=dev,
        step_name="step_VB",
        step_source="VB",
        v1=vb_start,
        v2=vb_stop,
        vg=float(args.vg),
        vd=float(args.vd),
        vs=float(args.vs),
        vb=float(args.vb),
        tstop=tstop,
        tstep=tstep,
        tr=tr,
        td=td,
    )

    _write(work_dir / tran_vg_name, tran_vg)
    _write(work_dir / tran_vb_name, tran_vb)

    tran_meas: dict[str, dict[str, float]] = {}
    for cir_name in [tran_vg_name, tran_vb_name]:
        rel = Path("temp_ls_caps_vs_ac") / cir_name
        stdout = _run_ngspice(rel, netlists_dir=netlists_dir)
        _write(out_dir / f"{cir_name}.log.txt", stdout)
        tran_meas[cir_name] = {
            "qg": _parse_meas(stdout, "qg"),
            "qd": _parse_meas(stdout, "qd"),
            "qs": _parse_meas(stdout, "qs"),
            "qb": _parse_meas(stdout, "qb"),
        }

    # TRAN-based LS caps (repo convention)
    qd_vg = tran_meas[tran_vg_name]["qd"]
    qs_vg = tran_meas[tran_vg_name]["qs"]
    qb_vg = tran_meas[tran_vg_name]["qb"]
    qg_vg = tran_meas[tran_vg_name]["qg"]

    qd_vb = tran_meas[tran_vb_name]["qd"]
    qs_vb = tran_meas[tran_vb_name]["qs"]

    # Sign convention: ngspice defines i(Vx) as current through the voltage source
    # from its positive node to its negative node. Our AC extraction uses
    # C = -Im(i(Vx))/w under the corresponding excitation. For VG-step LS caps,
    # the consistent time-domain equivalent is C = - (∫ i(Vx) dt) / ΔV.
    cgd_tran = -qd_vg / dv_g
    cgs_tran = -qs_vg / dv_g
    cgb_tran = -qb_vg / dv_g
    cgg_tran = -qg_vg / dv_g
    csb_tran = qs_vb / dv_b
    cdb_tran = qd_vb / dv_b

    # Print summary
    rows = [
        ("cgg", cgg_tran * 1e15, cgg_pred * 1e15),
        ("cgs", cgs_tran * 1e15, cgs_pred * 1e15),
        ("cgd", cgd_tran * 1e15, cgd_pred * 1e15),
        ("cgb", cgb_tran * 1e15, cgb_pred * 1e15),
        ("csb", csb_tran * 1e15, csb_pred * 1e15),
        ("cdb", cdb_tran * 1e15, cdb_pred * 1e15),
    ]

    print("Biases:")
    print(f"  Vg={args.vg} V, Vd={args.vd} V, Vs={args.vs} V, Vb={args.vb} V")
    print("Steps:")
    print(f"  VG: {vg_start} -> {vg_stop} V")
    print(f"  VB: {vb_start} -> {vb_stop} V")

    _print_table(rows)

    # Also write a tiny CSV
    csv_path = out_dir / "cap_compare.csv"
    lines = ["cap,tran_fF,ac_int_fF,rel_err"]
    for name, tran_ff, ac_ff in rows:
        denom = abs(ac_ff) if abs(ac_ff) > 0 else 1.0
        rel = (tran_ff - ac_ff) / denom
        lines.append(f"{name},{tran_ff:.12g},{ac_ff:.12g},{rel:.12g}")
    _write(csv_path, "\n".join(lines) + "\n")

    print(f"\nWrote outputs to: {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
