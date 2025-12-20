from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Plot unit-area Cgg–Vg from ngspice cv_data.txt")
    p.add_argument(
        "--results-dir",
        type=Path,
        required=True,
        help="Results directory containing data/cv_data.txt and plots/",
    )
    p.add_argument("--w-um", type=float, default=10.0, help="Gate width in um")
    p.add_argument("--l-um", type=float, default=0.045, help="Gate length in um")
    p.add_argument(
        "--freq-label",
        type=str,
        default="1MHz",
        help="Label used in the input column name, e.g. '1MHz' for 'Cgg_1MHz'",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()

    results_dir = args.results_dir.resolve()
    in_path = results_dir / "data" / "cv_data.txt"
    out_data = results_dir / "data" / "cv_data_unit_area.txt"
    out_plot = results_dir / "plots" / "cgg_unit_area_vs_vg.png"

    results_dir.joinpath("data").mkdir(parents=True, exist_ok=True)
    results_dir.joinpath("plots").mkdir(parents=True, exist_ok=True)

    area_um2 = args.w_um * args.l_um

    col_cgg = f"Cgg_{args.freq_label}"
    df = pd.read_csv(in_path, sep=r"\s+", engine="python")
    if "Vg" not in df.columns or col_cgg not in df.columns:
        raise SystemExit(f"Expected columns ['Vg', '{col_cgg}'] in {in_path}, got: {list(df.columns)}")

    vg = df["Vg"].to_numpy(dtype=float)
    cgg_f_per_um2 = df[col_cgg].to_numpy(dtype=float) / area_um2
    cgg_ff_per_um2 = cgg_f_per_um2 * 1e15

    out_df = pd.DataFrame(
        {
            "Vg": vg,
            col_cgg: df[col_cgg].to_numpy(dtype=float),
            "W_um": np.full_like(vg, args.w_um, dtype=float),
            "L_um": np.full_like(vg, args.l_um, dtype=float),
            "Area_um2": np.full_like(vg, area_um2, dtype=float),
            f"{col_cgg}_F_per_um2": cgg_f_per_um2,
            f"{col_cgg}_fF_per_um2": cgg_ff_per_um2,
        }
    )

    with out_data.open("w", encoding="utf-8") as f:
        f.write("# Unit-area normalized Cgg–Vg extracted from AC analysis\n")
        f.write("# Normalization: divide by gate geometric area W*L\n")
        f.write(f"# W = {args.w_um} um, L = {args.l_um} um, Area = {area_um2} um^2\n")
        out_df.to_csv(f, sep="\t", index=False, float_format="%.10g")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(vg, cgg_ff_per_um2, linewidth=2)
    ax.set_xlabel("Vg (V)")
    ax.set_ylabel("Cgg / (W·L) (fF/µm²)")
    ax.grid(True, alpha=0.3)
    ax.set_title(f"FreePDK45 NMOS_VTG: Unit-area Cgg–Vg ({args.freq_label})")
    fig.tight_layout()
    fig.savefig(out_plot, dpi=200)
    plt.close(fig)

    print("wrote", out_data)
    print("wrote", out_plot)
    print("points", len(vg), "Vg_min", float(np.min(vg)), "Vg_max", float(np.max(vg)))


if __name__ == "__main__":
    main()
