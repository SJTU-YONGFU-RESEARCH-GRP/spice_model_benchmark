# SPICE Model Noise Benchmark

This repository contains a SPICE noise analysis tool for MOSFET characterization. The tool analyzes various noise characteristics including thermal noise, flicker noise, shot noise, and their dependence on frequency, temperature, and device geometry.

## Overview

The noise analysis tool performs the following analyses:
- Thermal noise analysis at different bias points
- Flicker (1/f) noise analysis
- Shot noise analysis
- Temperature dependence analysis
- Geometry dependence analysis
- Frequency-dependent noise component analysis

## Components

- `noise_analysis.cir`: SPICE netlist for noise analysis
- `src/`: Python modules
  - `logger.py`: Logging functionality
  - `parser.py`: SPICE result parsing
  - `plotter.py`: Data visualization
  - `report_generator.py`: Markdown report generation
  - `noise_analyzer.py`: Main analysis module
- `run_noise_analysis.py`: Entry point script

## Recent Improvements

### No Synthetic Data

This tool has been upgraded to eliminate any use of synthetic data:

1. **Frequency Analysis**: The SPICE netlist now performs proper separation of thermal and flicker noise components directly in the simulation rather than using synthetic data generation.
   
2. **Geometry Dependence**: The analysis strictly uses SPICE simulation results and reports errors if the simulation data doesn't exhibit the expected variation with device geometry.

3. **Error Reporting**: All analyses now provide detailed error information when issues are encountered, instead of falling back to synthetic data.

## Known Issues

### Geometry Dependence Analysis

**Issue Description:**
The geometry dependence analysis may not show proper scaling with transistor length and width because the SPICE simulation results show identical noise values for different geometry parameters. The scaling factors should theoretically be close to -1.0 (inversely proportional to dimensions) for flicker noise, but are currently reported as approximately 0.00.

**Possible Causes:**
1. The SPICE model parameters might not be correctly configured to account for geometry scaling
2. The `altermod` commands in the SPICE netlist might not be properly updating the device parameters
3. The noise analysis settings might reset between simulation runs

**Approach:**
The tool has been updated to detect when noise values don't properly scale with geometry parameters. When this happens:
- The analysis will be marked as "Failed" in the report
- No synthetic data will be used as a fallback
- Detailed error information will be included in the report

## Usage

1. Ensure you have ngspice and Python installed
2. Install required Python packages:
   ```
   pip install numpy pandas matplotlib
   ```
3. Run the analysis:
   ```
   python run_noise_analysis.py
   ```

4. Results will be generated in the `results/` directory:
   - `results/data/`: Raw data files
   - `results/plots/`: Generated plots
   - `results/logs/`: Log files
   - `results/REPORT.md`: Final report with analysis results

## Improvement Suggestions

To fix the geometry dependence issues:
1. Verify that the FreePDK45 model correctly handles L and W parameter changes for noise calculations
2. Check that `altermod @M1[L]` and `altermod @M1[W]` commands are working as expected
3. Consider using a test circuit that verifies parameter changes between simulation runs
4. Use a SPICE model that is known to have correct noise scaling with geometry 