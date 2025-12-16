import argparse
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


def fit_unit_area_caps(results_dir: Path):
    """Given a results directory containing cap_vs_LW*.csv, fit C vs (L*W).

    Returns a list of rows:
      (device, cap_name, slope_fF_per_um2, intercept_fF, R2, C_per_area_F_per_m2)
    where device is "NMOS" or "PMOS".
    """
    rows = []

    def _fit_one(path: Path, cols, device_label: str):
        if not path.exists():
            return
        data = np.loadtxt(path, delimiter=",", skiprows=1)
        if data.ndim == 1:
            data = data[None, :]
        L = data[:, 0]
        W = data[:, 1]
        A = L * W  # um^2
        for i, name in enumerate(cols, start=2):
            C = data[:, i]
            m, b = np.polyfit(A, C, 1)  # C = m*A + b
            C_pred = m * A + b
            ss_res = np.sum((C - C_pred) ** 2)
            ss_tot = np.sum((C - C.mean()) ** 2)
            r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
            # m: fF/um^2 -> F/m^2 (1 fF/um^2 = 1e-3 F/m^2)
            m_F_per_m2 = m * 1e-3
            rows.append(
                (
                    device_label,
                    name,
                    float(m),
                    float(b),
                    float(r2),
                    float(m_F_per_m2),
                )
            )

    _fit_one(results_dir / "cap_vs_LW.csv", ["Cgs", "Cgd", "Cgb"], "NMOS")
    _fit_one(results_dir / "cap_vs_LW_pmos.csv", ["Cgs_p", "Cgd_p", "Cgb_p"], "PMOS")

    return rows


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Aggregate unit-area capacitances over multiple VDD values using "
            "existing cap_vs_LW*.csv results, and plot unit-area C vs VDD."
        )
    )
    parser.add_argument(
        "--pdk-name",
        type=str,
        default="PDK",
        help="Name of the PDK (used in plot titles and filenames).",
    )
    parser.add_argument(
        "--labels",
        nargs="+",
        required=True,
        help=(
            "List of result subdirectory names under test_cap_param/results/, "
            "e.g. sky130_tt_t27_vdd0p8 sky130_tt_t27_vdd1p0 sky130_tt_t27_vdd1p2."
        ),
    )
    parser.add_argument(
        "--vdds",
        nargs="+",
        type=float,
        required=True,
        help="List of VDD values (in volts) corresponding to --labels, same length.",
    )
    parser.add_argument(
        "--out-dir",
        type=str,
        default=None,
        help=(
            "Output directory for plots. If not set, defaults to "
            "test_cap_param/results/<pdk-name-lower>/plots_vdd."
        ),
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if len(args.labels) != len(args.vdds):
        raise ValueError("--labels and --vdds must have the same length")

    repo_root = Path(__file__).resolve().parents[1]
    results_root = repo_root / "test_cap_param" / "results"

    pdk_lower = args.pdk_name.lower()

    if args.out_dir is not None:
        out_dir = Path(args.out_dir)
    else:
        out_dir = results_root / pdk_lower / "plots_vdd"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Collect unit-area fits for each VDD
    groups = {}  # key: (device, cap_name) -> list of {"vdd": v, "slope": m, "C_per_area": c}

    for label, vdd in zip(args.labels, args.vdds):
        results_dir = results_root / label.lower()
        if not results_dir.exists():
            print(f"[WARN] Results directory not found for label {label}: {results_dir}")
            continue
        rows = fit_unit_area_caps(results_dir)
        for device_label, cap_name, m, b, r2, m_F_per_m2 in rows:
            key = (device_label, cap_name)
            groups.setdefault(key, []).append(
                {
                    "vdd": float(vdd),
                    "slope_fF_per_um2": float(m),
                    "C_per_area_F_per_m2": float(m_F_per_m2),
                }
            )

    # Plot unit-area C vs VDD for each (device, cap_name)
    for (device, cap_name), records in sorted(groups.items()):
        records = sorted(records, key=lambda r: r["vdd"])
        vdds = [r["vdd"] for r in records]
        slopes = [r["slope_fF_per_um2"] for r in records]

        plt.figure(figsize=(6, 4))
        plt.plot(vdds, slopes, marker="o")
        plt.xlabel("VDD (V)")
        plt.ylabel("Unit-area C (slope, fF/µm²)")
        plt.title(f"{args.pdk_name} {device} {cap_name}: C/A vs VDD")
        plt.grid(True, linestyle="--", alpha=0.4)
        plt.tight_layout()

        fname = f"{args.pdk_name}_{device}_{cap_name}_unitC_vs_VDD.png".replace("/", "-")
        out_path = out_dir / fname
        out_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(out_path, dpi=300)
        plt.close()
        print(f"[INFO] Saved {out_path}")


if __name__ == "__main__":
    main()
