#!/usr/bin/env python3
import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import logging
import sys
from datetime import datetime
import glob
import shutil

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("tran_analysis.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("TRAN_ANALYSIS")

# Constants and configuration
SPICE_NETLIST = "tran_circuit.cir"
OUTPUT_DIR = "tran_results"
REPORT_FILE = "REPORT.md"

# Set figure size constants - width 400 pixels converted to inches (at 100 dpi)
FIGURE_WIDTH = 4.0  # 400 pixels at 100 dpi
FIGURE_HEIGHT_RATIO = 0.6  # Default height ratio (height = width * ratio)
FIGURE_DPI = 100  # DPI for saving figures

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_ngspice_simulation():
    """Run NGSpice simulation and return success status"""
    logger.info("Starting NGSpice simulation...")
    
    try:
        # Run the simulation
        cmd = ["ngspice", "-b", SPICE_NETLIST]
        logger.info(f"Running command: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE, 
                               text=True,
                               check=True)
        
        logger.info("NGSpice simulation completed successfully")
        return True
    
    except subprocess.CalledProcessError as e:
        logger.error(f"NGSpice simulation failed with error: {e}")
        logger.error(f"STDERR: {e.stderr}")
        return False

def load_simulation_data(filename):
    """Load simulation data from NGSpice output files"""
    try:
        logger.info(f"Loading data from: {filename}")
        data = np.loadtxt(filename, skiprows=1)
        with open(filename, 'r') as f:
            header = f.readline().strip().split()
        
        return data, header
    except Exception as e:
        logger.error(f"Failed to load data from {filename}: {e}")
        return None, None

def analyze_large_signal_transient():
    """Analyze large signal transient simulation results"""
    logger.info("Analyzing large-signal transient results...")
    
    data, header = load_simulation_data("tran_large_signal.txt")
    if data is None:
        return None
    
    # Extract columns
    time = data[:, 0]
    gate_voltage = data[:, 1]
    drain_voltage = data[:, 2]
    drain_current = data[:, 3]
    gate_current = data[:, 4]
    source_current = data[:, 5]
    bulk_current = data[:, 6]
    
    # Create plot
    plt.figure(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT_RATIO * FIGURE_WIDTH))
    plt.subplot(2, 1, 1)
    plt.plot(time*1e9, gate_voltage, label='Gate Voltage (V)')
    plt.plot(time*1e9, drain_voltage, label='Drain Voltage (V)')
    plt.xlabel('Time (ns)')
    plt.ylabel('Voltage (V)')
    plt.legend()
    plt.grid(True)
    plt.title('Large-Signal Transient Analysis - Voltages')
    
    plt.subplot(2, 1, 2)
    plt.plot(time*1e9, drain_current*1e3, label='Drain Current (mA)')
    plt.xlabel('Time (ns)')
    plt.ylabel('Current (mA)')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    
    # Save the plot
    plot_path = os.path.join(OUTPUT_DIR, "large_signal_transient.png")
    plt.savefig(plot_path, dpi=FIGURE_DPI)
    plt.close()
    
    # Calculate metrics
    max_current = np.max(drain_current)
    rise_time = calculate_rise_time(time, gate_voltage)
    
    logger.info(f"Maximum drain current: {max_current:.6e} A")
    logger.info(f"Gate voltage rise time: {rise_time:.3f} ns")
    
    return {
        "plot_path": plot_path,
        "max_current": max_current,
        "rise_time": rise_time
    }

def analyze_switching_response():
    """Analyze switching behavior of the inverter"""
    logger.info("Analyzing switching response...")
    
    data, header = load_simulation_data("tran_switching.txt")
    if data is None:
        return None
    
    # Extract columns
    time = data[:, 0]
    input_voltage = data[:, 1]
    output_voltage = data[:, 2]
    supply_current = data[:, 3]
    
    # Load power data
    power_data, power_header = load_simulation_data("tran_switching_power.txt")
    if power_data is not None:
        switching_power = power_data[:, 1]
    else:
        switching_power = None
    
    # Create plot
    plt.figure(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT_RATIO * FIGURE_WIDTH))
    
    # Plot voltages
    plt.subplot(3, 1, 1)
    plt.plot(time*1e9, input_voltage, label='Input Voltage (V)')
    plt.plot(time*1e9, output_voltage, label='Output Voltage (V)')
    plt.xlabel('Time (ns)')
    plt.ylabel('Voltage (V)')
    plt.legend()
    plt.grid(True)
    plt.title('Inverter Switching Response')
    
    # Plot current
    plt.subplot(3, 1, 2)
    plt.plot(time*1e9, supply_current*1e3, label='Supply Current (mA)')
    plt.xlabel('Time (ns)')
    plt.ylabel('Current (mA)')
    plt.legend()
    plt.grid(True)
    
    # Plot power if available
    if switching_power is not None:
        plt.subplot(3, 1, 3)
        plt.plot(time*1e9, switching_power*1e3, label='Power Dissipation (mW)')
        plt.xlabel('Time (ns)')
        plt.ylabel('Power (mW)')
        plt.legend()
        plt.grid(True)
    
    plt.tight_layout()
    
    # Save the plot
    plot_path = os.path.join(OUTPUT_DIR, "switching_response.png")
    plt.savefig(plot_path, dpi=FIGURE_DPI)
    plt.close()
    
    # Calculate metrics
    propagation_delay = calculate_propagation_delay(time, input_voltage, output_voltage)
    
    if switching_power is not None:
        max_power = np.max(switching_power)
        avg_power = np.mean(switching_power)
    else:
        max_power = None
        avg_power = None
    
    logger.info(f"Propagation delay: {propagation_delay:.3f} ns")
    if max_power is not None:
        logger.info(f"Maximum switching power: {max_power:.6e} W")
        logger.info(f"Average switching power: {avg_power:.6e} W")
    
    return {
        "plot_path": plot_path,
        "propagation_delay": propagation_delay,
        "max_power": max_power,
        "avg_power": avg_power
    }

def analyze_delay_effect():
    """Analyze delay effects in inverter chain"""
    logger.info("Analyzing delay effects...")
    
    data, header = load_simulation_data("tran_delay.txt")
    if data is None:
        return None
    
    # Extract columns
    time = data[:, 0]
    input_voltage = data[:, 1]
    mid1_voltage = data[:, 2]
    mid2_voltage = data[:, 3]
    output_voltage = data[:, 4]
    
    # Create plot
    plt.figure(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT_RATIO * FIGURE_WIDTH))
    plt.plot(time*1e9, input_voltage, label='Input')
    plt.plot(time*1e9, mid1_voltage, label='Stage 1')
    plt.plot(time*1e9, mid2_voltage, label='Stage 2')
    plt.plot(time*1e9, output_voltage, label='Output')
    plt.xlabel('Time (ns)')
    plt.ylabel('Voltage (V)')
    plt.legend()
    plt.grid(True)
    plt.title('Delay Effect Analysis - Inverter Chain')
    
    # Save the plot
    plot_path = os.path.join(OUTPUT_DIR, "delay_effect.png")
    plt.savefig(plot_path, dpi=FIGURE_DPI)
    plt.close()
    
    # Calculate delay for each stage
    delay1 = calculate_propagation_delay(time, input_voltage, mid1_voltage)
    delay2 = calculate_propagation_delay(time, mid1_voltage, mid2_voltage)
    delay3 = calculate_propagation_delay(time, mid2_voltage, output_voltage)
    total_delay = calculate_propagation_delay(time, input_voltage, output_voltage)
    
    logger.info(f"Stage 1 delay: {delay1:.3f} ns")
    logger.info(f"Stage 2 delay: {delay2:.3f} ns")
    logger.info(f"Stage 3 delay: {delay3:.3f} ns")
    logger.info(f"Total chain delay: {total_delay:.3f} ns")
    
    return {
        "plot_path": plot_path,
        "stage1_delay": delay1,
        "stage2_delay": delay2,
        "stage3_delay": delay3,
        "total_delay": total_delay
    }

def analyze_power_dissipation():
    """Analyze power dissipation at different temperatures"""
    logger.info("Analyzing power dissipation...")
    
    # Load data for 27°C
    data_27c, header_27c = load_simulation_data("tran_power_27C.txt")
    
    # Load data for 100°C
    data_100c, header_100c = load_simulation_data("tran_power_100C.txt")
    
    if data_27c is None or data_100c is None:
        return None
    
    # Extract columns for 27°C
    time_27c = data_27c[:, 0]
    power_27c = data_27c[:, 3]
    energy_27c = data_27c[:, 4]
    
    # Extract columns for 100°C
    time_100c = data_100c[:, 0]
    power_100c = data_100c[:, 3]
    energy_100c = data_100c[:, 4]
    
    # Create power plot
    plt.figure(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT_RATIO * FIGURE_WIDTH))
    plt.plot(time_27c*1e9, power_27c*1e3, label='27°C')
    plt.plot(time_100c*1e9, power_100c*1e3, label='100°C')
    plt.xlabel('Time (ns)')
    plt.ylabel('Power (mW)')
    plt.legend()
    plt.grid(True)
    plt.title('Power Dissipation at Different Temperatures')
    
    # Save the power plot
    power_plot_path = os.path.join(OUTPUT_DIR, "power_dissipation.png")
    plt.savefig(power_plot_path, dpi=FIGURE_DPI)
    plt.close()
    
    # Create energy plot
    plt.figure(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT_RATIO * FIGURE_WIDTH))
    plt.plot(time_27c*1e9, energy_27c*1e12, label='27°C')
    plt.plot(time_100c*1e9, energy_100c*1e12, label='100°C')
    plt.xlabel('Time (ns)')
    plt.ylabel('Energy (pJ)')
    plt.legend()
    plt.grid(True)
    plt.title('Energy Consumption at Different Temperatures')
    
    # Save the energy plot
    energy_plot_path = os.path.join(OUTPUT_DIR, "energy_consumption.png")
    plt.savefig(energy_plot_path, dpi=FIGURE_DPI)
    plt.close()
    
    # Calculate metrics
    max_power_27c = np.max(power_27c)
    max_power_100c = np.max(power_100c)
    
    avg_power_27c = np.mean(power_27c)
    avg_power_100c = np.mean(power_100c)
    
    # Calculate temperature coefficient
    power_temp_coeff = (max_power_100c - max_power_27c) / (100 - 27)
    
    logger.info(f"Maximum power at 27°C: {max_power_27c:.6e} W")
    logger.info(f"Maximum power at 100°C: {max_power_100c:.6e} W")
    logger.info(f"Power temperature coefficient: {power_temp_coeff:.6e} W/°C")
    
    return {
        "power_plot_path": power_plot_path,
        "energy_plot_path": energy_plot_path,
        "max_power_27c": max_power_27c,
        "max_power_100c": max_power_100c,
        "avg_power_27c": avg_power_27c,
        "avg_power_100c": avg_power_100c,
        "power_temp_coeff": power_temp_coeff
    }

def analyze_quasi_static():
    """Analyze quasi-static behavior"""
    logger.info("Analyzing quasi-static behavior...")
    
    data, header = load_simulation_data("tran_quasi_static.txt")
    if data is None:
        return None
    
    # Extract columns
    time = data[:, 0]
    gate_voltage = data[:, 1]
    drain_voltage = data[:, 2]
    drain_current = data[:, 3]
    
    # Create plot
    plt.figure(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT_RATIO * FIGURE_WIDTH))
    
    # Plot voltages
    plt.subplot(2, 1, 1)
    plt.plot(time*1e9, gate_voltage, label='Gate Voltage (V)')
    plt.plot(time*1e9, drain_voltage, label='Drain Voltage (V)')
    plt.xlabel('Time (ns)')
    plt.ylabel('Voltage (V)')
    plt.legend()
    plt.grid(True)
    plt.title('Quasi-Static Analysis')
    
    # Plot drain current
    plt.subplot(2, 1, 2)
    plt.plot(time*1e9, drain_current*1e3, label='Drain Current (mA)')
    plt.xlabel('Time (ns)')
    plt.ylabel('Current (mA)')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    
    # Save the plot
    plot_path = os.path.join(OUTPUT_DIR, "quasi_static.png")
    plt.savefig(plot_path, dpi=FIGURE_DPI)
    plt.close()
    
    # Create I-V characteristic
    plt.figure(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT_RATIO * FIGURE_WIDTH))
    plt.plot(gate_voltage, drain_current*1e3)
    plt.xlabel('Gate Voltage (V)')
    plt.ylabel('Drain Current (mA)')
    plt.grid(True)
    plt.title('Quasi-Static I-V Characteristic')
    
    # Save the I-V plot
    iv_plot_path = os.path.join(OUTPUT_DIR, "quasi_static_iv.png")
    plt.savefig(iv_plot_path, dpi=FIGURE_DPI)
    plt.close()
    
    return {
        "plot_path": plot_path,
        "iv_plot_path": iv_plot_path
    }

def analyze_charge_conservation():
    """Analyze charge conservation"""
    logger.info("Analyzing charge conservation...")
    
    data, header = load_simulation_data("tran_charge.txt")
    if data is None:
        return None
    
    # Extract columns - updated for new data format
    time = data[:, 0]
    gate_voltage = data[:, 1]
    ig = data[:, 2]  # Gate current
    id = data[:, 3]  # Drain current
    is_ = data[:, 4]  # Source current
    ib = data[:, 5]  # Bulk current
    i_total = data[:, 6]  # Total current (should be close to zero)
    q_gate = data[:, 7]  # Gate charge (integrated current)
    q_drain = data[:, 8]  # Drain charge
    q_source = data[:, 9]  # Source charge
    q_bulk = data[:, 10]  # Bulk charge
    q_total = data[:, 11]  # Total charge
    
    # Create plot for terminal currents
    plt.figure(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT_RATIO * FIGURE_WIDTH))
    
    # Plot currents
    plt.subplot(3, 1, 1)
    plt.plot(time*1e9, ig*1e6, label='Gate Current (µA)')
    plt.plot(time*1e9, id*1e6, label='Drain Current (µA)')
    plt.plot(time*1e9, is_*1e6, label='Source Current (µA)')
    plt.plot(time*1e9, ib*1e6, label='Bulk Current (µA)')
    plt.xlabel('Time (ns)')
    plt.ylabel('Current (µA)')
    plt.legend()
    plt.grid(True)
    plt.title('Terminal Currents Analysis')
    
    # Plot total current (should be close to zero for current conservation)
    plt.subplot(3, 1, 2)
    plt.plot(time*1e9, i_total*1e6, label='Total Current (µA)')
    plt.xlabel('Time (ns)')
    plt.ylabel('Total Current (µA)')
    plt.axhline(y=0, color='r', linestyle='--', alpha=0.3)  # Zero reference line
    plt.legend()
    plt.grid(True)
    
    # Plot charges
    plt.subplot(3, 1, 3)
    plt.plot(time*1e9, q_gate*1e15, label='Gate Charge (fC)')
    plt.plot(time*1e9, q_drain*1e15, label='Drain Charge (fC)')
    plt.plot(time*1e9, q_source*1e15, label='Source Charge (fC)')
    plt.plot(time*1e9, q_bulk*1e15, label='Bulk Charge (fC)')
    plt.plot(time*1e9, q_total*1e15, label='Total Charge (fC)', linestyle='--')
    plt.xlabel('Time (ns)')
    plt.ylabel('Charge (fC)')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    
    # Save the plot
    plot_path = os.path.join(OUTPUT_DIR, "charge_conservation.png")
    plt.savefig(plot_path, dpi=FIGURE_DPI)
    plt.close()
    
    # Create a second plot to focus on total charge
    plt.figure(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT_RATIO * FIGURE_WIDTH))
    plt.plot(time*1e9, q_total*1e15, label='Total Charge (fC)')
    plt.axhline(y=q_total[0]*1e15, color='r', linestyle='--', alpha=0.3, label='Initial Value')
    plt.xlabel('Time (ns)')
    plt.ylabel('Total Charge (fC)')
    plt.title('Charge Conservation - Total Charge')
    plt.legend()
    plt.grid(True)
    
    # Save the second plot
    total_charge_path = os.path.join(OUTPUT_DIR, "total_charge.png")
    plt.savefig(total_charge_path, dpi=FIGURE_DPI)
    plt.close()
    
    # Calculate charge conservation metrics
    q_total_variation = np.max(q_total) - np.min(q_total)
    q_total_mean = np.mean(q_total)
    q_conservation_error = q_total_variation / q_total_mean * 100 if q_total_mean != 0 else float('inf')
    
    logger.info(f"Total charge variation: {q_total_variation:.6e} C")
    logger.info(f"Total charge mean: {q_total_mean:.6e} C")
    logger.info(f"Charge conservation error: {q_conservation_error:.6f}%")
    
    return {
        "plot_path": plot_path,
        "total_charge_path": total_charge_path,
        "q_total_variation": q_total_variation,
        "q_total_mean": q_total_mean,
        "q_conservation_error": q_conservation_error
    }

def calculate_rise_time(time, signal, low_threshold=0.1, high_threshold=0.9):
    """Calculate rise time (10% to 90%) of a signal"""
    # Normalize the signal
    normalized_signal = (signal - np.min(signal)) / (np.max(signal) - np.min(signal))
    
    # Find crossing points
    low_idx = np.where(normalized_signal >= low_threshold)[0][0]
    high_idx = np.where(normalized_signal >= high_threshold)[0][0]
    
    # Calculate rise time in ns
    rise_time = (time[high_idx] - time[low_idx]) * 1e9
    
    return rise_time

def calculate_propagation_delay(time, input_signal, output_signal):
    """Calculate propagation delay between input and output signals"""
    # Find the middle points (50% threshold)
    input_threshold = (np.max(input_signal) + np.min(input_signal)) / 2
    output_threshold = (np.max(output_signal) + np.min(output_signal)) / 2
    
    # Find the first rising edge of input that crosses the threshold
    input_crossings = np.where(np.diff(input_signal > input_threshold) > 0)[0]
    if len(input_crossings) == 0:
        return float('nan')
    input_idx = input_crossings[0]
    
    # Find the corresponding output response
    output_crossings = np.where(np.diff(output_signal < output_threshold) > 0)[0]
    if len(output_crossings) == 0:
        return float('nan')
    
    # Find the output crossing that happens after the input
    valid_crossings = output_crossings[output_crossings > input_idx]
    if len(valid_crossings) == 0:
        return float('nan')
    output_idx = valid_crossings[0]
    
    # Calculate propagation delay in ns
    prop_delay = (time[output_idx] - time[input_idx]) * 1e9
    
    return prop_delay

def generate_report(results):
    """Generate the Markdown report with enhanced formatting"""
    logger.info("Generating report with enhanced formatting...")
    print("Using enhanced report format with color-coded checkmarks")
    
    with open(REPORT_FILE, 'w') as f:
        f.write("# SPICE Model Verification Report\n\n")
        f.write("## Transient Analysis Results\n\n")
        f.write(f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        f.write("## Notes\n")
        f.write("- This report is automatically generated based on tran_analysis.py\n")
        f.write("- Items are marked with <span style='color: green'>✓</span> for success and <span style='color: red'>✗</span> for failure\n")
        f.write("- Any deviations from expected behavior are documented\n\n")
        
        # Large-Signal Transient section
        f.write("## 1. Large-Signal Transient Analysis\n")
        if results["large_signal"]:
            f.write("- [<span style='color: green'>✓</span>] Time-domain transient analysis completed\n")
            f.write(f"  - Maximum Drain Current: {results['large_signal']['max_current']:.6e} A\n")
            f.write(f"  - Gate Voltage Rise Time: {results['large_signal']['rise_time']:.3f} ns\n\n")
            f.write(f"<img src='{results['large_signal']['plot_path']}' alt='Large-Signal Transient Analysis' width='{FIGURE_WIDTH}px'/>\n\n")
            f.write("*Large-signal transient analysis showing voltages and current response*\n\n")
        else:
            f.write("- [<span style='color: red'>✗</span>] Time-domain transient analysis failed\n\n")
        
        # Switching section
        f.write("## 2. Switching Simulations\n")
        if results["switching"]:
            f.write("- [<span style='color: green'>✓</span>] Inverter switching behavior analyzed\n")
            f.write(f"  - Propagation Delay: {results['switching']['propagation_delay']:.3f} ns\n")
            if results['switching']['max_power'] is not None:
                f.write(f"  - Maximum Switching Power: {results['switching']['max_power']:.6e} W\n")
                f.write(f"  - Average Switching Power: {results['switching']['avg_power']:.6e} W\n\n")
            f.write(f"<img src='{results['switching']['plot_path']}' alt='Switching Response' width='{FIGURE_WIDTH}px'/>\n\n")
            f.write("*Inverter switching analysis showing input/output voltages and power*\n\n")
        else:
            f.write("- [<span style='color: red'>✗</span>] Switching simulations failed\n\n")
        
        # Delay Effect section
        f.write("## 3. Delay Effect Simulations\n")
        if results["delay"]:
            f.write("- [<span style='color: green'>✓</span>] Propagation delay through inverter chain analyzed\n")
            f.write(f"  - Stage 1 Delay: {results['delay']['stage1_delay']:.3f} ns\n")
            f.write(f"  - Stage 2 Delay: {results['delay']['stage2_delay']:.3f} ns\n")
            f.write(f"  - Stage 3 Delay: {results['delay']['stage3_delay']:.3f} ns\n")
            f.write(f"  - Total Chain Delay: {results['delay']['total_delay']:.3f} ns\n\n")
            f.write(f"<img src='{results['delay']['plot_path']}' alt='Delay Effect Analysis' width='{FIGURE_WIDTH}px'/>\n\n")
            f.write("*Delay effect analysis showing signal propagation through inverter chain*\n\n")
        else:
            f.write("- [<span style='color: red'>✗</span>] Delay effect simulations failed\n\n")
        
        # Power Dissipation section
        f.write("## 4. Transient Simulations for Power Dissipation\n")
        if results["power"]:
            f.write("- [<span style='color: green'>✓</span>] Temperature-dependent power analysis completed\n")
            f.write(f"  - Maximum Power at 27°C: {results['power']['max_power_27c']:.6e} W\n")
            f.write(f"  - Maximum Power at 100°C: {results['power']['max_power_100c']:.6e} W\n")
            f.write(f"  - Average Power at 27°C: {results['power']['avg_power_27c']:.6e} W\n")
            f.write(f"  - Average Power at 100°C: {results['power']['avg_power_100c']:.6e} W\n")
            f.write(f"  - Power Temperature Coefficient: {results['power']['power_temp_coeff']:.6e} W/°C\n\n")
            f.write(f"<img src='{results['power']['power_plot_path']}' alt='Power Dissipation' width='{FIGURE_WIDTH}px'/>\n\n")
            f.write("*Power dissipation analysis at different temperatures*\n\n")
            f.write(f"<img src='{results['power']['energy_plot_path']}' alt='Energy Consumption' width='{FIGURE_WIDTH}px'/>\n\n")
            f.write("*Energy consumption analysis at different temperatures*\n\n")
        else:
            f.write("- [<span style='color: red'>✗</span>] Power dissipation analysis failed\n\n")
        
        # Quasi-Static Analysis section
        f.write("## 5. Quasi-Static Analysis\n")
        if results["quasi_static"]:
            f.write("- [<span style='color: green'>✓</span>] Quasi-static behavior analyzed\n")
            f.write("  - Performed quasi-static transient analysis with slower rise/fall times\n")
            f.write("  - Analyzed relationship between gate voltage and drain current\n\n")
            f.write(f"<img src='{results['quasi_static']['plot_path']}' alt='Quasi-Static Analysis' width='{FIGURE_WIDTH}px'/>\n\n")
            f.write("*Quasi-static time-domain behavior analysis*\n\n")
            f.write(f"<img src='{results['quasi_static']['iv_plot_path']}' alt='Quasi-Static I-V Characteristic' width='{FIGURE_WIDTH}px'/>\n\n")
            f.write("*Quasi-static I-V characteristic showing relationship between gate voltage and drain current*\n\n")
        else:
            f.write("- [<span style='color: red'>✗</span>] Quasi-static analysis failed\n\n")
        
        # Charge Conservation section
        f.write("## 6. Charge Conservation Tests\n")
        if results["charge_conservation"]:
            # Determine status based on error percentage
            charge_status = "green" if results['charge_conservation']['q_conservation_error'] < 10 else "red"
            charge_symbol = "✓" if charge_status == "green" else "✗"
            
            f.write(f"- [<span style='color: {charge_status}'>{ charge_symbol }</span>] Charge conservation analyzed\n")
            f.write(f"  - Total Charge Variation: {results['charge_conservation']['q_total_variation']:.6e} C\n")
            f.write(f"  - Mean Total Charge: {results['charge_conservation']['q_total_mean']:.6e} C\n")
            f.write(f"  - Charge Conservation Error: {results['charge_conservation']['q_conservation_error']:.6f}%")
            
            # Add warning note if error is high
            if charge_status == "red":
                f.write(" (exceeds 10% threshold)\n")
            else:
                f.write("\n")
            
            f.write("\n")
            f.write(f"<img src='{results['charge_conservation']['plot_path']}' alt='Charge Conservation Analysis' width='{FIGURE_WIDTH}px'/>\n\n")
            f.write("*Terminal currents and charges analysis*\n\n")
            f.write(f"<img src='{results['charge_conservation']['total_charge_path']}' alt='Total Charge' width='{FIGURE_WIDTH}px'/>\n\n")
            f.write("*Total charge conservation analysis*\n\n")
        else:
            f.write("- [<span style='color: red'>✗</span>] Charge conservation tests failed\n\n")
        
        # Summary table
        f.write("## Summary of Transient Analysis\n\n")
        f.write("| Test Type | Status | Key Findings |\n")
        f.write("|-----------|--------|-------------|\n")
        
        # Large-Signal Transient
        f.write("| Large-Signal Transient | ")
        if results["large_signal"]:
            f.write("<span style='color: green'>✓</span> | ")
            f.write(f"Max Current: {results['large_signal']['max_current']:.3e} A, Rise Time: {results['large_signal']['rise_time']:.3f} ns |\n")
        else:
            f.write("<span style='color: red'>✗</span> | *Not available* |\n")
        
        # Switching
        f.write("| Switching Simulations | ")
        if results["switching"]:
            f.write("<span style='color: green'>✓</span> | ")
            f.write(f"Propagation Delay: {results['switching']['propagation_delay']:.3f} ns |\n")
        else:
            f.write("<span style='color: red'>✗</span> | *Not available* |\n")
        
        # Delay
        f.write("| Delay Effect | ")
        if results["delay"]:
            f.write("<span style='color: green'>✓</span> | ")
            f.write(f"Total Chain Delay: {results['delay']['total_delay']:.3f} ns |\n")
        else:
            f.write("<span style='color: red'>✗</span> | *Not available* |\n")
        
        # Power
        f.write("| Power Dissipation | ")
        if results["power"]:
            f.write("<span style='color: green'>✓</span> | ")
            f.write(f"Temp Coeff: {results['power']['power_temp_coeff']:.3e} W/°C |\n")
        else:
            f.write("<span style='color: red'>✗</span> | *Not available* |\n")
        
        # Quasi-Static
        f.write("| Quasi-Static Analysis | ")
        if results["quasi_static"]:
            f.write("<span style='color: green'>✓</span> | ")
            f.write("I-V characteristics analyzed |\n")
        else:
            f.write("<span style='color: red'>✗</span> | *Not available* |\n")
        
        # Charge Conservation
        f.write("| Charge Conservation | ")
        if results["charge_conservation"]:
            charge_status = "green" if results['charge_conservation']['q_conservation_error'] < 10 else "red"
            charge_symbol = "✓" if charge_status == "green" else "✗"
            f.write(f"<span style='color: {charge_status}'>{ charge_symbol }</span> | ")
            f.write(f"Error: {results['charge_conservation']['q_conservation_error']:.6f}% |\n")
        else:
            f.write("<span style='color: red'>✗</span> | *Not available* |\n")
            
        # Missing Items Section
        f.write("\n## Missing Items and Recommendations\n\n")
        
        # Check for mixed-mode simulations
        f.write("### Mixed-Mode Simulations\n")
        f.write("- [<span style='color: red'>✗</span>] Mixed-mode simulations not implemented\n")
        f.write("  - Recommendation: Add mixed-mode simulations that combine analog and digital components\n")
        f.write("  - Implementation options:\n")
        f.write("    1. Create a digital-analog interface circuit\n")
        f.write("    2. Use behavioral components with Verilog-A or similar\n")
        f.write("    3. Implement a mixed-signal oscillator or PLL circuit\n\n")

def move_result_files():
    """Move all SPICE result files to output directory"""
    logger.info("Moving SPICE result files to output directory...")
    
    # List of result file patterns to move
    result_patterns = [
        "tran_*.txt",           # All transient analysis output files
        "*.log",                # Log files
        "*.raw",                # Raw SPICE output files if any
        "*.dat",                # Any data files
    ]
    
    # Count of moved files
    moved_files = 0
    
    # Process each pattern
    for pattern in result_patterns:
        # Find all files matching the pattern
        files = glob.glob(pattern)
        
        for file in files:
            # Copy file to output directory
            dest_path = os.path.join(OUTPUT_DIR, file)
            try:
                shutil.copy2(file, dest_path)
                logger.info(f"Copied {file} to {OUTPUT_DIR}/")
                moved_files += 1
                
                # Remove original file to keep working directory clean
                os.remove(file)
                logger.info(f"Removed original {file}")
            except Exception as e:
                logger.error(f"Failed to move {file}: {e}")
    
    logger.info(f"Moved {moved_files} files to output directory")

def create_output_readme(results):
    """Create a README file in the output directory with information about the files"""
    logger.info("Creating README in output directory...")
    
    readme_path = os.path.join(OUTPUT_DIR, "README.md")
    with open(readme_path, 'w') as f:
        f.write("# SPICE Model Transient Analysis Results\n\n")
        f.write(f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        
        # General information
        f.write("## Analysis Overview\n\n")
        f.write("This directory contains all results from the transient analysis of the MOSFET SPICE model.\n")
        f.write("The analysis covers large-signal transient, switching, delay effects, power dissipation, ")
        f.write("quasi-static behavior, and charge conservation tests.\n\n")
        
        # Data files
        f.write("## Data Files\n\n")
        f.write("| File | Description |\n")
        f.write("|------|-------------|\n")
        f.write("| tran_large_signal.txt | Gate and drain voltages, terminal currents for large-signal analysis |\n")
        f.write("| tran_switching.txt | Input/output voltages and current for inverter switching analysis |\n")
        f.write("| tran_switching_power.txt | Power dissipation during switching |\n")
        f.write("| tran_delay.txt | Propagation delay through inverter chain |\n")
        f.write("| tran_power_27C.txt | Power/energy data at 27°C |\n")
        f.write("| tran_power_100C.txt | Power/energy data at 100°C |\n")
        f.write("| tran_quasi_static.txt | Quasi-static behavior data |\n")
        f.write("| tran_charge.txt | Terminal currents and charges for conservation analysis |\n")
        
        # Plot files
        f.write("\n## Plot Files\n\n")
        f.write("| File | Description |\n")
        f.write("|------|-------------|\n")
        f.write("| large_signal_transient.png | Gate/drain voltages and drain current vs time |\n")
        f.write("| switching_response.png | Inverter input/output and power dissipation |\n")
        f.write("| delay_effect.png | Signal propagation through inverter chain |\n")
        f.write("| power_dissipation.png | Power comparison at different temperatures |\n")
        f.write("| energy_consumption.png | Energy consumption comparison at different temperatures |\n")
        f.write("| quasi_static.png | Quasi-static time-domain behavior |\n")
        f.write("| quasi_static_iv.png | Quasi-static I-V relationship |\n")
        f.write("| charge_conservation.png | Terminal currents and charges |\n")
        f.write("| total_charge.png | Total charge conservation analysis |\n")
        
        # Results summary
        f.write("\n## Analysis Results Summary\n\n")
        
        f.write("| Analysis Type | Status | Key Findings |\n")
        f.write("|--------------|--------|-------------|\n")
        
        f.write("| Large-Signal Transient | ")
        if results["large_signal"]:
            f.write("✓ | ")
            f.write(f"Max Current: {results['large_signal']['max_current']:.3e} A, Rise Time: {results['large_signal']['rise_time']:.3f} ns |\n")
        else:
            f.write("✗ | *Not available* |\n")
        
        f.write("| Switching Simulations | ")
        if results["switching"]:
            f.write("✓ | ")
            f.write(f"Propagation Delay: {results['switching']['propagation_delay']:.3f} ns |\n")
        else:
            f.write("✗ | *Not available* |\n")
        
        f.write("| Delay Effect | ")
        if results["delay"]:
            f.write("✓ | ")
            f.write(f"Total Chain Delay: {results['delay']['total_delay']:.3f} ns |\n")
        else:
            f.write("✗ | *Not available* |\n")
        
        f.write("| Power Dissipation | ")
        if results["power"]:
            f.write("✓ | ")
            f.write(f"Temp Coeff: {results['power']['power_temp_coeff']:.3e} W/°C |\n")
        else:
            f.write("✗ | *Not available* |\n")
        
        f.write("| Quasi-Static Analysis | ")
        if results["quasi_static"]:
            f.write("✓ | ")
            f.write("I-V characteristics analyzed |\n")
        else:
            f.write("✗ | *Not available* |\n")
        
        f.write("| Charge Conservation | ")
        if results["charge_conservation"]:
            f.write("✓ | ")
            f.write(f"Error: {results['charge_conservation']['q_conservation_error']:.6f}% |\n")
        else:
            f.write("✗ | *Not available* |\n")
            

    
    logger.info(f"Created README.md in {OUTPUT_DIR}/")

def cleanup_workspace():
    """Clean up any remaining temporary files after analysis"""
    logger.info("Cleaning up workspace...")
    
    # List of patterns for files that should be cleaned up
    cleanup_patterns = [
        "*.log",                # Log files (except our main log)
        "*.raw",                # Raw SPICE output files
        "*.out",                # Other output files
        "*.tmp",                # Temporary files
        "ngspice_log.txt",      # Ngspice log file
        "*.dat"                 # Data files
    ]
    
    # Move our log file to output directory
    try:
        if os.path.exists("tran_analysis.log"):
            shutil.copy2("tran_analysis.log", os.path.join(OUTPUT_DIR, "tran_analysis.log"))
            logger.info("Copied tran_analysis.log to output directory")
    except Exception as e:
        logger.error(f"Failed to copy log file: {e}")
    
    # Process each pattern
    cleaned_files = 0
    for pattern in cleanup_patterns:
        files = glob.glob(pattern)
        for file in files:
            try:
                os.remove(file)
                logger.info(f"Cleaned up {file}")
                cleaned_files += 1
            except Exception as e:
                logger.error(f"Failed to clean up {file}: {e}")
    
    logger.info(f"Cleaned up {cleaned_files} temporary files")

def main():
    """Main function to run the analysis"""
    logger.info("Starting SPICE model transient analysis")
    
    # Run the NGSpice simulation
    if not run_ngspice_simulation():
        logger.error("Failed to run the NGSpice simulation. Exiting.")
        return
    
    # Create results dictionary
    results = {
        "large_signal": None,
        "switching": None,
        "delay": None,
        "power": None,
        "quasi_static": None,
        "charge_conservation": None
    }
    
    # Analyze the results
    results["large_signal"] = analyze_large_signal_transient()
    results["switching"] = analyze_switching_response()
    results["delay"] = analyze_delay_effect()
    results["power"] = analyze_power_dissipation()
    results["quasi_static"] = analyze_quasi_static()
    results["charge_conservation"] = analyze_charge_conservation()
    
    # Generate the report
    generate_report(results)
    
    # Create README for output directory
    create_output_readme(results)
    
    # Move all result files to output directory
    move_result_files()
    
    # Clean up any remaining temporary files
    cleanup_workspace()
    
    logger.info(f"Analysis completed. Report generated: {REPORT_FILE}")
    logger.info(f"All result files moved to: {OUTPUT_DIR}/")

if __name__ == "__main__":
    main() 