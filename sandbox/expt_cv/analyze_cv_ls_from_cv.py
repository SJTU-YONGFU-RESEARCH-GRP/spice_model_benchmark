import argparse
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


def load_cv_data(cv_path: Path) -> np.ndarray:
    if not cv_path.exists():
        raise FileNotFoundError(f"CV data file not found: {cv_path}")
    data = np.loadtxt(cv_path, comments="#", skiprows=1)
    if data.ndim == 1:
        data = data[None, :]
    return data


def select_c_column(data: np.ndarray, freq_hz: float) -> np.ndarray:
    freq_to_col = {
        1.0e3: 1,   # Cgg at 1 kHz
        1.0e4: 2,   # Cgg at 10 kHz
        1.0e5: 3,   # Cgg at 100 kHz
        1.0e6: 4,   # Cgg at 1 MHz
    }
    if freq_hz not in freq_to_col:
        raise ValueError(f"Unsupported frequency {freq_hz} Hz; supported: {sorted(freq_to_col.keys())}")
    col = freq_to_col[freq_hz]
    if data.shape[1] <= col:
        raise ValueError(
            f"CV data has only {data.shape[1]} columns, cannot access column {col} "
            f"for frequency {freq_hz} Hz."
        )
    return data[:, 0], data[:, col]


def reconstruct_charge(vg: np.ndarray, c: np.ndarray):
    vg = np.asarray(vg, dtype=float)
    c = np.asarray(c, dtype=float)
    if vg.shape != c.shape:
        raise ValueError("vg and c must have the same shape")
    order = np.argsort(vg)
    vg_sorted = vg[order]
    c_sorted = c[order]
    q = np.zeros_like(c_sorted)
    for k in range(1, len(vg_sorted)):
        dv = vg_sorted[k] - vg_sorted[k - 1]
        q[k] = q[k - 1] + 0.5 * (c_sorted[k] + c_sorted[k - 1]) * dv
    return vg_sorted, c_sorted, q


def compute_large_signal_cap_from_ac(vg: np.ndarray, q: np.ndarray, v1: float, v2: float) -> float:
    vg = np.asarray(vg, dtype=float)
    q = np.asarray(q, dtype=float)
    if vg.ndim != 1 or q.ndim != 1:
        raise ValueError("vg and q must be 1-D arrays")
    if vg.size < 2:
        raise ValueError("Need at least two VG points to compute large-signal capacitance")
    if v1 == v2:
        raise ValueError("v1 and v2 must be different")
    vmin_data = float(vg.min())
    vmax_data = float(vg.max())
    if not (vmin_data <= v1 <= vmax_data and vmin_data <= v2 <= vmax_data):
        raise ValueError(
            f"Requested voltage range [{v1}, {v2}] is outside data range "
            f"[{vmin_data}, {vmax_data}]"
        )
    vg_sorted = vg
    q_sorted = q
    if not np.all(np.diff(vg_sorted) >= 0):
        order = np.argsort(vg_sorted)
        vg_sorted = vg_sorted[order]
        q_sorted = q_sorted[order]
    q1 = float(np.interp(v1, vg_sorted, q_sorted))
    q2 = float(np.interp(v2, vg_sorted, q_sorted))
    dv = v2 - v1
    return (q2 - q1) / dv


def read_ls_caps_dc(ls_caps_path: Path):
    if not ls_caps_path.exists():
        raise FileNotFoundError(f"ls_caps_dc.txt not found at {ls_caps_path}")
    with ls_caps_path.open("r") as f:
        header = f.readline().strip().split()
    col_map = {name: i for i, name in enumerate(header)}
    required = ["Vg", "Vd", "Qg", "Qd", "Qs", "Qb"]
    data = np.loadtxt(ls_caps_path, skiprows=1)
    if data.ndim == 1:
        data = data[None, :]
    if data.shape[0] < 2:
        raise ValueError("ls_caps_dc.txt has fewer than two bias points")
    missing = [name for name in required if name not in col_map]
    if not missing:
        vg = data[:, col_map["Vg"]]
        vd = data[:, col_map["Vd"]]
        qg = data[:, col_map["Qg"]]
        qd = data[:, col_map["Qd"]]
        qs = data[:, col_map["Qs"]]
        qb = data[:, col_map["Qb"]]
    else:
        if data.shape[1] < 6:
            raise ValueError(
                f"ls_caps_dc.txt has only {data.shape[1]} columns and is missing "
                f"required names {missing}. Header: {header}"
            )
        vg, vd, qg, qd, qs, qb = data[:, 0], data[:, 1], data[:, 2], data[:, 3], data[:, 4], data[:, 5]
    return vg, vd, qg, qd, qs, qb


def compute_large_signal_caps_from_dc(vg, qd, qs, qb):
    vg = np.asarray(vg, dtype=float)
    qd = np.asarray(qd, dtype=float)
    qs = np.asarray(qs, dtype=float)
    qb = np.asarray(qb, dtype=float)
    if vg.size < 2:
        raise ValueError("ls_caps_dc.txt must contain at least two Vg points")
    dv = vg[-1] - vg[0]
    if dv == 0.0:
        raise ValueError("ΔVg is zero in ls_caps_dc.txt; cannot compute large-signal caps")
    cgs = -(qs[-1] - qs[0]) / dv
    cgd = -(qd[-1] - qd[0]) / dv
    cgb = -(qb[-1] - qb[0]) / dv
    cgg = cgs + cgd + cgb
    return cgs, cgd, cgb, cgg


def plot_cv_and_q(vg, c, q, out_path: Path, freq_hz: float):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax1 = plt.subplots(figsize=(6, 4))
    vg = np.asarray(vg, dtype=float)
    c = np.asarray(c, dtype=float)
    q = np.asarray(q, dtype=float)
    ax1.plot(vg, c * 1e15, "b-", label="Cgg (from AC)")
    ax1.set_xlabel("Vg (V)")
    ax1.set_ylabel("Cgg (fF)", color="b")
    ax1.tick_params(axis="y", labelcolor="b")
    ax2 = ax1.twinx()
    ax2.plot(vg, q * 1e15, "r--", label="Qg (reconstructed)")
    ax2.set_ylabel("Qg (fC)", color="r")
    ax2.tick_params(axis="y", labelcolor="r")
    title = f"Reconstructed Q(Vg) and Cgg(Vg) from AC, f={freq_hz/1e6:.3g} MHz"
    ax1.set_title(title)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="best")
    fig.tight_layout()
    fig.savefig(out_path, dpi=300)
    plt.close(fig)


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Reconstruct large-signal capacitance from small-signal CV data "
            "by integrating C(Vg) to obtain Q(Vg) and taking ΔQ/ΔVg."
        )
    )
    parser.add_argument(
        "--cv-file",
        type=str,
        default="results/cv_full_data.txt",
        help="Path to CV data file (e.g. results/cv_full_data.txt)",
    )
    parser.add_argument(
        "--freq",
        type=float,
        default=1.0e6,
        help="Frequency in Hz to select Cgg(Vg) column (default: 1e6)",
    )
    parser.add_argument(
        "--v1",
        type=float,
        default=None,
        help="Start gate voltage for large-signal capacitance (default: min(Vg))",
    )
    parser.add_argument(
        "--v2",
        type=float,
        default=None,
        help="End gate voltage for large-signal capacitance (default: max(Vg))",
    )
    parser.add_argument(
        "--dc-file",
        type=str,
        default=None,
        help="Optional path to ls_caps_dc.txt for DC large-signal comparison",
    )
    parser.add_argument(
        "--plot",
        action="store_true",
        help="If set, generate a plot of Cgg(Vg) and reconstructed Qg(Vg)",
    )
    parser.add_argument(
        "--out-prefix",
        type=str,
        default="cv_q_reconstructed",
        help="Output prefix for plots (default: cv_q_reconstructed)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    script_dir = Path(__file__).resolve().parent
    cv_path = Path(args.cv_file)
    if not cv_path.is_absolute():
        cv_path = script_dir / cv_path
    data = load_cv_data(cv_path)
    vg_raw, c_raw = select_c_column(data, args.freq)
    vg_sorted, c_sorted, q_sorted = reconstruct_charge(vg_raw, c_raw)
    v1 = args.v1 if args.v1 is not None else float(vg_sorted.min())
    v2 = args.v2 if args.v2 is not None else float(vg_sorted.max())
    if v1 > v2:
        v1, v2 = v2, v1
    cls_ac = compute_large_signal_cap_from_ac(vg_sorted, q_sorted, v1, v2)
    print("[AC->LS] Using Cgg from AC:")
    print(f"  Data file      : {cv_path}")
    print(f"  Frequency      : {args.freq:.3g} Hz")
    print(f"  Voltage range  : V1={v1:.6g} V, V2={v2:.6g} V")
    print(f"  C_ls(AC)       : {cls_ac:.6e} F ({cls_ac*1e15:.6g} fF)")
    if args.plot:
        results_dir = script_dir / "results"
        out_name = f"{args.out_prefix}_f_{args.freq:.0f}Hz.png"
        out_path = results_dir / out_name
        plot_cv_and_q(vg_sorted, c_sorted, q_sorted, out_path, args.freq)
        print(f"[PLOT] Saved CV/Q plot to {out_path}")
    if args.dc_file is not None:
        dc_path = Path(args.dc_file)
        if not dc_path.is_absolute():
            dc_path = script_dir / dc_path
        try:
            vg_dc, vd_dc, qg_dc, qd_dc, qs_dc, qb_dc = read_ls_caps_dc(dc_path)
        except Exception as e:
            print(f"[DC] Failed to read DC file {dc_path}: {e}")
            return
        cgs_dc, cgd_dc, cgb_dc, cgg_dc = compute_large_signal_caps_from_dc(vg_dc, qd_dc, qs_dc, qb_dc)
        v1_dc = float(vg_dc[0])
        v2_dc = float(vg_dc[-1])
        print("[DC LS] From ls_caps_dc.txt endpoint charges:")
        print(f"  DC file        : {dc_path}")
        print(f"  Vg endpoints   : V1={v1_dc:.6g} V, V2={v2_dc:.6g} V")
        print(f"  Cgs_LS(DC)     : {cgs_dc:.6e} F ({cgs_dc*1e15:.6g} fF)")
        print(f"  Cgd_LS(DC)     : {cgd_dc:.6e} F ({cgd_dc*1e15:.6g} fF)")
        print(f"  Cgb_LS(DC)     : {cgb_dc:.6e} F ({cgb_dc*1e15:.6g} fF)")
        print(f"  Cgg_LS(DC,sum) : {cgg_dc:.6e} F ({cgg_dc*1e15:.6g} fF)")
        rel_diff = None
        if cgg_dc != 0.0:
            rel_diff = (cls_ac - cgg_dc) / cgg_dc
            print(f"[COMPARE] C_ls(AC) / Cgg_LS(DC) - 1 = {rel_diff:.3e} (relative)")
        else:
            print("[COMPARE] Cgg_LS(DC) is zero; cannot compute relative difference")


if __name__ == "__main__":
    main()
