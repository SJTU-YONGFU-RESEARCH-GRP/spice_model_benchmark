# SPICE Model Benchmark System

This project provides a comprehensive benchmarking system for SPICE models, allowing for the automated verification and validation of semiconductor device models with a focus on MOSFETs.

## Overview

The system is designed to run various types of SPICE simulations on a semiconductor device model, analyze the results, and generate a comprehensive verification report. It implements a structured verification methodology to evaluate model quality across multiple domains:

- DC analysis (IV characteristics, temperature dependence, thermodynamic analysis)
- Transient analysis (large-signal response, switching performance, delay effects)
- AC analysis (small-signal parameters, S-parameters, non-quasi-static effects)
- Noise analysis (thermal, flicker, and shot noise)
- Geometry and layout analysis

Note: The AC pipeline also derives *large-signal* effective capacitances by integrating the AC C(V) curves (e.g., Cgg from `cv_data.txt`) and writes the results under `results/data/`.

## Quick Start Guide

### Option 1: Install as a Python Package (Recommended)

1. **Install the package**:
   ```bash
   pip install git+https://github.com/yourusername/spice_model_benchmark.git
   # or clone and install locally:
   git clone https://github.com/yourusername/spice_model_benchmark.git
   cd spice_model_benchmark
   pip install -e .
   ```

2. **Ensure NGSPICE is installed and available on your system path**

3. **Run a benchmark with a single command**:
   ```bash
   # Using the command-line interface
   spice-benchmark path/to/your/model.inc

   # Or using Python API
   python -c "from spice_model_benchmark import benchmark_spice_model; benchmark_spice_model('path/to/your/model.inc')"
   ```

4. **View the results**:
   - The verification report is generated at `spice_benchmark_results/REPORT.md`
   - Visualization plots are created in `spice_benchmark_results/plots/`
   - Raw data is stored in `spice_benchmark_results/data/`

### Option 2: Run from Source (Legacy)

1. **Install prerequisites**:
   ```bash
   pip install numpy matplotlib pandas scipy tqdm colorama
   ```

2. **Ensure NGSPICE is installed and available on your system path**

3. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/spice_model_benchmark.git
   cd spice_model_benchmark
   ```

4. **Run a simple benchmark**:
   ```bash
   cd src
   python mosfet_simulation.py
   ```

5. **View the results**:
   - The verification report is generated at `results/REPORT.md`
   - Visualization plots are created in `results/plots/`
   - Raw data is stored in `results/data/`

## Programmatic Usage

### Python API

The package provides a simple Python API for easy integration into your workflows:

```python
from spice_model_benchmark import benchmark_spice_model

# Run a complete benchmark
success = benchmark_spice_model(
    model_file="path/to/your/model.inc",
    output_dir="my_benchmark_results",
    modes=["dc", "transient", "ac", "noise"]  # or None for all
)

if success:
    print("Benchmark completed successfully!")
```

### Advanced Usage with Custom Circuits

```python
from spice_model_benchmark import benchmark_spice_model

# Run with custom circuit files
success = benchmark_spice_model(
    model_file="my_model.inc",
    output_dir="custom_results",
    dc_circuit="custom_dc.cir",
    transient_circuit="custom_transient.cir",
    dpi=600,  # High-resolution plots
    log_level="DEBUG"  # Detailed logging
)
```

### Using the Full Simulation Class

For maximum control, use the `MOSFETSimulation` class directly:

```python
from spice_model_benchmark import MOSFETSimulation

# Create simulation instance
sim = MOSFETSimulation(
    dc_circuit_file="netlists/dc_circuit.cir",
    transient_circuit_file="netlists/transient_circuit.cir",
    noise_circuit_file="netlists/noise_circuit.cir",
    ac_circuit_file="netlists/ac_circuit.cir",
    output_dir="full_control_results",
    dpi=300
)

# Run specific analyses
success = sim.run(modes=["dc", "transient"])
```

## Examples

See the `examples/` directory for complete working examples:

- `examples/simple_benchmark.py`: Basic usage with minimal code
- `examples/advanced_benchmark.py`: Advanced usage with custom settings

Run examples with:
```bash
python examples/simple_benchmark.py path/to/your/model.inc
```

## Detailed Instructions

### Preparing Model Files

1. Place your MOSFET model file in the `models/` directory
2. Update the circuit netlists in `netlists/` to reference your model
3. Ensure your model file includes the correct parameters for your device

### Running Simulations

#### Using the Command-Line Interface (Recommended)

After installation, use the `spice-benchmark` command:

```bash
# Run with default settings
spice-benchmark path/to/your/model.inc

# Run with custom output directory
spice-benchmark path/to/your/model.inc --output-dir my_results

# Run only specific analyses
spice-benchmark path/to/your/model.inc --modes dc transient

# Run with high-resolution plots
spice-benchmark path/to/your/model.inc --dpi 600

# Get help
spice-benchmark --help
```

#### Using the Legacy Script

The original script is still available for advanced usage:

```bash
# Change to the src directory
cd src

# Run with default settings
python mosfet_simulation.py

# Run with custom circuit files
python mosfet_simulation.py --dc-circuit ../netlists/custom_dc.cir --transient-circuit ../netlists/custom_trans.cir

# Run specific verification tests only
python mosfet_simulation.py --verify dc,transient

# Run with increased verbosity
python mosfet_simulation.py --verbose

# Run with custom output directory
python mosfet_simulation.py --output-dir ../my_results

# Skip certain simulation types
python mosfet_simulation.py --skip noise,ac

# For more options
python mosfet_simulation.py --help
```

### Interpreting Results

The verification process produces:

1. **Verification Report** (`results/REPORT.md`): A comprehensive document with pass/fail indicators for all verification tests
2. **Raw Data** (`results/data/`): CSV files containing simulation data for further analysis
3. **Visualization Plots** (`results/plots/`): PNG images showing various model characteristics

Key metrics to check in the report:
- ✓/✗ indicators showing pass/fail status for each test
- Detailed measurements and operating point information
- Temperature coefficients and scaling behavior

Additional AC outputs (if `--mode ac` ran successfully):
- `<output-dir>/data/ac_ls_caps_from_cv_integral.csv`: Large-signal capacitances computed from AC C(V) integral along the Vg sweep path.
- `<output-dir>/data/ac_qg_from_cv_integral.csv`: Integrated Qg(Vg) curve derived from Cgg(Vg).

### Customizing Verification Criteria

1. Edit `src/verification_parameters.py` to modify thresholds for verification tests
2. Create custom circuit netlists in the `netlists/` directory
3. Modify plot settings in `src/plot_generator.py` for customized visualizations

## Documentation

For detailed information about the benchmark system, refer to the following documentation:

- [METHODOLOGY.md](docs/METHODOLOGY.md): Comprehensive explanation of the verification methodology and implementation details
- [CHECKLIST.md](docs/CHECKLIST.md): Verification checklist with detailed criteria for each test
- [Benchmarks for SPICE Modeling and Parameter Extraction Based on AI/ML](docs/Benchmarks_for_SPICE_Modeling_and_Parameter_Extraction_Based_on_AI_ML.pdf): Research paper on benchmark methodology

## Directory Structure

```
spice_model_benchmark/
├── docs/                  # Documentation files
│   ├── METHODOLOGY.md     # Detailed verification methodology
│   ├── CHECKLIST.md       # Verification criteria checklist
│   └── Benchmarks_for_SPICE_Modeling_and_Parameter_Extraction_Based_on_AI_ML.pdf
├── examples/              # Usage examples
│   ├── simple_benchmark.py     # Basic usage example
│   └── advanced_benchmark.py   # Advanced usage example
├── models/                # MOSFET model files
├── netlists/              # Circuit netlist files
│   ├── dc_circuit.cir     # Circuit for DC analysis
│   ├── transient_circuit.cir  # Circuit for transient analysis
│   ├── noise_circuit.cir  # Circuit for noise analysis
│   └── ac_circuit.cir     # Circuit for AC analysis
├── src/                   # Source code (Python package)
│   ├── __init__.py        # Package initialization
│   ├── cli.py             # Command-line interface
│   ├── mosfet_simulation.py   # Main simulation controller
│   ├── data_reader.py     # Read and parse simulation results
│   ├── plot_generator.py  # Generate plots from simulation data
│   ├── simulation_runner.py   # Execute SPICE simulations
│   ├── verification_manager.py # Verify and report results
│   ├── verification_parameters.py # Configurable verification parameters
│   └── logger.py          # Logging utilities
├── pyproject.toml         # Modern Python packaging configuration
├── requirements.txt       # Legacy dependency specification
├── results/               # Simulation results (example)
│   ├── data/              # Raw data files
│   ├── plots/             # Generated plots and visualizations
│   └── REPORT.md          # Verification report
└── README.md              # This file
```

## Key Features

### Comprehensive Verification

- **DC Analysis**: Verifies IV characteristics, subthreshold behavior, saturation behavior, and KCL compliance
- **Temperature Analysis**: Validates behavior across -40°C to 150°C range, temperature coefficients
- **Transient Analysis**: Tests transient response, switching behavior, delay effects, power dissipation
- **AC Analysis**: Examines CV characteristics, S-parameters, and non-quasi-static effects
- **AC-Integral LS Caps**: Computes large-signal effective capacitances from AC C(V) by voltage integration (e.g., Cgg_ls from Cgg(Vg))
- **Noise Analysis**: Characterizes thermal, flicker (1/f), and shot noise across frequencies and bias points

### Visualization

The system generates detailed plots for different aspects of the device behavior:

- IV characteristics curves with log-scale insets for subthreshold behavior
- Capacitance-voltage plots showing gate capacitance components
- S-parameter plots for RF/high-frequency performance
- Noise spectra across different frequencies and temperatures
- Transient analysis visualizations for timing and switching performance
- Temperature-dependent behavior visualization
- Charge conservation plots

### Automated Reporting

The verification process generates a comprehensive Markdown report that includes:
- Summary tables for each analysis domain
- Detailed verification results with pass/fail indicators
- Key metrics and parameters extracted from simulations
- Embedded plots for visual verification
- Tables of measured values for further analysis

## Requirements

### System Requirements
- Python 3.8+
- NGSPICE (version 30 or newer recommended)

### Python Dependencies
When installed via pip, all dependencies are automatically managed:
- NumPy >= 1.21.0
- Matplotlib >= 3.4.0
- Pandas >= 1.3.0
- SciPy >= 1.7.0
- tqdm >= 4.62.0
- colorama >= 0.4.4

### Manual Installation
If installing manually, install dependencies with:
```bash
pip install numpy matplotlib pandas scipy tqdm colorama
```

## Troubleshooting

### Common Issues

1. **NGSPICE not found**: Ensure NGSPICE is installed and in your system path
   ```bash
   which ngspice  # Should return a path
   ngspice --version  # Should display version information
   ```

2. **Missing simulation data**: Check that your model file is correctly referenced in the netlists

3. **Failed verification tests**: Examine the specific test details in REPORT.md to understand which aspects of the model need improvement

4. **Visualization errors**: Ensure your Python environment has matplotlib properly installed

### Getting Help

For additional issues, please file an issue on the GitHub repository or contact the repository maintainers.

## License

This project is provided as open-source software under the MIT License. See LICENSE file for details.

## Citation

If you use this benchmark system in your research, please cite:

```
@software{spice_model_benchmark,
  author = {Your Name},
  title = {SPICE Model Benchmark System},
  year = {2023},
  url = {https://github.com/yourusername/spice_model_benchmark}
}
``` 