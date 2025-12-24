#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

try:
    import pandas as pd
except Exception:  # pragma: no cover
    pd = None


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from spice_model_benchmark import benchmark_spice_model  # noqa: E402


@dataclass(frozen=True)
class RunResult:
    sweep: str  # "W" or "L"
    w: str
    l: str
    out_dir: Path
    vg: np.ndarray
    cgg_f: np.ndarray
    ls_caps_f: Dict[str, float]


def _parse_csv_list(s: str) -> List[str]:
    items = [x.strip() for x in s.split(",")]
    return [x for x in items if x]


_SPICE_MULTIPLIERS: Dict[str, float] = {
    "f": 1e-15,
    "p": 1e-12,
    "n": 1e-9,
    "u": 1e-6,
    "m": 1e-3,
    "k": 1e3,
    "meg": 1e6,
    "g": 1e9,
    "t": 1e12,
}


def _parse_spice_number(s: str) -> float:
    """Parse a SPICE-style number with optional suffix (e.g., 10u, 0.045u, 1e-6).

    Notes:
    - 'm' is milli (1e-3). Use 'meg' for mega (1e6).
    """

    raw = s.strip()
    m = re.match(r"^([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)\s*([a-zA-Z]+)?$", raw)
    if not m:
        raise ValueError(f"Cannot parse SPICE number: {s!r}")
    base = float(m.group(1))
    suf = (m.group(2) or "").strip().lower()
    if not suf:
        return base
    if suf not in _SPICE_MULTIPLIERS:
        raise ValueError(f"Unknown SPICE suffix {suf!r} in {s!r}")
    return base * _SPICE_MULTIPLIERS[suf]


def _sanitize_token(s: str) -> str:
    # Make a filesystem-friendly token.
    s = s.strip()
    s = s.replace("/", "_")
    s = s.replace(" ", "")
    s = s.replace(".", "p")
    return re.sub(r"[^a-zA-Z0-9_\-]+", "", s)


def _patch_ac_netlist_wl(template_text: str, w: str, l: str) -> str:
    """Patch all MOS instances in an AC netlist to use given W/L.

    We conservatively rewrite only lines that:
    - start with 'M' (SPICE MOS instance)
    - contain both 'L=' and 'W='
    """

    out_lines: List[str] = []
    l_re = re.compile(r"\bL\s*=\s*[^\s]+")
    w_re = re.compile(r"\bW\s*=\s*[^\s]+")

    for line in template_text.splitlines(True):
        s = line.lstrip()
        if s.startswith("M") and ("L=" in line or "L =" in line) and ("W=" in line or "W =" in line):
            line = l_re.sub(f"L={l}", line)
            line = w_re.sub(f"W={w}", line)
        out_lines.append(line)
    return "".join(out_lines)


def _absolutize_spice_includes(netlist_text: str, *, base_dir: Path) -> str:
    """Rewrite relative .inc/.include/.lib paths to absolute paths.

    When we copy a netlist into a run directory, ngspice executes with cwd set
    to that run directory. Any relative include paths in the original template
    (which assumed cwd=netlists/) must be rewritten.
    """

    def _rewrite_path_token(tok: str) -> str:
        raw = tok.strip()
        if not raw:
            return tok
        quote = ""
        if (raw.startswith("'") and raw.endswith("'")) or (raw.startswith('"') and raw.endswith('"')):
            quote = raw[0]
            raw = raw[1:-1]
        p = Path(raw)
        if not p.is_absolute():
            p = (base_dir / p).resolve()
        new_raw = p.as_posix()
        return f"{quote}{new_raw}{quote}" if quote else new_raw

    out_lines: List[str] = []
    for line in netlist_text.splitlines(True):
        stripped = line.strip()
        lower = stripped.lower()
        if lower.startswith(".inc") or lower.startswith(".include"):
            parts = line.split()
            if len(parts) >= 2:
                parts[1] = _rewrite_path_token(parts[1])
                line = " ".join(parts) + ("\n" if not line.endswith("\n") else "")
        elif lower.startswith(".lib"):
            parts = line.split()
            if len(parts) >= 2:
                parts[1] = _rewrite_path_token(parts[1])
                line = " ".join(parts) + ("\n" if not line.endswith("\n") else "")
        out_lines.append(line)
    return "".join(out_lines)


def _read_cv_cgg_1mhz(out_dir: Path) -> Tuple[np.ndarray, np.ndarray]:
    cv_path = out_dir / "data" / "cv_data.txt"
    if not cv_path.exists():
        raise FileNotFoundError(f"cv_data.txt not found: {cv_path}")

    if pd is None:
        arr = np.genfromtxt(cv_path, names=True, dtype=float, encoding=None)
        vg = np.atleast_1d(arr["Vg"]).astype(float)
        cgg = np.atleast_1d(arr["Cgg_1MHz"]).astype(float)
        return vg, cgg

    df = pd.read_csv(cv_path, delim_whitespace=True)
    if "Vg" not in df.columns or "Cgg_1MHz" not in df.columns:
        raise ValueError(f"Unexpected cv_data.txt columns: {list(df.columns)}")
    vg = df["Vg"].to_numpy(dtype=float)
    cgg = df["Cgg_1MHz"].to_numpy(dtype=float)
    return vg, cgg


def _read_ls_caps(out_dir: Path) -> Dict[str, float]:
    ls_path = out_dir / "data" / "ac_ls_caps_from_cv_integral.csv"
    if not ls_path.exists():
        raise FileNotFoundError(f"ac_ls_caps_from_cv_integral.csv not found: {ls_path}")

    ls_caps: Dict[str, float] = {}
    if pd is None:
        # Fallback CSV parsing
        with open(ls_path, "r", encoding="utf-8") as f:
            header = f.readline().strip().split(",")
            if header[:2] != ["cap", "ac_int_F"]:
                raise ValueError(f"Unexpected header in {ls_path}: {header}")
            for line in f:
                parts = line.strip().split(",")
                if len(parts) < 2:
                    continue
                cap = parts[0]
                try:
                    val = float(parts[1])
                except Exception:
                    continue
                if cap in {"Cgg", "Cgs", "Cgd", "Cgb"}:
                    ls_caps[cap] = val
        return ls_caps

    df = pd.read_csv(ls_path)
    for _, row in df.iterrows():
        cap = str(row.get("cap", ""))
        if cap in {"Cgg", "Cgs", "Cgd", "Cgb"}:
            try:
                ls_caps[cap] = float(row["ac_int_F"])
            except Exception:
                pass
    return ls_caps


def _run_one_ac(
    ac_template_path: Path,
    spiceinit_path: Optional[Path],
    output_root: Path,
    sweep: str,
    w: str,
    l: str,
) -> RunResult:
    run_name = f"{sweep}_sweep__W_{_sanitize_token(w)}__L_{_sanitize_token(l)}"
    out_dir = output_root / "runs" / run_name
    out_dir.mkdir(parents=True, exist_ok=True)

    # Generate a runnable AC netlist in the run directory.
    tpl = ac_template_path.read_text(encoding="utf-8", errors="ignore")
    patched = _patch_ac_netlist_wl(tpl, w=w, l=l)
    patched = _absolutize_spice_includes(patched, base_dir=ac_template_path.parent)
    run_ac_netlist = out_dir / "ac_circuit.cir"
    run_ac_netlist.write_text(patched, encoding="utf-8")

    # Ensure ngspice picks up .spiceinit when SimulationRunner chdir()s into out_dir.
    if spiceinit_path is not None and spiceinit_path.exists():
        (out_dir / ".spiceinit").write_text(
            spiceinit_path.read_text(encoding="utf-8", errors="ignore"),
            encoding="utf-8",
        )

    # NOTE: current benchmark_spice_model signature requires model_file but it is
    # not used by MOSFETSimulation; pass an existing repo file.
    dummy_model = REPO_ROOT / "netlists" / "sky130.spice"
    if not dummy_model.exists():
        dummy_model = REPO_ROOT / "README.md"

    ok = benchmark_spice_model(
        model_file=str(dummy_model),
        output_dir=str(out_dir),
        modes=["ac"],
        ac_circuit=str(run_ac_netlist),
    )
    if not ok:
        raise RuntimeError(f"AC run failed for W={w}, L={l}. See: {out_dir}")

    vg, cgg = _read_cv_cgg_1mhz(out_dir)
    order = np.argsort(vg)
    vg = vg[order]
    cgg = cgg[order]

    ls_caps = _read_ls_caps(out_dir)

    return RunResult(
        sweep=sweep,
        w=w,
        l=l,
        out_dir=out_dir,
        vg=vg,
        cgg_f=cgg,
        ls_caps_f=ls_caps,
    )


def _plot_cv_overlay(results: List[RunResult], out_path: Path, title: str) -> None:
    plt.figure(figsize=(7.5, 5.0))
    for r in results:
        label = f"W={r.w}, L={r.l}"
        plt.plot(r.vg, r.cgg_f * 1e15, linewidth=1.8, label=label)

    plt.xlabel("Vg (V)")
    plt.ylabel("Cgg@1MHz (fF)")
    plt.title(title)
    plt.grid(True, alpha=0.3)
    if len(results) <= 12:
        plt.legend(fontsize=8)
    else:
        plt.legend(fontsize=6, ncol=2)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


def _write_summary_csv(rows: List[RunResult], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("sweep,W,L,Cgg_ls_F,Cgs_ls_F,Cgd_ls_F,Cgb_ls_F,Cgg_ls_fF,Cgs_ls_fF,Cgd_ls_fF,Cgb_ls_fF,out_dir\n")
        for r in rows:
            def g(name: str) -> float:
                return float(r.ls_caps_f.get(name, float("nan")))

            cgg = g("Cgg")
            cgs = g("Cgs")
            cgd = g("Cgd")
            cgb = g("Cgb")
            f.write(
                f"{r.sweep},{r.w},{r.l},"
                f"{cgg:.16g},{cgs:.16g},{cgd:.16g},{cgb:.16g},"
                f"{cgg*1e15:.12g},{cgs*1e15:.12g},{cgd*1e15:.12g},{cgb*1e15:.12g},"
                f"{r.out_dir.as_posix()}\n"
            )


def _plot_ls_caps_stats(
    w_results: List[RunResult],
    l_results: List[RunResult],
    out_path: Path,
) -> None:
    # Grouped bar chart for (Cgg,Cgs,Cgd,Cgb) across W sweep and L sweep.
    caps = ["Cgg", "Cgs", "Cgd", "Cgb"]

    def vals(rs: List[RunResult], cap: str) -> np.ndarray:
        v = []
        for r in rs:
            v.append(float(r.ls_caps_f.get(cap, float("nan"))) * 1e15)
        return np.array(v, dtype=float)

    fig, axes = plt.subplots(2, 1, figsize=(10.5, 7.0), sharey=True)

    for ax, rs, xlab, title in [
        (axes[0], w_results, "W", "Large-signal caps (AC integral) vs W"),
        (axes[1], l_results, "L", "Large-signal caps (AC integral) vs L"),
    ]:
        if not rs:
            ax.axis("off")
            continue

        xlabels = [r.w if xlab == "W" else r.l for r in rs]
        x = np.arange(len(xlabels), dtype=float)
        width = 0.18

        for i, cap in enumerate(caps):
            ax.bar(
                x + (i - 1.5) * width,
                vals(rs, cap),
                width=width,
                label=cap,
            )

        ax.set_xticks(x)
        ax.set_xticklabels(xlabels, rotation=0)
        ax.set_ylabel("LS cap (fF)")
        ax.set_title(title)
        ax.grid(True, axis="y", alpha=0.3)
        ax.legend(ncol=4, fontsize=9)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close(fig)


def _plot_ls_caps_stats_grid(
    results: List[RunResult],
    out_path: Path,
) -> None:
    """Grouped bar chart across all (W,L) points.

    X-axis is each (W,L) combination; bars are {Cgg,Cgs,Cgd,Cgb}.
    This can get crowded for 20 points, so we rotate labels.
    """

    if not results:
        return

    caps = ["Cgg", "Cgs", "Cgd", "Cgb"]

    def vals(rs: List[RunResult], cap: str) -> np.ndarray:
        v = []
        for r in rs:
            v.append(float(r.ls_caps_f.get(cap, float("nan"))) * 1e15)
        return np.array(v, dtype=float)

    fig, ax = plt.subplots(1, 1, figsize=(12.5, 5.5))
    xlabels = [f"W={r.w}\nL={r.l}" for r in results]
    x = np.arange(len(xlabels), dtype=float)
    width = 0.18

    for i, cap in enumerate(caps):
        ax.bar(
            x + (i - 1.5) * width,
            vals(results, cap),
            width=width,
            label=cap,
        )

    ax.set_xticks(x)
    ax.set_xticklabels(xlabels, rotation=90, fontsize=8)
    ax.set_ylabel("LS cap (fF)")
    ax.set_title("Large-signal caps (AC integral) across (W, L) grid")
    ax.grid(True, axis="y", alpha=0.3)
    ax.legend(ncol=4, fontsize=9)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close(fig)


def _pearson_r(x: np.ndarray, y: np.ndarray) -> float:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    x = x[mask]
    y = y[mask]
    if x.size < 2:
        return float("nan")
    xs = float(np.std(x))
    ys = float(np.std(y))
    if xs == 0.0 or ys == 0.0:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


def _linear_fit_r2(X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, float, np.ndarray]:
    """Fit y ~= [1, X] * beta, return (beta, R^2, yhat)."""
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    mask = np.isfinite(y)
    for j in range(X.shape[1]):
        mask &= np.isfinite(X[:, j])
    X = X[mask]
    y = y[mask]
    if y.size < 2:
        beta = np.full(X.shape[1] + 1, float("nan"), dtype=float)
        return beta, float("nan"), np.full(y.size, float("nan"), dtype=float)

    A = np.concatenate([np.ones((X.shape[0], 1), dtype=float), X], axis=1)
    beta, *_ = np.linalg.lstsq(A, y, rcond=None)
    yhat = A @ beta
    sse = float(np.sum((y - yhat) ** 2))
    sst = float(np.sum((y - float(np.mean(y))) ** 2))
    r2 = float("nan") if sst == 0.0 else float(1.0 - sse / sst)
    return beta.astype(float), r2, yhat


def _analyze_cgg_ls_linearity(rows: List[RunResult], output_root: Path) -> None:
    """Analyze linear correlation of large-signal Cgg with W, L, and area.

    Outputs:
    - output_root/cgg_ls_linearity.md
    - output_root/plots/cgg_ls_vs_w.png
    - output_root/plots/cgg_ls_vs_l.png
    - output_root/plots/cgg_ls_vs_area.png
    """

    if not rows:
        return

    # Use convenient units for analysis/plots
    w_um = np.array([_parse_spice_number(r.w) * 1e6 for r in rows], dtype=float)
    l_um = np.array([_parse_spice_number(r.l) * 1e6 for r in rows], dtype=float)
    area_um2 = w_um * l_um

    y_fF = np.array([float(r.ls_caps_f.get("Cgg", float("nan"))) * 1e15 for r in rows], dtype=float)

    plots_dir = output_root / "plots"
    plots_dir.mkdir(parents=True, exist_ok=True)

    r_w = _pearson_r(w_um, y_fF)
    r_l = _pearson_r(l_um, y_fF)
    r_a = _pearson_r(area_um2, y_fF)

    beta_a, r2_a, _ = _linear_fit_r2(area_um2, y_fF)  # y = b0 + b1*A
    beta_w, r2_w, _ = _linear_fit_r2(w_um, y_fF)      # y = b0 + b1*W
    beta_l, r2_l, _ = _linear_fit_r2(l_um, y_fF)      # y = b0 + b1*L

    # Physically-motivated: y = b0 + b1*A + b2*W
    beta_aw, r2_aw, _ = _linear_fit_r2(np.column_stack([area_um2, w_um]), y_fF)
    # Slightly richer: y = b0 + b1*A + b2*W + b3*L
    beta_awl, r2_awl, _ = _linear_fit_r2(np.column_stack([area_um2, w_um, l_um]), y_fF)

    def _scatter_with_fit(x: np.ndarray, y: np.ndarray, beta: np.ndarray, xlabel: str, title: str, out_path: Path) -> None:
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)
        mask = np.isfinite(x) & np.isfinite(y)
        x = x[mask]
        y = y[mask]
        if x.size == 0:
            return

        xs = np.linspace(float(np.min(x)), float(np.max(x)), 200)
        ys = beta[0] + beta[1] * xs

        plt.figure(figsize=(7.5, 5.0))
        plt.scatter(x, y, s=35, alpha=0.85)
        plt.plot(xs, ys, linewidth=2.0)
        plt.xlabel(xlabel)
        plt.ylabel("Cgg_ls (fF)")
        plt.title(title)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(out_path, dpi=200)
        plt.close()

    _scatter_with_fit(
        w_um,
        y_fF,
        beta_w,
        xlabel="W (µm)",
        title=f"Cgg_ls vs W (linear fit, R²={r2_w:.4f})",
        out_path=plots_dir / "cgg_ls_vs_w.png",
    )
    _scatter_with_fit(
        l_um,
        y_fF,
        beta_l,
        xlabel="L (µm)",
        title=f"Cgg_ls vs L (linear fit, R²={r2_l:.4f})",
        out_path=plots_dir / "cgg_ls_vs_l.png",
    )
    _scatter_with_fit(
        area_um2,
        y_fF,
        beta_a,
        xlabel="Area W·L (µm²)",
        title=f"Cgg_ls vs Area (linear fit, R²={r2_a:.4f})",
        out_path=plots_dir / "cgg_ls_vs_area.png",
    )

    report = output_root / "cgg_ls_linearity.md"
    uniq_w = sorted({r.w for r in rows})
    uniq_l = sorted({r.l for r in rows})
    with open(report, "w", encoding="utf-8") as f:
        f.write("# Cgg_ls 线性相关分析\n\n")
        f.write(f"点数: {len(rows)}\n\n")
        f.write(f"W 取值数: {len(uniq_w)}（{', '.join(uniq_w)}）\n\n")
        f.write(f"L 取值数: {len(uniq_l)}（{', '.join(uniq_l)}）\n\n")

        f.write("## Pearson 线性相关系数 r\n\n")
        f.write(f"- r(Cgg_ls, W): {r_w:.6f}\n")
        f.write(f"- r(Cgg_ls, L): {r_l:.6f}\n")
        f.write(f"- r(Cgg_ls, W·L): {r_a:.6f}\n\n")

        f.write("## 线性回归 (R²)\n\n")
        f.write("单位：Cgg_ls 用 fF，W/L 用 µm，面积用 µm²。\n\n")

        f.write(f"- 模型A: Cgg = b0 + b1·(W·L)\n")
        f.write(f"  - R² = {r2_a:.6f}, b0={beta_a[0]:.6g}, b1={beta_a[1]:.6g} (fF/µm²)\n")
        f.write(f"- 模型W: Cgg = b0 + b1·W\n")
        f.write(f"  - R² = {r2_w:.6f}, b0={beta_w[0]:.6g}, b1={beta_w[1]:.6g} (fF/µm)\n")
        f.write(f"- 模型L: Cgg = b0 + b1·L\n")
        f.write(f"  - R² = {r2_l:.6f}, b0={beta_l[0]:.6g}, b1={beta_l[1]:.6g} (fF/µm)\n")

        f.write(f"- 模型AW: Cgg = b0 + b1·(W·L) + b2·W\n")
        f.write(
            f"  - R² = {r2_aw:.6f}, b0={beta_aw[0]:.6g}, b1={beta_aw[1]:.6g} (fF/µm²), b2={beta_aw[2]:.6g} (fF/µm)\n"
        )
        f.write(f"- 模型AWL: Cgg = b0 + b1·(W·L) + b2·W + b3·L\n")
        f.write(
            f"  - R² = {r2_awl:.6f}, b0={beta_awl[0]:.6g}, b1={beta_awl[1]:.6g} (fF/µm²), b2={beta_awl[2]:.6g} (fF/µm), b3={beta_awl[3]:.6g} (fF/µm)\n"
        )

        f.write("\n## 输出文件\n\n")
        f.write("- plots/cgg_ls_vs_w.png\n")
        f.write("- plots/cgg_ls_vs_l.png\n")
        f.write("- plots/cgg_ls_vs_area.png\n")


def main() -> int:
    ap = argparse.ArgumentParser(
        description="FreePDK45 W/L sweep for AC C-V curves and large-signal caps (AC-integral)."
    )
    ap.add_argument(
        "--ac-template",
        type=str,
        default=str(REPO_ROOT / "netlists" / "ac_circuit.cir"),
        help="AC netlist template to patch W/L (default: netlists/ac_circuit.cir)",
    )
    ap.add_argument(
        "--spiceinit",
        type=str,
        default=str(REPO_ROOT / "netlists" / ".spiceinit"),
        help=".spiceinit to copy into each run directory (default: netlists/.spiceinit)",
    )
    ap.add_argument(
        "--output-root",
        type=str,
        default=str(REPO_ROOT / "tmp_wl_sweep_cv"),
        help="Output root directory (will create runs/ and plots/)",
    )
    ap.add_argument(
        "--grid",
        action="store_true",
        help="Run full W×L grid (all combinations) instead of separate W-sweep/L-sweep.",
    )
    ap.add_argument(
        "--w-list",
        type=str,
        default="5u,10u,20u",
        help="Comma-separated W list for W-sweep (example: 5u,10u,20u)",
    )
    ap.add_argument(
        "--l-list",
        type=str,
        default="0.045u,0.09u,0.18u",
        help="Comma-separated L list for L-sweep (example: 0.045u,0.09u)",
    )
    ap.add_argument(
        "--fixed-w",
        type=str,
        default=None,
        help="Fixed W for L-sweep (default: uses base config variables.W)",
    )
    ap.add_argument(
        "--fixed-l",
        type=str,
        default=None,
        help="Fixed L for W-sweep (default: uses base config variables.L)",
    )

    args = ap.parse_args()

    ac_template_path = Path(args.ac_template)
    if not ac_template_path.exists():
        raise FileNotFoundError(f"AC template not found: {ac_template_path}")

    spiceinit_path = Path(args.spiceinit) if args.spiceinit else None
    output_root = Path(args.output_root)

    fixed_l = args.fixed_l or "0.045u"
    fixed_w = args.fixed_w or "10u"

    w_list = _parse_csv_list(args.w_list)
    l_list = _parse_csv_list(args.l_list)

    # Run sweeps
    w_results: List[RunResult] = []
    l_results: List[RunResult] = []
    grid_results: List[RunResult] = []

    if args.grid:
        for w in w_list:
            for l in l_list:
                grid_results.append(
                    _run_one_ac(
                        ac_template_path,
                        spiceinit_path,
                        output_root,
                        "WL",
                        w=w,
                        l=l,
                    )
                )
        all_rows = grid_results
    else:
        for w in w_list:
            w_results.append(
                _run_one_ac(
                    ac_template_path,
                    spiceinit_path,
                    output_root,
                    "W",
                    w=w,
                    l=fixed_l,
                )
            )

        for l in l_list:
            l_results.append(
                _run_one_ac(
                    ac_template_path,
                    spiceinit_path,
                    output_root,
                    "L",
                    w=fixed_w,
                    l=l,
                )
            )

        all_rows = w_results + l_results

    # Plots
    plots_dir = output_root / "plots"
    if args.grid:
        _plot_cv_overlay(
            grid_results,
            plots_dir / "cv_cgg_1MHz_wl_grid.png",
            title="FreePDK45 Cgg@1MHz vs Vg (W×L grid)",
        )
        _plot_ls_caps_stats_grid(
            grid_results,
            plots_dir / "ls_caps_stats_grid.png",
        )
    else:
        _plot_cv_overlay(
            w_results,
            plots_dir / "cv_cgg_1MHz_w_sweep.png",
            title=f"FreePDK45 Cgg@1MHz vs Vg (W sweep, L={fixed_l})",
        )
        _plot_cv_overlay(
            l_results,
            plots_dir / "cv_cgg_1MHz_l_sweep.png",
            title=f"FreePDK45 Cgg@1MHz vs Vg (L sweep, W={fixed_w})",
        )

        _plot_ls_caps_stats(
            w_results,
            l_results,
            plots_dir / "ls_caps_stats.png",
        )

    # Summary table
    _write_summary_csv(all_rows, output_root / "wl_sweep_ls_caps_summary.csv")

    # Cgg_ls linearity analysis (W/L/Area)
    _analyze_cgg_ls_linearity(all_rows, output_root)

    print(f"Done. Results under: {output_root}")
    print(f"- Overlay plots: {plots_dir}")
    print(f"- Summary CSV: {output_root / 'wl_sweep_ls_caps_summary.csv'}")
    print(f"- Cgg_ls linearity: {output_root / 'cgg_ls_linearity.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
