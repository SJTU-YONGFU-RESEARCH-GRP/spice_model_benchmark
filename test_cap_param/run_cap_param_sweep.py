import subprocess
import textwrap
from pathlib import Path
import shutil
import re
import argparse

import numpy as np
import matplotlib.pyplot as plt


# This script sweeps MOSFET length/width and extracts large-signal
# gate-related capacitances (Cgs, Cgd, Cgb) using the 5.1 endpoint
# charge method defined in docs/mos_large_signal_caps.md.
#
# It generates, for each (L, W):
#   - a small DC netlist that biases a single NMOS_VTG device
#   - runs ngspice in batch mode
#   - reads ls_caps_dc.txt (Vg, Vd, Qg, Qd, Qs, Qb)
#   - computes Cgs/Cgd/Cgb by finite difference -ΔQ/ΔVg
#
# Results are saved in:
#   test_cap_param/results/cap_vs_LW.csv
#   test_cap_param/results/plots/*.png


def generate_netlist_from_template(
    template_path: Path,
    netlist_path: Path,
    L_um: float,
    W_um: float,
    vdd: float = 1.2,
) -> None:
    """Generate a DC netlist by patching freepdk45_dc_circuit.cir for given L, W.

    This reuses the already-working bias analysis and ls_caps_dc.txt writing
    logic based on @M2[qg]/@M2[qd]/..., and only changes the geometry of M2/M3
    and, optionally, rescales DC bias voltages for a different VDD.
    """
    text = template_path.read_text()
    lines = text.splitlines()

    L_str = f"L={L_um:.4f}u"
    W_str = f"W={W_um:.4f}u"

    new_lines = []
    for line in lines:
        # Look for the NMOS bias device line (M2) and replace its L/W
        stripped = line.strip()
        if stripped.startswith("M2 ") and "drain_bias" in stripped and "NMOS_VTG" in stripped:
            indent = line[: len(line) - len(line.lstrip())]
            new_line = (
                f"{indent}M2 drain_bias gate_bias source_bias bulk_bias "
                f"NMOS_VTG {L_str} {W_str}"
            )
            new_lines.append(new_line)
        # Look for the PMOS bias device line (M3) and replace its L/W
        elif stripped.startswith("M3 ") and "drain_pbias" in stripped and "PMOS_VTG" in stripped:
            indent = line[: len(line) - len(line.lstrip())]
            new_line = (
                f"{indent}M3 drain_pbias gate_pbias source_pbias bulk_pbias "
                f"PMOS_VTG {L_str} {W_str}"
            )
            new_lines.append(new_line)
        # Look for the Sky130 NMOS bias device line (X2) and replace its L/W
        elif stripped.startswith("X2 ") and "drain_bias" in stripped and "sky130_fd_pr__nfet_01v8" in stripped:
            indent = line[: len(line) - len(line.lstrip())]
            new_line = (
                f"{indent}X2 drain_bias gate_bias source_bias bulk_bias "
                f"sky130_fd_pr__nfet_01v8 l={L_um:.4f} w={W_um:.4f}"
            )
            new_lines.append(new_line)
        # Look for the Sky130 PMOS bias device line (X3) and replace its L/W
        elif stripped.startswith("X3 ") and "drain_pbias" in stripped and "sky130_fd_pr__pfet_01v8" in stripped:
            indent = line[: len(line) - len(line.lstrip())]
            new_line = (
                f"{indent}X3 drain_pbias gate_pbias source_pbias bulk_pbias "
                f"sky130_fd_pr__pfet_01v8 l={L_um:.4f} w={W_um:.4f}"
            )
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    # Optionally rescale DC bias voltages to emulate a different nominal VDD
    # while preserving the relative bias points (e.g. 0, 0.5*VDD, 1.0*VDD).
    if vdd is not None:
        base_vdd = 1.2
        if base_vdd > 0 and abs(vdd - base_vdd) > 1e-9:
            scale = vdd / base_vdd
            bias_keywords = [
                "Vds_iv",
                "Vgs_iv",
                "Vs_iv",
                "Vb_iv",
                "Vds_bias",
                "Vgs_bias",
                "Vs_bias",
                "Vb_bias",
                "Vdp_pbias",
                "Vgp_pbias",
                "Vsp_pbias",
                "Vbp_pbias",
                "alter Vds_bias",
                "alter Vgs_bias",
                "alter Vdp_pbias",
                "alter Vgp_pbias",
                "alter Vsp_pbias",
                "alter Vbp_pbias",
                "dc Vds_iv",
            ]

            scaled_lines = []
            for line in new_lines:
                stripped = line.strip()
                if not stripped or stripped.startswith(
                    ("*", ".option", ".include", ".inc", ".end", ".control", ".endc")
                ):
                    scaled_lines.append(line)
                    continue

                if not any(key in stripped for key in bias_keywords):
                    scaled_lines.append(line)
                    continue

                def _scale_number(m):
                    try:
                        val = float(m.group(0))
                    except ValueError:
                        return m.group(0)
                    return f"{val * scale:.6g}"

                scaled_line = re.sub(r"([-+]?\d*\.?\d+)", _scale_number, line)
                scaled_lines.append(scaled_line)

            new_lines = scaled_lines

    netlist_path.write_text("\n".join(new_lines) + "\n")


def run_ngspice(netlist_path: Path, cwd: Path = None) -> None:
    """Run ngspice -b on the given netlist, raising on failure.

    The 'netlist_path' may be absolute or relative to 'cwd'. If 'cwd' is not
    provided, the netlist's parent directory is used as the working directory,
    matching the original behavior.
    """
    if cwd is None:
        cwd = netlist_path.parent
    cmd = ["ngspice", "-b", str(netlist_path)]
    result = subprocess.run(
        cmd,
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"ngspice failed for {netlist_path} with code {result.returncode}\n"
            f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )


def read_ls_caps_dc(ls_caps_path: Path):
    """Read ls_caps_dc.txt and return (Vg, Vd, Qg, Qd, Qs, Qb) arrays.

    The file is expected to have a one-line header followed by two or more
    data rows, with whitespace-separated columns:
        Vg Vd Qg Qd Qs Qb
    """
    if not ls_caps_path.exists():
        raise FileNotFoundError(f"ls_caps_dc.txt not found at {ls_caps_path}")

    # Read header to map columns (robust if order changes slightly)
    with ls_caps_path.open("r") as f:
        header = f.readline().strip().split()
    col_map = {name: i for i, name in enumerate(header)}

    required = ["Vg", "Vd", "Qg", "Qd", "Qs", "Qb"]
    missing = [name for name in required if name not in col_map]

    data = np.loadtxt(ls_caps_path, skiprows=1)
    if data.ndim == 1:
        # If only one row, force 2D
        data = data[None, :]

    if data.shape[0] < 2:
        raise ValueError("ls_caps_dc.txt has fewer than two bias points")
    if not missing:
        # All required names are present, use header-based mapping
        vg = data[:, col_map["Vg"]]
        vd = data[:, col_map["Vd"]]
        qg = data[:, col_map["Qg"]]
        qd = data[:, col_map["Qd"]]
        qs = data[:, col_map["Qs"]]
        qb = data[:, col_map["Qb"]]
    else:
        # Fallback: header does not contain the canonical names, but if we
        # have at least 6 numeric columns, interpret the first six as
        # (Vg, Vd, Qg, Qd, Qs, Qb). This is mainly for PDK templates that
        # use wrdata directly on vectors like v(gate_bias) and @M[...] where
        # the column names are implementation-dependent.
        if data.shape[1] < 6:
            raise ValueError(
                f"ls_caps_dc.txt has only {data.shape[1]} columns and is missing "
                f"required names {missing}. Header: {header}"
            )
        vg = data[:, 0]
        vd = data[:, 1]
        qg = data[:, 2]
        qd = data[:, 3]
        qs = data[:, 4]
        qb = data[:, 5]

    return vg, vd, qg, qd, qs, qb


def compute_caps_from_endpoint(vg, qd, qs, qb):
    """Compute (Cgs, Cgd, Cgb) from endpoint charges using -ΔQ/ΔVg.

    Uses the first and last points in vg as (Vg1, Vg2).
    """
    i_start = 0
    i_end = len(vg) - 1
    dv = vg[i_end] - vg[i_start]
    if abs(dv) <= 0.0:
        raise ValueError("ΔVg is zero; cannot compute large-signal capacitances")

    cgs = -(qs[i_end] - qs[i_start]) / dv
    cgd = -(qd[i_end] - qd[i_start]) / dv
    cgb = -(qb[i_end] - qb[i_start]) / dv
    return cgs, cgd, cgb


def parse_args():
    """Parse command-line arguments for multi-PDK capacitance sweep."""
    parser = argparse.ArgumentParser(
        description=(
            "Sweep MOS L/W and extract large-signal gate-related capacitances "
            "(Cgs, Cgd, Cgb) using DC endpoint charge method (5.1) for a given PDK."
        )
    )
    parser.add_argument(
        "--pdk",
        default="FreePDK45",
        help="PDK name used in plot titles and generated netlist names (default: FreePDK45)",
    )
    parser.add_argument(
        "--dc-netlist",
        dest="dc_netlist",
        default=None,
        help=(
            "Path to the base DC bias/charge-extraction netlist template. "
            "If not provided, defaults to netlists/freepdk45_dc_circuit.cir. "
            "The template must write ls_caps_dc.txt and ls_caps_dc_pmos.txt."
        ),
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
            "Nominal supply voltage in volts used for the DC bias points. "
            "The default 1.2 V matches the reference netlists. When changed, "
            "DC source levels in the generated netlists are scaled so that "
            "their ratios to VDD are preserved."
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

    # NMOS and PMOS records: each entry is (L_um, W_um, Cgs, Cgd, Cgb)
    records_nmos = []
    records_pmos = []
    # Keep track of points that failed (either ngspice or post-processing)
    failed_points = []  # (L_um, W_um, stage, message)
    # Points for which we already have valid NMOS+PMOS results from previous runs
    existing_points = set()  # keys are (round(L_um, 3), round(W_um, 1))

    # Determine template netlist for the selected PDK. Templates live in the
    # top-level netlists directory (or at an explicit path), not in the
    # per-PDK generated netlist directory.
    if args.dc_netlist is not None:
        template_path = Path(args.dc_netlist).resolve()
    else:
        template_path = base_netlists_dir / "freepdk45_dc_circuit.cir"

    template_stem = template_path.stem

    # Try to reuse existing results from previous runs (incremental mode).
    # We only reuse points that exist in both NMOS and PMOS CSVs.
    nmos_map = {}
    pmos_map = {}

    if not args.fresh:
        csv_n_path = results_dir / "cap_vs_LW.csv"
        if csv_n_path.exists():
            try:
                data_n_prev = np.loadtxt(csv_n_path, delimiter=",", skiprows=1)
                if data_n_prev.ndim == 1:
                    data_n_prev = data_n_prev[None, :]
                for row in data_n_prev:
                    L_prev, W_prev, Cgs_fF_prev, Cgd_fF_prev, Cgb_fF_prev = row
                    key = (round(L_prev, 3), round(W_prev, 1))
                    nmos_map[key] = (
                        L_prev,
                        W_prev,
                        Cgs_fF_prev * 1e-15,
                        Cgd_fF_prev * 1e-15,
                        Cgb_fF_prev * 1e-15,
                    )
                print(
                    f"[INFO] Found existing NMOS CSV {csv_n_path} with "
                    f"{len(nmos_map)} points"
                )
            except Exception as e:
                print(f"[WARN] Failed to load existing NMOS CSV {csv_n_path}: {e}")

        csv_p_path = results_dir / "cap_vs_LW_pmos.csv"
        if csv_p_path.exists():
            try:
                data_p_prev = np.loadtxt(csv_p_path, delimiter=",", skiprows=1)
                if data_p_prev.ndim == 1:
                    data_p_prev = data_p_prev[None, :]
                for row in data_p_prev:
                    L_prev, W_prev, Cgs_p_fF_prev, Cgd_p_fF_prev, Cgb_p_fF_prev = row
                    key = (round(L_prev, 3), round(W_prev, 1))
                    pmos_map[key] = (
                        L_prev,
                        W_prev,
                        Cgs_p_fF_prev * 1e-15,
                        Cgd_p_fF_prev * 1e-15,
                        Cgb_p_fF_prev * 1e-15,
                    )
                print(
                    f"[INFO] Found existing PMOS CSV {csv_p_path} with "
                    f"{len(pmos_map)} points"
                )
            except Exception as e:
                print(f"[WARN] Failed to load existing PMOS CSV {csv_p_path}: {e}")

        # Reuse only points that are present in both NMOS and PMOS maps.
        if nmos_map and pmos_map:
            existing_points = set(nmos_map.keys()) & set(pmos_map.keys())
            for key in sorted(existing_points):
                records_nmos.append(nmos_map[key])
                records_pmos.append(pmos_map[key])
            if existing_points:
                print(
                    f"[INFO] Reusing {len(existing_points)} existing (L,W) points "
                    f"from previous CSVs."
                )

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

            if netlist_path.exists():
                print(
                    f"[INFO] Netlist {netlist_name} already exists; "
                    f"skipping generation and reusing it."
                )
            else:
                print(
                    f"[INFO] Generating netlist for L={L_um}um, W={W_um}um -> {netlist_name}"
                )
                generate_netlist_from_template(
                    template_path,
                    netlist_path,
                    L_um,
                    W_um,
                    vdd=vdd,
                )

            print(f"[INFO] Running ngspice for {netlist_name}")
            # Run ngspice from the top-level netlists directory so that
            # relative .include "../models/..." and wrdata paths match the
            # original layout, even though the generated netlists live in a
            # per-PDK subdirectory.
            try:
                netlist_rel = netlist_path.relative_to(base_netlists_dir)
                run_ngspice(netlist_rel, cwd=base_netlists_dir)
            except Exception as e:  # ngspice failure
                msg = str(e)
                print(
                    f"[WARN] ngspice failed for L={L_um}um, W={W_um}um: {msg}\n"
                    f"       Skipping this point and continuing."
                )
                failed_points.append((L_um, W_um, "ngspice", msg))
                continue

            # Post-processing: read NMOS/PMOS charges and compute caps.
            try:
                # NMOS charges (wrdata writes relative to the ngspice working
                # directory, which is the top-level netlists directory).
                ls_caps_path = base_netlists_dir / "ls_caps_dc.txt"
                print(f"[INFO] Reading NMOS charges from {ls_caps_path}")
                vg, vd, qg, qd, qs, qb = read_ls_caps_dc(ls_caps_path)

                cgs, cgd, cgb = compute_caps_from_endpoint(vg, qd, qs, qb)
                records_nmos.append((L_um, W_um, cgs, cgd, cgb))

                # PMOS charges
                ls_caps_p_path = base_netlists_dir / "ls_caps_dc_pmos.txt"
                print(f"[INFO] Reading PMOS charges from {ls_caps_p_path}")
                vg_p, vd_p, qg_p, qd_p, qs_p, qb_p = read_ls_caps_dc(ls_caps_p_path)

                cgs_p, cgd_p, cgb_p = compute_caps_from_endpoint(
                    vg_p, qd_p, qs_p, qb_p
                )
                records_pmos.append((L_um, W_um, cgs_p, cgd_p, cgb_p))
            except Exception as e:  # data reading or capacitance computation failure
                msg = str(e)
                print(
                    f"[WARN] Post-processing failed for L={L_um}um, W={W_um}um: {msg}\n"
                    f"       Skipping this point and continuing."
                )
                failed_points.append((L_um, W_um, "post", msg))
                continue

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

    # Convert to numpy arrays for easier processing (NMOS)
    if records_nmos:
        data_n = np.array(records_nmos)
        L_vals = data_n[:, 0]
        W_vals = data_n[:, 1]
        Cgs_vals = data_n[:, 2]
        Cgd_vals = data_n[:, 3]
        Cgb_vals = data_n[:, 4]
    else:
        print("[WARN] No successful NMOS points collected; skipping NMOS outputs.")
        return

    # Convert to numpy arrays for easier processing (PMOS)
    if records_pmos:
        data_p = np.array(records_pmos)
        L_vals_p = data_p[:, 0]
        W_vals_p = data_p[:, 1]
        Cgs_p_vals = data_p[:, 2]
        Cgd_p_vals = data_p[:, 3]
        Cgb_p_vals = data_p[:, 4]
    else:
        print("[WARN] No successful PMOS points collected; skipping PMOS outputs.")
        return

    # Save NMOS CSV in fF for convenience
    csv_path = results_dir / "cap_vs_LW.csv"
    header = "L_um,W_um,Cgs_fF,Cgd_fF,Cgb_fF"
    arr_to_save = np.column_stack([
        L_vals,
        W_vals,
        Cgs_vals * 1e15,
        Cgd_vals * 1e15,
        Cgb_vals * 1e15,
    ])
    np.savetxt(csv_path, arr_to_save, delimiter=",", header=header, comments="")
    print(f"[INFO] Saved NMOS sweep data to {csv_path}")

    # Save PMOS CSV in fF for convenience
    csv_p_path = results_dir / "cap_vs_LW_pmos.csv"
    header_p = "L_um,W_um,Cgs_p_fF,Cgd_p_fF,Cgb_p_fF"
    arr_to_save_p = np.column_stack([
        L_vals_p,
        W_vals_p,
        Cgs_p_vals * 1e15,
        Cgd_p_vals * 1e15,
        Cgb_p_vals * 1e15,
    ])
    np.savetxt(csv_p_path, arr_to_save_p, delimiter=",", header=header_p, comments="")
    print(f"[INFO] Saved PMOS sweep data to {csv_p_path}")

    # Plot NMOS C vs W for several L
    for cap_name, cap_vals in [("Cgs", Cgs_vals), ("Cgd", Cgd_vals), ("Cgb", Cgb_vals)]:
        plt.figure(figsize=(6, 4))
        for L_um in L_list_um:
            mask = np.isclose(L_vals, L_um)
            if not np.any(mask):
                continue
            W_sub = W_vals[mask]
            C_sub = cap_vals[mask] * 1e15  # fF
            order = np.argsort(W_sub)
            W_sub = W_sub[order]
            C_sub = C_sub[order]
            plt.plot(W_sub, C_sub, marker="o", label=f"L={L_um:.3f}um")

        plt.xlabel("W (um)")
        plt.ylabel(f"{cap_name} (fF)")
        plt.title(f"{cap_name} vs W at different L ({pdk_name} NMOS)")
        plt.grid(True, linestyle="--", alpha=0.4)
        plt.legend()
        out_path = plots_dir / f"{cap_name}_vs_W.png"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        plt.tight_layout()
        plt.savefig(out_path, dpi=300)
        plt.close()
        print(f"[INFO] Saved plot {out_path}")

    # Plot PMOS C vs W for several L
    for cap_name, cap_vals in [("Cgs_p", Cgs_p_vals), ("Cgd_p", Cgd_p_vals), ("Cgb_p", Cgb_p_vals)]:
        plt.figure(figsize=(6, 4))
        for L_um in L_list_um:
            mask = np.isclose(L_vals_p, L_um)
            if not np.any(mask):
                continue
            W_sub = W_vals_p[mask]
            C_sub = cap_vals[mask] * 1e15  # fF
            order = np.argsort(W_sub)
            W_sub = W_sub[order]
            C_sub = C_sub[order]
            plt.plot(W_sub, C_sub, marker="o", label=f"L={L_um:.3f}um")

        plt.xlabel("W (um)")
        plt.ylabel(f"{cap_name} (fF)")
        plt.title(f"{cap_name} vs W at different L ({pdk_name} PMOS)")
        plt.grid(True, linestyle="--", alpha=0.4)
        plt.legend()
        out_path = plots_dir / f"{cap_name}_vs_W_pmos.png"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        plt.tight_layout()
        plt.savefig(out_path, dpi=300)
        plt.close()
        print(f"[INFO] Saved plot {out_path}")

    # Plot PMOS C vs L for several W
    for cap_name, cap_vals in [("Cgs_p", Cgs_p_vals), ("Cgd_p", Cgd_p_vals), ("Cgb_p", Cgb_p_vals)]:
        plt.figure(figsize=(6, 4))
        for W_um in W_list_um:
            mask = np.isclose(W_vals_p, W_um)
            if not np.any(mask):
                continue
            L_sub = L_vals_p[mask]
            C_sub = cap_vals[mask] * 1e15  # fF
            order = np.argsort(L_sub)
            L_sub = L_sub[order]
            C_sub = C_sub[order]
            plt.plot(L_sub, C_sub, marker="o", label=f"W={W_um:.1f}um")

        plt.xlabel("L (um)")
        plt.ylabel(f"{cap_name} (fF)")
        plt.title(f"{cap_name} vs L at different W ({pdk_name} PMOS)")
        plt.grid(True, linestyle="--", alpha=0.4)
        plt.legend()
        out_path = plots_dir / f"{cap_name}_vs_L_pmos.png"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        plt.tight_layout()
        plt.savefig(out_path, dpi=300)
        plt.close()
        print(f"[INFO] Saved plot {out_path}")

    # Plot NMOS C vs L for several W
    for cap_name, cap_vals in [("Cgs", Cgs_vals), ("Cgd", Cgd_vals), ("Cgb", Cgb_vals)]:
        plt.figure(figsize=(6, 4))
        for W_um in W_list_um:
            mask = np.isclose(W_vals, W_um)
            if not np.any(mask):
                continue
            L_sub = L_vals[mask]
            C_sub = cap_vals[mask] * 1e15  # fF
            order = np.argsort(L_sub)
            L_sub = L_sub[order]
            C_sub = C_sub[order]
            plt.plot(L_sub, C_sub, marker="o", label=f"W={W_um:.1f}um")

        plt.xlabel("L (um)")
        plt.ylabel(f"{cap_name} (fF)")
        plt.title(f"{cap_name} vs L at different W ({pdk_name} NMOS)")
        plt.grid(True, linestyle="--", alpha=0.4)
        plt.legend()
        out_path = plots_dir / f"{cap_name}_vs_L.png"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        plt.tight_layout()
        plt.savefig(out_path, dpi=300)
        plt.close()
        print(f"[INFO] Saved plot {out_path}")


if __name__ == "__main__":
    main()
