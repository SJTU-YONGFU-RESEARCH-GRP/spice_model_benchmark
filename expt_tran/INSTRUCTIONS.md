# SPICE Model Transient Analysis Instructions

This package provides tools for performing comprehensive transient analysis on MOSFET SPICE models according to the verification checklist. The analysis covers large-signal transient, switching, delay, power dissipation, quasi-static, and charge conservation tests.

## Prerequisites

Before running the analysis, ensure you have the following installed:

1. **ngspice** - Version 42 or higher recommended
2. **Python 3.6+** - With the following packages:
   - numpy
   - matplotlib
   - logging
   - subprocess

To install required Python packages:

```bash
pip install numpy matplotlib
```

## File Structure

- `tran_circuit.cir` - SPICE netlist for transient analysis
- `tran_analysis.py` - Python script for running simulations and generating reports
- `CHECKLIST.md` - Reference for SPICE model verification requirements
- `models/` - Directory containing SPICE models (ensure FreePDK45 model is available)

## Running the Analysis

1. **Check model paths**: Ensure the path to the FreePDK45 model in `tran_circuit.cir` is correct:
   ```
   .inc ./models/ngspice-cmos/FreePDK45/nom.inc
   ```
   Adjust this path if your models are located elsewhere.

2. **Create output directory**: The script will automatically create a directory named `tran_results` to store output plots.

3. **Run the analysis script**:
   ```bash
   python tran_analysis.py
   ```

4. **View the results**:
   - A log file `tran_analysis.log` will be created with detailed information
   - The output directory `tran_results` will contain all generated plots
   - A comprehensive report `REPORT.md` will be generated with all analysis results

## Analysis Components

The script performs the following analyses:

1. **Large-Signal Transient Analysis**
   - Time-domain response to pulse input
   - Current and voltage waveforms

2. **Switching Simulations**
   - Inverter switching behavior
   - Propagation delays
   - Switching power measurement

3. **Delay Effect Simulations**
   - Multi-stage inverter chain
   - Stage-by-stage delay analysis
   - Total chain delay measurement

4. **Power Dissipation Analysis**
   - Temperature-dependent power analysis (27°C and 100°C)
   - Power-temperature coefficient calculation
   - Energy consumption tracking

5. **Quasi-Static Analysis**
   - Slower transitions for observing quasi-static behavior
   - Relationship between gate voltage and drain current

6. **Charge Conservation Tests**
   - Terminal charge tracking
   - Total charge conservation verification
   - Charge conservation error calculation

## Troubleshooting

- If ngspice returns an error, check:
  - Model paths are correct
  - ngspice is properly installed
  - Netlist syntax for any errors

- If plots aren't generated, ensure:
  - matplotlib and numpy are installed
  - You have write permissions in the current directory
  - The simulation completed successfully

## Contact

For issues or questions, please file an issue in the repository. 