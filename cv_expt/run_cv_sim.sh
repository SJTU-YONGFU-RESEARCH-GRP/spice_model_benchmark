#!/bin/bash

# Run CV simulation and generate plots
# This script runs the MOSFET CV simulation and then plots the results

# Create directories
mkdir -p plots
mkdir -p results

# Clean up any existing data files
rm -f results/cv_full_data.txt results/cv_sim.log

# Run ngspice simulation using the CV-specific circuit
echo "Running MOSFET CV simulation..."
ngspice -b cv_mos_realistic.cir -o sim_log.txt

# Check if simulation was successful
if [ $? -eq 0 ]; then
    echo "Simulation completed successfully."
    
    # Check if result files exist
    if [ ! -f results/cv_full_data.txt ]; then
        echo "Error: Simulation data file not found. Check sim_log.txt for details."
        exit 1
    fi
    
    # Print a sample of the data for verification
    echo "Sample of CV data (first 5 lines):"
    head -5 results/cv_full_data.txt
    
    # Run plotting script
    echo "Generating plots..."
    python3 plot_cv_curves.py
    
    echo "Done! CV simulation and plotting complete."
    echo "Check the plots/ directory for generated CV plots:"
    echo "  - plots/cv_components.png: MOSFET capacitance components"
    echo "  - plots/cv_multifreq_characteristics.png: CV curves at different frequencies"
else
    echo "Simulation failed. Check sim_log.txt for details."
fi 