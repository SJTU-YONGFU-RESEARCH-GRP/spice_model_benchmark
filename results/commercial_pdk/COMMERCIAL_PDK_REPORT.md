# Commercial Foundry PDK Verification & Benchmarking Report

Generated automatically by **SPICE Model Benchmark Framework**.
Hardware Environment: `{'platform': 'Linux-5.14.0-611.26.1.el9_7.x86_64-x86_64-with-glibc2.34', 'processor': 'x86_64', 'cpu_model': 'Intel(R) Xeon(R) CPU E5-2678 v3 @ 2.50GHz', 'total_threads': '48', 'physical_cores': '24', 'sockets': '2', 'total_memory': '377Gi'}`.

---

## 1. Commercial PDK Device Performance Summary

| PDK Library | Foundry | Technology Node | Native EDA | $V_{DD}$ | $I_{on}$ | $V_{th}$ | Peak $G_m$ | $I_{on}/I_{off}$ | Status |
|:---|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Cadence_GPDK045** | Cadence | 45nm Bulk CMOS | `spectre` | 1.0 V | 0.427 mA | 0.635 V | 1.17 mS | 1.03e+07 | **✓ PASS** |
| **Synopsys_SAED14** | Synopsys | 14nm FinFET | `hspice` | 0.8 V | 0.138 mA | 0.410 V | 0.36 mS | 4.06e+05 | **✓ PASS** |
| **Synopsys_SAED32** | Synopsys | 32nm Bulk CMOS | `hspice` | 1.05 V | 0.355 mA | 0.336 V | 0.50 mS | 1.56e+03 | **✓ PASS** |
| **SMIC_180nm_BCD** | SMIC | 180nm BCD | `hspice` | 1.8 V | 5.950 mA | 0.674 V | 5.30 mS | 2.25e+07 | **✓ PASS** |
| **TSMC_16nm_FFC** | TSMC | 16nm FinFET | `hspice` | 0.8 V | 14.970 mA | 0.470 V | 45.34 mS | 9.06e+06 | **✓ PASS** |

---

## 2. Commercial CMOS Inverter Transfer Benchmark

| PDK Library | Technology Node | Supply $V_{DD}$ | $V_M$ (Switching) | Peak Gain $|A_v|$ | $NM_L$ | $NM_H$ | Status |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Cadence_GPDK045** | 45nm Bulk CMOS | 1.0 V | 0.495 V | 16.43 | 0.418 V | 0.425 V | **✓ PASS** |
| **Synopsys_SAED14** | 14nm FinFET | 0.8 V | 0.435 V | 19.30 | 0.343 V | 0.271 V | **✓ PASS** |
| **Synopsys_SAED32** | 32nm Bulk CMOS | 1.05 V | 0.520 V | 2.91 | 0.257 V | 0.272 V | **✓ PASS** |
| **SMIC_180nm_BCD** | 180nm BCD | 1.8 V | 0.860 V | 20.15 | 0.597 V | 0.727 V | **✓ PASS** |
| **TSMC_16nm_FFC** | 16nm FinFET | 0.8 V | 0.425 V | 26.70 | 0.366 V | 0.313 V | **✓ PASS** |

---

## 3. Publication-Grade Overlay Plots

- **Drive Current & Threshold Spread**: [commercial_pdk_drive_comparison.svg](plots/commercial_pdk_drive_comparison.svg) | [PNG](plots/commercial_pdk_drive_comparison.png)
- **CMOS Inverter DC Transfer Characteristic**: [commercial_inverter_vtc_overlay.svg](plots/commercial_inverter_vtc_overlay.svg) | [PNG](plots/commercial_inverter_vtc_overlay.png)

---
*Report automatically compiled at 2026-11-26 07:25:30*.
