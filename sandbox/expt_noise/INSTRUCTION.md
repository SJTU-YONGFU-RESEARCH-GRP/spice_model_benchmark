# Noise Analysis Tool Instructions

This document provides instructions for setting up and running the noise analysis tool for MOSFET characterization.

## Prerequisites

Before using this tool, ensure you have the following installed:

1. **Python 3.6+**: The tool is built using Python and requires version 3.6 or higher.
2. **NGSpice**: The SPICE simulator used for circuit analysis.
3. **FreePDK45 Models**: The tool uses the FreePDK45 model files for MOSFET characterization.

## Installation

Follow these steps to set up the tool:

1. Clone or download this repository to your local machine.

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure ngspice is in your system PATH and can be executed from the command line.

4. Make the main script executable:
   ```bash
   chmod +x run_noise_analysis.py
   ```

## Running the Analysis

### Basic Usage

To run the noise analysis with default settings:

```bash
./run_noise_analysis.py
```

This will:
1. Use the default SPICE file (`noise_analysis.cir`)
2. Create a `results` directory for output
3. Run the analysis and generate a report

### Advanced Options

The tool provides several command-line options:

```bash
./run_noise_analysis.py --spice-file=path/to/spice/file.cir --output-dir=my_results --spice-cmd=ngspice --log-level=DEBUG
```

Options:
- `--spice-file`: Path to the SPICE netlist file (default: `noise_analysis.cir`)
- `--output-dir`: Directory for storing results (default: `results`)
- `--spice-cmd`: Command to run SPICE simulator (default: `ngspice`)
- `--log-level`: Logging level, one of: DEBUG, INFO, WARNING, ERROR, CRITICAL (default: INFO)

## Output Structure

The tool generates the following outputs:

1. **Data files**: Raw data from SPICE simulations in the `results/data` directory
2. **Plots**: Visualizations of noise analysis in the `results/plots` directory
3. **Logs**: Log files in the `results/logs` directory
4. **Report**: A comprehensive Markdown report (`REPORT.md`) in the output directory

## Report Content

The generated report includes:

1. Introduction and simulation setup details
2. Noise characteristics analysis:
   - Thermal noise
   - Flicker (1/f) noise
   - Shot noise
3. Frequency-dependent noise analysis
4. Temperature dependence of noise
5. Device geometry dependence (W, L scaling)
6. Conclusions and observations

## Troubleshooting

If you encounter issues:

1. Check the log files in the `results/logs` directory for detailed information
2. Ensure ngspice is properly installed and accessible
3. Verify the SPICE file exists and is correctly formatted
4. Ensure the FreePDK45 model files are in the correct location

## Example

```bash
# Run with default settings
./run_noise_analysis.py

# Specify a custom SPICE file and output directory
./run_noise_analysis.py --spice-file=my_circuit.cir --output-dir=custom_results
```

After running, open the generated `REPORT.md` file in your output directory to view the comprehensive analysis results. 