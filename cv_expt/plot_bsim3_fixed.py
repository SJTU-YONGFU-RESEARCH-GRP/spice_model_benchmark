#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# Create output directory for plots if it doesn't exist
os.makedirs('results', exist_ok=True)

# Plot CV at different frequencies
def plot_cv_multifreq():
    try:
        # Check if file exists
        data_file = 'results/cv_bsim3_data.txt'
        if not os.path.exists(data_file):
            print(f"Error: {data_file} file not found")
            return
            
        print(f"Loading data from {data_file}")
        
        # Read file and handle potential header lines
        with open(data_file, 'r') as f:
            lines = f.readlines()
            
        # Skip header line
        if lines[0].strip().startswith('Vg'):
            data_lines = lines[1:]
        else:
            data_lines = lines
            
        if len(data_lines) == 0:
            print("Error: No valid data found in data file")
            return
            
        # Debug: show first few lines
        print("First few lines of data:")
        for i, line in enumerate(data_lines[:3]):
            print(f"  {line.strip()}")
        
        # Manual parsing with fixed column handling
        vg_values = []
        cgg_1k_values = []
        cgg_10k_values = []
        cgg_100k_values = []
        cgg_1m_values = []
        
        for line in data_lines:
            parts = line.strip().split()
            if len(parts) >= 5:
                try:
                    vg = float(parts[0])
                    # Extract capacitance values, handling potential parsing issues
                    try:
                        cgg_1k = abs(float(parts[1]))
                    except:
                        cgg_1k = 0.0
                        
                    try:
                        cgg_10k = abs(float(parts[2]))
                    except:
                        cgg_10k = 0.0
                        
                    try:
                        cgg_100k = abs(float(parts[3]))
                    except:
                        cgg_100k = 0.0
                        
                    try:
                        cgg_1m = abs(float(parts[4]))
                    except:
                        cgg_1m = 0.0
                    
                    vg_values.append(vg)
                    cgg_1k_values.append(cgg_1k)
                    cgg_10k_values.append(cgg_10k)
                    cgg_100k_values.append(cgg_100k)
                    cgg_1m_values.append(cgg_1m)
                except:
                    pass
        
        if not vg_values:
            print("Error: No valid data could be parsed")
            return
            
        # Convert to numpy arrays
        vg = np.array(vg_values)
        cgg_1k = np.array(cgg_1k_values)
        cgg_10k = np.array(cgg_10k_values)
        cgg_100k = np.array(cgg_100k_values)
        cgg_1m = np.array(cgg_1m_values)
        
        # Scale to fF for better readability
        scale_factor = 1e15  # Convert F to fF
        cgg_1k *= scale_factor
        cgg_10k *= scale_factor
        cgg_100k *= scale_factor
        cgg_1m *= scale_factor
        
        print(f"Data loaded: {len(vg)} points")
        print(f"Vg range: {min(vg):.2f}V to {max(vg):.2f}V")
        
        # Create the plot
        plt.figure(figsize=(12, 8))
        
        # Plot for each frequency
        plt.plot(vg, cgg_1k, 'g-', linewidth=2.5, label='1 kHz')
        plt.plot(vg, cgg_10k, 'r-', linewidth=2, label='10 kHz')
        plt.plot(vg, cgg_100k, 'b-', linewidth=2, label='100 kHz')
        plt.plot(vg, cgg_1m, 'k-', linewidth=2, label='1 MHz')
        
        # Add threshold voltage line
        vth = 0.5  # Approximate Vth from BSIM3 model
        plt.axvline(x=vth, color='gray', linestyle='--', linewidth=1.5, label=f'Vth ≈ {vth}V')
        
        # Add regions
        plt.axvspan(-0.8, 0, alpha=0.1, color='blue', label='Accumulation')
        plt.axvspan(0, vth, alpha=0.1, color='green', label='Depletion')
        plt.axvspan(vth, max(vg), alpha=0.1, color='red', label='Inversion')
        
        # Set plot labels and properties
        plt.xlabel('Gate Voltage (V)', fontsize=12)
        plt.ylabel('Gate Capacitance (fF)', fontsize=12)
        plt.title('BSIM3 MOSFET Gate Capacitance vs Gate Voltage at Different Frequencies', fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.legend(loc='upper right')
        
        # Set y-axis limits
        y_max = np.max([np.max(cgg_1k), np.max(cgg_10k), np.max(cgg_100k), np.max(cgg_1m)])
        plt.ylim(0, y_max*1.2)
        
        # Add x and y axis lines at origin
        plt.axhline(y=0, color='k', linestyle='-', alpha=0.2)
        plt.axvline(x=0, color='k', linestyle='-', alpha=0.2)
        
        # Save the figure
        plt.tight_layout()
        plt.savefig('results/bsim3_cv_multifreq.png', dpi=300)
        print("CV multifrequency plot saved as 'results/bsim3_cv_multifreq.png'")
        
    except Exception as e:
        print(f"Error plotting CV multifrequency: {e}")
        import traceback
        traceback.print_exc()

# Run the plotting function
if __name__ == "__main__":
    print("Running BSIM3 CV plotting script (fixed version)")
    print(f"Current working directory: {os.getcwd()}")
    plot_cv_multifreq() 