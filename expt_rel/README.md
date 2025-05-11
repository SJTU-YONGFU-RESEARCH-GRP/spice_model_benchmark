# MOSFET Environmental and Reliability Analysis

This repository contains a comprehensive framework for analyzing environmental and reliability aspects of MOSFET models using SPICE simulations. The analysis covers all items in the "Environmental and Reliability Analysis" section of the SPICE model verification checklist.

## Overview

The implementation provides tools to analyze:

1. **Temperature and Thermal Effects**
   - Temperature-dependent characteristics
   - Power dissipation analysis
   - Thermal-electrical coupling
   - Frequency-dependent thermal response

2. **Process and Statistical Variation**
   - Process corner analysis (TT, FF, SS, FS, SF)
   - Monte Carlo simulations
   - Parameter sensitivity analysis
   - Variability quantification

3. **Reliability and Aging**
   - Long-term aging effects
   - Hot-carrier injection (HCI) simulation
   - Negative bias temperature instability (NBTI)
   - Stress-dependent degradation

## Features

- **Robust Error Handling**: Gracefully handles issues with SPICE simulations, missing data files, and malformed outputs.
- **No Synthetic Data**: Reports errors and missing data instead of generating synthetic data.
- **Comprehensive Reporting**: Creates detailed reports with visualizations and analysis results based only on actual SPICE output.
- **Full Checklist Coverage**: Reports the status of all Environmental and Reliability Analysis checklist items.

## Requirements

- ngspice (version 42 or newer)
- Python 3.7 or newer
- Required Python packages (listed in requirements.txt):
  - numpy
  - pandas
  - matplotlib

## Quick Start

1. Install required packages:
   ```
   pip install -r requirements.txt
   ```

2. Run the analysis:
   ```
   python env_reliability_analysis.py
   ```

3. View the report:
   ```
   open REPORT.md
   ```

## Directory Structure

```
.
├── env_reliability.cir        # SPICE netlist for environmental and reliability analysis
├── env_reliability_analysis.py # Python analysis script
├── INSTRUCTIONS.md            # Usage instructions and implementation details
├── README.md                  # This file
├── requirements.txt           # Python package requirements
├── REPORT_TEMPLATE.md         # Example output report
├── results/                   # Generated during analysis (will be created if missing)
│   └── plots/                 # Generated plots (will be created if missing)
└── REPORT.md                  # Generated report (will be created automatically)
```

## Documentation

For detailed information, see:
- [INSTRUCTIONS.md](INSTRUCTIONS.md): Usage instructions and implementation details
- [REPORT_TEMPLATE.md](REPORT_TEMPLATE.md): Example output report

## Current Status

The analysis reports on SPICE simulation results and clearly indicates which analyses could not be completed due to missing data. No synthetic data is generated - all results are based only on actual SPICE simulation output. See [INSTRUCTIONS.md](INSTRUCTIONS.md) for details on known issues and how to fix them.

## License

This project is available under the MIT License.