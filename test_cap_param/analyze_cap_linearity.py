import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import argparse
import csv
import re
from dataclasses import dataclass
from typing import Optional


def linear_fit(x: np.ndarray, y: np.ndarray):
    """Perform simple linear regression y = m*x + b and return (m, b, R^2).

    Args:
        x: 1D array of independent variable.
        y: 1D array of dependent variable.

    Returns:
        slope, intercept, r2
    """
    x = np.asarray(x)
    y = np.asarray(y)
    if x.size < 2:
        return np.nan, np.nan, np.nan

    # Fit y = m*x + b
    m, b = np.polyfit(x, y, 1)
    y_pred = m * x + b
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return m, b, r2


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Analyze capacitance linearity (C vs W, C vs L) for a given PDK "
            "using the cap_vs_LW*.csv outputs from run_cap_param_sweep.py."
        )
    )
    parser.add_argument(
        "--pdk",
        default="FreePDK45",
        help=(
            "PDK name; should match the --pdk used for run_cap_param_sweep.py "
            "(default: FreePDK45)."
        ),
    )
    parser.add_argument(
        "--by-bin",
        action=argparse.BooleanOptionalAction,
        default=True,
        help=(
            "If the PDK model provides lmin/lmax/wmin/wmax bin ranges, also compute "
            "bin-aware linear fits (no cross-bin mixing) and emit *_by_bin CSVs/plots. "
            "Enabled by default; use --no-by-bin to disable."
        ),
    )
    return parser.parse_args()


@dataclass(frozen=True)
class BinRange:
    bin_id: int
    lmin_um: float
    lmax_um: float
    wmin_um: float
    wmax_um: float

    def contains(self, L_um: float, W_um: float) -> bool:
        return (self.lmin_um <= L_um <= self.lmax_um) and (self.wmin_um <= W_um <= self.wmax_um)


def _parse_cadence180_bins(repo_root: Path, device: str) -> list[BinRange]:
    scs = repo_root / "pdk" / "cadence180" / "models" / "spectre" / f"{device}1.scs"
    if not scs.exists():
        return []

    # Example:
    # 4: type=n lmin=0.18e-6  lmax=0.501e-6   wmin=10e-6   wmax=100.001e-6
    pat = re.compile(
        r"^\s*(\d+):.*?lmin\s*=\s*([0-9.+\-eE]+)\s+"
        r"lmax\s*=\s*([0-9.+\-eE]+)\s+"
        r"wmin\s*=\s*([0-9.+\-eE]+)\s+"
        r"wmax\s*=\s*([0-9.+\-eE]+)",
        re.IGNORECASE,
    )
    out: list[BinRange] = []
    for line in scs.read_text(errors="ignore").splitlines():
        m = pat.match(line)
        if not m:
            continue
        bin_id = int(m.group(1))
        lmin_um = float(m.group(2)) * 1e6
        lmax_um = float(m.group(3)) * 1e6
        wmin_um = float(m.group(4)) * 1e6
        wmax_um = float(m.group(5)) * 1e6
        out.append(BinRange(bin_id=bin_id, lmin_um=lmin_um, lmax_um=lmax_um, wmin_um=wmin_um, wmax_um=wmax_um))
    return out


def _parse_sky130_bins(repo_root: Path, device: str) -> list[BinRange]:
    # device: "nfet" or "pfet"
    if device == "nfet":
        path = (
            repo_root
            / "models"
            / "skywater-pdk-libs-sky130_fd_pr"
            / "cells"
            / "nfet_01v8"
            / "sky130_fd_pr__nfet_01v8.pm3.spice"
        )
    elif device == "pfet":
        path = (
            repo_root
            / "models"
            / "skywater-pdk-libs-sky130_fd_pr"
            / "cells"
            / "pfet_01v8"
            / "sky130_fd_pr__pfet_01v8.pm3.spice"
        )
    else:
        return []
    if not path.exists():
        return []

    # Sky130 .pm3.spice files commonly contain bin ranges as single lines that include
    # lmin/lmax/wmin/wmax (meters). We'll parse those directly.
    lmin_re = re.compile(r"\blmin\s*=\s*([0-9.+\-eE]+)")
    lmax_re = re.compile(r"\blmax\s*=\s*([0-9.+\-eE]+)")
    wmin_re = re.compile(r"\bwmin\s*=\s*([0-9.+\-eE]+)")
    wmax_re = re.compile(r"\bwmax\s*=\s*([0-9.+\-eE]+)")

    out: list[BinRange] = []
    for raw in path.read_text(errors="ignore").splitlines():
        m_lmin = lmin_re.search(raw)
        m_lmax = lmax_re.search(raw)
        m_wmin = wmin_re.search(raw)
        m_wmax = wmax_re.search(raw)
        if not (m_lmin and m_lmax and m_wmin and m_wmax):
            continue
        lmin_um = float(m_lmin.group(1)) * 1e6
        lmax_um = float(m_lmax.group(1)) * 1e6
        wmin_um = float(m_wmin.group(1)) * 1e6
        wmax_um = float(m_wmax.group(1)) * 1e6
        out.append(
            BinRange(
                bin_id=len(out) + 1,
                lmin_um=lmin_um,
                lmax_um=lmax_um,
                wmin_um=wmin_um,
                wmax_um=wmax_um,
            )
        )

    return out


def _get_bins(repo_root: Path, pdk_lower: str, device: str) -> list[BinRange]:
    # device: "nmos" or "pmos"
    if "cadence180" in pdk_lower:
        return _parse_cadence180_bins(repo_root, "nmos" if device == "nmos" else "pmos")
    if "sky130" in pdk_lower:
        return _parse_sky130_bins(repo_root, "nfet" if device == "nmos" else "pfet")
    return []


def _assign_bin_ids(L_vals: np.ndarray, W_vals: np.ndarray, bins: list[BinRange]) -> np.ndarray:
    if not bins:
        return np.full_like(L_vals, fill_value=-1, dtype=int)
    out = np.full(L_vals.shape, fill_value=-1, dtype=int)
    for i, (L_um, W_um) in enumerate(zip(L_vals, W_vals)):
        for br in bins:
            if br.contains(float(L_um), float(W_um)):
                out[i] = br.bin_id
                break
    return out


def _write_fit_csv_by_bin(
    out_csv: Path,
    x_label: str,
    rows: list[dict],
):
    # rows must contain keys: x_label, bin_id, lmin_um, lmax_um, wmin_um, wmax_um, npoints, slope_fF_per_um, intercept_fF, R2
    header = (
        f"{x_label},bin_id,lmin_um,lmax_um,wmin_um,wmax_um,npoints,"
        "slope_fF_per_um,intercept_fF,R2"
    )
    out_data = np.array(
        [
            [
                r[x_label],
                r["bin_id"],
                r["lmin_um"],
                r["lmax_um"],
                r["wmin_um"],
                r["wmax_um"],
                r["npoints"],
                r["slope_fF_per_um"],
                r["intercept_fF"],
                r["R2"],
            ]
            for r in rows
        ],
        dtype=float,
    )
    np.savetxt(out_csv, out_data, delimiter=",", header=header, comments="")


def _plot_r2_by_bin(out_png: Path, x_label: str, rows: list[dict], title: str):
    if not rows:
        return
    xs = np.array([r[x_label] for r in rows], dtype=float)
    r2s = np.array([r["R2"] for r in rows], dtype=float)
    bins = np.array([int(r["bin_id"]) for r in rows], dtype=int)

    plt.figure(figsize=(7, 4))
    sc = plt.scatter(xs, r2s, c=bins, cmap="tab20", s=35)
    plt.xlabel(x_label)
    plt.ylabel("R^2")
    plt.ylim(0.0, 1.05)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.title(title)
    cbar = plt.colorbar(sc)
    cbar.set_label("bin_id")
    plt.tight_layout()
    plt.savefig(out_png, dpi=300)
    plt.close()


def _load_cap_csv(csv_path: Path):
    """Load cap_vs_LW*.csv.

    Expected format:
      - First row is header
      - First two columns are L_um, W_um
      - Remaining columns are capacitances in fF (any names)
    """
    with csv_path.open("r", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)

    if len(header) < 3:
        raise ValueError(f"CSV header has <3 columns: {header}")

    header_norm = [h.strip() for h in header]
    if header_norm[0].lower() != "l_um" or header_norm[1].lower() != "w_um":
        raise ValueError(
            f"Unexpected first columns in {csv_path}: {header_norm[:2]} (expected L_um,W_um)"
        )

    data = np.loadtxt(csv_path, delimiter=",", skiprows=1)
    if data.size == 0:
        raise ValueError(f"No data rows in {csv_path}")
    if data.ndim == 1:
        data = data[None, :]

    if data.shape[1] != len(header_norm):
        raise ValueError(
            f"CSV column count mismatch for {csv_path}: header={len(header_norm)} data={data.shape[1]}"
        )

    L_vals = data[:, 0]
    W_vals = data[:, 1]
    cap_names = header_norm[2:]
    cap_cols = {name: data[:, 2 + i] for i, name in enumerate(cap_names)}
    return L_vals, W_vals, cap_cols


def _write_fit_csv(out_csv: Path, x_values: np.ndarray, x_label: str, m: np.ndarray, b: np.ndarray, r2: np.ndarray):
    header = f"{x_label},slope_fF_per_um,intercept_fF,R2"
    out_data = np.column_stack([x_values, m, b, r2])
    np.savetxt(out_csv, out_data, delimiter=",", header=header, comments="")


def _plot_r2(out_png: Path, x_values: np.ndarray, x_label: str, r2: np.ndarray, title: str):
    plt.figure(figsize=(6, 4))
    plt.plot(x_values, r2, marker="o")
    plt.xlabel(x_label)
    plt.ylabel("R^2")
    plt.ylim(0.0, 1.05)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(out_png, dpi=300)
    plt.close()


def main():
    args = parse_args()
    pdk_name = args.pdk
    pdk_lower = pdk_name.lower()

    repo_root = Path(__file__).resolve().parents[1]
    test_dir = repo_root / "test_cap_param"
    # Results are organized per-PDK under test_cap_param/results/<pdk_lower>/
    results_root = test_dir / "results"
    results_dir = results_root / pdk_lower
    plots_dir = results_dir / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)

    # ===== NMOS data =====
    csv_path = results_dir / "cap_vs_LW.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"Input CSV not found: {csv_path}")

    L_vals, W_vals, caps = _load_cap_csv(csv_path)
    L_unique = np.unique(L_vals)
    W_unique = np.unique(W_vals)

    bins_n = _get_bins(repo_root, pdk_lower, "nmos")
    bin_id_n = _assign_bin_ids(L_vals, W_vals, bins_n)

    # 1) NMOS: per fixed L, fit C(W)
    for cap_name, C_fF in caps.items():
        slopes = []
        intercepts = []
        r2_list = []
        L_used = []

        for L_um in L_unique:
            mask = np.isclose(L_vals, L_um)
            if not np.any(mask):
                continue
            W_sub = W_vals[mask]
            C_sub = C_fF[mask]
            order = np.argsort(W_sub)
            W_sub = W_sub[order]
            C_sub = C_sub[order]

            m, b, r2 = linear_fit(W_sub, C_sub)
            slopes.append(m)
            intercepts.append(b)
            r2_list.append(r2)
            L_used.append(L_um)

        slopes = np.array(slopes)
        intercepts = np.array(intercepts)
        r2_arr = np.array(r2_list)

        out_csv = results_dir / f"{cap_name}_linfit_C_vs_W_per_L.csv"
        _write_fit_csv(out_csv, np.array(L_used, dtype=float), "L_um", slopes, intercepts, r2_arr)

        out_png = plots_dir / f"R2_{cap_name}_C_vs_W_over_L.png"
        _plot_r2(out_png, np.array(L_used, dtype=float), "L (um)", r2_arr, f"Linearity of {cap_name} vs W (R^2 per L)")

        # Bin-aware (optional)
        if args.by_bin and bins_n:
            rows: list[dict] = []
            for L_um in L_unique:
                mask_L = np.isclose(L_vals, L_um)
                if not np.any(mask_L):
                    continue
                for br in bins_n:
                    mask = mask_L & (bin_id_n == br.bin_id)
                    if np.count_nonzero(mask) < 2:
                        continue
                    W_sub = W_vals[mask]
                    C_sub = C_fF[mask]
                    order = np.argsort(W_sub)
                    W_sub = W_sub[order]
                    C_sub = C_sub[order]
                    m, b, r2 = linear_fit(W_sub, C_sub)
                    rows.append(
                        {
                            "L_um": float(L_um),
                            "bin_id": float(br.bin_id),
                            "lmin_um": float(br.lmin_um),
                            "lmax_um": float(br.lmax_um),
                            "wmin_um": float(br.wmin_um),
                            "wmax_um": float(br.wmax_um),
                            "npoints": float(W_sub.size),
                            "slope_fF_per_um": float(m),
                            "intercept_fF": float(b),
                            "R2": float(r2),
                        }
                    )

            out_csv_bin = results_dir / f"{cap_name}_linfit_C_vs_W_per_L_by_bin.csv"
            _write_fit_csv_by_bin(out_csv_bin, "L_um", rows)
            out_png_bin = plots_dir / f"R2_{cap_name}_C_vs_W_over_L_by_bin.png"
            _plot_r2_by_bin(out_png_bin, "L_um", rows, f"Linearity of {cap_name} vs W (R^2 per L per bin)")

    # 2) NMOS: per fixed W, fit C(L)
    for cap_name, C_fF in caps.items():
        slopes = []
        intercepts = []
        r2_list = []
        W_used = []

        for W_um in W_unique:
            mask = np.isclose(W_vals, W_um)
            if not np.any(mask):
                continue
            L_sub = L_vals[mask]
            C_sub = C_fF[mask]
            order = np.argsort(L_sub)
            L_sub = L_sub[order]
            C_sub = C_sub[order]

            m, b, r2 = linear_fit(L_sub, C_sub)
            slopes.append(m)
            intercepts.append(b)
            r2_list.append(r2)
            W_used.append(W_um)

        slopes = np.array(slopes)
        intercepts = np.array(intercepts)
        r2_arr = np.array(r2_list)

        out_csv = results_dir / f"{cap_name}_linfit_C_vs_L_per_W.csv"
        _write_fit_csv(out_csv, np.array(W_used, dtype=float), "W_um", slopes, intercepts, r2_arr)

        out_png = plots_dir / f"R2_{cap_name}_C_vs_L_over_W.png"
        _plot_r2(out_png, np.array(W_used, dtype=float), "W (um)", r2_arr, f"Linearity of {cap_name} vs L (R^2 per W)")

        # Bin-aware (optional)
        if args.by_bin and bins_n:
            rows: list[dict] = []
            for W_um in W_unique:
                mask_W = np.isclose(W_vals, W_um)
                if not np.any(mask_W):
                    continue
                for br in bins_n:
                    mask = mask_W & (bin_id_n == br.bin_id)
                    if np.count_nonzero(mask) < 2:
                        continue
                    L_sub = L_vals[mask]
                    C_sub = C_fF[mask]
                    order = np.argsort(L_sub)
                    L_sub = L_sub[order]
                    C_sub = C_sub[order]
                    m, b, r2 = linear_fit(L_sub, C_sub)
                    rows.append(
                        {
                            "W_um": float(W_um),
                            "bin_id": float(br.bin_id),
                            "lmin_um": float(br.lmin_um),
                            "lmax_um": float(br.lmax_um),
                            "wmin_um": float(br.wmin_um),
                            "wmax_um": float(br.wmax_um),
                            "npoints": float(L_sub.size),
                            "slope_fF_per_um": float(m),
                            "intercept_fF": float(b),
                            "R2": float(r2),
                        }
                    )

            out_csv_bin = results_dir / f"{cap_name}_linfit_C_vs_L_per_W_by_bin.csv"
            _write_fit_csv_by_bin(out_csv_bin, "W_um", rows)
            out_png_bin = plots_dir / f"R2_{cap_name}_C_vs_L_over_W_by_bin.png"
            _plot_r2_by_bin(out_png_bin, "W_um", rows, f"Linearity of {cap_name} vs L (R^2 per W per bin)")

    # ===== PMOS data (optional) =====
    csv_p_path = results_dir / "cap_vs_LW_pmos.csv"
    if not csv_p_path.exists():
        return

    L_vals_p, W_vals_p, caps_p = _load_cap_csv(csv_p_path)
    L_unique_p = np.unique(L_vals_p)
    W_unique_p = np.unique(W_vals_p)

    bins_p = _get_bins(repo_root, pdk_lower, "pmos")
    bin_id_p = _assign_bin_ids(L_vals_p, W_vals_p, bins_p)

    # 3) PMOS: C(W) per L
    for cap_name, C_fF in caps_p.items():
        slopes = []
        intercepts = []
        r2_list = []
        L_used = []
        for L_um in L_unique_p:
            mask = np.isclose(L_vals_p, L_um)
            if not np.any(mask):
                continue
            W_sub = W_vals_p[mask]
            C_sub = C_fF[mask]
            order = np.argsort(W_sub)
            W_sub = W_sub[order]
            C_sub = C_sub[order]

            m, b, r2 = linear_fit(W_sub, C_sub)
            slopes.append(m)
            intercepts.append(b)
            r2_list.append(r2)
            L_used.append(L_um)

        slopes = np.array(slopes)
        intercepts = np.array(intercepts)
        r2_arr = np.array(r2_list)

        out_csv = results_dir / f"{cap_name}_linfit_C_vs_W_per_L.csv"
        _write_fit_csv(out_csv, np.array(L_used, dtype=float), "L_um", slopes, intercepts, r2_arr)

        out_png = plots_dir / f"R2_{cap_name}_C_vs_W_over_L.png"
        _plot_r2(
            out_png,
            np.array(L_used, dtype=float),
            "L (um)",
            r2_arr,
            f"Linearity of {cap_name} vs W (R^2 per L) [PMOS]",
        )

        if args.by_bin and bins_p:
            rows: list[dict] = []
            for L_um in L_unique_p:
                mask_L = np.isclose(L_vals_p, L_um)
                if not np.any(mask_L):
                    continue
                for br in bins_p:
                    mask = mask_L & (bin_id_p == br.bin_id)
                    if np.count_nonzero(mask) < 2:
                        continue
                    W_sub = W_vals_p[mask]
                    C_sub = C_fF[mask]
                    order = np.argsort(W_sub)
                    W_sub = W_sub[order]
                    C_sub = C_sub[order]
                    m, b, r2 = linear_fit(W_sub, C_sub)
                    rows.append(
                        {
                            "L_um": float(L_um),
                            "bin_id": float(br.bin_id),
                            "lmin_um": float(br.lmin_um),
                            "lmax_um": float(br.lmax_um),
                            "wmin_um": float(br.wmin_um),
                            "wmax_um": float(br.wmax_um),
                            "npoints": float(W_sub.size),
                            "slope_fF_per_um": float(m),
                            "intercept_fF": float(b),
                            "R2": float(r2),
                        }
                    )

            out_csv_bin = results_dir / f"{cap_name}_linfit_C_vs_W_per_L_by_bin.csv"
            _write_fit_csv_by_bin(out_csv_bin, "L_um", rows)
            out_png_bin = plots_dir / f"R2_{cap_name}_C_vs_W_over_L_by_bin.png"
            _plot_r2_by_bin(out_png_bin, "L_um", rows, f"Linearity of {cap_name} vs W (R^2 per L per bin) [PMOS]")

    # 4) PMOS: C(L) per W
    for cap_name, C_fF in caps_p.items():
        slopes = []
        intercepts = []
        r2_list = []
        W_used = []
        for W_um in W_unique_p:
            mask = np.isclose(W_vals_p, W_um)
            if not np.any(mask):
                continue
            L_sub = L_vals_p[mask]
            C_sub = C_fF[mask]
            order = np.argsort(L_sub)
            L_sub = L_sub[order]
            C_sub = C_sub[order]

            m, b, r2 = linear_fit(L_sub, C_sub)
            slopes.append(m)
            intercepts.append(b)
            r2_list.append(r2)
            W_used.append(W_um)

        slopes = np.array(slopes)
        intercepts = np.array(intercepts)
        r2_arr = np.array(r2_list)

        out_csv = results_dir / f"{cap_name}_linfit_C_vs_L_per_W.csv"
        _write_fit_csv(out_csv, np.array(W_used, dtype=float), "W_um", slopes, intercepts, r2_arr)

        out_png = plots_dir / f"R2_{cap_name}_C_vs_L_over_W.png"
        _plot_r2(
            out_png,
            np.array(W_used, dtype=float),
            "W (um)",
            r2_arr,
            f"Linearity of {cap_name} vs L (R^2 per W) [PMOS]",
        )

        if args.by_bin and bins_p:
            rows: list[dict] = []
            for W_um in W_unique_p:
                mask_W = np.isclose(W_vals_p, W_um)
                if not np.any(mask_W):
                    continue
                for br in bins_p:
                    mask = mask_W & (bin_id_p == br.bin_id)
                    if np.count_nonzero(mask) < 2:
                        continue
                    L_sub = L_vals_p[mask]
                    C_sub = C_fF[mask]
                    order = np.argsort(L_sub)
                    L_sub = L_sub[order]
                    C_sub = C_sub[order]
                    m, b, r2 = linear_fit(L_sub, C_sub)
                    rows.append(
                        {
                            "W_um": float(W_um),
                            "bin_id": float(br.bin_id),
                            "lmin_um": float(br.lmin_um),
                            "lmax_um": float(br.lmax_um),
                            "wmin_um": float(br.wmin_um),
                            "wmax_um": float(br.wmax_um),
                            "npoints": float(L_sub.size),
                            "slope_fF_per_um": float(m),
                            "intercept_fF": float(b),
                            "R2": float(r2),
                        }
                    )

            out_csv_bin = results_dir / f"{cap_name}_linfit_C_vs_L_per_W_by_bin.csv"
            _write_fit_csv_by_bin(out_csv_bin, "W_um", rows)
            out_png_bin = plots_dir / f"R2_{cap_name}_C_vs_L_over_W_by_bin.png"
            _plot_r2_by_bin(out_png_bin, "W_um", rows, f"Linearity of {cap_name} vs L (R^2 per W per bin) [PMOS]")


if __name__ == "__main__":
    main()
