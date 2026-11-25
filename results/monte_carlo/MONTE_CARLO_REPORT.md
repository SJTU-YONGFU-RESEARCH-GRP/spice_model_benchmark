# Statistical Variation & Monte Carlo Mismatch Benchmark Report

Generated automatically by **SPICE Model Benchmark Framework**.
Hardware Environment: `{'platform': 'Linux-5.14.0-611.26.1.el9_7.x86_64-x86_64-with-glibc2.34', 'processor': 'x86_64', 'cpu_model': 'Intel(R) Xeon(R) CPU E5-2678 v3 @ 2.50GHz', 'total_threads': '48', 'physical_cores': '24', 'sockets': '2', 'total_memory': '377Gi'}`.

---

## 1. Executive Summary

- **Target PDK**: `FreePDK45`
- **Monte Carlo Sample Count**: `50 iterations`
- **Device Parameter Spread**:
  - $I_{on}$ Drive Current: $\mu = 1.146\text{ mA}$, $\sigma = 0.049\text{ mA}$ ($\text{CV} = 4.26\%$)
  - $V_{th}$ Threshold Voltage: $\mu = 0.312\text{ V}$, $\sigma = 15.41\text{ mV}$
  - Cross-Correlation ($I_{on}$ vs $V_{th}$): $r = -0.584$
- **6T-SRAM Yield & Stability**:
  - Hold Static Noise Margin: $\mu = 300.4\text{ mV}$, $\sigma = 10.0\text{ mV}$, Failure Rate ($<100\text{mV}$): `0.0%`
  - Read Static Noise Margin: $\mu = 144.2\text{ mV}$, $\sigma = 4.8\text{ mV}$, Failure Rate ($<50\text{mV}$): `0.0%`

---

## 2. Statistical Moments & Distribution Table

| Benchmark Metric | Mean ($\mu$) | Std Dev ($\sigma$) | CV (\%) | Median | Min | Max | $\mu - 3\sigma$ | $\mu + 3\sigma$ |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **$I_{on}$ Drive (mA)** | 1.146 | 0.049 | 4.26% | 1.145 | 1.018 | 1.219 | 0.999 | 1.292 |
| **$V_{th}$ Threshold (V)** | 0.312 | 0.015 | 4.93% | 0.313 | 0.278 | 0.341 | 0.266 | 0.359 |
| **Peak $G_m$ (mS)** | 1.71 | 0.06 | 3.49% | 1.71 | 1.53 | 1.81 | 1.53 | 1.88 |
| **Inverter $V_M$ (V)** | 0.520 | 0.011 | 2.16% | 0.515 | 0.500 | 0.545 | 0.486 | 0.553 |
| **SRAM Hold SNM (mV)** | 300.4 | 10.0 | 3.33% | 300.0 | 276.4 | 316.9 | 270.4 | 330.4 |
| **SRAM Read SNM (mV)** | 144.2 | 4.8 | 3.33% | 144.0 | 132.7 | 152.1 | 129.8 | 158.6 |

---

## 3. Publication-Grade Visualizations (`dev-plot` Style)

- **Device Variation 4-Panel (Histograms, CDF, Correlation)**: [monte_carlo_device_spread.svg](plots/monte_carlo_device_spread.svg) | [PNG](plots/monte_carlo_device_spread.png)
- **6T-SRAM Static Noise Margin Yield**: [monte_carlo_sram_snm_yield.svg](plots/monte_carlo_sram_snm_yield.svg) | [PNG](plots/monte_carlo_sram_snm_yield.png)

---
*Report automatically compiled at 2026-11-26 07:11:38*.
