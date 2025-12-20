from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main() -> None:
    repo = Path(__file__).resolve().parents[1]

    in_path = repo / "results_ac_cmatrix" / "data" / "cv_data.txt"
    out_data = repo / "results_ac_cmatrix" / "data" / "cv_data_unit_area.txt"
    plot_dir = repo / "results_ac_cmatrix" / "plots"

    # Geometry from netlists/ac_circuit.cir
    w_um = 10.0
    l_um = 0.045
    area_um2 = w_um * l_um

    cv = pd.read_csv(in_path, sep=r"\s+", engine="python")

    required = ["Vg", "Cgg_1MHz", "Cgs_1MHz", "Cgd_1MHz", "Cgb_1MHz"]
    missing = [c for c in required if c not in cv.columns]
    if missing:
        raise SystemExit(f"Missing columns in {in_path}: {missing}. Found: {list(cv.columns)}")

    cap_cols = [c for c in cv.columns if c.startswith("C")]
    cv_unit = cv.copy()
    for c in cap_cols:
        cv_unit[c] = cv_unit[c] / area_um2  # F/um^2

    # Convenience columns (fF/um^2)
    for c in ["Cgg_1MHz", "Cgs_1MHz", "Cgd_1MHz", "Cgb_1MHz"]:
        cv_unit[f"{c}_fF_per_um2"] = cv_unit[c] * 1e15

    plot_dir.mkdir(parents=True, exist_ok=True)

    # Write normalized data (tab-separated for easy inspection)
    with out_data.open("w", encoding="utf-8") as f:
        f.write("# Unit-area normalized capacitance extracted from AC analysis\n")
        f.write("# Normalization: divide by gate geometric area W*L\n")
        f.write(f"# W = {w_um} um, L = {l_um} um, Area = {area_um2} um^2\n")
        f.write("# Columns starting with 'C' are in F/um^2 after normalization\n")
        f.write("# Extra *_fF_per_um2 columns are in fF/um^2\n")
        cv_unit.to_csv(f, sep="\t", index=False, float_format="%.10g")

    vg = cv_unit["Vg"].to_numpy(dtype=float)

    def save_curve(col_fF_per_um2: str, filename: str, title: str) -> None:
        y = cv_unit[col_fF_per_um2].to_numpy(dtype=float)
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(vg, y, linewidth=2)
        ax.set_xlabel("Vg (V)")
        ax.set_ylabel("Cap / (W·L) (fF/µm²)")
        ax.grid(True, alpha=0.3)
        ax.set_title(title)
        fig.tight_layout()
        fig.savefig(plot_dir / filename, dpi=200)
        plt.close(fig)

    save_curve(
        "Cgs_1MHz_fF_per_um2",
        "ac_cgs_1MHz_unit_area.png",
        "FreePDK45: Unit-area Cgs–Vg (1 MHz)",
    )
    save_curve(
        "Cgd_1MHz_fF_per_um2",
        "ac_cgd_1MHz_unit_area.png",
        "FreePDK45: Unit-area Cgd–Vg (1 MHz)",
    )
    save_curve(
        "Cgb_1MHz_fF_per_um2",
        "ac_cgb_1MHz_unit_area.png",
        "FreePDK45: Unit-area Cgb–Vg (1 MHz)",
    )

    # Console summary for quick verification
    def stats(col: str) -> tuple[float, float]:
        arr = cv_unit[col].to_numpy(dtype=float)
        return float(np.nanmin(arr)), float(np.nanmax(arr))

    for name in ["Cgs_1MHz_fF_per_um2", "Cgd_1MHz_fF_per_um2", "Cgb_1MHz_fF_per_um2"]:
        lo, hi = stats(name)
        print(name, "range(fF/um^2):", lo, "to", hi)

    print("wrote", out_data)
    print("wrote", plot_dir / "ac_cgs_1MHz_unit_area.png")
    print("wrote", plot_dir / "ac_cgd_1MHz_unit_area.png")
    print("wrote", plot_dir / "ac_cgb_1MHz_unit_area.png")


if __name__ == "__main__":
    main()
