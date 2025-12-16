import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import argparse


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
    return parser.parse_args()


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

    # Load CSV: columns are L_um, W_um, Cgs_fF, Cgd_fF, Cgb_fF
    data = np.loadtxt(csv_path, delimiter=",", skiprows=1)
    L_vals = data[:, 0]
    W_vals = data[:, 1]
    Cgs_fF = data[:, 2]
    Cgd_fF = data[:, 3]
    Cgb_fF = data[:, 4]

    L_unique = np.unique(L_vals)
    W_unique = np.unique(W_vals)

    caps = {
        "Cgs": Cgs_fF,
        "Cgd": Cgd_fF,
        "Cgb": Cgb_fF,
    }

    # 1) NMOS: 对每个固定 L，拟合 C(W) 的线性关系，评估关于 W 的线性程度
    for cap_name, C_fF in caps.items():
        slopes = []
        intercepts = []
        r2_list = []
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

        slopes = np.array(slopes)
        intercepts = np.array(intercepts)
        r2_arr = np.array(r2_list)

        # 保存线性回归结果到 CSV
        out_csv = results_dir / f"{cap_name}_linfit_C_vs_W_per_L.csv"
        header = "L_um,slope_fF_per_um,intercept_fF,R2"
        out_data = np.column_stack([L_unique, slopes, intercepts, r2_arr])
        np.savetxt(out_csv, out_data, delimiter=",", header=header, comments="")

        # 画 R^2 vs L 曲线
        plt.figure(figsize=(6, 4))
        plt.plot(L_unique, r2_arr, marker="o")
        plt.xlabel("L (um)")
        plt.ylabel("R^2")
        plt.ylim(0.0, 1.05)
        plt.grid(True, linestyle="--", alpha=0.4)
        plt.title(f"Linearity of {cap_name} vs W (R^2 per L)")
        out_png = plots_dir / f"R2_{cap_name}_C_vs_W_over_L.png"
        plt.tight_layout()
        plt.savefig(out_png, dpi=300)
        plt.close()

    # 2) NMOS: 对每个固定 W，拟合 C(L) 的线性关系，评估关于 L 的线性程度
    for cap_name, C_fF in caps.items():
        slopes = []
        intercepts = []
        r2_list = []
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

        slopes = np.array(slopes)
        intercepts = np.array(intercepts)
        r2_arr = np.array(r2_list)

        # 保存线性回归结果到 CSV
        out_csv = results_dir / f"{cap_name}_linfit_C_vs_L_per_W.csv"
        header = "W_um,slope_fF_per_um,intercept_fF,R2"
        out_data = np.column_stack([W_unique, slopes, intercepts, r2_arr])
        np.savetxt(out_csv, out_data, delimiter=",", header=header, comments="")

        # 画 R^2 vs W 曲线
        plt.figure(figsize=(6, 4))
        plt.plot(W_unique, r2_arr, marker="o")
        plt.xlabel("W (um)")
        plt.ylabel("R^2")
        plt.ylim(0.0, 1.05)
        plt.grid(True, linestyle="--", alpha=0.4)
        plt.title(f"Linearity of {cap_name} vs L (R^2 per W)")
        out_png = plots_dir / f"R2_{cap_name}_C_vs_L_over_W.png"
        plt.tight_layout()
        plt.savefig(out_png, dpi=300)
        plt.close()

    # ===== PMOS data (optional) =====
    csv_p_path = results_dir / "cap_vs_LW_pmos.csv"
    if not csv_p_path.exists():
        return

    data_p = np.loadtxt(csv_p_path, delimiter=",", skiprows=1)
    L_vals_p = data_p[:, 0]
    W_vals_p = data_p[:, 1]
    Cgs_p_fF = data_p[:, 2]
    Cgd_p_fF = data_p[:, 3]
    Cgb_p_fF = data_p[:, 4]

    L_unique_p = np.unique(L_vals_p)
    W_unique_p = np.unique(W_vals_p)

    caps_p = {
        "Cgs_p": Cgs_p_fF,
        "Cgd_p": Cgd_p_fF,
        "Cgb_p": Cgb_p_fF,
    }

    # 3) PMOS: C(W) per L
    for cap_name, C_fF in caps_p.items():
        slopes = []
        intercepts = []
        r2_list = []
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

        slopes = np.array(slopes)
        intercepts = np.array(intercepts)
        r2_arr = np.array(r2_list)

        out_csv = results_dir / f"{cap_name}_linfit_C_vs_W_per_L.csv"
        header = "L_um,slope_fF_per_um,intercept_fF,R2"
        out_data = np.column_stack([L_unique_p, slopes, intercepts, r2_arr])
        np.savetxt(out_csv, out_data, delimiter=",", header=header, comments="")

        plt.figure(figsize=(6, 4))
        plt.plot(L_unique_p, r2_arr, marker="o")
        plt.xlabel("L (um)")
        plt.ylabel("R^2")
        plt.ylim(0.0, 1.05)
        plt.grid(True, linestyle="--", alpha=0.4)
        plt.title(f"Linearity of {cap_name} vs W (R^2 per L) [PMOS]")
        out_png = plots_dir / f"R2_{cap_name}_C_vs_W_over_L.png"
        plt.tight_layout()
        plt.savefig(out_png, dpi=300)
        plt.close()

    # 4) PMOS: C(L) per W
    for cap_name, C_fF in caps_p.items():
        slopes = []
        intercepts = []
        r2_list = []
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

        slopes = np.array(slopes)
        intercepts = np.array(intercepts)
        r2_arr = np.array(r2_list)

        out_csv = results_dir / f"{cap_name}_linfit_C_vs_L_per_W.csv"
        header = "W_um,slope_fF_per_um,intercept_fF,R2"
        out_data = np.column_stack([W_unique_p, slopes, intercepts, r2_arr])
        np.savetxt(out_csv, out_data, delimiter=",", header=header, comments="")

        plt.figure(figsize=(6, 4))
        plt.plot(W_unique_p, r2_arr, marker="o")
        plt.xlabel("W (um)")
        plt.ylabel("R^2")
        plt.ylim(0.0, 1.05)
        plt.grid(True, linestyle="--", alpha=0.4)
        plt.title(f"Linearity of {cap_name} vs L (R^2 per W) [PMOS]")
        out_png = plots_dir / f"R2_{cap_name}_C_vs_L_over_W.png"
        plt.tight_layout()
        plt.savefig(out_png, dpi=300)
        plt.close()


if __name__ == "__main__":
    main()
