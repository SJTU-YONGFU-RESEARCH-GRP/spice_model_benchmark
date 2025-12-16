import argparse
import subprocess
import sys
from pathlib import Path
import re

import numpy as np


def make_corner_temp_template(base_template: Path, corner: str, temp_c: float, out_path: Path) -> None:
    """Generate a FreePDK45 DC template for a given corner and temperature.

    This patches:
      - model include (nom.inc -> {corner}.inc)
      - global TEMP/TNOM options
      - all 'option temp=' lines in the control block.
    """
    text = base_template.read_text()

    # Patch corner include: ../models/FreePDK45/nom.inc -> ../models/FreePDK45/{corner}.inc
    text = text.replace(
        "../models/FreePDK45/nom.inc",
        f"../models/FreePDK45/{corner}.inc",
    )

    # Patch global .option temp / TEMP / tnom / TNOM
    text = re.sub(r"\.option\s+temp=\s*[-0-9.]+", f".option temp={temp_c}", text, flags=re.IGNORECASE)
    text = re.sub(r"\.option\s+TEMP=\s*[-0-9.]+", f".option TEMP={temp_c}", text, flags=re.IGNORECASE)
    text = re.sub(r"tnom=\s*[-0-9.]+", f"tnom={temp_c}", text, flags=re.IGNORECASE)
    text = re.sub(r"TNOM=\s*[-0-9.]+", f"TNOM={temp_c}", text, flags=re.IGNORECASE)

    # Patch bias / DC analysis 'option temp=' inside control block
    text = re.sub(r"\boption\s+temp=\s*[-0-9.]+", f"option temp={temp_c}", text)

    out_path.write_text(text)


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
            "Run FreePDK45 MOS large-signal cap sweeps over multiple corners and "
            "temperatures, then fit unit-area capacitances."
        )
    )
    parser.add_argument(
        "--corners",
        nargs="+",
        default=["nom", "ff", "ss"],
        help="List of FreePDK45 corners to use (default: nom ff ss)",
    )
    parser.add_argument(
        "--temps",
        nargs="+",
        type=float,
        default=[-40.0, 0.0, 27.0, 85.0, 125.0],
        help="List of temperatures in Celsius for bias analysis (default: -40 0 27 85 125)",
    )
    parser.add_argument(
        "--max-L-count",
        type=int,
        default=None,
        help="If set, forward to run_cap_param_sweep.py to limit number of L points.",
    )
    parser.add_argument(
        "--max-W-count",
        type=int,
        default=None,
        help="If set, forward to run_cap_param_sweep.py to limit number of W points.",
    )
    parser.add_argument(
        "--fresh",
        action="store_true",
        help=(
            "Pass --fresh to run_cap_param_sweep.py so each (corner,temp) run "
            "does not reuse previous CSV results."
        ),
    )
    return parser.parse_args()


def main():
    args = parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    base_netlists_dir = repo_root / "netlists"
    base_template = base_netlists_dir / "freepdk45_dc_circuit.cir"

    if not base_template.exists():
        raise FileNotFoundError(f"Base FreePDK45 DC template not found: {base_template}")

    test_dir = repo_root / "test_cap_param"
    results_root = test_dir / "results"
    results_root.mkdir(parents=True, exist_ok=True)

    summary_path = results_root / "freepdk45_all_unit_area_caps.csv"
    if not summary_path.exists():
        summary_path.write_text(
            "pdk,corner,temp_C,device,cap_name,slope_fF_per_um2,intercept_fF,R2,"\
            "C_per_area_F_per_m2\n"
        )

    for corner in args.corners:
        for temp_c in args.temps:
            label = f"FreePDK45_{corner}_T{int(temp_c)}"
            pdk_lower = label.lower()

            print(f"\n[INFO] Running FreePDK45 sweep for corner={corner}, temp={temp_c} °C")

            # Create corner+temp-specific DC template
            corner_temp_netlist = base_netlists_dir / f"freepdk45_dc_circuit_{corner}_T{int(temp_c)}.cir"
            make_corner_temp_template(base_template, corner, temp_c, corner_temp_netlist)

            # Build command for run_cap_param_sweep.py
            cmd = [
                sys.executable,
                "test_cap_param/run_cap_param_sweep.py",
                "--pdk",
                label,
                "--dc-netlist",
                str(corner_temp_netlist.relative_to(repo_root)),
            ]
            if args.max_L_count is not None:
                cmd += ["--max-L-count", str(args.max_L_count)]
            if args.max_W_count is not None:
                cmd += ["--max-W-count", str(args.max_W_count)]
            if args.fresh:
                cmd += ["--fresh"]

            result = subprocess.run(cmd, cwd=str(repo_root))
            if result.returncode != 0:
                print(
                    f"[WARN] run_cap_param_sweep.py failed for corner={corner}, "
                    f"temp={temp_c} (label={label}), skipping this combination."
                )
                continue

            # Fit unit-area caps for this (corner,temp)
            results_dir = results_root / pdk_lower
            rows = fit_unit_area_caps(results_dir)

            with summary_path.open("a") as f:
                for device_label, cap_name, m, b, r2, m_F_per_m2 in rows:
                    f.write(
                        f"FreePDK45,{corner},{temp_c:.1f},{device_label},{cap_name},"
                        f"{m:.6g},{b:.6g},{r2:.6g},{m_F_per_m2:.6g}\n"
                    )

            print(
                f"[INFO] Appended {len(rows)} rows for corner={corner}, temp={temp_c} °C "
                f"to {summary_path}"
            )


if __name__ == "__main__":
    main()
