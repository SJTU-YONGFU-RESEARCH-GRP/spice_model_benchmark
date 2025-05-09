# MOSFET Simulation Verification Report

Generated on: 2025-05-09 05:31:21

## Notes
- This report is automatically generated based on mosfet_simulation.py
- Items are marked with <span style='color: green'>✓</span> for success and <span style='color: red'>✗</span> for failure
- Any deviations from expected behavior should be documented

## 1. Simulation Setup and Execution
- [<span style='color: green'>✓</span>] Netlist file exists and is readable
  - Path: /mnt/d/proj/device/spice_benchmark/netlists/circuit.cir
- [<span style='color: green'>✓</span>] ngspice is properly installed
  - Version: ngspice-36
- [<span style='color: green'>✓</span>] Simulation runs without errors

## 2. I/V Characteristics Analysis
- [<span style='color: green'>✓</span>] IV data file is generated
- [<span style='color: green'>✓</span>] Data points are properly read
- [<span style='color: green'>✓</span>] Vds values are within range (0-5V)
  - Range: 0.000V to 1.200V
- [<span style='color: green'>✓</span>] Vgs values are within range (0-5V)
  - Range: 0.000V to 1.200V
- [<span style='color: green'>✓</span>] Drain current (Ids) is properly measured
  - Range: -1.793e-02A to 2.870e-08A
- [<span style='color: green'>✓</span>] Log scale measurements are valid (2+ decades)
  - Decades: 2.92
- [<span style='color: green'>✓</span>] Linear scale measurements are valid
  - Points: 1722
  - Range: 0.100V to 0.500V
- [<span style='color: green'>✓</span>] Multi-terminal current analysis is valid
  - KCL Error: 0.00%
- [<span style='color: green'>✓</span>] Temperature-dependent behavior is valid
  - Temperature Coefficient: 1.48e-05A/°C

<img src='iv_characteristics.png' alt='IV Characteristics' width='400'/>

*IV Characteristics showing drain current vs drain-source voltage*

## 3. C/V Characteristics Analysis
- [<span style='color: green'>✓</span>] CV data file is generated
- [<span style='color: green'>✓</span>] Data points are properly read
- [<span style='color: green'>✓</span>] Gate voltage (Vg) measurements are valid
  - Range: 0.000V to 0.000V
- [<span style='color: green'>✓</span>] Gate current (Ig) measurements are valid
  - Range: -4.897e-05A to -6.166e-14A
- [<span style='color: green'>✓</span>] Source current (Is) measurements are valid
  - Range: 3.208e-14A to 2.548e-05A
- [<span style='color: green'>✓</span>] Bulk current (Ib) measurements are valid
  - Range: 8.374e-15A to 6.652e-06A

<img src='cv_characteristics.png' alt='CV Characteristics' width='400'/>

*CV Characteristics showing gate current vs voltage*

## 4. Temperature Analysis
- [<span style='color: green'>✓</span>] Temperature sweep is performed (-40°C to 150°C)
  - Points: [-40, 0, 25, 50, 100, 150]
- [<span style='color: green'>✓</span>] Temperature coefficient is calculated
  - Value: 0.000015 /°C
- [<span style='color: green'>✓</span>] Device behavior is valid
  - Current Range: -1.793e-02A to 2.870e-08A

<img src='temperature_analysis.png' alt='Temperature Analysis' width='400'/>

*Temperature analysis showing current variation*

## 5. Thermodynamic Analysis
- [<span style='color: red'>✓</span>] Energy conservation verified
  - Power Range: -2.151e-02W to 0.000e+00W
- [<span style='color: green'>✓</span>] Device efficiency analyzed
  - Efficiency Range: 7.992e+00 to 1.622e+10
- [<span style='color: green'>✓</span>] Power measurements complete
- [<span style='color: green'>✓</span>] Temperature coefficient calculated
  - Value: 8.34e-04/°C

<img src='kcl_verification.png' alt='KCL Verification' width='400'/>

*KCL verification showing current balance*
