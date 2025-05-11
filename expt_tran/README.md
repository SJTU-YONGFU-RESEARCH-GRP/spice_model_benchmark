# SPICE Model Transient Analysis Framework

This repository contains tools for comprehensive transient analysis of MOSFET SPICE models. It is designed to verify model accuracy according to standard verification checklists.

## Overview

The transient analysis framework provides:

1. **Comprehensive Verification**: Tests that conform to industry-standard verification requirements
2. **Automated Analysis**: Python scripts for running simulations and generating reports
3. **Visual Results**: Automatic generation of plots and visualizations
4. **Detailed Metrics**: Quantitative metrics for model evaluation

## Key Features

- **Large-Signal Transient Analysis**: Examines device response to pulse inputs
- **Switching Analysis**: Evaluates device performance in digital circuits
- **Delay Effects**: Measures propagation delays in multi-stage circuits
- **Power Dissipation**: Analyzes power and energy consumption with temperature effects
- **Quasi-Static Analysis**: Verifies model accuracy in slow transition regions
- **Charge Conservation**: Validates physical consistency of the model

## Directory Structure

```
├── CHECKLIST.md           # Verification checklist
├── INSTRUCTIONS.md        # Detailed instructions for running the analysis
├── README.md              # This file
├── tran_analysis.py       # Python script for running and analyzing simulations
├── tran_circuit.cir       # SPICE netlist for transient analysis
├── models/                # Directory containing SPICE models
└── tran_results/          # Generated plots and data (created by script)
```

## Getting Started

See [INSTRUCTIONS.md](INSTRUCTIONS.md) for detailed setup and usage instructions.

Quick start:

```bash
# Install required Python packages
pip install numpy matplotlib

# Run the analysis
python tran_analysis.py

# View results in REPORT.md and tran_results/ directory
```

## Requirements

- NGSpice (version 42 or higher recommended)
- Python 3.6+
- NumPy and Matplotlib Python packages
- FreePDK45 SPICE models

## License

This software is available under the MIT License. 