"""
RF & Analog Benchmarks: Higher-order derivatives (gm2, gm3), linearity, and harmonic distortion (HD2, HD3, IIP3).

Implements quality assurance standards from:
- Colin C. McAndrew et al., "Benchmarks for SPICE Modeling and Parameter Extraction Based on AI/ML",
  IEEE Transactions on Electron Devices (TED), April 2025.
- Hongwei Yao et al., "NeuralCM-QA: Quality Assurance and Physical Benchmarking for Neural Compact Models",
  IEEE TCAD, 2026.
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


@dataclass
class RFAnalogMetrics:
    """Higher-order derivative, linearity, and distortion metrics."""
    vbias_V: float
    peak_gm_mS: float
    gm_at_bias_mS: float
    gm2_at_bias_mS_per_V: float
    gm3_at_bias_mS_per_V2: float
    hd2_pct: float             # 2nd harmonic distortion at vin_amp (%)
    hd3_pct: float             # 3rd harmonic distortion at vin_amp (%)
    hd2_dBc: float             # 2nd harmonic distortion (dBc)
    hd3_dBc: float             # 3rd harmonic distortion (dBc)
    aiip3_V: float             # IIP3 input voltage amplitude (V)
    iip3_dBm: float            # IIP3 in dBm (50 ohm reference)
    iip3_dBV: float            # IIP3 in dBV
    p1db_dBm: float            # 1-dB compression point (dBm, 50 ohm reference)
    gm2_ripples: int           # Spurious sign changes in gm2
    gm3_ripples: int           # Spurious sign changes in gm3
    smoothness_score: float    # Roughness penalty (lower is smoother)
    rf_qa_passed: bool         # Pass criteria: bounded distortion & ripple-free derivatives

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def calculate_derivatives(
    vg: np.ndarray,
    id_arr: np.ndarray,
    gm_arr: Optional[np.ndarray] = None
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate 1st (gm), 2nd (gm2), and 3rd (gm3) derivatives of Id w.r.t Vg.

    Args:
        vg: Gate voltage array (strictly monotonic)
        id_arr: Drain current array
        gm_arr: Optional pre-simulated transconductance array

    Returns:
        (gm, gm2, gm3) numpy arrays
    """
    vg = np.asarray(vg, dtype=float)
    id_arr = np.asarray(id_arr, dtype=float)

    if gm_arr is not None and len(gm_arr) == len(vg):
        gm = np.asarray(gm_arr, dtype=float)
    else:
        gm = np.gradient(id_arr, vg)

    gm2 = np.gradient(gm, vg)
    gm3 = np.gradient(gm2, vg)

    return gm, gm2, gm3


def audit_derivative_smoothness(
    vg: np.ndarray,
    gm2: np.ndarray,
    gm3: np.ndarray,
    threshold: float = 1e-11
) -> Tuple[int, int, float]:
    """Audit higher-order derivatives for non-physical ripples/oscillations.

    Args:
        vg: Gate voltage array
        gm2: Second derivative array
        gm3: Third derivative array
        threshold: Absolute noise floor threshold

    Returns:
        (gm2_ripples, gm3_ripples, roughness_score)
    """
    def _count_sign_changes(arr: np.ndarray) -> int:
        clean = np.where(np.abs(arr) < threshold, 0.0, arr)
        nz = clean[clean != 0]
        if len(nz) <= 1:
            return 0
        return int(len(np.where(np.diff(np.sign(nz)))[0]))

    gm2_ripples = _count_sign_changes(gm2)
    gm3_ripples = _count_sign_changes(gm3)

    # Normalized integrated roughness of 3rd derivative
    dv = np.gradient(vg)
    integrated_roughness = float(np.sum(np.abs(gm3) * np.abs(dv)))
    max_gm2 = float(np.max(np.abs(gm2))) if np.max(np.abs(gm2)) > 1e-12 else 1.0
    roughness_score = integrated_roughness / max_gm2

    return gm2_ripples, gm3_ripples, roughness_score


def evaluate_rf_analog_linearity(
    vg: np.ndarray,
    id_arr: np.ndarray,
    gm_arr: Optional[np.ndarray] = None,
    vbias: Optional[float] = None,
    vin_amp: float = 0.05
) -> RFAnalogMetrics:
    """Evaluate Taylor-series linearity, harmonic distortion (HD2, HD3), and IIP3.

    Taylor expansion around operating bias Vbias:
        id(vg) = a1*v + a2*v^2 + a3*v^3 + ...
        where:
          a1 = gm
          a2 = (1/2) * gm2
          a3 = (1/6) * gm3

    Distortion formulas:
        HD2 = (1/2) * |a2 / a1| * Vin
        HD3 = (1/4) * |a3 / a1| * Vin^2
        Aiip3 = sqrt( (4/3) * |a1 / a3| )
        IIP3 (dBm, 50 ohm) = 10 + 20*log10(Aiip3)
        A_1dB = sqrt( 0.145 * |a1 / a3| )

    Args:
        vg: Gate voltage array (monotonic)
        id_arr: Drain current array
        gm_arr: Optional pre-simulated transconductance array
        vbias: Target gate bias voltage (defaults to peak gm bias)
        vin_amp: Input sinusoidal amplitude (default 50 mV)

    Returns:
        RFAnalogMetrics dataclass instance
    """
    vg = np.asarray(vg, dtype=float)
    id_arr = np.asarray(id_arr, dtype=float)
    gm, gm2, gm3 = calculate_derivatives(vg, id_arr, gm_arr)

    # Determine evaluation bias point
    peak_idx = int(np.argmax(gm))
    peak_gm = float(gm[peak_idx])

    if vbias is None:
        bias_idx = peak_idx
        vbias = float(vg[bias_idx])
    else:
        bias_idx = int(np.argmin(np.abs(vg - vbias)))
        vbias = float(vg[bias_idx])

    gm_val = max(abs(float(gm[bias_idx])), 1e-12)
    gm2_val = float(gm2[bias_idx])
    gm3_val = float(gm3[bias_idx])

    a1 = gm_val
    a2 = 0.5 * gm2_val
    a3 = (1.0 / 6.0) * gm3_val

    # Harmonic distortion at vin_amp (fraction and dBc)
    hd2 = 0.5 * (abs(a2) / a1) * vin_amp
    hd3 = 0.25 * (abs(a3) / a1) * (vin_amp ** 2)

    hd2_pct = float(hd2 * 100.0)
    hd3_pct = float(hd3 * 100.0)
    hd2_dBc = float(20.0 * np.log10(max(hd2, 1e-12)))
    hd3_dBc = float(20.0 * np.log10(max(hd3, 1e-12)))

    # IIP3 and 1-dB compression
    if abs(a3) > 1e-15:
        aiip3 = float(np.sqrt((4.0 / 3.0) * (a1 / abs(a3))))
        aiip3 = min(aiip3, 100.0)  # Bound unphysically large values
        iip3_dBV = float(20.0 * np.log10(max(aiip3, 1e-9)))
        iip3_dBm = float(10.0 + iip3_dBV)  # 50 ohm: P(dBm) = 10 + 20*log10(V_peak)
        a1db = float(np.sqrt(0.145 * (a1 / abs(a3))))
        p1db_dBm = float(10.0 + 20.0 * np.log10(max(a1db, 1e-9)))
    else:
        aiip3 = 10.0
        iip3_dBV = 20.0
        iip3_dBm = 30.0
        p1db_dBm = 20.0

    gm2_ripples, gm3_ripples, roughness_score = audit_derivative_smoothness(vg, gm2, gm3)

    # QA criteria: physical compactness, bounded ripples in higher derivatives
    rf_qa_passed = (
        gm2_ripples <= 5 and
        gm3_ripples <= 8 and
        hd2 < 0.50 and
        hd3 < 0.30
    )

    return RFAnalogMetrics(
        vbias_V=vbias,
        peak_gm_mS=peak_gm * 1e3,
        gm_at_bias_mS=gm_val * 1e3,
        gm2_at_bias_mS_per_V=gm2_val * 1e3,
        gm3_at_bias_mS_per_V2=gm3_val * 1e3,
        hd2_pct=hd2_pct,
        hd3_pct=hd3_pct,
        hd2_dBc=hd2_dBc,
        hd3_dBc=hd3_dBc,
        aiip3_V=aiip3,
        iip3_dBm=iip3_dBm,
        iip3_dBV=iip3_dBV,
        p1db_dBm=p1db_dBm,
        gm2_ripples=gm2_ripples,
        gm3_ripples=gm3_ripples,
        smoothness_score=roughness_score,
        rf_qa_passed=rf_qa_passed
    )


def plot_rf_analog_derivatives(
    vg: np.ndarray,
    id_arr: np.ndarray,
    gm: np.ndarray,
    gm2: np.ndarray,
    gm3: np.ndarray,
    title: str,
    output_path: Path,
    vbias: Optional[float] = None,
    dpi: int = 300
) -> Tuple[Path, Path]:
    """Plot higher-order derivative breakdown (Id, gm, gm2, gm3) adhering to dev-plot style.

    Generates both PNG and SVG figures.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Typography according to dev-plot skill
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Arial", "Liberation Sans", "DejaVu Sans"]
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    plt.rcParams["axes.titleweight"] = "bold"

    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # Helper styling
    def _style_ax(ax):
        ax.grid(alpha=0.35, linewidth=1.1)
        ax.tick_params(axis="both", labelsize=10)
        for spine in ax.spines.values():
            spine.set_linewidth(2.0)
        ax.spines["top"].set_visible(True)
        ax.spines["right"].set_visible(True)

    # 1. Id vs Vg
    ax1 = axes[0, 0]
    _style_ax(ax1)
    ax1.plot(vg, id_arr * 1e3, color="#0033cc", linewidth=4.0, label=r"$I_d$ (mA)")
    if vbias is not None:
        ax1.axvline(vbias, color="#7f3fbf", linestyle="--", linewidth=2.0, label=f"Bias ({vbias:.2f}V)")
    ax1.set_title(r"Transfer Characteristic $I_d(V_g)$", fontsize=14, weight="bold")
    ax1.set_xlabel(r"$V_g$ (V)", fontsize=11, weight="bold")
    ax1.set_ylabel(r"$I_d$ (mA)", fontsize=11, weight="bold")
    ax1.legend(loc="upper left", framealpha=0.9)

    # 2. gm vs Vg
    ax2 = axes[0, 1]
    _style_ax(ax2)
    ax2.plot(vg, gm * 1e3, color="#0033cc", linewidth=4.0, label=r"$g_m = \partial I_d / \partial V_g$")
    if vbias is not None:
        ax2.axvline(vbias, color="#7f3fbf", linestyle="--", linewidth=2.0)
    ax2.set_title(r"Transconductance $g_m$ (1st Deriv)", fontsize=14, weight="bold")
    ax2.set_xlabel(r"$V_g$ (V)", fontsize=11, weight="bold")
    ax2.set_ylabel(r"$g_m$ (mS)", fontsize=11, weight="bold")
    ax2.legend(loc="upper right", framealpha=0.9)

    # 3. gm2 vs Vg
    ax3 = axes[1, 0]
    _style_ax(ax3)
    ax3.plot(vg, gm2 * 1e3, color="#cc0000", linewidth=3.5, label=r"$g_{m2} = \partial^2 I_d / \partial V_g^2$")
    ax3.axhline(0, color="black", linestyle=":", linewidth=1.0)
    if vbias is not None:
        ax3.axvline(vbias, color="#7f3fbf", linestyle="--", linewidth=2.0)
    ax3.set_title(r"2nd Order Derivative $g_{m2}$ ($HD_2$ Source)", fontsize=14, weight="bold")
    ax3.set_xlabel(r"$V_g$ (V)", fontsize=11, weight="bold")
    ax3.set_ylabel(r"$g_{m2}$ (mS/V)", fontsize=11, weight="bold")
    ax3.legend(loc="upper right", framealpha=0.9)

    # 4. gm3 vs Vg
    ax4 = axes[1, 1]
    _style_ax(ax4)
    ax4.plot(vg, gm3 * 1e3, color="#7f3fbf", linewidth=3.5, label=r"$g_{m3} = \partial^3 I_d / \partial V_g^3$")
    ax4.axhline(0, color="black", linestyle=":", linewidth=1.0)
    if vbias is not None:
        ax4.axvline(vbias, color="#7f3fbf", linestyle="--", linewidth=2.0)
    ax4.set_title(r"3rd Order Derivative $g_{m3}$ ($HD_3 / IIP_3$ Source)", fontsize=14, weight="bold")
    ax4.set_xlabel(r"$V_g$ (V)", fontsize=11, weight="bold")
    ax4.set_ylabel(r"$g_{m3}$ (mS/V$^2$)", fontsize=11, weight="bold")
    ax4.legend(loc="upper right", framealpha=0.9)

    fig.suptitle(f"{title} — High-Order Derivative Audit (IEEE TED 2025)", fontsize=16, weight="bold", y=0.99)
    fig.tight_layout()

    png_path = output_path.with_suffix(".png")
    svg_path = output_path.with_suffix(".svg")

    fig.savefig(png_path, dpi=dpi)
    fig.savefig(svg_path, format="svg")
    plt.close(fig)

    return png_path, svg_path
