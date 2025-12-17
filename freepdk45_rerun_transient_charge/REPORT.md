# MOSFET Simulation Verification Report
Generated on: 2025-12-16 20:08:10

## Table of Contents
1. [Simulation Setup and Execution](#1-simulation-setup-and-execution)
2. [Summary](#2-summary)
   - [Transient Analysis Summary](#transient-analysis-summary)
3. [Transient Analysis](#3-transient-analysis)
   - [Large-Signal Transient](#large-signal-transient)
   - [Switching Simulations](#switching-simulations)
   - [Delay Effect Simulations](#delay-effect-simulations)

## Notes
- This report is automatically generated based on mosfet_simulation.py
- Items are marked with <span style='color: green'>✓</span> for success and <span style='color: red'>✗</span> for failure
- Any deviations from expected behavior should be documented

## 1. Simulation Setup and Execution
- [<span style='color: green'>✓</span>] Circuit file exists and is readable
  - Path: /data1/duhaochen/spice_model_benchmark/netlists/transient_circuit.cir
- [<span style='color: green'>✓</span>] ngspice is properly installed
  - Version: ngspice-45+
- [<span style='color: green'>✓</span>] Simulation runs without errors

## 2. Summary
### Transient Analysis Summary
| Test Type | Status | Key Findings |
|-----------|--------|-------------|
| [Large-Signal Transient](#large-signal-transient) | <span style='color: green'>✓</span> | Max Current: 2.934e-05A, Rise Time: 0.1ps |
| [Switching Simulations](#switching-simulations) | <span style='color: green'>✓</span> | Propagation Delay: 10.7ps, Power: 5.659e-03W (max), 1.470e-03W (avg) |
| [Delay Effect](#delay-effect-simulations) | <span style='color: green'>✓</span> | Total Chain Delay: 25.0ps |
| [Power Dissipation](#transient-simulations-for-power-dissipation) | <span style='color: green'>✓</span> | Temp Coeff: -1.718433e-05W/°C |
| [Quasi-Static Analysis](#quasi-static-analysis) | <span style='color: green'>✓</span> | I-V characteristics analyzed: None |
| [Charge Conservation](#charge-conservation-tests) | <span style='color: red'>✗</span> | Max |Ierr|: 9.85e-11 A, Max |Qerr|: 9.95e-19 C |

## 3. Transient Analysis
### Large-Signal Transient
- [<span style='color: green'>✓</span>] Large Signal Transient Verified
  - Maximum Drain Current: 2.934381e-05A
  - Gate Voltage Rise Time: 0.1ps

*Large-signal transient analysis showing voltages and current response*

<img src='plots/trans_large_signal_transient.png' alt='Large-Signal Transient Analysis' width='400'/>

### Switching Simulations
- [<span style='color: green'>✓</span>] Propagation Delay Verified
  - Propagation Delay: 10.7ps

  - Maximum Switching Power: 5.659051e-03W

  - Average Switching Power: 1.470466e-03W

*Inverter switching analysis showing input/output voltages and power*

<img src='plots/trans_switching_response.png' alt='Switching Response' width='400'/>

### Delay Effect Simulations
- [<span style='color: green'>✓</span>] Propagation delay through inverter chain analyzed
  - Stage 1 Delay: 13.7ps

  - Stage 2 Delay: 6.1ps

  - Stage 3 Delay: 5.1ps

  - Total Delay: 25.0ps

*Delay effect analysis showing signal propagation through inverter chain*

<img src='plots/trans_delay_effect.png' alt='Delay Effect Analysis' width='400'/>

### Transient Simulations for Power Dissipation
- [<span style='color: green'>✓</span>] Temperature-dependent power analysis completed
  - Maximum Power at 27°C: 5.659051e-03W

  - Maximum Power at 100°C: 4.404595e-03W

  - Average Power at 27°C: 1.470466e-03W

  - Average Power at 100°C: 1.017077e-03W

  - Power Temperature Coefficient: -1.718433e-05W/°C

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
- [<span style='color: red'>✗</span>] Charge conservation analyzed

  - Max current error: 9.853002e-11A

  - Max charge error: 9.952276e-19C

  - Thresholds: I<1.00e-12A, Q<1.00e-15C

*Terminal currents and charges analysis*

<img src='plots/trans_charge_conservation.png' alt='Charge Conservation Analysis' width='400'/>

*Total charge conservation analysis*

<img src='plots/trans_total_charge.png' alt='Total Charge' width='400'/>

