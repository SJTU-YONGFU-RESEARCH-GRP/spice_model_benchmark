import csv
from pathlib import Path

import matplotlib.pyplot as plt


def load_summary(csv_path: Path):
    """Load sky130_all_unit_area_caps.csv into a structured dict.

    Returns a dict keyed by (device, cap_name) with values being lists of
    (corner, temp_C, slope_fF_per_um2, C_per_area_F_per_m2).
    """
    groups = {}
    with csv_path.open("r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            device = row["device"].strip()
            cap_name = row["cap_name"].strip()
            corner = row["corner"].strip()
            try:
                temp = float(row["temp_C"])
                slope = float(row["slope_fF_per_um2"])
                c_per_area = float(row["C_per_area_F_per_m2"])
            except ValueError:
                continue
            key = (device, cap_name)
            groups.setdefault(key, []).append(
                {
                    "corner": corner,
                    "temp_C": temp,
                    "slope_fF_per_um2": slope,
                    "C_per_area_F_per_m2": c_per_area,
                }
            )
    return groups


def plot_unit_area_vs_temp(groups, out_dir: Path, pdk_name: str = "Sky130"):
    """For each (device, cap_name), plot slope_fF_per_um2 vs temp for each corner."""
    out_dir.mkdir(parents=True, exist_ok=True)

    for (device, cap_name), records in sorted(groups.items()):
        # Organize by corner
        by_corner = {}
        for rec in records:
            by_corner.setdefault(rec["corner"], []).append(rec)

        plt.figure(figsize=(6, 4))
        for corner, recs in sorted(by_corner.items()):
            recs = sorted(recs, key=lambda r: r["temp_C"])
            temps = [r["temp_C"] for r in recs]
            slopes = [r["slope_fF_per_um2"] for r in recs]
            plt.plot(temps, slopes, marker="o", label=f"corner={corner}")

        plt.xlabel("Temperature (°C)")
        plt.ylabel("Unit-area C (slope, fF/µm²)")
        plt.title(f"{pdk_name} {device} {cap_name}: C/A vs Temperature")
        plt.grid(True, linestyle="--", alpha=0.4)
        plt.legend()
        plt.tight_layout()

        fname = f"{pdk_name}_{device}_{cap_name}_unitC_vs_temp.png".replace("/", "-")
        out_path = out_dir / fname
        out_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(out_path, dpi=300)
        plt.close()
        print(f"[INFO] Saved {out_path}")


def main():
    repo_root = Path(__file__).resolve().parents[1]
    summary_csv = repo_root / "test_cap_param" / "results" / "sky130_all_unit_area_caps.csv"
    if not summary_csv.exists():
        raise FileNotFoundError(f"Summary CSV not found: {summary_csv}")

    groups = load_summary(summary_csv)

    plots_dir = repo_root / "test_cap_param" / "results" / "sky130" / "plots"
    plot_unit_area_vs_temp(groups, plots_dir, pdk_name="Sky130")


if __name__ == "__main__":
    main()
