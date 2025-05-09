# SPICE Model Verification Complexity Levels

## Basic Complexity
These are fundamental checks that form the foundation of any device model verification:

### Simple Setup & Analysis
- **Accurate DC modeling for all terminal currents, on relevant log/linear scales**
  - DC sweep simulations
  - Log and linear scale current-voltage (I-V) characteristics
  - Multi-terminal DC analysis

- **Exhibits physical monotonicity over bias, geometry, and temperature**
  - Parameter sweep simulations
  - Bias point analysis
  - Temperature sweep simulations

### Moderate Setup & Analysis
- **Accurate capacitance/charge modeling**
  - AC small-signal simulations
  - Capacitance-voltage (C-V) measurements
  - Charge conservation tests

- **Obeys the laws of thermodynamics**
  - DC simulations to verify energy conservation
  - Transient simulations to check power dissipation
  - Temperature-dependent simulations

### Complex Setup & Analysis
- **Smoothness (ideally C∞-continuous)**
  - Derivative analysis simulations
  - Continuity check simulations
  - Parameter sweep simulations

## Intermediate Complexity
These checks require more sophisticated analysis and simulation setups:

### Simple Setup & Analysis
- **Exhibits relevant physical symmetries (currents, charges, their derivatives)**
  - Symmetry test simulations
  - Cross-derivative analysis
  - Terminal permutation tests

- **Exhibits asymptotic correctness over geometry, temperature, and bias**
  - Extreme condition simulations
  - Limit analysis simulations
  - Parameter sweep simulations

### Moderate Setup & Analysis
- **Works for large-signal transient simulation, including delay effects**
  - Time-domain transient analysis
  - Delay effect simulations
  - Switching simulations

- **Models DC and capacitance interaction where relevant**
  - Large-signal transient simulations
  - Quasi-static simulations
  - Mixed-mode simulations

### Complex Setup & Analysis
- **Accurate noise modeling**
  - Noise analysis simulations
  - Thermal noise simulations
  - Flicker noise simulations
  - Shot noise simulations

- **Full geometry dependence**
  - Parameter sweep simulations
  - Monte Carlo simulations for geometry variations
  - Layout-dependent effect (LDE) simulations

- **Complete temperature dependence**
  - Temperature sweep simulations
  - Thermal analysis
  - Temperature-dependent parameter extraction

## Advanced Complexity
These are the most complex verifications requiring sophisticated analysis and often multiple simulation types:

### Simple Setup & Analysis
- **Verified to converge reliably in at least one circuit simulator**
  - Convergence test simulations
  - Multiple simulator verification
  - Stress test simulations

### Moderate Setup & Analysis
- **Behaves "well" under unreasonable geometry, temperature, or bias conditions**
  - Corner case simulations
  - Stress test simulations
  - Extreme condition simulations

- **Accurate modeling of high-frequency/non-quasi-static effects where relevant**
  - High-frequency AC simulations
  - S-parameter analysis
  - RF simulations

- **Models all necessary LDEs (likely Linear Differential Equations)**
  - Layout-dependent simulations
  - Stress effect simulations
  - Proximity effect simulations

### Complex Setup & Analysis
- **Includes modeling of electrothermal effects (with frequency dependence)**
  - Thermal-electrical coupled simulations
  - Frequency-dependent thermal analysis
  - Power dissipation simulations

- **Includes or enables modeling of global and local statistical variation**
  - Monte Carlo simulations
  - Process corner simulations
  - Statistical analysis

- **Includes or enables model tuning to process specification corners**
  - Corner case simulations
  - Process variation simulations
  - Temperature corner simulations

- **Enables modeling of aging**
  - Long-term reliability simulations
  - Stress test simulations
  - Degradation analysis

- **Enables modeling of parasitics for different layouts**
  - Layout extraction simulations
  - Parasitic extraction
  - RC extraction simulations 