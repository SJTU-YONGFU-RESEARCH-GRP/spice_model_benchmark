# MOSFET Simulation Verification Report
Generated on: 2026-11-23 16:25:48

## Table of Contents
1. [Simulation Setup and Execution](#1-simulation-setup-and-execution)
2. [Summary](#2-summary)
   - [DC Analysis Summary](#dc-analysis-summary)
   - [AC Analysis Summary](#ac-analysis-summary)
   - [Transient Analysis Summary](#transient-analysis-summary)
   - [Noise Analysis Summary](#noise-analysis-summary)
3. [DC Analysis](#3-dc-analysis)
   - [DC Operating Point Analysis](#dc-operating-point-analysis)
   - [Bias Point Analysis](#bias-point-analysis)
   - [Temperature Analysis](#temperature-analysis)
   - [Thermodynamic Analysis](#thermodynamic-analysis)
   - [Physical Properties Analysis](#physical-properties-analysis)
4. [AC Analysis](#4-ac-analysis)
   - [Small-Signal Analysis](#small-signal-analysis)
   - [S-Parameter Analysis](#s-parameter-analysis)
   - [Non-Quasi-Static (NQS) Effects Analysis](#non-quasi-static-effects-analysis)
   - [Charge Conservation Analysis](#charge-conservation-analysis)
5. [Transient Analysis](#5-transient-analysis)
   - [Large-Signal Transient](#large-signal-transient)
   - [Switching Simulations](#switching-simulations)
   - [Delay Effect Simulations](#delay-effect-simulations)
6. [Noise Analysis](#6-noise-analysis)
   - [Thermal Noise Analysis](#thermal-noise-analysis)
   - [Flicker Noise Analysis](#flicker-noise-analysis)
   - [Shot Noise Analysis](#shot-noise-analysis)

## Notes
- This report is automatically generated based on mosfet_simulation.py
- Items are marked with <span style='color: green'>✓</span> for success and <span style='color: red'>✗</span> for failure
- Any deviations from expected behavior should be documented

## 1. Simulation Setup and Execution
- [<span style='color: green'>✓</span>] Circuit file exists and is readable
  - Path: /data1/yongfu/proj/spice_model_benchmark/netlists/dc_circuit.cir, /data1/yongfu/proj/spice_model_benchmark/netlists/transient_circuit.cir, /data1/yongfu/proj/spice_model_benchmark/netlists/noise_circuit.cir, /data1/yongfu/proj/spice_model_benchmark/netlists/ac_circuit.cir
- [<span style='color: green'>✓</span>] ngspice is properly installed
  - Version: ngspice-45.2
- [<span style='color: green'>✓</span>] Simulation runs without errors
- [<span style='color: red'>✗</span>] Circuit file exists and is readable
  - Path: Not available
- [<span style='color: red'>✗</span>] ngspice is properly installed
  - Version: Not available
- [<span style='color: red'>✗</span>] Simulation runs without errors

## 2. Summary
### DC Analysis Summary
| Test Type | Status | Key Findings |
|-----------|--------|-------------|
| [DC Operating Point Analysis](#dc-operating-point-analysis) | <span style='color: green'>✓</span> | VDS: 0.00V to 1.20V, VGS: 0.00V to 1.20V, IDS: -1.79e-02A to 2.87e-08A |
| [Bias Point Analysis](#bias-point-analysis) | <span style='color: green'>✓</span> | Points: 9 VDS points, 9 VGS points, Currents: IDS: -1.53e-02A to 2.71e-08A, IG: -3.73e-07A to 1.34e-08A, IS: 1.01e-39A to 1.53e-02A, IB: -1.42e-38A to 3.30e-07A, KCL Error: 0.00%, Power: 0.00e+00W to 1.84e-02W, Temp: -40°C |
| [Temperature Analysis](#temperature-analysis) | <span style='color: green'>✓</span> | Temp Points: [np.int64(-40), np.int64(0), np.int64(25), np.int64(50), np.int64(100), np.int64(150)], TC: 0.000015 /°C, IDS: -1.793e-02A to 2.870e-08A |
| [Thermodynamic Analysis](#thermodynamic-analysis) | <span style='color: green'>✓</span> | Power: 0.000e+00W to 2.151e-02W, Efficiency: 7.992e+00 to 1.622e+10, TC: 8.34e-04/°C |
| [Gummel Symmetry Test (GST)](#physical-properties--symmetry-analysis) | <span style='color: green'>✓</span> | Asymmetry Error: 0.00e+00, Odd/Even Symmetry: Pass |
| [Zero-Bias Passivity](#physical-properties--symmetry-analysis) | <span style='color: green'>✓</span> | Max Leakage: 1.42e-38 A, Passive: Pass |
| [3rd-Order Derivatives (Gm3) & Vth](#physical-properties--symmetry-analysis) | <span style='color: green'>✓</span> | Vth: 0.309 V, Peak Gm: 1.7150e-02 S, Gm3 Ripple-free: Pass |
| [Output Conductance & Higher Derivatives (Gds3)](#physical-properties--symmetry-analysis) | <span style='color: green'>✓</span> | Gds Saturation: 3.2418e-03 S, Derivatives Finite: Pass |
| [Asymptotic Extrapolation Testing](#physical-properties--symmetry-analysis) | <span style='color: green'>✓</span> | Vgs=-2V Leakage: 4.8363e-02 A, Overdrive (2.5V): 3.0140e-02 A, Stable: Pass |
| [Dynamic Self-Heating ($g_o(f)$ Dispersion)](#physical-properties--symmetry-analysis) | <span style='color: green'>✓</span> | Dispersion Ratio: 0.3400, Thermal Pole: 6.31e+10 Hz |

### AC Analysis Summary
| Test Type | Status | Key Findings |
|-----------|--------|-------------|
| [Small Signal Analysis](#small-signal-analysis) | <span style='color: green'>✓</span> | Gate capacitance range: 7.08fF to 13.98fF |
| [S-Parameter Analysis](#s-parameter-analysis) | <span style='color: green'>✓</span> | S11 range: -0dB to -0dB, S21 range: 2dB to 2dB |
| [Non-Quasi-Static (NQS) Effects Analysis](#non-quasi-static-effects-analysis) | <span style='color: green'>✓</span> | Max phase shift: 179.997 |
| [Charge Conservation Analysis](#charge-conservation-analysis) | <span style='color: green'>✓</span> | Total charge error: 0.0 |

### Transient Analysis Summary
| Test Type | Status | Key Findings |
|-----------|--------|-------------|
| [Large-Signal Transient](#large-signal-transient) | <span style='color: green'>✓</span> | Max Current: 3.111e-05A, Rise Time: 0.1ps |
| [Switching Simulations](#switching-simulations) | <span style='color: green'>✓</span> | Propagation Delay: 10.2ps, Power: 5.658e-03W (max), 3.619e-04W (avg) |
| [Delay Effect](#delay-effect-simulations) | <span style='color: green'>✓</span> | Total Chain Delay: 25.5ps |
| [Power Dissipation](#transient-simulations-for-power-dissipation) | <span style='color: green'>✓</span> | Temp Coeff: -1.715215e-05W/°C |
| [Quasi-Static Analysis](#quasi-static-analysis) | <span style='color: green'>✓</span> | I-V characteristics analyzed: None |
| [Charge Conservation](#charge-conservation-tests) | <span style='color: green'>✓</span> | Error: None |

### Noise Analysis Summary
| Test Type | Status | Key Findings |
|-----------|--------|-------------|
| [Thermal Noise](#thermal-noise-analysis) | <span style='color: green'>✓</span> | Floor: 3.44e-09 V²/Hz, Range: 2.16e-15 to 1.36e-08 V²/Hz |
| [Flicker (1/f) Noise](#flicker-noise-analysis) | <span style='color: green'>✓</span> | Exponent: 0.5075, Corner Freq: 1.12e+00 Hz |
| [Shot Noise](#shot-noise-analysis) | <span style='color: green'>✓</span> | Level: 3.79e-09 V²/Hz, Variation: 1.4676 |
| [Temperature Dependence](#temperature-dependence) | <span style='color: green'>✓</span> | Coefficient: 2.77e-11 V²/Hz/°C, Range: -40.0°C to 150.0°C |
| [Bias Dependence](#bias-dependence) | <span style='color: green'>✓</span> | Analyzed at 6 bias points |

## 3. DC Analysis
### DC Operating Point Analysis
- [<span style='color: green'>✓</span>] IV data file is generated
- [<span style='color: green'>✓</span>] Data points are properly read
- [<span style='color: green'>✓</span>] Vds values are within range
  - Range: 0.00V to 1.20V
- [<span style='color: green'>✓</span>] Vgs values are within range
  - Range: 0.00V to 1.20V
- [<span style='color: green'>✓</span>] Drain current (Ids) is properly measured
  - Range: -1.79e-02A to 2.87e-08A

*IV Characteristics showing drain current vs drain-source voltage*

<img src='plots/dc_iv_characteristics.png' alt='IV Characteristics' width='400'/>

### Bias Point Analysis
- [<span style='color: green'>✓</span>] Voltage Biasing Points
  - Points: 9 VDS points, 9 VGS points
- [<span style='color: green'>✓</span>] Current Range
  - IDS: -1.53e-02A to 2.71e-08A
  - IG: -3.73e-07A to 1.34e-08A
  - IS: 1.01e-39A to 1.53e-02A
  - IB: -1.42e-38A to 3.30e-07A
- [<span style='color: green'>✓</span>] KCL Error Range
  - KCL Error: 0.00%

*KCL verification showing current balance*

<img src='plots/dc_kcl_verification.png' alt='KCL Verification' width='400'/>

### Temperature Analysis
- [<span style='color: green'>✓</span>] Temperature sweep is performed
  - Points: [np.int64(-40), np.int64(0), np.int64(25), np.int64(50), np.int64(100), np.int64(150)]
- [<span style='color: green'>✓</span>] Temperature coefficient is calculated
  - Temperature Coefficient: 0.000015 /°C
- [<span style='color: green'>✓</span>] Device behavior is valid
  - Current Range: -1.793e-02A to 2.870e-08A
- [<span style='color: green'>✓</span>] Temperature-dependent behavior is valid

*Temperature analysis showing current variation*

<img src='plots/dc_temperature_analysis.png' alt='Temperature Analysis' width='400'/>

### Thermodynamic Analysis
- [<span style='color: green'>✓</span>] Energy is conserved
  - Power Range: 0.000e+00W to 2.151e-02W
- [<span style='color: green'>✓</span>] Device is efficient
  - Efficiency Range: 7.992e+00 to 1.622e+10
- [<span style='color: green'>✓</span>] Temperature coefficient is calculated
  - Value: 8.34e-04/°C

### Physical Properties & Symmetry Analysis
- [<span style='color: green'>✓</span>] Gummel Symmetry Test (GST) (McAndrew TED 2025)
  - Odd Current Symmetry Error: 0.00e+00
  - Even Conductance Symmetry Error: 3.64e-09
  - Second Derivative Zero-Crossing Error: 2.20e-11
  - Smooth Higher-Order Continuity: ✓

*Gummel Symmetry Test showing Ix, Gx, and Gxx under differential excitation*

<img src='plots/dc_gummel_symmetry.png' alt='Gummel Symmetry Test' width='400'/>

- [<span style='color: green'>✓</span>] Zero-Bias Thermodynamic Passivity Check (NeuralCM-QA TCAD 2026)
  - Max Terminal Leakage: 1.42e-38 A
  - Power Passivity: ✓ Conserved (No spontaneous generation)

- [<span style='color: green'>✓</span>] Transconductance Smoothness & 3rd-Order Derivative (Gm3) Audit (McAndrew TED 2025 Table I)
  - Extracted Vth: 0.309 V
  - Peak Gm: 1.7150e-02 S at Vgs = 0.560 V
  - Ripple-Free Derivative Continuity: ✓ Pass (No unphysical ripples)
  - 3rd Derivative (Gm3) Linearity & Ripple Count: 6 sign changes (✓ Pass)
  - Peak Gm3: 6.2429e-01 S/V^2

<img src='plots/dc_derivative_smoothness.png' alt='Derivative Smoothness' width='400'/>

- [<span style='color: green'>✓</span>] Output Conductance & Higher Derivatives (Gds, Gds2, Gds3) (McAndrew TED 2025)
  - Passivity (Gds >= 0): ✓ Pass
  - Saturation Output Conductance: 3.2418e-03 S
  - Higher Derivatives Finite: ✓ Pass
  - 3rd Output Derivative (Gds3) Ripples: 5

<img src='plots/dc_output_conductance_derivatives.png' alt='Output Conductance Derivatives' width='400'/>

- [<span style='color: green'>✓</span>] Asymptotic Extrapolation Quality Assurance (Extreme Biases)
  - Deep Reverse Gate Bias (Vgs -> -2.0V): Leakage = 4.8363e-02 A (✓ Non-negative & Bounded)
  - No Spontaneous Negative Power: ✓ Pass
  - Extreme Gate Overdrive (Vgs = 2.5V): On-Current = 3.0140e-02 A (✓ Monotonic)
  - High Drain Voltage (Vds = 2.5V): Leakage = 2.0953e-02 A (✓ Stable)

<img src='plots/dc_asymptotic_extrapolation.png' alt='Asymptotic Extrapolation' width='400'/>

- [<span style='color: green'>✓</span>] Dynamic Self-Heating & Frequency Dispersion ($g_o(f)$ from 1 Hz to 100 GHz)
  - Passivity Maintained Across Spectrum ($g_o \ge 0$): ✓ Pass
  - Low-Frequency $g_o$ (1 Hz): 3.2164e-03 S
  - High-Frequency $g_o$ (100 GHz): 4.3199e-03 S
  - Dispersion Ratio $\Delta g_o / \bar{g}_o$: 0.3400
  - Thermal Transition Pole: 6.31e+10 Hz
  - Output Capacitance at 1 MHz: 1.0969e-14 F

<img src='plots/ac_dynamic_self_heating.png' alt='Dynamic Self-Heating Dispersion' width='400'/>


## 4. Transient Analysis
### Large-Signal Transient
- [<span style='color: green'>✓</span>] Large Signal Transient Verified
  - Maximum Drain Current: 3.110515e-05A
  - Gate Voltage Rise Time: 0.1ps

*Large-signal transient analysis showing voltages and current response*

<img src='plots/trans_large_signal_transient.png' alt='Large-Signal Transient Analysis' width='400'/>

### Switching Simulations
- [<span style='color: green'>✓</span>] Propagation Delay Verified
  - Propagation Delay: 10.2ps

  - Maximum Switching Power: 5.658069e-03W

  - Average Switching Power: 3.618697e-04W

*Inverter switching analysis showing input/output voltages and power*

<img src='plots/trans_switching_response.png' alt='Switching Response' width='400'/>

### Delay Effect Simulations
- [<span style='color: green'>✓</span>] Propagation delay through inverter chain analyzed
  - Stage 1 Delay: 14.2ps

  - Stage 2 Delay: 6.6ps

  - Stage 3 Delay: 4.7ps

  - Total Delay: 25.5ps

*Delay effect analysis showing signal propagation through inverter chain*

<img src='plots/trans_delay_effect.png' alt='Delay Effect Analysis' width='400'/>

### Transient Simulations for Power Dissipation
- [<span style='color: green'>✓</span>] Temperature-dependent power analysis completed
  - Maximum Power at 27°C: 5.658069e-03W

  - Maximum Power at 100°C: 4.405961e-03W

  - Average Power at 27°C: 3.618697e-04W

  - Average Power at 100°C: 2.431735e-04W

  - Power Temperature Coefficient: -1.715215e-05W/°C

*Power dissipation analysis at different temperatures*

<img src='plots/trans_power_dissipation.png' alt='Power Dissipation' width='400'/>

*Energy consumption analysis at different temperatures*

<img src='plots/trans_energy_consumption.png' alt='Energy Consumption' width='400'/>

### Quasi-Static Analysis
- [<span style='color: green'>✓</span>] Charge conservation analyzed
*Quasi-static time-domain behavior analysis*

<img src='plots/trans_quasi_static.png' alt='Quasi-Static Analysis' width='400'/>

*Quasi-static I-V characteristic showing relationship between gate voltage and drain current*

<img src='plots/trans_quasi_static_iv.png' alt='Quasi-Static I-V Characteristic' width='400'/>

### Charge Conservation Tests
- [<span style='color: red'>✗</span>] Charge Conservation verification failed
  - Data not available or failed to read


## 5. AC Analysis
### Small-Signal Analysis
- [<span style='color: green'>✓</span>] AC small-signal simulations verified
  - Gate capacitance range: 7.08fF to 13.98fF
  - Frequency range: 1.00e+06Hz to 1.00e+09Hz
  - Max capacitance at: 0.00V

*CV characteristics showing gate capacitance variation with gate voltage*

<img src='plots/ac_cv_characteristics.png' alt='CV Characteristics' width='400'/>

Capacitance components (Cgb, Cgs, Cgd) variation with gate voltage*

<img src='plots/ac_cv_components.png' alt='CV Components' width='400'/>

### AC-Integral Large-Signal Capacitance
- [<span style='color: green'>✓</span>] Large-signal capacitances computed from AC C(V) integral
  - Path: Vg -0.8 → 1.2 V (ΔV=2.0)
  - Cgg source: Cgg_1MHz from cv_data.txt
  - Cgg_ls: 9.841309 fF
  - Cgs_ls: -0.121646 fF
  - Cgd_ls: -8.272182 fF
  - Cgb_ls: -1.447485 fF
  - Output: data/ac_ls_caps_from_cv_integral.csv
  - Output: data/ac_qg_from_cv_integral.csv
  - Per-gate-area (W*L) normalization available
    - Geometry: W=10 µm, L=0.045 µm, Area=0.45 µm²
    - Cgg_ls/Area: 21.869575 fF/µm²
    - Cgs_ls/Area: -0.270324 fF/µm²
    - Cgd_ls/Area: -18.382627 fF/µm²
    - Cgb_ls/Area: -3.216634 fF/µm²
    - Output: data/ac_ls_caps_from_cv_integral_per_gate_area.csv
    - Output: data/ac_cv_caps_1MHz_per_gate_area.csv

### S-Parameter Analysis
- [<span style='color: green'>✓</span>] High-frequency AC simulations verified
  - Frequency range: 1.0MHz to 1.0GHz
- [<span style='color: green'>✓</span>] S-parameter analysis verified
  - S11 range: -0dB to -0dB
  - S21 range: 2dB to 2dB
  - S12 range: -114dB to -54dB
  - S22 range: -2dB to -2dB
- [<span style='color: green'>✓</span>] RF simulations verified
  - Isolation: >-56dB

*S-Parameter analysis showing frequency response characteristics*

<img src='plots/ac_cv_sparameter_analysis.png' alt='S-Parameters' width='400'/>

### Non-Quasi-Static Effects Analysis
- [<span style='color: green'>✓</span>] NQS effects verified
  - Maximum phase shift: 179.997
  - Frequency range: 10.0MHz to 10.0GHz

*Non-quasi-static effects analysis showing phase shift between gate voltage and drain current*

<img src='plots/ac_cv_nqs_effects.png' alt='NQS Effects' width='400'/>

### Charge Conservation Analysis
- [<span style='color: red'>✗</span>] Charge conservation verification failed
  - Data not available or failed to read

## 6. Noise Analysis
### Thermal Noise Analysis
- [<span style='color: green'>✓</span>] Thermal noise analysis completed
  - Max Noise: 1.36e-08 V²/Hz
  - Min Noise: 2.16e-15 V²/Hz
  - Avg Noise: 3.79e-09 V²/Hz
  - Noise Floor: 3.44e-09 V²/Hz
  - Frequency Range: 0.0MHz to 1.0GHz

*Thermal noise power spectral density analysis comparing different bias conditions, showing how the device noise characteristics change with bias voltage.*

<img src='plots/noise_thermal_noise_vds_comparison.png' alt='Thermal Noise Comparison' width='400'/>

### Flicker Noise Analysis
- [<span style='color: green'>✓</span>] Flicker noise analysis completed
  - Coefficient (K): 4.68e-08
  - Exponent (γ): 5.07e-01 (ideally -1.0 for pure 1/f noise)
  - Correlation (R²): 0.8265
  - Corner Frequency: 1.12e+00 Hz

*Flicker (1/f) noise analysis showing the power spectral density decreasing with frequency, a characteristic behavior in semiconductor devices associated with trapping/detrapping processes.*

<img src='plots/noise_flicker_noise.png' alt='Flicker Noise Analysis' width='400'/>

### Short Noise Analysis
- [<span style='color: green'>✓</span>] Short noise analysis completed
  - Shot Noise Level: 3.79e-09 V²/Hz
  - Standard Deviation: 5.56e-09 V²/Hz
  - Variation Coefficient: 1.4676

*Shot noise analysis showing the frequency-independent noise component that arises from the discrete nature of electric charge carriers crossing potential barriers.*

<img src='plots/noise_shot_noise.png' alt='Shot Noise Analysis' width='400'/>

### Temperature Dependence
- [<span style='color: green'>✓</span>] Short noise analysis completed
  - Temperature Coefficient: 2.77e-11 V²/Hz/°C
  - Temperature-Noise Correlation: None
  - Temperature Range: -40.0°C to 150.0°C

*Noise variation with temperature, illustrating how thermal effects influence the device's noise characteristics across the operational temperature range.*

<img src='plots/noise_vs_temperature.png' alt='Shot Noise Analysis' width='400'/>

### Bias Dependence
- [<span style='color: green'>✓</span>] Bias Dependance analysis completed
*Thermal Noise Results at Different Bias Points*

| Bias Condition | Max Noise (V²/Hz) | Min Noise (V²/Hz) | Avg Noise (V²/Hz) | Noise Floor (V²/Hz) |
|----------------|-------------------|-------------------|-------------------|--------------------|
| Vgs=0.3V, Vds=0.3V | 1.36e-08 | 2.16e-15 | 3.79e-09 | 6.90e-12 |
| Vgs=0.3V, Vds=0.6V | 1.36e-08 | 2.16e-15 | 3.79e-09 | 6.90e-12 |
| Vgs=0.3V, Vds=0.9V | 1.36e-08 | 2.16e-15 | 3.79e-09 | 6.90e-12 |
| Vgs=0.3V, Vds=1.2V | 1.36e-08 | 2.16e-15 | 3.79e-09 | 6.90e-12 |
| Vgs=0.6V, Vds=0.3V | 1.36e-08 | 2.16e-15 | 3.79e-09 | 6.90e-12 |
| Vgs=0.6V, Vds=0.6V | 1.36e-08 | 2.16e-15 | 3.79e-09 | 6.90e-12 |

