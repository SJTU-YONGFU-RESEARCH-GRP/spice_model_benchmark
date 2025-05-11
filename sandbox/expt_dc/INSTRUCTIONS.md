# DC Analysis Instructions

This directory contains scripts and netlists to perform comprehensive DC analysis on SPICE models according to the checklist in `docs/CHECKLIST.md`.

## Prerequisites

1. **ngspice**: The simulation requires ngspice to be installed on your system.
   ```
   sudo apt-get install ngspice
   ```

2. **Python Environment**: The analysis scripts require Python 3.6+ with the following packages:
   - numpy
   - matplotlib
   - pandas
   - scipy
   - tqdm
   - colorama

   These can be installed using the project's requirements.txt:
   ```
   pip install -r ../requirements.txt
   ```

## Directory Structure

- `dc_analysis.cir`: SPICE netlist for DC analysis
- `dc_analyzer.py`: Python script that runs simulations and generates reports
- `output/`: Directory where simulation results will be stored
- `REPORT.md`: Generated report with analysis results and plots

## Running the Analysis

1. Navigate to the project root directory:
   ```
   cd /path/to/spice_model_benchmark
   ```

2. Run the DC analysis script:
   ```
   python dc_expt/dc_analyzer.py
   ```
   
   This will:
   - Run the SPICE simulation with the dc_analysis.cir netlist
   - Parse the generated output files
   - Create plots in the output/plots directory
   - Generate a comprehensive REPORT.md with results

3. View the results:
   The script will generate a `REPORT.md` file containing all analysis results and references to generated plots.

## DC Analysis Components

The analysis covers all aspects of DC verification specified in the checklist:

1. **DC Operating Point Analysis**
   - DC sweep simulations (0V to 1.2V)
   - Linear and log scale I-V characteristics
   - Multi-terminal analysis (KCL verification)
   - Bias point analysis (transconductance, output resistance)

2. **Temperature Dependence**
   - Temperature sweep (-40°C to 150°C)
   - Temperature coefficient calculation
   - Temperature-dependent parameter extraction

3. **Thermodynamic Analysis**
   - Energy conservation verification
   - Device efficiency analysis
   - Power temperature coefficient

4. **Physical Properties**
   - Physical monotonicity over bias
   - Parameter sweep simulations
   - Physical symmetries
   - Terminal permutation tests

## Troubleshooting

If you encounter any issues:

1. Check the log file at `dc_expt/dc_analysis.log` for detailed error information.
2. Ensure ngspice is properly installed and accessible in your PATH.
3. Verify that all required Python packages are installed.
4. Make sure the SPICE models at `models/ngspice-cmos/FreePDK45/nom.inc` are accessible.

## Output

The analysis generates the following outputs:

1. Raw simulation data files in the `output/` directory
2. Plots in the `output/plots/` directory
3. A comprehensive markdown report `REPORT.md` with analysis results and plots 