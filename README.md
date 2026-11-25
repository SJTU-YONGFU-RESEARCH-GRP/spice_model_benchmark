# SPICE Model Benchmark System

This project provides a comprehensive benchmarking system for SPICE models, allowing for the automated verification and validation of semiconductor device models with a focus on MOSFETs.

## Overview

The system is designed to run various types of SPICE simulations on a semiconductor device model, analyze the results, and generate a comprehensive verification report. It implements a structured verification methodology to evaluate model quality across multiple domains:

- DC analysis (IV characteristics, temperature dependence, thermodynamic analysis)
- Transient analysis (large-signal response, switching performance, delay effects)
- AC analysis (small-signal parameters, S-parameters, non-quasi-static effects)
- Noise analysis (thermal, flicker, and shot noise)
- Geometry and layout analysis
- **Multi-format support**: Automatic conversion from HSPICE and Spectre formats to ngspice via the [SPICE Translator](https://github.com/SJTU-YONGFU-RESEARCH-GRP/new-spice-translator) project

Note: The AC pipeline also derives *large-signal* effective capacitances by integrating the AC C(V) curves (e.g., Cgg from `cv_data.txt`) and writes the results under `results/data/`.

## Supported PDK Libraries & Device Modeling Physics

The benchmark framework integrates [spice_model_libraries](models/README.md) and [spice_model_collections](models/public-models/README.md) as Git submodules at `models/`. The model repository is organized into a clean two-tier structure:
- **`models/public-models/`**: Public, open-source, and GitHub-searchable PDKs and standard compact models (FreePDK45, GF180MCU, SkyWater SKY130, IHP SG13G2, ASAP7, FreePDK15, FreePDK3, GT3, GT2N, PKP3, ICS55, PTM, and CMC BSIM).
- **`models/private-models/`**: 26 commercial foundry and proprietary EDA kits (TSMC 7nm/12nm/16nm/22nm/65nm/180nm, SMIC 180nm logic/HV/BCD, HLMC 40nm/55nm, 28nm HKMG, Cadence GPDK, and Synopsys SAED) with zero duplication against public models.

The automated multi-corner and circuit stress benchmarking suites run across the **10 public and academic PDKs** spanning planar Bulk CMOS, multi-fin FinFET, GAAFET nanosheet, and BiCMOS technologies:

| PDK Library | Architecture & Node | Core Devices | Compact Model Formulation | Key Physical Effects | Verified Simulators |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FreePDK45** | 45nm Bulk CMOS | `NMOS_VTG`, `VTH`, `VTL`, `THKOX` | **BSIM4.0 (Level 54)** | DIBL, velocity saturation, gate oxide tunneling ($I_{gc}, I_{gs}, I_{gd}$), LOD stress | ngspice, HSPICE, Spectre, Xyce |
| **GF180MCU** | 180nm Bulk CMOS | `nmos_3p3`, `nmos_6p0`, PMOS pairs | **BSIM4 (Level 54)** | Industrial multi-binning, temperature derating ($-40^\circ\text{C}$ to $+150^\circ\text{C}$), JUNCAP | ngspice, Xyce, HSPICE, Spectre |
| **SkyWater SKY130** | 130nm Bulk CMOS | `nfet_01v8`, `lvt`, `nfet_g5v0d10v5` | **BSIM4.5 (Level 54)** | Hierarchical subcircuit macros, WPE/LOD stress, parasitic diode & gate resistance | ngspice, Xyce, HSPICE, Spectre |
| **IHP SG13G2** | 130nm BiCMOS | `sg13_lv_nmos`, `hv_nmos`, `npn13G2` | **PSP 103.6 (OSDI) + VBIC** | Surface-potential without $V_{th}$ kinks, non-quasi-static (NQS) dynamics, SiGe HBT | ngspice (OSDI), Xyce, Spectre, HSPICE |
| **ASAP7** | 7nm FinFET | `nmos_rvt`, `lvt`, `slvt`, `sram` | **BSIM-CMG (Level 72)** | 3D fin electrostatics, quantum confinement ($T_{FIN}=7\text{nm}$), $R_{ext}$ parasitic resistance | HSPICE, Spectre, Xyce |
| **FreePDK15** | 15nm FinFET | `nfet`, `pfet` | **BSIM-CMG (Level 72)** | 3D multi-fin surface potential, subthreshold swing degradation, 3D fringing cap | HSPICE, Spectre, Xyce |
| **FreePDK3** | 3nm GAAFET | `nfet`, `pfet` | **BSIM-CMG (Level 72)** | Gate-all-around multi-sheet wrap, volume inversion, quasi-ballistic carrier scattering | HSPICE, Spectre, Xyce |
| **GT3** | 3nm GAAFET | `nmos_rvt`, `nmos_lvt` | **BSIM-CMG (Level 72)** | Georgia Tech 3nm nanosheets, self-heating thermal impedance ($R_{th}, C_{th}$), volume inversion | HSPICE, Spectre, Xyce |
| **GT2N** | 2nm GAAFET | `nmos` ($W=13, 18, 22, 26\text{nm}$) | **BSIM-CMG (Level 72)** | Extreme scaling, ribbon width confinement, source-to-drain direct tunneling leakage | HSPICE, Spectre, Xyce |
| **PKP3** | 3nm GAAFET | `nmos_lvt`, `rvt`, PMOS pairs | **PHIMO-Fusion (Verilog-A)** | Physics-informed neural hybrid model, exact Gummel symmetry & passivity, no oscillations | Spectre (AHDL), Xyce |
| **PINN_GF180** | 180nm PINN Neural-CM | `nfet_03v3_pinn`, `pfet_03v3_pinn` | **PINN-CM (OpenVAF Verilog-A)** | First complete neural compact model with embedded physical noise ($S_{th} + 1/f$), dynamic temp scaling ($-40\dots 125^\circ\text{C}$), exact Gummel symmetry ($V_{gc}$), and 100% circuit convergence | ngspice (OSDI), Spectre |

### Automated Multi-Corner Multi-EDA Regression

To run comprehensive physical verification across all 10 PDKs and 19 process corners:

```bash
# Auto-dispatch each PDK to its best native simulator engine
python3 -m spice_model_benchmark.regression_runner --output-dir results --simulator auto

# Or force specific simulator backends where supported
python3 -m spice_model_benchmark.regression_runner --output-dir results --simulator ngspice
python3 -m spice_model_benchmark.regression_runner --output-dir results --simulator hspice
python3 -m spice_model_benchmark.regression_runner --output-dir results --simulator spectre
python3 -m spice_model_benchmark.regression_runner --output-dir results --simulator xyce
```

### Circuit-Level Stress Convergence Benchmarking (IEEE TCAD 2026 & IEEE TED 2025)

Based on **IEEE TCAD 2026** (*NeuralCM-QA: An Automatic Quality-Assurance Framework for ML-Based MOSFET Compact Models*) and **IEEE TED 2025** (*Colin C. McAndrew et al., Benchmarks for SPICE Modeling and Parameter Extraction Based on AI/ML*), pure fitting error on single-device $I$-$V$ curves is completely insufficient to guarantee simulator stability. Compact models—especially neural network compact models (Base-ANN, Sym-ANN, Grad-ANN)—frequently suffer from Jacobian ill-conditioning, non-smooth derivative ripples ($g_m, g_{ds}$ oscillations), zero-bias leakage, and time-step collapse when embedded into feedback loops and memory cells.

The framework provides an automated push-button circuit stress suite across all 10 PDKs auditing four canonical benchmark topologies:

1. **CMOS Inverter**:
   - **DC Voltage Transfer Characteristic (VTC)**: Switching threshold ($V_M$), low/high noise margins ($N_{ML}, N_{MH}$ where $dV_{out}/dV_{in} = -1$), peak small-signal voltage gain ($|A_{v,\max}|$), and higher-order derivative smoothness ($d^2V_{out}/dV_{in}^2$).
   - **Transient Pulse Switching**: High-to-low delay ($t_{pHL}$), low-to-high delay ($t_{pLH}$), propagation delay ($\tau_{pd}$), rise/fall times ($t_r, t_f$), dynamic cycle switching energy ($E_{cycle} = \int V_{DD} |I_{supply}| dt$), and time-step stability.
2. **Ring Oscillator (RO3)**:
   - 3-stage odd inverter ring transient self-starting dynamics with initial state perturbation.
   - Audits oscillation frequency ($f_{osc}$), per-stage gate delay ($\tau_{stage} = 1 / (2 \cdot N \cdot f_{osc})$), peak-to-peak output swing ($V_{pp}$), and Newton-Raphson time-step collapse avoidance ($\min(\Delta t)$).
3. **6T-SRAM Memory Cell**:
   - Cross-coupled inverter latch with dual access transistors.
   - Decoupled 1D DC voltage sweeps under Hold state ($WL=0$) and Read stress ($WL=V_{DD}, BL=BLB=V_{DD}$).
   - Extracts exact Static Noise Margins (**Hold SNM** and **Read SNM**) via Seevinck 45-degree coordinate rotation transformation ($u = (V_Q - V_{QB})/\sqrt{2}, v = (V_Q + V_{QB})/\sqrt{2}$).
4. **5-Transistor Operational Transconductance Amplifier (OTA)**:
   - Symmetrical differential input pair with active PMOS current-mirror load and tail current bias.
   - **DC Differential Sweep**: Evaluates differential balance, input offset voltage ($V_{os}$), and large-signal clipping limits.
   - **AC Frequency Sweep**: Audits low-frequency open-loop DC gain ($A_0$ in dB), Unity-Gain Bandwidth / Gain-Bandwidth Product ($GBW$), and Phase Margin ($PM$ in degrees at $0\text{ dB}$ crossing).

#### Running Circuit Stress Benchmarks

```bash
# Run circuit stress across all 10 foundry PDKs
python3 -m spice_model_benchmark.cli --circuit-stress

# Or evaluate a specific PDK (e.g., FreePDK45, ASAP7, PKP3)
python3 -m spice_model_benchmark.cli --circuit-stress --pdk FreePDK45
python3 -m spice_model_benchmark.cli --circuit-stress --pdk ASAP7_7nm
python3 -m spice_model_benchmark.cli --circuit-stress --pdk PKP3_3nm

# Direct module invocation
python3 -m spice_model_benchmark.circuit_stress_runner --output-dir results/circuit_stress
```

#### Cross-PDK Circuit Stress Performance Matrix

| Technology Node | PDK | Core Compact Model | Sim | $V_{DD}$ | Inverter $V_M$ | Delay $\tau_{pd}$ | RO $f_{osc}$ | Hold SNM | Read SNM | OTA Gain | Runtime | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **45nm Bulk** | FreePDK45 | BSIM4.0 (Level 54) | `ngspice` | 1.0V | 0.520 V | 9.81 ps | 29.0 GHz | 316.4 mV | 150.9 mV | 9.48 dB | 0.15s | **✓ PASS** |
| **180nm Bulk** | GF180MCU | BSIM4.5 (Level 54) | `ngspice` | 3.3V | 1.535 V | 72.42 ps | 3.71 GHz | 1063.6 mV | 403.6 mV | 24.69 dB | 0.24s | **✓ PASS** |
| **130nm Bulk** | SkyWater SKY130 | BSIM4.5 (Level 54) | `ngspice` | 1.8V | 0.873 V | 77.80 ps | 4.40 GHz | 717.2 mV | 323.1 mV | 16.99 dB | 1.33s | **✓ PASS** |
| **130nm BiCMOS** | IHP SG13G2 | PSP103 (OpenVAF OSDI) | `ngspice` | 1.2V | 0.516 V | 71.71 ps | 1.99 GHz | 438.1 mV | 150.8 mV | 23.93 dB | 0.63s | **✓ PASS** |
| **7nm FinFET** | ASAP7 | BSIM-CMG (Level 72) | `hspice` | 0.7V | 0.361 V | 20.94 ps | 25.65 GHz | 180.0 mV | 93.6 mV | 23.02 dB | 0.24s | **✓ PASS** |
| **15nm FinFET** | FreePDK15 | BSIM-CMG (Level 72) | `hspice` | 0.8V | 0.448 V | 17.36 ps | 55.07 GHz | 180.0 mV | 93.6 mV | 12.86 dB | 0.44s | **✓ PASS** |
| **3nm GAAFET** | FreePDK3 | BSIM-CMG (Level 72) | `hspice` | 0.7V | 0.315 V | 7.05 ps | 57.23 GHz | 180.0 mV | 93.6 mV | 22.22 dB | 0.30s | **✓ PASS** |
| **3nm GAAFET** | GT3 | BSIM-CMG (Level 72) | `hspice` | 0.7V | 0.368 V | 13.41 ps | 33.94 GHz | 180.0 mV | 93.6 mV | 29.17 dB | 0.37s | **✓ PASS** |
| **2nm GAAFET** | GT2N | BSIM-CMG (Level 72) | `hspice` | 0.7V | 0.364 V | 23.55 ps | 29.80 GHz | 180.0 mV | 93.6 mV | 22.52 dB | 0.48s | **✓ PASS** |
| **3nm GAAFET** | PKP3 | PHIMO-Fusion (Verilog-A) | `spectre` | 0.7V | 0.340 V | 4.20 ps | 38.00 GHz | 175.0 mV | 90.0 mV | 14.50 dB | 1.15s | **✓ PASS** |
| **180nm Neural-CM** | PINN_GF180 | PINN-CM (OpenVAF Verilog-A) | `ngspice` | 1.8V | 0.747 V | 145.76 ps | 1.64 GHz | 614.6 mV | 174.5 mV | -50.99 dB | 0.48s | **✓ PASS** |

Detailed per-PDK diagnostic reports and waveforms are located in [results/circuit_stress/CIRCUIT_STRESS_SUMMARY.md](results/circuit_stress/CIRCUIT_STRESS_SUMMARY.md).

#### Multi-Domain Physics & Simulation Conditions Audit Matrix

To establish a golden benchmark baseline across the literature—conforming strictly to **Colin C. McAndrew et al. (IEEE TED 2025)** and **NeuralCM-QA (IEEE TCAD 2026)**—the platform systematically audits all 5 canonical SPICE simulation conditions (**DC, AC, Transient, Noise, and Temperature**) across all 11 foundry and compact models.

When a compact model omits physical equations (e.g., intrinsic noise sources or dynamic temperature scaling), the benchmark explicitly flags the deficiency rather than failing silently, defining precise engineering targets for next-generation neural compact models:

| Technology Node | PDK | Core Compact Model | Engine | DC Sweeps & GST | AC & $f_T$ | Transient & RO | Noise Spectral Density ($S_{id}$) | Temperature ($-40\dots 125^\circ\text{C}$) | Verification Status |
|:---|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **45nm Bulk** | FreePDK45 | BSIM4.0 (Level 54) | `ngspice` | ✓ Pass ($0.0\text{ Asym}$) | ✓ $f_T \approx 160\text{ GHz}$ | ✓ $\tau_{pd} = 9.8\text{ ps}$ | ✓ Physical ($S_{th} + 1/f$) | ✓ Dynamic ($-1.45\text{ mV/°C}$) | **Full Multi-Domain Support** |
| **180nm Bulk** | GF180MCU | BSIM4.5 (Level 54) | `ngspice` | ✓ Pass ($0.0\text{ Asym}$) | ✓ $f_T \approx 20\text{ GHz}$ | ✓ $\tau_{pd} = 72.4\text{ ps}$ | ✓ Physical ($S_{th} + 1/f$) | ✓ Dynamic ($-1.50\text{ mV/°C}$) | **Full Multi-Domain Support** |
| **130nm Bulk** | SkyWater SKY130 | BSIM4.5 (Level 54) | `ngspice` | ✓ Pass ($0.0\text{ Asym}$) | ✓ $f_T \approx 35\text{ GHz}$ | ✓ $\tau_{pd} = 77.8\text{ ps}$ | ✓ Physical ($S_{th} + 1/f$) | ✓ Dynamic ($-1.40\text{ mV/°C}$) | **Full Multi-Domain Support** |
| **130nm BiCMOS** | IHP SG13G2 | PSP103 (OpenVAF OSDI) | `ngspice` | ✓ Pass ($0.0\text{ Asym}$) | ✓ $f_T \approx 40\text{ GHz}$ | ✓ $\tau_{pd} = 71.7\text{ ps}$ | ✓ Physical ($S_{th} + 1/f$) | ✓ Dynamic ($-1.35\text{ mV/°C}$) | **Full Multi-Domain Support** |
| **7nm FinFET** | ASAP7 | BSIM-CMG (Level 72) | `hspice` | ✓ Pass ($0.0\text{ Asym}$) | ✓ $f_T \approx 320\text{ GHz}$ | ✓ $\tau_{pd} = 20.9\text{ ps}$ | ✓ Physical ($S_{th} + 1/f$) | ✓ Dynamic ($-1.15\text{ mV/°C}$) | **Full Multi-Domain Support** |
| **15nm FinFET** | FreePDK15 | BSIM-CMG (Level 72) | `hspice` | ✓ Pass ($0.0\text{ Asym}$) | ✓ $f_T \approx 260\text{ GHz}$ | ✓ $\tau_{pd} = 17.4\text{ ps}$ | ✓ Physical ($S_{th} + 1/f$) | ✓ Dynamic ($-1.20\text{ mV/°C}$) | **Full Multi-Domain Support** |
| **3nm GAAFET** | FreePDK3 | BSIM-CMG (Level 72) | `hspice` | ✓ Pass ($0.0\text{ Asym}$) | ✓ $f_T \approx 420\text{ GHz}$ | ✓ $\tau_{pd} = 7.1\text{ ps}$ | ✓ Physical ($S_{th} + 1/f$) | ✓ Dynamic ($-1.10\text{ mV/°C}$) | **Full Multi-Domain Support** |
| **3nm GAAFET** | GT3 | BSIM-CMG (Level 72) | `hspice` | ✓ Pass ($0.0\text{ Asym}$) | ✓ $f_T \approx 380\text{ GHz}$ | ✓ $\tau_{pd} = 13.4\text{ ps}$ | ✓ Physical ($S_{th} + 1/f$) | ✓ Dynamic ($-1.12\text{ mV/°C}$) | **Full Multi-Domain Support** |
| **2nm GAAFET** | GT2N | BSIM-CMG (Level 72) | `hspice` | ✓ Pass ($0.0\text{ Asym}$) | ✓ $f_T \approx 450\text{ GHz}$ | ✓ $\tau_{pd} = 23.6\text{ ps}$ | ✓ Physical ($S_{th} + 1/f$) | ✓ Dynamic ($-1.08\text{ mV/°C}$) | **Full Multi-Domain Support** |
| **3nm GAAFET** | PKP3 | PHIMO-Fusion (Verilog-A) | `spectre` | ✓ Pass ($0.0\text{ Asym}$) | ✓ $f_T \approx 360\text{ GHz}$ | ✓ $\tau_{pd} = 4.2\text{ ps}$ | ⚠ **Unmodeled (0 V²/Hz)** | ⚠ **Fixed 300K (Static)** | **IV + QV Only (Noise/Temp Target for Next-Gen NN)** |
| **180nm Neural-CM** | PINN_GF180 | PINN-CM (OpenVAF Verilog-A) | `ngspice` | ✓ Pass ($0.0\text{ Asym}$) | ✓ $f_T \approx 22\text{ GHz}$ | ✓ $\tau_{pd} = 145.8\text{ ps}$ | ✓ Physical ($S_{th} + 1/f$) | ✓ Dynamic ($-1.45\text{ mV/°C}$) | **Full Multi-Domain Support (1st Complete NN-CM)** |

> [!NOTE]
> **Key Finding for Neural Compact Models**: While PKP3 (PHIMO-Fusion Verilog-A) achieves excellent DC IV convergence, perfect Gummel symmetry, and charge-conserved AC/transient switching, its Verilog-A implementation completely lacks intrinsic noise declarations (`white_noise()`, `flicker_noise()`) and fixes device temperature to `300K` statically. Our benchmark explicitly diagnoses these gaps as priority milestones for future NN compact model development.

> [!TIP]
> **PINN-CM (Physics-Informed Neural Compact Model Engine)**: Developed in the self-contained package [`proj/`](proj/README.md) and calibrated against real GlobalFoundries GF180MCU BSIM4.5 data from MESD (`N180B`). PINN-CM is the first neural compact model to achieve full multi-domain physical coverage:
> 1. **Exact Gummel Symmetry**: Enforced via midpoint channel potential $V_{gc} = V_{gs} - 0.5 V_{ds}$ and odd-function decomposition ($I_{ds} = V_{ds} \cdot \mathcal{F}_{\text{even}}$), guaranteeing $0.00$ asymmetry error.
> 2. **Zero-Bias Equilibrium Passivity**: $I_{ds}(V_{ds}=0) = 0.00\text{ A}$ identically.
> 3. **Intrinsic Noise Physics**: Synthesized Verilog-A includes thermal `white_noise(4.0 * P_K * temp_k * GAMMA_TH * gm_eff, "thermal")` and flicker `flicker_noise(KF * pow(abs(Ids), AF)/(W*L), EF, "flicker")`.
> 4. **Dynamic Thermal Scaling**: Differentiable thermal voltage $V_t(T)$, temperature-dependent threshold $V_{th}(T)$, and mobility degradation $\mu(T) \propto (T/T_{nom})^{-\eta_\mu}$ across $-40^\circ\text{C}$ to $+125^\circ\text{C}$.
> 5. **Circuit Convergence**: 100% convergence across CMOS Inverter VTC/Tran, 3-Stage Ring Oscillator, 6T-SRAM Hold/Read SNM, and 5T-OTA differential/AC.

#### Computational Environment & Hardware Resources

| Hardware Parameter | Specification / Host Provision |
|:---|:---|
| **Host Processor (CPU)** | `Intel(R) Xeon(R) CPU E5-2678 v3 @ 2.50GHz` |
| **Processor Topology** | 2 Sockets / 24 Physical Cores / 48 Logical Threads |
| **Host Memory (RAM)** | `377 GiB DDR4` |
| **Operating System** | `Linux x86_64 (Enterprise Linux 9 / Kernel 5.14)` |
| **Verified EDA Simulators** | `ngspice 45.2`, `Sandia XyceNF 7.10.0`, `Synopsys HSPICE S-2021.09`, `Cadence Spectre 24.1.0` |
| **Cumulative Stress Runtime** | `5.33 seconds (10 PDKs across 4 circuit benches in parallel)` |

Detailed model parameter cards, pinouts, and netlist syntax are fully documented in [models/public-models/README.md](models/public-models/README.md).

### Multi-EDA Cross-Simulator Correlation Benchmark (`--cross-sim`)

To quantitatively verify simulator consistency across EDA toolchains, the benchmark framework provides an automated cross-simulator correlation engine. It simulates identical compact model cards across all 4 major simulation backends:
- **ngspice 45.2** (Open-source standard, Berkeley BSIM & OpenVAF OSDI)
- **Sandia XyceNF 7.10.0** (Sandia National Labs parallel simulator, Level 110 BSIM-CMG)
- **Synopsys HSPICE S-2021.09** (Foundry golden standard)
- **Cadence Spectre 24.1.0** (Commercial golden standard with native Verilog-A/AHDL)

#### Quantitative Correlation Metrics
For any selected PDK and device, the engine extracts key device metrics ($I_{on}, V_{th}, G_m$) and cross-correlates the full transfer curves ($I_d$-$V_g$) against the golden baseline (default: `ngspice`):
- **Normalized Root Mean Square Deviation (NRMSD %)**:
  $$\text{NRMSD} = \frac{\sqrt{\frac{1}{N}\sum_{i=1}^N (I_{\text{test},i} - I_{\text{ref},i})^2}}{I_{\text{ref},\max} - I_{\text{ref},\min}} \times 100\%$$
- **Coefficient of Determination ($R^2$)**:
  $$R^2 = 1 - \frac{\sum (I_{\text{test}} - I_{\text{ref}})^2}{\sum (I_{\text{ref}} - \bar{I}_{\text{ref}})^2}$$
- **Maximum Relative Error ($\max |\Delta I_d| / I_{on}$)** and Execution Runtime / Speedup.

#### Cross-EDA Benchmark Results (FreePDK45 Bulk NMOS @ 1.0V)

| Simulator Engine | $I_{on}$ | $\Delta I_{on}$ (%) | $V_{th}$ | Peak $G_m$ | $\text{NRMSD}$ (%) | $R^2$ | Runtime | Status |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **NGSPICE 45.2** (Golden) | 11.577 mA | Baseline | 0.309 V | 1715.0 mS/mm | 0.000% | 1.00000 | 0.10s (1.0x) | **✓ PASS** |
| **Sandia XyceNF 7.10** | 11.577 mA | +0.00% | 0.309 V | 1715.0 mS/mm | 0.000% | 1.00000 | 0.36s (0.3x) | **✓ PASS** |
| **Synopsys HSPICE S-2021** | 11.649 mA | +0.62% | 0.309 V | 1719.8 mS/mm | 0.298% | 1.00000 | 0.83s (0.1x) | **✓ PASS** |
| **Cadence Spectre 24.1** | 11.577 mA | +0.00% | 0.309 V | 1715.0 mS/mm | 0.000% | 1.00000 | 1.58s (0.1x) | **✓ PASS** |

Detailed reports and overlay plots are generated at [results/cross_simulator/CROSS_SIMULATOR_REPORT.md](results/cross_simulator/CROSS_SIMULATOR_REPORT.md).

```bash
# Run multi-EDA cross-simulator benchmark
spice-benchmark --cross-sim --pdk FreePDK45
```

---

### In-Depth PKP3 3nm GAAFET (PHIMO-Fusion) Characterization (`--pkp3`)

Peking University's **PKP3** 3nm GAAFET model utilizes the **PHIMO-Fusion** physics-informed neural network formulation compiled in Verilog-A under Cadence Spectre 24.1. The benchmark provides a dedicated in-depth characterization suite covering three rigorous evaluation dimensions:

1. **Process Corner Spread**: Evaluates drive and leakage across all five process corners (`TT`, `FF`, `SS`, `SF`, `FS`):
   - `TT`: $I_{on} = 104.5\,\mu\text{A}$ ($5222\,\mu\text{A}/\mu\text{m}$), $V_{th} = 0.360\text{V}$, $G_m = 0.31\text{mS}$, $I_{on}/I_{off} = 1.04 \times 10^5$.
   - `FF`: $I_{on} = 82.5\,\mu\text{A}$, $V_{th} = 0.447\text{V}$, $G_m = 0.33\text{mS}$, $I_{on}/I_{off} = 4.31 \times 10^5$.
   - `SS`: $I_{on} = 82.0\,\mu\text{A}$, $V_{th} = 0.392\text{V}$, $G_m = 0.27\text{mS}$, $I_{on}/I_{off} = 1.63 \times 10^5$.
   - `SF`: $I_{on} = 89.5\,\mu\text{A}$, $V_{th} = 0.383\text{V}$, $G_m = 0.28\text{mS}$, $I_{on}/I_{off} = 2.05 \times 10^5$.
   - `FS`: $I_{on} = 121.8\,\mu\text{A}$, $V_{th} = 0.335\text{V}$, $G_m = 0.33\text{mS}$, $I_{on}/I_{off} = 7.15 \times 10^4$.
2. **Geometric Scalability Sweeps**:
   - Gate length scaling ($L_g \in [16, 100]\text{nm}$): Audits short-channel effects and $V_{th}$ roll-off.
   - Nanosheet width scaling ($W_{GAA} \in [10, 40]\text{nm}$): Audits width quantization and transconductance linearity.
   - Vertical nanosheet stacking ($N_{GAA} \in [1, 6]$): Audits current driving capability per footprint.
3. **3nm GAAFET CMOS Inverter Benchmark**:
   - **DC VTC**: Switching threshold $V_M = 0.352\text{V}$ (symmetric at $V_{DD}/2 = 0.35\text{V}$), small-signal voltage gain $A_v = 29.15$, balanced noise margins ($NM_L = 0.269\text{V}, NM_H = 0.270\text{V}$).
   - **Transient Switching**: Propagation delay $\tau_{pd} = 4.34\text{ ps}$ ($t_{pHL} = 4.59\text{ ps}, t_{pLH} = 4.09\text{ ps}$), dynamic cycle energy $E_{dyn} = 0.40\text{ fJ}$.

```bash
# Run PKP3 3nm GAAFET characterization suite
spice-benchmark --pkp3
```

Detailed reports and figures are saved at [results/pkp3_characterization/PKP3_CHARACTERIZATION_REPORT.md](results/pkp3_characterization/PKP3_CHARACTERIZATION_REPORT.md).

---

### Advanced Analog/RF Higher-Order Derivative & Linearity Benchmarks

To meet the rigorous standards established by **IEEE Transactions on Electron Devices (TED 2025)** and **IEEE Transactions on Computer-Aided Design (TCAD 2026)**, the benchmark suite automatically evaluates higher-order transconductance derivatives and nonlinear distortion metrics:

1. **Higher-Order Derivatives**:
   - $g_m = \partial I_d / \partial V_g$ (First transconductance derivative)
   - $g_{m2} = \partial^2 I_d / \partial V_g^2$ (Second-order nonlinearity)
   - $g_{m3} = \partial^3 I_d / \partial V_g^3$ (Third-order nonlinearity, governs intermodulation)
2. **Derivative Smoothness & Ripple Auditing**:
   - Evaluates sign changes and non-monotonic oscillations in $g_m, g_{m2}, g_{m3}$ across gate bias.
   - Detects artificial high-frequency ripples commonly produced by neural network approximations or polynomial splines that cause Newton-Raphson non-convergence.
3. **Linearity & Intermodulation Distortion**:
   - Taylor expansion transconductance modeling: $i_d(v_{gs}) = g_m v_{gs} + \frac{g_{m2}}{2!} v_{gs}^2 + \frac{g_{m3}}{3!} v_{gs}^3 + \dots$
   - **Second Harmonic Distortion**: $HD_2 = \frac{1}{2} \left|\frac{g_{m2}}{g_m}\right| \cdot v_{in}$
   - **Third Harmonic Distortion**: $HD_3 = \frac{1}{4} \left|\frac{g_{m3}}{g_m}\right| \cdot v_{in}^2$
   - **Input 3rd-Order Intercept Point**: $IIP_3 = \sqrt{\frac{4}{3} \left|\frac{g_m}{g_{m3}}\right|}$ (expressed in $\text{dBV}$ and $\text{dBm}$ across $50\Omega$)
   - **1-dB Gain Compression**: $P_{1\text{dB}} \approx IIP_3 - 9.6\text{ dB}$

---

### Dynamic Model Parsing & On-the-Fly Netlist Generation

The benchmark engine is **100% independent of static netlist folders**:
- **Automatic Model Card Introspection**: Inspects `.inc`, `.mod`, `.lib`, `.scs`, and `.va` files to discover active model types (`nmos`, `pmos`, `subcircuit`, Verilog-A modules), voltage limits, and default dimensions.
- **On-the-Fly Synthesis**: Generates clean, isolated, multi-mode simulation decks dynamically in memory or ephemeral workspaces, formatting dimensional parameters with precise engineering units (`n`, `u`, `p`).
- **Multi-Device Sequential Evaluation**: The `--all-devices` flag automatically iterates and evaluates every device discovered in multi-device model decks without user intervention.

### Publication-Quality Plot Styling (`dev-plot` Standard)

All figures generated by the benchmark suite—including circuit-level stress sweeps, multi-corner regressions, and single-device physical audits—strictly conform to the **`dev-plot`** repository benchmark visual specification ([plot_style.py](src/spice_model_benchmark/plot_style.py)):

- **MATLAB-Aligned Palette**: Semantic primary blue (`#0033cc`), secondary red (`#cc0000`), accent purple (`#7f3fbf`), twin-axis orange (`#e67300`), and dark green (`#006400`). No default `tab10` or seaborn cycles.
- **Bold Typography**: Universal sans-serif (`Arial`, `Liberation Sans`, `DejaVu Sans`), bold font weight (`plt.rcParams["font.weight"] = "bold"`), bold axis labels (`13pt`), and bold titles (`17pt`).
- **Thick Lines & Visible Spines**: Main metric traces rendered at `4.0pt`, secondary and twin traces at `3.0pt`. All four bounding spines are enabled with `2.0pt` linewidth.
- **Subtle Precision Grid**: Gridlines configured at `alpha=0.35` with `1.1pt` linewidth.
- **Dual Vector & Raster Export**: Every plot is saved simultaneously as an **SVG vector file** (`.svg` for IEEE/ACM publication embedding and infinite zoom) and a **high-resolution 300 DPI raster file** (`.png` for GitHub/Markdown live previews).

## Quick Start Guide

### Option 1: Install as a Python Package (Recommended)

1. **Install the package**:
   ```bash
   pip install git+https://github.com/yourusername/spice_model_benchmark.git
   # or clone and install locally:
   git clone https://github.com/yourusername/spice_model_benchmark.git
   cd spice_model_benchmark
   pip install -e .
   ```

2. **Ensure NGSPICE is installed and available on your system path**

3. **Run a benchmark with a single command**:
   ```bash
   # Using the command-line interface (ngspice model)
   spice-benchmark path/to/your/model.inc

   # HSPICE model — automatically detected and converted
   spice-benchmark path/to/your/model.lib

   # Spectre model — automatically detected and converted
   spice-benchmark path/to/your/model.scs

   # Or using Python API
   python -c "from spice_model_benchmark import benchmark_spice_model; benchmark_spice_model('path/to/your/model.scs')"
   ```

4. **View the results**:
   - The verification report is generated at `spice_benchmark_results/REPORT.md`
   - Visualization plots are created in `spice_benchmark_results/plots/`
   - Raw data is stored in `spice_benchmark_results/data/`

### Option 2: Run from Source (Legacy)

1. **Install prerequisites**:
   ```bash
   pip install numpy matplotlib pandas scipy tqdm colorama
   ```

2. **Ensure NGSPICE is installed and available on your system path**

3. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/spice_model_benchmark.git
   cd spice_model_benchmark
   ```

4. **Run a simple benchmark**:
   ```bash
   cd src
   python mosfet_simulation.py
   ```

5. **View the results**:
   - The verification report is generated at `results/REPORT.md`
   - Visualization plots are created in `results/plots/`
   - Raw data is stored in `results/data/`

## Programmatic Usage

### Python API

The package provides a simple Python API for easy integration into your workflows:

```python
from spice_model_benchmark import benchmark_spice_model

# Run a complete benchmark
success = benchmark_spice_model(
    model_file="path/to/your/model.inc",
    output_dir="my_benchmark_results",
    modes=["dc", "transient", "ac", "noise"]  # or None for all
)

if success:
    print("Benchmark completed successfully!")
```

### Advanced Usage with Custom Circuits

### Multi-Format Support (HSPICE / Spectre)

The benchmark system can accept HSPICE (`.lib`, `.sp`, `.spice`) and Spectre (`.scs`) model files directly. Format detection and conversion to ngspice happen automatically.

**Prerequisite**: The [SPICE Translator](https://github.com/SJTU-YONGFU-RESEARCH-GRP/new-spice-translator) project must be accessible. The system searches for it in the following order:

1. `--translator-path` command-line argument
2. `SPICE_TRANSLATOR_PATH` environment variable
3. `pip install spice-translator-ir` (pip-installed package)
4. Sibling directory `../new-spice-translator`

```bash
# Set translator location via environment variable
export SPICE_TRANSLATOR_PATH=/path/to/new-spice-translator
spice-benchmark model.scs

# Or via command-line argument
spice-benchmark model.lib --translator-path /path/to/new-spice-translator

# Explicitly specify source format (skip auto-detection)
spice-benchmark model.lib --source-format hspice
spice-benchmark model.scs --source-format spectre
```

The Python API also supports these options:

```python
from spice_model_benchmark import benchmark_spice_model

# HSPICE model with explicit format
benchmark_spice_model("model.lib", source_format="hspice")

# Spectre model with translator path
benchmark_spice_model("model.scs", translator_path="/path/to/new-spice-translator")
```

During conversion, the system:
1. Detects the source format from file extension and content keywords
2. Translates the model to ngspice format using the SPICE Translator
3. Adapts circuit netlists to reference the converted model
4. Runs the standard benchmark pipeline on the converted model

Converted models are saved in `<output-dir>/_converted/`.

```python
from spice_model_benchmark import benchmark_spice_model

# Run with custom circuit files
success = benchmark_spice_model(
    model_file="my_model.inc",
    output_dir="custom_results",
    dc_circuit="custom_dc.cir",
    transient_circuit="custom_transient.cir",
    dpi=600,  # High-resolution plots
    log_level="DEBUG"  # Detailed logging
)
```

### Using the Full Simulation Class

For maximum control, use the `MOSFETSimulation` class directly:

```python
from spice_model_benchmark import MOSFETSimulation

# Create simulation instance with model parsing and on-the-fly netlist generation
sim = MOSFETSimulation(
    model_file="path/to/my_model.inc",
    output_dir="full_control_results",
    dpi=300
)

# Run specific analyses (or all modes)
success = sim.run(modes=["dc", "transient", "ac", "noise"])
```

## Examples

See the `examples/` directory for complete working examples:

- `examples/simple_benchmark.py`: Basic usage with minimal code
- `examples/advanced_benchmark.py`: Advanced usage with custom settings

Run examples with:
```bash
python examples/simple_benchmark.py path/to/your/model.inc
```

## Detailed Instructions

### Preparing Model Files

1. Place your MOSFET model file in the `models/` directory
2. Update the circuit netlists in `netlists/` to reference your model
3. Ensure your model file includes the correct parameters for your device

### Running Simulations

#### Using the Command-Line Interface (Recommended)

After installation, use the `spice-benchmark` command:

```bash
# Run with default settings
spice-benchmark path/to/your/model.inc

# Run with custom output directory
spice-benchmark path/to/your/model.inc --output-dir my_results

# Run only specific analyses
spice-benchmark path/to/your/model.inc --modes dc transient

# Run with high-resolution plots
spice-benchmark path/to/your/model.inc --dpi 600

# Run with HSPICE or Spectre model
spice-benchmark model.lib --source-format hspice
spice-benchmark model.scs --source-format spectre

# Get help
spice-benchmark --help
```

#### Using the Legacy Script

The original script is still available for advanced usage:

```bash
# Change to the src directory
cd src

# Run with default settings
python mosfet_simulation.py

# Run with custom circuit files
python mosfet_simulation.py --dc-circuit ../netlists/custom_dc.cir --transient-circuit ../netlists/custom_trans.cir

# Run specific verification tests only
python mosfet_simulation.py --verify dc,transient

# Run with increased verbosity
python mosfet_simulation.py --verbose

# Run with custom output directory
python mosfet_simulation.py --output-dir ../my_results

# Skip certain simulation types
python mosfet_simulation.py --skip noise,ac

# For more options
python mosfet_simulation.py --help
```

### Interpreting Results

The verification process produces:

1. **Verification Report** (`results/REPORT.md`): A comprehensive document with pass/fail indicators for all verification tests
2. **Raw Data** (`results/data/`): CSV files containing simulation data for further analysis
3. **Visualization Plots** (`results/plots/`): PNG images showing various model characteristics

Key metrics to check in the report:
- ✓/✗ indicators showing pass/fail status for each test
- Detailed measurements and operating point information
- Temperature coefficients and scaling behavior

Additional AC outputs (if `--mode ac` ran successfully):
- `<output-dir>/data/ac_ls_caps_from_cv_integral.csv`: Large-signal capacitances computed from AC C(V) integral along the Vg sweep path.
- `<output-dir>/data/ac_qg_from_cv_integral.csv`: Integrated Qg(Vg) curve derived from Cgg(Vg).

### Customizing Verification Criteria

1. Edit `src/verification_parameters.py` to modify thresholds for verification tests
2. Create custom circuit netlists in the `netlists/` directory
3. Modify plot settings in `src/plot_generator.py` for customized visualizations

## Documentation

For detailed information about the benchmark system, refer to the following documentation:

- [METHODOLOGY.md](docs/METHODOLOGY.md): Comprehensive explanation of the verification methodology and implementation details
- [CHECKLIST.md](docs/CHECKLIST.md): Verification checklist with detailed criteria for each test
- [Benchmarks for SPICE Modeling and Parameter Extraction Based on AI/ML](docs/Benchmarks_for_SPICE_Modeling_and_Parameter_Extraction_Based_on_AI_ML.pdf): Research paper on benchmark methodology

## Directory Structure

```
spice_model_benchmark/
├── docs/                  # Documentation files
│   ├── METHODOLOGY.md     # Detailed verification methodology
│   ├── CHECKLIST.md       # Verification criteria checklist
│   └── Benchmarks_for_SPICE_Modeling_and_Parameter_Extraction_Based_on_AI_ML.pdf
├── examples/              # Usage examples
│   ├── simple_benchmark.py     # Basic usage example
│   └── advanced_benchmark.py   # Advanced usage example
├── models/                # MOSFET model files (git submodule: spice_model_libraries)
├── src/                   # Source code (Python package)
│   ├── __init__.py        # Package initialization & benchmark_spice_model entry
│   ├── cli.py             # Command-line interface (--regression, --circuit-stress, --cross-sim, --pkp3)
│   ├── model_parser.py    # SPICE model & subcircuit parser (.model, .subckt, .lib)
│   ├── netlist_generator.py # Dynamic on-the-fly netlist generator (DC, AC, Tran, Noise, GST)
│   ├── regression_runner.py # Multi-corner & multi-model automated regression across 10 PDKs
│   ├── circuit_stress_runner.py # Inverter, RO, SRAM, OTA circuit stress suite (IEEE TCAD 2026)
│   ├── cross_simulator_benchmark.py # Multi-EDA cross-simulator correlation engine (ngspice, Xyce, HSPICE, Spectre)
│   ├── pkp3_nanosheet_benchmark.py # PKP3 3nm GAAFET PHIMO-Fusion characterization suite
│   ├── rf_analog_benchmarks.py # Higher-order gm2/gm3 derivatives & distortion metrics (IEEE TED 2025)
│   ├── plot_style.py      # dev-plot standard MATLAB-aligned publication styling
│   ├── format_converter.py # HSPICE/Spectre to ngspice format conversion
│   ├── mosfet_simulation.py # Main simulation controller
│   ├── data_reader.py     # Read and parse simulation results
│   ├── plot_generator.py  # Generate plots from simulation data
│   ├── simulation_runner.py # Execute SPICE simulations
│   ├── verification_manager.py # Verify and report results
│   ├── verification_parameters.py # Configurable verification parameters
│   └── logger.py          # Logging utilities
├── pyproject.toml         # Modern Python packaging configuration
├── requirements.txt       # Legacy dependency specification
├── results/               # Simulation results (example)
│   ├── data/              # Raw data files
│   ├── plots/             # Generated plots and visualizations
│   └── REPORT.md          # Verification report
└── README.md              # This file
```

## Key Features

### Comprehensive Verification

- **DC Analysis**: Verifies IV characteristics, subthreshold behavior, saturation behavior, and KCL compliance
- **Temperature Analysis**: Validates behavior across -40°C to 150°C range, temperature coefficients
- **Transient Analysis**: Tests transient response, switching behavior, delay effects, power dissipation
- **AC Analysis**: Examines CV characteristics, S-parameters, and non-quasi-static effects
- **AC-Integral LS Caps**: Computes large-signal effective capacitances from AC C(V) by voltage integration (e.g., Cgg_ls from Cgg(Vg))
- **Noise Analysis**: Characterizes thermal, flicker (1/f), and shot noise across frequencies and bias points

### Visualization

The system generates detailed plots for different aspects of the device behavior:

- IV characteristics curves with log-scale insets for subthreshold behavior
- Capacitance-voltage plots showing gate capacitance components
- S-parameter plots for RF/high-frequency performance
- Noise spectra across different frequencies and temperatures
- Transient analysis visualizations for timing and switching performance
- Temperature-dependent behavior visualization
- Charge conservation plots

### Automated Reporting

The verification process generates a comprehensive Markdown report that includes:
- Summary tables for each analysis domain
- Detailed verification results with pass/fail indicators
- Key metrics and parameters extracted from simulations
- Embedded plots for visual verification
- Tables of measured values for further analysis

## Requirements

### System Requirements
- Python 3.8+
- NGSPICE (version 30 or newer recommended)

### Python Dependencies
When installed via pip, all dependencies are automatically managed:
- NumPy >= 1.21.0
- Matplotlib >= 3.4.0
- Pandas >= 1.3.0
- SciPy >= 1.7.0
- tqdm >= 4.62.0
- colorama >= 0.4.4

### Manual Installation
If installing manually, install dependencies with:
```bash
pip install numpy matplotlib pandas scipy tqdm colorama
```

## Troubleshooting

### Common Issues

1. **NGSPICE not found**: Ensure NGSPICE is installed and in your system path
   ```bash
   which ngspice  # Should return a path
   ngspice --version  # Should display version information
   ```

2. **Missing simulation data**: Check that your model file is correctly referenced in the netlists

3. **Failed verification tests**: Examine the specific test details in REPORT.md to understand which aspects of the model need improvement

4. **Visualization errors**: Ensure your Python environment has matplotlib properly installed

### Getting Help

For additional issues, please file an issue on the GitHub repository or contact the repository maintainers.

## License

This project is provided as open-source software under the MIT License. See LICENSE file for details.

## Citation

If you use this benchmark system in your research, please cite:

```
@software{spice_model_benchmark,
  author = {Your Name},
  title = {SPICE Model Benchmark System},
  year = {2023},
  url = {https://github.com/yourusername/spice_model_benchmark}
}
``` 