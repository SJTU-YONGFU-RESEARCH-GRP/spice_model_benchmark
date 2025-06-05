# MOSFET Simulation Verification Report

Generated on: 2025-06-05 16:51:54

## Table of Contents
1. [Simulation Setup and Execution](#1-simulation-setup-and-execution)
2. [Summary](#2-summary)
   - [DC Analysis Summary](#dc-analysis-summary)
3. [DC Analysis](#3-dc-analysis)
   - [DC Operating Point Analysis](#dc-operating-point-analysis)
   - [Temperature Dependence](#temperature-dependence)
   - [Thermodynamic Analysis](#thermodynamic-analysis)
   - [Physical Properties](#physical-properties)

## Notes
- This report is automatically generated based on mosfet_simulation.py
- Items are marked with <span style='color: green'>✓</span> for success and <span style='color: red'>✗</span> for failure
- Any deviations from expected behavior should be documented

## 1. Simulation Setup and Execution
- [<span style='color: green'>✓</span>] Circuit file exists and is readable
  - Path: /mnt/d/proj/spice_model_benchmark/netlists/dc_circuit.cir
- [<span style='color: green'>✓</span>] ngspice is properly installed
  - Version: ngspice-36
- [<span style='color: green'>✓</span>] Simulation runs without errors

## 2. Summary
### DC Analysis Summary
| Test Type | Status | Key Findings |
|-----------|--------|-------------|
| [IV Characteristics](#dc-operating-point-analysis) | <span style='color: green'>✓</span> | VDS: 0.00V to 1.20V, VGS: 0.00V to 1.20V, IDS: -1.79e-02A to 2.87e-08A |
| [Temperature Analysis](#temperature-dependence) | <span style='color: green'>✓</span> | Temp Points: [-40, 0, 25, 50, 100, 150], TC: 0.000015 /°C, IDS: -1.793e-02A to 2.870e-08A |
| [Thermodynamic Analysis](#thermodynamic-analysis) | <span style='color: green'>✓</span> | Power: 0.000e+00W to 2.151e-02W, Efficiency: 7.992e+00 to 1.622e+10, TC: 8.34e-04/°C |
| [Bias Point Analysis](#dc-operating-point-analysis) | <span style='color: green'>✓</span> | Points: 9 VDS points, 9 VGS points, Currents: IDS: -1.53e-02A to 2.71e-08A, IG: -3.73e-07A to 1.34e-08A, IS: 1.01e-39A to 1.53e-02A, IB: -1.42e-38A to 3.30e-07A, KCL Error: 0.00%, Power: 0.00e+00W to 1.84e-02W, Temp: -40°C |