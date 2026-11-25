# IEEE TCAD Publication Plan: AutoBench-CM

**Target Journal**: *IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems* (IEEE TCAD)  
**Article Type**: Regular Research Paper (12–14 double-column pages, IEEEtran template)  
**Working Title**:  
> **"AutoBench-CM: A Unified Multi-EDA Verification and Circuit-Convergence Benchmarking Framework for Advanced and Neural Compact Models"**  
*(Alternative Title: "From Curve Fitting to Circuit Convergence: An Automated Multi-Domain Quality-Assurance Platform and Physics-Guaranteed Neural Compact Model Architecture")*

---

## 1. Executive Summary & Research Motivation

### 1.1 The Crisis in Compact Modeling & ML-Based EDA
Compact models serve as the indispensable mathematical interface between semiconductor physics and circuit design. However, as semiconductor technology scales to sub-3nm nanosheets (GAAFET) and complex heterogeneous nodes, developing classical analytical models (BSIM-CMG, PSP) has become an engineering bottleneck requiring multi-year derivation and thousands of calibration parameters.

While machine learning (ML) and neural network compact models (Base-ANN, Sym-ANN, Grad-ANN, Phys-ANN) have emerged to accelerate model generation, their deployment in production EDA environments is severely blocked by what the literature terms the **"Curve-Fitting Trap"**:
- **Fitting Accuracy $\neq$ Physical Viability**: An ML model achieving $R^2 > 0.999$ on DC $I$-$V$ curves frequently exhibits transconductance oscillations ($g_m, g_{ds}, g_{m3}$ ripples), violating Jacobian smoothness and causing Newton-Raphson non-convergence in SPICE.
- **Physical Inconsistencies**: Models violate thermodynamic passivity ($I_{ds}(0, 0) \neq 0$ generating artificial DC energy), fail Gummel symmetry ($I_{ds}(V_{ds}) \neq -I_{ds}(-V_{ds})$) leading to failure in bidirectional transmission gates, or fail dynamic charge conservation ($\sum Q \neq 0$).
- **Multi-Domain Blind Spots**: As diagnosed in recent literature (**Colin C. McAndrew et al., IEEE TED 2025** and **Hongwei Yao et al., NeuralCM-QA, IEEE TCAD 2026**), published neural models routinely:
  1. Completely omit intrinsic noise physics ($S_{th} + 1/f$ noise spectral density is identically zero).
  2. Fix device temperature to room temperature ($300\text{ K}$), incapable of multi-temperature circuit simulation ($-40^\circ\text{C}$ to $+125^\circ\text{C}$).
  3. Lack automated transpilation, relying on brittle, manually authored Verilog-A templates prone to compilation syntax crashes.
  4. Are evaluated only on open-source simulators (ngspice) with synthetic data, never tested against commercial EDA standards (Spectre, HSPICE), commercial foundry PDKs with proprietary C-plugins (TSMC TMI), or statistical mismatch yield (Pelgrom's Law).

### 1.2 Our Core Scientific Proposal
This paper presents a **closed-loop solution** to this crisis:
1. **The Testing Platform (AutoBench-CM)**: An automated, push-button, and netlist-independent quality-assurance platform evaluating arbitrary compact models across 5 physical domains (DC, AC, Transient, Noise, and Temperature) and 4 canonical circuit stress benchmarks across 4 major EDA engines (`ngspice 45.2`, `Sandia XyceNF 7.10.0`, `Synopsys HSPICE S-2021.09`, `Cadence Spectre 24.1.0`).
2. **The Exemplar Solution (PINN-CM)**: A production-ready Physics-Informed Neural Compact Model calibrated on real GlobalFoundries GF180MCU silicon data that systematically resolves all open limitations of NeuralCM-QA (automated PyTorch-to-Verilog-A transpiler, $V_{ds}^2$ topological Gummel symmetry, zero-bias passivity, intrinsic noise, dynamic thermal scaling, and 100% convergence across all circuit benchmarks).

---

## 2. Core Contributions & Novelty Claims

| Innovation Dimension | State of the Art (NeuralCM-QA, IEEE TCAD 2026) | Our Proposed AutoBench-CM + PINN-CM Framework |
|:---|:---|:---|
| **Netlist Architecture** | Hardcoded static netlist templates per model; manual pin matching. | **100% Netlist-Independent**: Dynamic introspection of arbitrary model cards (`.inc`, `.lib`, `.scs`, `.va`) with on-the-fly multi-mode simulation synthesis. |
| **EDA Toolchain Scope** | Evaluated on single backend (OpenVAF + ngspice). | **Full Cross-EDA Matrix**: Automated correlation across 4 industry engines (`ngspice`, `Xyce`, `HSPICE`, `Spectre`) with quantitative $NRMSD$ & $R^2$ matrices. |
| **Foundry PDK Compatibility** | Academic / open-source PDKs only (FreePDK45, 5nm TCAD). | **Commercial PDK Engine**: Verified across 5 commercial PDKs (`Cadence GPDK45`, `Synopsys SAED14/32`, `SMIC 180nm BCD`, `TSMC 16FFC` with native **TMI C-plugin**). |
| **Statistical Variation & Yield** | Strictly nominal (TT corner); zero variation support. | **Pelgrom Mismatch Engine**: Evaluates device distribution moments ($\mu, \sigma, CV\%$, skewness, kurtosis) and 6T-SRAM Hold/Read SNM yield ($P(\text{fail})$). |
| **Static Code Quality** | Basic OpenVAF syntax grammar checking. | **7-Rule Static Physical Linter**: Audits dynamic temperature, noise declarations, Gummel parity, zero-bias passivity, and Spectre AHDL dialect detection with SHA256 caching. |
| **Neural Code Generation** | *Identified as future work* (manual Verilog-A coding). | **Automated Transpilation Pipeline**: End-to-end PyTorch-to-Verilog-A code generator with OpenVAF binary OSDI compilation. |
| **Multi-Domain Physics** | DC and AC only; **zero noise**; static $300\text{ K}$ temp. | **5-Domain Full Coverage**: Native thermal white noise + $1/f$ flicker noise, plus differentiable thermal scaling ($-40^\circ\text{C}$ to $+125^\circ\text{C}$). |
| **Silicon Calibration** | Synthetic BSIM4 simulations & TCAD decks. | **Calibrated on Real Silicon Tape-Out Data** (GlobalFoundries GF180MCU MESD dataset `N180B`). |

---

## 3. Streamlined Manuscript Blueprint (6 Core Sections)

To conform to standard **IEEE TCAD / IEEE TED** article structure and avoid thematic fragmentation, the manuscript is organized into **6 cohesive sections**:

```
+--------------------------------------------------------------------------------------------------------+
|                                    6-SECTION MANUSCRIPT BLUEPRINT                                      |
+--------------------------------------------------------------------------------------------------------+
| Section I   | Introduction: The Limitations of Pure I-V Fitting in Modern EDA Compact Modeling        |
| Section II  | Prior Art & Physical Consistency Requirements (BSIM, NeuralCM-QA, McAndrew TED 2025)     |
| Section III | AutoBench-CM: Architecture, Multi-Domain Auditing, & Circuit Stress Benchmarks           |
| Section IV  | Multi-EDA Cross-Simulator Correlation & Commercial Foundry PDK Verification              |
| Section V   | Case Study & Experimental Validation: Physics-Informed Neural Compact Modeling (PINN-CM) |
| Section VI  | Conclusion & Open-Source Perspectives                                                    |
+--------------------------------------------------------------------------------------------------------+
```

---

### Section I: Introduction
- **1.1 The Scaling Challenge**: From Bulk CMOS to FinFET, GAAFET nanosheets, and multi-gate 3D architectures; the exponential rise in compact model formulation complexity.
- **1.2 The "Curve-Fitting Trap"**: Why low RMSE ($R^2 > 0.999$) on DC curves is deceptively inadequate; Jacobian stiffness, non-smooth derivative ripples, time-step collapse, and symmetry violations.
- **1.3 Limitations of Prior Verification Frameworks**: Multi-domain blind spots in recent academic efforts (missing noise, static 300K temperature, reliance on static netlists, absence of commercial EDA correlation).
- **1.4 Paper Contributions & Organization**: Summary of AutoBench-CM platform and PINN-CM exemplar solution.

### Section II: Prior Art & Physical Consistency Requirements
- **2.1 Standard vs. Emerging Compact Models**: BSIM4 (Level 54), BSIM-CMG (Level 72), PSP (Level 103), and emerging neural compact models (ANN, PINN, PHIMO-Fusion).
- **2.2 Review of ML Compact Models & Prior QA**: In-depth analysis of NeuralCM-QA (IEEE TCAD 2026), APEX, and PCNN; failure mode taxonomy (Type A: Syntax, Type B: Physical Inconsistency, Type C: Numerical Stiffness, Type D: Multi-Domain Omission).
- **2.3 Standards Conformance**: Four essential physical criteria defined by Colin C. McAndrew et al. (IEEE TED 2025): thermodynamic passivity, Gummel symmetry parity, dynamic multi-domain coverage, and numerical smoothness.

### Section III: AutoBench-CM System Architecture & Benchmarking Methodology
- **3.1 Dynamic Model Card Introspection & On-the-Fly Synthesis**:
  - Parsing hierarchical `.inc`, `.lib`, `.scs`, and `.va` files.
  - Automatic port topology inference, polarity detection, and parameter extraction.
  - On-the-fly synthesis of clean, isolated SPICE simulation decks in memory without static netlists.
- **3.2 Multi-Domain Physical Quality Auditing**:
  - **DC & Higher-Order Linearity**: Transconductance continuity ($G_m, G_{ds}$) and polynomial derivatives ($G_{m2}, G_{m3}, VIP_2, VIP_3, IIP_3$).
  - **Gummel Symmetry Test (GST)**: Exact odd-function parity ($I_{ds}(V_{ds}) = -I_{ds}(-V_{ds})$) and derivative parity ($G_x$ even, $G_{xx}$ odd).
  - **Zero-Bias Passivity & Charge Conservation**: $I_{ds}(0, V_{gs}) \equiv 0.0\text{ A}$ identically; multi-terminal charge neutrality ($Q_s = -(Q_g + Q_d + Q_b)$).
  - **Dynamic Thermal Scaling**: Differentiable thermal voltage $V_t(T)$, threshold drift $V_{th}(T)$, and mobility degradation across $-40^\circ\text{C}$ to $+150^\circ\text{C}$.
  - **Intrinsic Noise Spectral Density**: Verification of white thermal noise ($S_{th} = 4 k_B T \gamma g_m$) and $1/f$ flicker noise ($S_{1/f} \propto I_{ds}^{A_F}/f$).
- **3.3 Circuit-Level Stress Convergence Harness**:
  - **CMOS Inverter**: VTC switching threshold ($V_M$), gain ($|A_{v,\max}|$), noise margins ($NM_L, NM_H$), propagation delay ($\tau_{pd}$), dynamic cycle energy ($E_{cycle}$).
  - **Ring Oscillator (RO3)**: 3-stage self-starting transient dynamics, gate delay ($\tau_{stage}$), and time-step collapse avoidance ($\min(\Delta t)$).
  - **6T-SRAM Memory Latch**: Decoupled Hold and Read stress DC sweeps; Seevinck 45° coordinate rotation transformation extracting Hold SNM and Read SNM butterfly margins.
  - **5T-OTA**: Open-loop DC differential gain ($A_0$), Unity-Gain Bandwidth ($GBW$), and Phase Margin ($PM$).
- **3.4 Static Physical Linting & OpenVAF OSDI Compilation**:
  - 7-rule pre-simulation physical audit (`RULE_TEMP_DYNAMIC`, `RULE_INTRINSIC_NOISE`, `RULE_GUMMEL_SYMMETRY`, `RULE_ZERO_BIAS_PASSIVITY`, `RULE_CONTINUITY_SMOOTHNESS`, `RULE_CHARGE_CONSERVATION`, `RULE_DIALECT_COMPATIBILITY`).
  - Automated binary compilation into `.osdi` libraries with incremental SHA256 caching.

### Section IV: Multi-EDA Cross-Simulator Correlation & Industrial PDK Verification
- **4.1 Multi-EDA Cross-Simulator Correlation Engine**:
  - Automated co-simulation of identical model cards across 4 industry simulators: `ngspice 45.2`, `Sandia XyceNF 7.10.0`, `Synopsys HSPICE S-2021.09`, and `Cadence Spectre 24.1.0`.
  - Quantitative cross-correlation metrics: Normalized Root-Mean-Square Deviation ($NRMSD$) and coefficient of determination ($R^2$).
- **4.2 Commercial Foundry PDK Multi-Corner & C-Plugin Verification**:
  - Native verification across Cadence GPDK045 (`spectre`), Synopsys SAED14/SAED32 (`hspice`), and SMIC 180nm BCD (`hspice`).
  - Automated integration of TSMC's proprietary **TMI (TSMC Model Interface)** C-plugin shared library (`libTMImodel.so`), validating multi-fin 3D FinFET (16FFC) Level 72 models.
- **4.3 Statistical Variation & Memory Yield Modeling**:
  - Parametric mismatch based on Pelgrom's Law ($\sigma(\Delta V_{th}) = A_{Vth} / \sqrt{WL}$).
  - Device distribution moments ($\mu, \sigma, CV\%$, skewness, kurtosis, $\pm 3\sigma$).
  - Mapping device-level statistical spreads to 6T-SRAM Hold/Read SNM margin collapse and failure rates ($P(\text{fail}) = P(SNM \le 0)$).

### Section V: Case Study & Experimental Validation: Physics-Informed Neural Compact Modeling (PINN-CM)
- **5.1 Addressing the Open Gaps of Prior Art (NeuralCM-QA)**:
  - Systematic comparison against NeuralCM-QA's Base-ANN, Sym-ANN, Grad-ANN, and Phys-ANN architectures.
- **5.2 Mathematical Formulation & Physics Guarantees**:
  - **Topological Symmetry Formulation**: $I_{ds} = V_{ds} \cdot \mathcal{F}_{\text{even}}(V_{ds}^2, V_{gs}, V_{bs}, T, W, L)$, guaranteeing exact Gummel symmetry and zero-bias passivity by network topology rather than penalty loss.
  - **Differentiable Thermal Embedding**: Physical temperature modeling from $-40^\circ\text{C}$ to $+125^\circ\text{C}$.
  - **Dynamic Conservative Charges & Intrinsic Noise**: Complete synthesis of $Q_s = -(Q_g + Q_d + Q_b)$, `white_noise()`, and `flicker_noise()`.
- **5.3 Automated PyTorch-to-Verilog-A Transpilation**:
  - End-to-end code generator transpiling trained neural weights into human-readable IEEE Verilog-A code and OpenVAF OSDI binaries.
- **5.4 Silicon Calibration on GlobalFoundries GF180MCU**:
  - Training on real tape-out silicon electrical measurements (`N180B-nmos1`).
- **5.5 Experimental Results & Cross-PDK Showdown**:
  - Full multi-domain and circuit stress benchmark results (Inverter, RO, 6T-SRAM, OTA) across 15+ technology nodes (180nm Bulk to 2nm GAAFET).
  - Head-to-head comparison demonstrating PINN-CM's 100% convergence and full multi-domain physical coverage.

### Section VI: Conclusion & Future Outlook
- Summary of findings, open-source platform availability, and implications for AI-driven semiconductor modeling.

---

## 4. Figures & Tables Manifest

### 4.1 Planned Figures

| Figure # | Planned Caption & Visual Contents | Data Source / Artifact Path |
|:---:|:---|:---|
| **Fig. 1** | **Overall AutoBench-CM Framework Architecture**: Block diagram showing dynamic introspection, on-the-fly netlist generator, 5-domain physical audit, circuit stress harness, and multi-EDA backends. | Conceptual Diagram (draw.io / TikZ) |
| **Fig. 2** | **Multi-Domain Physics & Derivative Smoothness**: Higher-order transconductance derivatives ($G_m, G_{ds}, G_{m2}, G_{m3}$) and $VIP_3$ linearity curves showing absence of ripples. | `results/data/` & RF derivatives |
| **Fig. 3** | **Gummel Symmetry Test (GST) Parity Verification**: Symmetrical $I_{ds}$ vs. $V_{ds} \in [-0.1\text{V}, +0.1\text{V}]$ sweeps and odd-derivative parity across zero bias. | `results/pkp3_characterization/plots/` |
| **Fig. 4** | **Circuit-Level Stress Convergence Waveforms**: (a) CMOS inverter VTC with unit-gain points; (b) 3-stage ring oscillator transient self-starting oscillations; (c) 6T-SRAM Hold/Read butterfly curves with Seevinck rotation; (d) 5T-OTA differential transfer and AC Bode plot. | `results/circuit_stress/plots/` |
| **Fig. 5** | **Multi-EDA Cross-Simulator Correlation Overlay**: Comparative $I_d$-$V_{gs}$ curves across ngspice, Xyce, HSPICE, and Spectre for FreePDK45 and ASAP7. | `results/cross_simulator/plots/` |
| **Fig. 6** | **Commercial Foundry PDK Benchmark Overlay**: Multi-corner drive currents ($I_{on}$) and CMOS inverter VTC curves across Cadence GPDK45, SAED14, SAED32, SMIC 180nm BCD, and TSMC 16FFC. | `results/commercial_pdk/plots/commercial_pdk_drive_comparison.svg` & `commercial_inverter_vtc_overlay.svg` |
| **Fig. 7** | **Statistical Variation & Monte Carlo Mismatch**: (a) Gaussian distributions for $I_{on}$ and $V_{th}$ with $\pm 3\sigma$ bounds; (b) Inverter switching threshold $V_M$ spread; (c) 6T-SRAM Hold and Read SNM distributions under Pelgrom mismatch. | `results/monte_carlo/plots/monte_carlo_device_spread.svg` & `monte_carlo_sram_snm_yield.svg` |
| **Fig. 8** | **Verilog-A Physical Linter & OpenVAF Compilation Flow**: 7-rule audit diagnostics, score radar chart, and SHA256-cached OSDI shared library compilation. | `results/veriloga/VERILOGA_LINT_REPORT.md` |
| **Fig. 9** | **Architecture of the Proposed PINN-CM**: Neural conductance network $\mathcal{F}_{\text{even}}(V_{ds}^2)$, differentiable physical temperature embedding, dynamic charge branch, and intrinsic noise generator. | `proj/src/pinn_model.py` block diagram |
| **Fig. 10** | **PINN-CM Silicon Calibration on GF180MCU**: Measured silicon tape-out data vs. PINN-CM predicted curves across multi-bias DC sweeps and dynamic temperatures ($-40^\circ\text{C}$ to $+125^\circ\text{C}$). | `proj/data/N180B-nmos1.json` vs. model output |
| **Fig. 11** | **Intrinsic Noise Spectral Density Verification**: Simulated output current noise $S_{id}(f)$ showing thermal noise floor and $1/f$ flicker noise slope for PINN-CM. | `proj/models/nfet_03v3_pinn.va` noise simulation |
| **Fig. 12** | **Circuit Convergence Comparison (PINN-CM vs. NeuralCM-QA Models)**: Transient waveforms of 3-stage RO and 6T-SRAM SNM butterfly curves comparing Base-ANN, Sym-ANN, Grad-ANN, and PINN-CM. | Co-simulated waveforms |

### 4.2 Planned Tables

| Table # | Table Title & Contents | Primary Data Source |
|:---:|:---|:---|
| **Table I** | **Multi-Domain Physics & Simulation Compliance Audit**: 11 compact models across 5 SPICE domains (DC, AC, Tran, Noise, Temp). | `README.md` & `results/circuit_stress/` |
| **Table II** | **Circuit Stress Performance Matrix**: Technology nodes (180nm to 2nm GAAFET), Inverter $V_M$, delay $\tau_{pd}$, RO $f_{osc}$, Hold SNM, Read SNM, OTA gain, and runtime. | `results/circuit_stress/CIRCUIT_STRESS_SUMMARY.md` |
| **Table III** | **Multi-EDA Cross-Simulator Correlation Matrix**: Quantitative $NRMSD$ and $R^2$ values across ngspice, Xyce, HSPICE, and Spectre. | `results/cross_simulator/cross_simulator_summary.json` |
| **Table IV** | **Commercial Foundry PDK Benchmark Metrics**: Multi-corner $I_{on}, V_{th}, G_m$, and inverter VTC metrics for Cadence GPDK45, SAED14, SAED32, SMIC 180nm, and TSMC 16FFC. | `results/commercial_pdk/commercial_pdk_summary.json` |
| **Table V** | **Statistical Variation & SRAM Yield Moments**: Statistical distributions ($\mu, \sigma, CV\%$, skewness, kurtosis, $\pm 3\sigma$) and failure rates for device and SRAM SNM. | `results/monte_carlo/monte_carlo_summary.json` |
| **Table VI** | **Verilog-A Physical Linter & OpenVAF Evaluation**: 7-rule audit pass/fail status, numerical scores, and OSDI compilation times across 4 candidate compact models. | `results/veriloga/veriloga_lint_summary.json` |
| **Table VII** | **Head-to-Head Comparison: NeuralCM-QA vs. PINN-CM**: Systematic comparison of Base-ANN, Sym-ANN, Grad-ANN, Phys-ANN, and PINN-CM across all physical and circuit metrics. | Synthesis of Table I, `analysis.md`, and `proj/` |

---

## 5. Execution Roadmap & Writing Milestones

```
+---------------------------------------------------------------------------------------------------------+
|                                    IEEE TCAD MANUSCRIPT TIMELINE                                        |
+---------------------------------------------------------------------------------------------------------+
| Phase 1: Environment & Skeleton Setup   | LaTeX template (IEEEtran.cls), BibTeX library, outline.       |
| Phase 2: Publication Figure Generation  | Vector SVG & 600 DPI PNG figures via dev-plot styling.       |
| Phase 3: Drafting Sections I & II       | Introduction, Prior Art, and Physical Consistency Criteria.   |
| Phase 4: Drafting Section III           | AutoBench-CM Architecture, Multi-Domain Auditing & Stress.    |
| Phase 5: Drafting Section IV            | Cross-EDA Correlation, Commercial PDKs (TMI) & Pelgrom Yield. |
| Phase 6: Drafting Section V             | Case Study: PINN-CM Formulation, Silicon Data & NeuralCM-QA.  |
| Phase 7: Synthesis, Review & Polish     | Section VI (Conclusion), Abstract, Cover Letter, IEEE check.  |
+---------------------------------------------------------------------------------------------------------+
```

### Detailed Phase Tasks

- [ ] **Phase 1: Environment & Repository Setup**
  - Create `publications/writings/tcad/` workspace layout:
    - `src/` (LaTeX source files split by section: `sec1_intro.tex`, `sec2_prior_art.tex`, `sec3_autobench.tex`, `sec4_multieda.tex`, `sec5_casestudy.tex`, `sec6_conclusion.tex`)
    - `figures/` (Vector PDF/SVG figures)
    - `tables/` (Formatted LaTeX tables)
    - `IEEEtran.cls` & `IEEEtran.bst`
  - Compile master `references.bib` integrating citations from:
    - McAndrew et al. (IEEE TED 2025)
    - Yao et al. (NeuralCM-QA, IEEE TCAD 2026)
    - Standard BSIM4 / BSIM-CMG / PSP compact modeling references
    - OpenVAF compiler (IEEE CICC / DAC)
    - Commercial simulator manuals (Spectre, HSPICE)

- [ ] **Phase 2: Publication Figure & Table Rendering**
  - Export all figures from `results/*/plots/` to standalone publication vector PDFs.
  - Generate high-contrast circuit schematics (RO3, 6T-SRAM, 5T-OTA, Inverter) in TikZ/vector format.
  - Transcribe JSON summaries (`circuit_stress_summary.json`, `commercial_pdk_summary.json`, `monte_carlo_summary.json`, `veriloga_lint_summary.json`) into clean LaTeX tables with consistent booktabs formatting.

- [ ] **Phase 3: Drafting Sections I & II (Motivation & Standards)**
  - Draft Section I (The Scaling Challenge, Curve-Fitting Trap, and Paper Outline).
  - Draft Section II (Compact modeling background, NeuralCM-QA critique, McAndrew TED 2025 criteria).

- [ ] **Phase 4: Drafting Sections III & IV (AutoBench-CM Core & Multi-EDA Platform)**
  - Draft Section III (Dynamic model parsing, 5-domain physical audit, circuit stress harness, static 7-rule linter).
  - Draft Section IV (Cross-simulator correlation, commercial PDK verification with TSMC TMI, Pelgrom Monte Carlo SRAM yield).

- [ ] **Phase 5: Drafting Section V (PINN-CM Case Study & Silicon Validation)**
  - Draft Section V-A & V-B (Mathematical formulation of PINN-CM, topological symmetry $V_{ds}^2$, differentiable thermal embedding, noise).
  - Draft Section V-C & V-D (Silicon tape-out calibration on GF180MCU and cross-PDK validation).
  - Draft Section V-E (Head-to-head comparison vs. NeuralCM-QA Base/Sym/Grad/Phys-ANN models).

- [ ] **Phase 6: Final Polish & Submission Package**
  - Draft Section VI (Conclusion & Open-Source Perspectives) and Abstract.
  - Multi-pass mathematical check of all equations and variables.
  - Verify compliance with IEEE TCAD author guidelines (two-column layout, caption styling, author bios).
  - Prepare cover letter highlighting relevance to the EDA/TCAD community.
