#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# Create output directory for plots if it doesn't exist
os.makedirs('results', exist_ok=True)

# Plot CV Components at 1MHz
def plot_cv_components():
    try:
        # Check if file exists
        data_file = 'results/cv_full_data.txt'
        if not os.path.exists(data_file):
            print(f"Error: {data_file} file not found")
            return
            
        print(f"Loading data from {data_file}")
        
        # Read file and handle potential header lines
        with open(data_file, 'r') as f:
            lines = f.readlines()
            
        # Skip header lines that start with #, Index, etc.
        data_lines = [line for line in lines if not line.strip().startswith(('#', 'Index'))]
        if len(data_lines) == 0:
            print("Error: No valid data found in data file")
            return
            
        # Debug: show first few lines
        print("First few lines of data:")
        for i, line in enumerate(data_lines[:3]):
            print(f"  {line.strip()}")
            
        # Manual parsing to handle potential format issues
        data = []
        for line in data_lines:
            try:
                parts = line.strip().split()
                # Check if we have a valid line with enough data
                if len(parts) >= 2:  # At least vg and capacitance values
                    row = []
                    row.append(float(parts[0]))  # Gate voltage
                    # Add capacitance values if available
                    for i in range(1, min(len(parts), 5)):
                        try:
                            row.append(float(parts[i]))
                        except:
                            row.append(0.0)
                    data.append(row)
            except:
                continue
                
        if not data:
            print("Error: No valid data could be parsed")
            return
            
        data = np.array(data)
        print(f"Data shape: {data.shape}")
        
        # Extract data columns
        vg = data[:, 0]  # Gate voltage
        
        # Use the 1MHz data as the total gate capacitance
        scale_factor = 1e15  # Convert to fF for better visibility
        
        # Get the Cgg at 1MHz - column index depends on data structure
        if data.shape[1] > 4:
            cgg = data[:, 4] * scale_factor
        else:
            cgg = data[:, 1] * scale_factor
        
        print(f"Data loaded: {len(vg)} points")
        print(f"Vg range: {min(vg):.2f}V to {max(vg):.2f}V")
        
        # Create the plot
        plt.figure(figsize=(12, 8))
        
        # Plot total gate capacitance
        plt.plot(vg, cgg, 'k-', linewidth=2.5, label='Total Gate Cap (Cgg)')
        
        # Add threshold voltage line
        vth = 0.4  # Approximate Vth
        plt.axvline(x=vth, color='gray', linestyle='--', linewidth=1.5, label=f'Vth ≈ {vth}V')
        
        # Add region shading
        plt.axvspan(-0.8, 0, alpha=0.1, color='blue', label='Accumulation')
        plt.axvspan(0, vth, alpha=0.1, color='green', label='Depletion')
        plt.axvspan(vth, 1.2, alpha=0.1, color='red', label='Inversion')
        
        # Set plot labels and properties
        plt.xlabel('Gate Voltage (V)', fontsize=12)
        plt.ylabel('Capacitance (fF)', fontsize=12)
        plt.title('MOSFET Gate Capacitance at 1MHz', fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.legend(loc='upper right')
        
        # Set y-axis limits
        plt.ylim(0, np.max(cgg)*1.2)
        
        # Add x and y axis lines at origin
        plt.axhline(y=0, color='k', linestyle='-', alpha=0.2)
        plt.axvline(x=0, color='k', linestyle='-', alpha=0.2)
        
        # Save the figure
        plt.tight_layout()
        plt.savefig('results/cv_components.png', dpi=300)
        print("CV components plot saved as 'results/cv_components.png'")
        
    except Exception as e:
        print(f"Error plotting CV components: {e}")
        import traceback
        traceback.print_exc()

# Plot CV at different frequencies
def plot_cv_multifreq():
    try:
        # Check if file exists
        data_file = 'results/cv_full_data.txt'
        if not os.path.exists(data_file):
            print(f"Error: {data_file} file not found")
            return
            
        print(f"Loading data from {data_file}")
        
        # Read file and handle potential header lines
        with open(data_file, 'r') as f:
            lines = f.readlines()
            
        # Skip header line
        data_lines = [line for line in lines if not line.strip().startswith(('#', 'Index'))]
        if len(data_lines) == 0:
            print("Error: No valid data found in data file")
            return
            
        # Manual parsing to handle potential format issues
        data = []
        for line in data_lines:
            try:
                parts = line.strip().split()
                # Check if we have a valid line with enough data
                if len(parts) >= 2:  # At least vg and one capacitance value
                    row = []
                    row.append(float(parts[0]))  # Gate voltage
                    # Add capacitance values if available
                    for i in range(1, min(len(parts), 5)):
                        try:
                            row.append(float(parts[i]))
                        except:
                            row.append(0.0)
                    data.append(row)
            except:
                continue
                
        if not data:
            print("Error: No valid data could be parsed")
            return
            
        data = np.array(data)
        print(f"Data shape: {data.shape}")
        
        # Extract data columns
        vg = data[:, 0]  # Gate voltage
        
        # Scale to fF for better readability
        scale_factor = 1e15  # Convert F to fF
        
        # Check if we have multifrequency data
        has_multifreq = data.shape[1] >= 5
        
        if has_multifreq:
            # Get capacitance values at different frequencies
            cgg_1k = data[:, 1] * scale_factor   # Cgg at 1kHz (column 2)
            cgg_10k = data[:, 2] * scale_factor  # Cgg at 10kHz (column 3)
            cgg_100k = data[:, 3] * scale_factor # Cgg at 100kHz (column 4)
            cgg_1m = data[:, 4] * scale_factor   # Cgg at 1MHz (column 5)
            
            print(f"Data loaded: {len(vg)} points")
            
            # Create the plot
            plt.figure(figsize=(12, 8))
            
            # Plot for each frequency
            plt.plot(vg, cgg_1k, 'g-', linewidth=2.5, label='1 kHz')
            plt.plot(vg, cgg_10k, 'r-', linewidth=2, label='10 kHz')
            plt.plot(vg, cgg_100k, 'b-', linewidth=2, label='100 kHz')
            plt.plot(vg, cgg_1m, 'k-', linewidth=2, label='1 MHz')
            
            # Add threshold voltage line
            vth = 0.4  # Approximate Vth
            plt.axvline(x=vth, color='gray', linestyle='--', linewidth=1.5, label=f'Vth ≈ {vth}V')
            
            # Add region shading
            plt.axvspan(-0.8, 0, alpha=0.1, color='blue', label='Accumulation')
            plt.axvspan(0, vth, alpha=0.1, color='green', label='Depletion')
            plt.axvspan(vth, 1.2, alpha=0.1, color='red', label='Inversion')
            
            # Set plot labels and properties
            plt.xlabel('Gate Voltage (V)', fontsize=12)
            plt.ylabel('Gate Capacitance (fF)', fontsize=12)
            plt.title('MOSFET Gate Capacitance vs Gate Voltage at Different Frequencies', fontsize=14)
            plt.grid(True, alpha=0.3)
            plt.legend(loc='lower right')
            
            # Set y-axis limits
            y_max = np.max([np.max(cgg_1k), np.max(cgg_10k), np.max(cgg_100k), np.max(cgg_1m)])
            plt.ylim(0, y_max*1.2)
            
            # Add x and y axis lines at origin
            plt.axhline(y=0, color='k', linestyle='-', alpha=0.2)
            plt.axvline(x=0, color='k', linestyle='-', alpha=0.2)
            
            # Save the figure
            plt.tight_layout()
            plt.savefig('results/cv_multifreq_characteristics.png', dpi=300)
            print("CV multifrequency plot saved as 'results/cv_multifreq_characteristics.png'")
        else:
            print("Warning: No multifrequency data available. Skipping multifrequency plot.")
        
    except Exception as e:
        print(f"Error plotting CV multifrequency: {e}")
        import traceback
        traceback.print_exc()

# Run the plotting functions
if __name__ == "__main__":
    print("Running CV plotting script")
    print(f"Current working directory: {os.getcwd()}")
    plot_cv_components()
    plot_cv_multifreq() 