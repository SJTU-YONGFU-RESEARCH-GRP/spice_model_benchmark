# SPICE Simulation Tool for MOSFET IV and CV Characteristics

This tool provides a Python-based interface for running SPICE simulations of MOSFET devices and generating IV (current-voltage) and CV (capacitance-voltage) characteristic plots.

## Prerequisites

### System Requirements
- Python 3.6 or higher
- ngspice simulator installed on your system

### Python Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### Installing ngspice
- **Windows**: Download and install from [ngspice official website](http://ngspice.sourceforge.net/download.html)
- **Linux**: `sudo apt-get install ngspice`
- **macOS**: `brew install ngspice`

## Directory Structure
```
.
├── src/
│   └── spice_simulation.py
├── circuit.cir
├── requirements.txt
├── logs/
└── results/
```

## Usage

### Basic Usage
Run the simulation with default settings:
```bash
python src/spice_simulation.py
```

### Command Line Options
The tool supports several command-line options:

- `--circuit`: Specify the SPICE netlist file
  ```bash
  python src/spice_simulation.py --circuit circuit.cir
  ```

- `--output-dir`: Specify output directory for plots
  ```bash
  python src/spice_simulation.py --output-dir results
  ```

- `--dpi`: Set plot resolution (default: 300)
  ```bash
  python src/spice_simulation.py --dpi 600
  ```

- `--debug`: Enable debug logging
  ```bash
  python src/spice_simulation.py --debug
  ```

### Output Files
The tool generates the following outputs:

1. **Log Files**
   - Location: `logs/`
   - Format: `spice_simulation_YYYYMMDD_HHMMSS.log`
   - Contains: Simulation progress, errors, and debug information

2. **Plot Files**
   - Location: `results/` (or custom output directory)
   - Files:
     - `iv_characteristics.png`: IV characteristics plot
     - `cv_characteristics.png`: CV characteristics plot

3. **Simulation Data**
   - `iv_data.txt`: Raw IV characteristics data
   - `cv_data.txt`: Raw CV characteristics data

## SPICE Netlist Format

The tool expects a SPICE netlist file with the following structure:

```spice
* MOSFET IV and CV Characteristics Simulation
.model nmos NMOS
+ LEVEL=3
+ L=1u
+ W=10u
+ KP=50u
+ VTO=0.7
+ GAMMA=0.5
+ PHI=0.6
+ LAMBDA=0.05
+ CGSO=1n
+ CGDO=1n
+ CGBO=1n
+ N=1.0
+ COX=3.45e-3

* Circuit definition
...

* Analysis commands
.dc Vds 0 5 0.1 Vgs 0 5 1
.ac DEC 10 1k 1G
.end
```

## Troubleshooting

### Common Issues

1. **ngspice not found**
   - Ensure ngspice is installed and in your system PATH
   - Verify installation: `ngspice --version`

2. **Missing data files**
   - Check if the simulation completed successfully
   - Verify the netlist file exists and is properly formatted

3. **Plot generation errors**
   - Ensure the output directory is writable
   - Check if the simulation generated valid data

### Debug Mode
For detailed troubleshooting, run with debug mode:
```bash
python src/spice_simulation.py --debug
```
This will provide additional logging information in the log file.

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details. 