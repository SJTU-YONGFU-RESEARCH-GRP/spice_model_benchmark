import argparse
import re
import shutil
import subprocess
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np


# This script sweeps MOSFET length/width and extracts **large-signal gate
# capacitance** using **transient charge integration**:
#
#   Q_total = ∫ Ig(t) dt
#   Cgg_LS  = |Q_total| / VDD
#
# This replaces the previous DC endpoint charge method (5.1), which is known
# to be inconsistent with AC/TRAN in ngspice for some BSIM models.
#
# Results are saved in:
#   test_cap_param/results/<pdk>/cap_vs_LW.csv        (NMOS)
#   test_cap_param/results/<pdk>/cap_vs_LW_pmos.csv   (PMOS, optional)
# with columns:
#   L_um, W_um, Cgg_fF


def generate_tran_netlist_from_template(
    template_path: Path,
    netlist_path: Path,
    L_um: float,
    W_um: float,
    vdd: float,
) -> None:
    """Patch .param lines in a transient template and write to netlist_path."""
    text = template_path.read_text()

    def _replace_param(text_in: str, name: str, value: float, default_suffix: str) -> str:
        pattern = rf"^\.param\s+{re.escape(name)}\s*=\s*([-+0-9.eE]+)([a-zA-Z]*)\b"
        m = re.search(pattern, text_in, flags=re.MULTILINE)
        suffix = m.group(2) if m is not None else default_suffix
        replacement = f".param {name}={value:.6g}{suffix}"
        return re.sub(pattern, replacement, text_in, flags=re.MULTILINE)

    text = _replace_param(text, "L_dut", L_um, default_suffix="u")
    text = _replace_param(text, "W_dut", W_um, default_suffix="u")
    text = _replace_param(text, "VDD", vdd, default_suffix="")
    netlist_path.write_text(text)


def run_ngspice(netlist_path: Path, cwd: Optional[Path] = None) -> str:
    """Run ngspice -b and return stdout, raising on failure."""
    if cwd is None:
        cwd = netlist_path.parent
    cmd = ["ngspice", "-b", str(netlist_path)]
    result = subprocess.run(cmd, cwd=str(cwd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"ngspice failed for {netlist_path} with code {result.returncode}\n"
            f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return result.stdout


def parse_q_total(stdout: str) -> Optional[float]:
    m = re.search(r"\bq_total\s*=\s*([-+0-9.eE]+)", stdout)
    if not m:
        return None
    try:
        return float(m.group(1))
    except Exception:
        return None


def parse_args():
    """Parse command-line arguments for multi-PDK capacitance sweep."""
    parser = argparse.ArgumentParser(
        description=(
            "Sweep MOS L/W and extract large-signal gate capacitance (Cgg) "
            "using transient charge integration (TRAN)."
        )
    )
    parser.add_argument(
        "--pdk",
        default="FreePDK45",
        help="PDK name used in plot titles and generated netlist names (default: FreePDK45)",
    )
    parser.add_argument(
        "--tran-netlist",
        dest="tran_netlist",
        default=None,
        help=(
            "Path to transient template netlist for NMOS. If not provided, uses "
            "netlists/freepdk45_tran_cap_template.cir or netlists/sky130_tran_cap_template.cir."
        ),
    )
    parser.add_argument(
        "--tran-netlist-pmos",
        dest="tran_netlist_pmos",
        default=None,
        help=(
            "Optional path to transient template netlist for PMOS. If not provided, uses "
            "netlists/freepdk45_tran_cap_template_pmos.cir or netlists/sky130_tran_cap_template_pmos.cir."
        ),
    )
    parser.add_argument(
        "--dc-netlist",
        dest="dc_netlist",
        default=None,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--L-scale",
        type=float,
        default=1.0,
        help=(
            "Scale factor applied to the default L sweep range based on 45nm "
            "(default: 1.0). For ~130nm you can use 3.0."
        ),
    )
    parser.add_argument(
        "--W-scale",
        type=float,
        default=1.0,
        help=(
            "Scale factor applied to the default W sweep range based on 45nm "
            "(default: 1.0)."
        ),
    )
    parser.add_argument(
        "--W-step-scale",
        type=float,
        default=1.0,
        help=(
            "Scale factor applied to the default W step (default: 1.0). "
            "Use 2.0 to double the W step and roughly halve the number of W points."
        ),
    )
    parser.add_argument(
        "--max-L-count",
        type=int,
        default=None,
        help=(
            "If set, use only the first N points of the L sweep list. "
            "Useful for quick tests on a small subset of the netlist grid."
        ),
    )
    parser.add_argument(
        "--max-W-count",
        type=int,
        default=None,
        help=(
            "If set, use only the first M points of the W sweep list. "
            "Useful for quick tests on a small subset of the W sweep list."
        ),
    )
    parser.add_argument(
        "--vdd",
        type=float,
        default=1.2,
        help=(
            "Gate step amplitude (VDD) in volts used for charge integration."
        ),
    )
    parser.add_argument(
        "--fresh",
        action="store_true",
        help=(
            "Do not reuse existing CSV results; recompute only the selected "
            "L/W grid from scratch."
        ),
    )
    return parser.parse_args()


def main():
    args = parse_args()
    # Derive PDK name/lowercase once and reuse both for paths and labeling.
    pdk_name = args.pdk
    pdk_lower = pdk_name.lower()

    repo_root = Path(__file__).resolve().parents[1]
    test_dir = repo_root / "test_cap_param"
    # Keep template netlists and .spiceinit in the top-level netlists directory,
    # but place generated sweep netlists into a per-PDK subdirectory.
    base_netlists_dir = repo_root / "netlists"
    netlist_dir = base_netlists_dir / pdk_lower
    # Place results into a per-PDK subdirectory to avoid mixing different PDKs.
    results_root = test_dir / "results"
    results_dir = results_root / pdk_lower
    plots_dir = results_dir / "plots"

    netlist_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)
    plots_dir.mkdir(parents=True, exist_ok=True)

    # Ensure ngspice in the per-PDK netlists directory sees the same .spiceinit
    # as the main project netlists directory. This is important for
    # enabling compatibility modes (e.g. ngbehavior=hsa) so that
    # terminal charge access @M1[qg] works consistently.
    main_spiceinit = base_netlists_dir / ".spiceinit"
    local_spiceinit = netlist_dir / ".spiceinit"
    if main_spiceinit.exists() and not local_spiceinit.exists():
        shutil.copy(main_spiceinit, local_spiceinit)

    # Define L/W sweep (in micrometers).

    if pdk_lower.startswith("sky130"):
        # For Sky130 1.8V devices (sky130_fd_pr__nfet_01v8 / sky130_fd_pr__pfet_01v8),
        # use (almost) the full valid geometry range from the BSIM models with
        # linear steps equal to 2% of the total range. Empirically, the extreme
        # point W = 100um at L = 0.15um can fall outside the binning envelopes
        # and trigger 'could not find a valid modelname', so we back off the
        # maximum width slightly.
        L_min_um = 0.15
        L_max_um = 98.0
        W_min_um = 2.0
        W_max_um = 98.0

        L_step_um = 0.02 * (L_max_um - L_min_um)
        W_step_um = 0.02 * (W_max_um - W_min_um)

        L_list_um = np.arange(L_min_um, L_max_um + 0.5 * L_step_um, L_step_um)
        W_list_um = np.arange(W_min_um, W_max_um + 0.5 * W_step_um, W_step_um)
    else:
        # L: log-spaced from 45 nm (0.045 um) to 10 um
        base_L_min_um = 0.045
        base_L_max_um = 10.0
        num_L = 30  # number of L points (log-spaced); adjust as needed

        L_min_um = base_L_min_um * args.L_scale
        L_max_um = base_L_max_um * args.L_scale
        L_list_um = np.logspace(np.log10(L_min_um), np.log10(L_max_um), num=num_L)

        # W: linearly spaced from 100 nm (0.1 um) to 50 um, step 100 nm (0.1 um)
        base_W_min_um = 0.1
        base_W_max_um = 50.0
        base_W_step_um = 0.1

        W_min_um = base_W_min_um * args.W_scale
        W_max_um = base_W_max_um * args.W_scale
        W_step_um = base_W_step_um * args.W_step_scale
        # use arange with a small epsilon to ensure inclusion of W_max_um
        W_list_um = np.arange(W_min_um, W_max_um + 0.5 * W_step_um, W_step_um)

    # Optionally restrict the number of L/W points for quick, partial sweeps.
    if args.max_L_count is not None:
        L_list_um = L_list_um[: args.max_L_count]
    if args.max_W_count is not None:
        W_list_um = W_list_um[: args.max_W_count]

    vdd = args.vdd

    # Records: each entry is (L_um, W_um, Cgg_F)
    records_nmos: list[tuple[float, float, float]] = []
    records_pmos: list[tuple[float, float, float]] = []
    # Keep track of points that failed (either ngspice or post-processing)
    failed_points = []  # (L_um, W_um, stage, message)
    existing_points: set[tuple[float, float]] = set()  # keys are (round(L,3), round(W,1))

    if args.dc_netlist is not None:
        print("[WARN] --dc-netlist is deprecated/ignored (now using TRAN method).")

    # Determine template netlists.
    if args.tran_netlist is not None:
        template_nmos = Path(args.tran_netlist).resolve()
    else:
        template_nmos = (
            base_netlists_dir / "sky130_tran_cap_template.cir"
            if pdk_lower.startswith("sky130")
            else base_netlists_dir / "freepdk45_tran_cap_template.cir"
        )

    if args.tran_netlist_pmos is not None:
        template_pmos = Path(args.tran_netlist_pmos).resolve()
    else:
        template_pmos = (
            base_netlists_dir / "sky130_tran_cap_template_pmos.cir"
            if pdk_lower.startswith("sky130")
            else base_netlists_dir / "freepdk45_tran_cap_template_pmos.cir"
        )

    template_stem = template_nmos.stem

    # Incremental reuse: reuse NMOS points already in cap_vs_LW.csv.
    if not args.fresh:
        csv_n_path = results_dir / "cap_vs_LW.csv"
        if csv_n_path.exists():
            try:
                with csv_n_path.open("r") as f:
                    header_line = f.readline().strip().lower()
                if "cgg" not in header_line:
                    print(
                        f"[WARN] Existing {csv_n_path} does not look like TRAN output "
                        f"(header: {header_line!r}); ignoring for incremental reuse."
                    )
                    raise ValueError("incompatible existing CSV header")
                data_prev = np.loadtxt(csv_n_path, delimiter=",", skiprows=1)
                if data_prev.ndim == 1:
                    data_prev = data_prev[None, :]
                for row in data_prev:
                    if len(row) < 3:
                        continue
                    L_prev, W_prev, Cgg_prev_fF = row[0], row[1], row[2]
                    key = (round(float(L_prev), 3), round(float(W_prev), 1))
                    existing_points.add(key)
                    records_nmos.append((float(L_prev), float(W_prev), float(Cgg_prev_fF) * 1e-15))
                if existing_points:
                    print(f"[INFO] Reusing {len(existing_points)} existing NMOS points from {csv_n_path}")
            except Exception as e:
                print(f"[WARN] Failed to load existing NMOS CSV {csv_n_path}: {e}")

    for L_um in L_list_um:
        for W_um in W_list_um:
            key = (round(L_um, 3), round(W_um, 1))
            if key in existing_points:
                print(
                    f"[INFO] Results already exist for L={L_um}um, W={W_um}um; "
                    f"skipping simulation for this point."
                )
                continue
            netlist_name = f"{template_stem}_L{L_um:.3f}u_W{W_um:.1f}u.cir"
            netlist_path = netlist_dir / netlist_name

            print(f"[INFO] Generating TRAN netlist for L={L_um}um, W={W_um}um -> {netlist_name}")
            generate_tran_netlist_from_template(template_nmos, netlist_path, L_um, W_um, vdd=vdd)

            print(f"[INFO] Running ngspice (TRAN) for {netlist_name}")
            # Run ngspice from the top-level netlists directory so that
            # relative .include "../models/..." and wrdata paths match the
            # original layout, even though the generated netlists live in a
            # per-PDK subdirectory.
            try:
                netlist_rel = netlist_path.relative_to(base_netlists_dir)
                stdout = run_ngspice(netlist_rel, cwd=base_netlists_dir)
            except Exception as e:  # ngspice failure
                msg = str(e)
                print(
                    f"[WARN] ngspice failed for L={L_um}um, W={W_um}um: {msg}\n"
                    f"       Skipping this point and continuing."
                )
                failed_points.append((L_um, W_um, "ngspice", msg))
                continue

            q_total = parse_q_total(stdout)
            if q_total is None:
                failed_points.append((L_um, W_um, "parse", "q_total not found"))
                continue
            cgg = abs(q_total) / vdd
            records_nmos.append((float(L_um), float(W_um), float(cgg)))

            # Optional PMOS (best-effort)
            if template_pmos.exists():
                netlist_name_p = f"{template_pmos.stem}_L{L_um:.3f}u_W{W_um:.1f}u.cir"
                netlist_path_p = netlist_dir / netlist_name_p
                generate_tran_netlist_from_template(template_pmos, netlist_path_p, L_um, W_um, vdd=vdd)
                try:
                    netlist_rel_p = netlist_path_p.relative_to(base_netlists_dir)
                    stdout_p = run_ngspice(netlist_rel_p, cwd=base_netlists_dir)
                    q_total_p = parse_q_total(stdout_p)
                    if q_total_p is not None:
                        cgg_p = abs(q_total_p) / vdd
                        records_pmos.append((float(L_um), float(W_um), float(cgg_p)))
                except Exception:
                    pass

    # If any points failed, write a small log for inspection.
    if failed_points:
        failed_log = results_dir / "failed_points.txt"
        with failed_log.open("w") as f:
            for L_um, W_um, stage, msg in failed_points:
                f.write(
                    f"L={L_um:.6g}um, W={W_um:.6g}um, stage={stage}, "
                    f"error={msg}\n"
                )
        print(
            f"[WARN] {len(failed_points)} (L,W) points failed. "
            f"Details written to {failed_log}"
        )

    if not records_nmos:
        print("[WARN] No successful NMOS points collected; skipping outputs.")
        return

    data_n = np.array(records_nmos, dtype=float)
    L_vals = data_n[:, 0]
    W_vals = data_n[:, 1]
    Cgg_vals = data_n[:, 2]

    # Save NMOS CSV in fF for convenience
    csv_path = results_dir / "cap_vs_LW.csv"
    header = "L_um,W_um,Cgg_fF"
    arr_to_save = np.column_stack([L_vals, W_vals, Cgg_vals * 1e15])
    np.savetxt(csv_path, arr_to_save, delimiter=",", header=header, comments="")
    print(f"[INFO] Saved NMOS sweep data to {csv_path}")

    if records_pmos:
        data_p = np.array(records_pmos, dtype=float)
        csv_p_path = results_dir / "cap_vs_LW_pmos.csv"
        header_p = "L_um,W_um,Cgg_fF"
        arr_to_save_p = np.column_stack([data_p[:, 0], data_p[:, 1], data_p[:, 2] * 1e15])
        np.savetxt(csv_p_path, arr_to_save_p, delimiter=",", header=header_p, comments="")
        print(f"[INFO] Saved PMOS sweep data to {csv_p_path}")

    # Plot NMOS Cgg vs W for several L
    plt.figure(figsize=(6, 4))
    for L_um in L_list_um:
        mask = np.isclose(L_vals, L_um)
        if not np.any(mask):
            continue
        W_sub = W_vals[mask]
        C_sub = Cgg_vals[mask] * 1e15
        order = np.argsort(W_sub)
        plt.plot(W_sub[order], C_sub[order], marker="o", label=f"L={L_um:.3f}um")
    plt.xlabel("W (um)")
    plt.ylabel("Cgg (fF)")
    plt.title(f"Cgg (TRAN) vs W at different L ({pdk_name} NMOS)")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    out_path = plots_dir / "Cgg_vs_W.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"[INFO] Saved plot {out_path}")

    # Plot NMOS Cgg vs L for several W
    plt.figure(figsize=(6, 4))
    for W_um in W_list_um:
        mask = np.isclose(W_vals, W_um)
        if not np.any(mask):
            continue
        L_sub = L_vals[mask]
        C_sub = Cgg_vals[mask] * 1e15
        order = np.argsort(L_sub)
        plt.plot(L_sub[order], C_sub[order], marker="o", label=f"W={W_um:.1f}um")
    plt.xlabel("L (um)")
    plt.ylabel("Cgg (fF)")
    plt.title(f"Cgg (TRAN) vs L at different W ({pdk_name} NMOS)")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    out_path = plots_dir / "Cgg_vs_L.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"[INFO] Saved plot {out_path}")


if __name__ == "__main__":
    main()
