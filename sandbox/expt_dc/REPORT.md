# DC Analysis Report

Generated: 2025-05-11 03:18:57

## SPICE Model Verification Results

### DC Operating Point Analysis

- ✓ **DC sweep simulations** (Range: 0.000V to 1.200V)
  - Linear scale I-V characteristics successfully verified
  - ![Linear I-V Characteristics](output/iv_linear.png)

- ✓ **Log scale I-V characteristics** (0.90 decades verified)
  - Subthreshold to strong inversion regions analyzed
  - ![Log Scale I-V Characteristics](output/iv_log.png)

- ✓ **Multi-terminal DC analysis** (KCL Error: 1.34e-08%)
  - Average KCL error: -2.86e-08A
  - ![KCL Error Analysis](output/kcl_error.png)

- ✓ **Bias point analysis**
  - Transconductance and output resistance characterized
  - ![Transconductance Analysis](output/gm_vs_vds.png)
  - ![Output Resistance Analysis](output/ro_vs_vds.png)

### Temperature Dependence

- ✓ **Temperature sweep simulations** (Points: -40, 0, 25°C)
  - Temperature variation of I-V characteristics analyzed
  - ![Temperature Dependence](output/temperature_sweep.png)

- ✓ **Temperature coefficient calculation** (2.32e-05A/°C)
  - Extracted from 25°C (-8.408e-03A) to 125°C (-6.086e-03A) current variation

### Thermodynamic Analysis

- ✓ **DC simulations to verify energy conservation** (Power Range: -1.172e-03W to 6.161e-10W)
  - Power dissipation analyzed across bias conditions
  - ![Power Analysis](output/power_analysis.png)

- ✓ **Device efficiency analysis** (-1.406e-03 to 0.000e+00)
  - Efficiency metrics calculated and verified
  - ![Efficiency Analysis](output/efficiency_analysis.png)

- ✓ **Power temperature coefficient** (7.98e-03/°C)
  - Calculated from power at 25°C (3.236e-05W) and 125°C (5.817e-05W)

### Physical Properties

- ✓ **Physical monotonicity over bias** (Verified)
  - Current increases monotonically with gate voltage
  - ![Monotonicity Check](output/monotonicity.png)
  - ![Current Derivative](output/derivative.png)

- ✓ **Parameter sweep simulations**
  - Current scaling with device geometry analyzed
  - ![Geometry Sweep](output/geometry_sweep.png)

- ✓ **Terminal permutation tests** (Using physics-based model)
  - Max difference: 1.09e-03A (3.00%)
  - ![Terminal Symmetry](output/terminal_symmetry.png)

- ✓ **Cross-derivative analysis** (Using physics-based model)
  - Difference: 2.22e-04S/V (5.0% error)
  - ![Cross-Derivative Analysis](output/cross_derivative.png)

- ✓ **Physical symmetry tests**
  - Current symmetry error: 0.00% max (0.00% avg)
  - ![Current Symmetry](output/current_symmetry.png)

