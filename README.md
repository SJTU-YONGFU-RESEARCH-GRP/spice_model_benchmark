# SPICE Model Benchmark System

This project provides a benchmarking system for SPICE models, allowing for the automated verification and validation of semiconductor device models.

## Overview

The system is designed to run various types of SPICE simulations on a semiconductor device model, analyze the results, and generate a comprehensive verification report. It supports:

- DC analysis (IV characteristics)
- Transient analysis
- Noise analysis
- Temperature sweep analysis
- Thermodynamic analysis

## Directory Structure

```
spice_model_benchmark/
├── netlists/              # Circuit netlist files
│   ├── dc_circuit.cir     # Circuit for DC analysis
│   ├── transient_circuit.cir  # Circuit for transient analysis
│   └── noise_circuit.cir  # Circuit for noise analysis
├── src/                   # Source code
│   ├── mosfet_simulation.py   # Main simulation controller
│   ├── data_reader.py     # Read and parse simulation results
│   ├── plot_generator.py  # Generate plots from simulation data
│   ├── simulation_runner.py   # Execute SPICE simulations
│   └── verification_manager.py    # Verify and report results
├── results/               # Simulation results
│   ├── data/              # Raw data files
│   └── plots/             # Generated plots and visualizations
└── README.md              # This file
```

## Usage

```bash
# Change to the src directory
cd src

# Run the simulation with default settings
python mosfet_simulation.py

# Run with custom circuit files
python mosfet_simulation.py --dc-circuit ../netlists/dc_circuit.cir --transient-circuit ../netlists/transient_circuit.cir --noise-circuit ../netlists/noise_circuit.cir

# For more options
python mosfet_simulation.py --help
```

## Output Files

The simulation will generate several outputs:

1. Raw simulation data in `results/data/`
2. Visualization plots in `results/plots/`
3. A verification report (REPORT.md) in the `results/` directory

## Visualization

The system generates plots for different aspects of the device behavior:

- IV characteristics curves (`plots/iv_characteristics.png`)
- Temperature analysis (`plots/temperature_analysis.png`) 
- KCL verification (`plots/kcl_verification.png`)
- Noise spectra (`plots/thermal_noise_vds_comparison.png`, `plots/flicker_noise.png`, etc.)
- Transient analysis results (`plots/large_signal_transient.png`, `plots/switching_response.png`, etc.)

## Requirements

- Python 3.6+
- NumPy
- Matplotlib
- NGSPICE (on system path)

## License

This project is provided as open-source software. 