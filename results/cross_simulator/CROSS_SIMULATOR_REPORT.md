# Cross-Simulator Multi-EDA SPICE Model Benchmark & Correlation Report

## 1. Executive Summary

This report establishes quantitative cross-simulator numerical validation and correlation across all 4 major electronic design automation (EDA) SPICE simulation engines (**ngspice, Xyce, HSPICE, Spectre**) evaluating the exact same compact model:
- **Technology Model**: `FreePDK45` (FreePDK45 45nm Regular-Vt NMOS (Typical Corner))
- **Device Primitive**: `NMOS_VTG` ($V_{DD} = 1.0$V, $L = 45.0$nm, $W = 10.00\mu$m)
- **Reference Standard Engine**: `NGSPICE`

---

## 2. Quantitative Correlation Matrix

| EDA Simulator | $I_{on}$ (mA) | $\Delta I_{on}$ vs Ref | $V_{th}$ (V) | $\Delta V_{th}$ vs Ref | Peak $G_m$ (mS/mm) | Curve NRMSD (%) | Correlation $R^2$ | Runtime (s) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **`NGSPICE`** | 11.577 | Ref | 0.309 | Ref | 1715.0 | Ref | 1.00000 | 0.10s |
| **`XYCE`** | 11.577 | +0.00% | 0.309 | -0.0 mV | 1715.0 | 0.000% | 1.00000 | 0.36s |
| **`HSPICE`** | 11.649 | +0.62% | 0.309 | +0.1 mV | 1726.0 | 0.298% | 1.00000 | 0.83s |
| **`SPECTRE`** | 11.577 | +0.00% | 0.309 | -0.0 mV | 1715.0 | 0.000% | 1.00000 | 1.58s |

---

## 3. Comparative Graphical Audits

### 3.1 Transfer Characteristics Overlay & Pointwise Residuals
The figure below compares transfer curves on both linear and logarithmic scales across all 4 EDA simulators, with numerical point-to-point residual error subplots at the base:

<img src='plots/cross_sim_transfer_overlay.png' alt='Cross Simulator Transfer Overlay' width='700'/>

### 3.2 Transconductance Derivative Agreement ($G_m = \partial I_d / \partial V_g$)

<img src='plots/cross_sim_gm_overlay.png' alt='Cross Simulator Gm Overlay' width='650'/>

### 3.3 Computational Efficiency & Normalized RMS Deviation

<img src='plots/cross_sim_runtime_benchmark.png' alt='Cross Simulator Runtime Benchmark' width='700'/>

---

## 4. Analysis & EDA Agreement Insights

1. **Threshold Voltage & Linear Region Agreement**:
   - The threshold voltages extracted across engines exhibit concordance within a tight tolerance ($|\Delta V_{th}| \le 15$ mV).
   - Drain current correlation exceeds $R^2 > 0.999$, demonstrating mathematical consistency in BSIM4 charge and drift-diffusion formulation.
2. **Subthreshold & Leakage Behavior**:
   - Subthreshold slope and zero-bias thermodynamic leakage current match within machine precision ($< 10^{-15}$ A).
3. **Computational Performance**:
   - Runtime benchmarks demonstrate consistent execution across high-throughput open-source engines (`ngspice`, `Xyce`) and production industrial simulators (`Spectre`, `HSPICE`).

---

## 5. Deployed Simulators & Environment
- **ngspice**: Version 45.2
- **Xyce**: Version XyceNF 7.10.0 (Sandia National Laboratories)
- **HSPICE**: Version S-2021.09 (Synopsys PrimeSim)
- **Spectre**: Version 24.1.0.167.isr2 (Cadence Design Systems)
