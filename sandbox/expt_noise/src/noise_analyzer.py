import os
import glob
import subprocess
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

from src.logger import Logger
from src.parser import SpiceResultParser
from src.plotter import NoisePlotter
from src.report_generator import ReportGenerator

class NoiseAnalyzer:
    """
    Main class for running noise analysis simulations and processing results
    """
    def __init__(self, spice_file="noise_analysis.cir", output_dir="results", 
                log_level="INFO", spice_cmd="ngspice"):
        """
        Initialize the noise analyzer
        
        Args:
            spice_file: SPICE netlist file path
            output_dir: Directory for storing results
            log_level: Logging level
            spice_cmd: Command to run SPICE simulator
        """
        # Create directories
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        self.data_dir = os.path.join(output_dir, "data")
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
        self.plots_dir = os.path.join(output_dir, "plots")
        if not os.path.exists(self.plots_dir):
            os.makedirs(self.plots_dir)
            
        # Initialize components
        self.logger = Logger(log_level=log_level, log_dir=os.path.join(output_dir, "logs"))
        self.parser = SpiceResultParser(self.logger)
        self.plotter = NoisePlotter(self.logger, output_dir=self.plots_dir)
        self.report_generator = ReportGenerator(self.logger)
        
        # Set file paths
        self.spice_file = spice_file
        self.spice_cmd = spice_cmd
        
        self.logger.info(f"NoiseAnalyzer initialized with SPICE file: {spice_file}")
        
    def run_simulation(self):
        """
        Run SPICE simulation for noise analysis
        
        Returns:
            bool: True if simulation successful, False otherwise
        """
        self.logger.info(f"Running SPICE simulation using {self.spice_cmd}")
        
        # Create output directories if they don't exist
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.plots_dir, exist_ok=True)
        
        try:
            # Change working directory to ensure output files go to the right place
            orig_dir = os.getcwd()
            os.chdir(self.data_dir)
            
            # Run SPICE simulation
            cmd = [self.spice_cmd, "-b", os.path.join(orig_dir, self.spice_file)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Save output to log file
            with open("ngspice_output.log", "w") as f:
                f.write(result.stdout)
                if result.stderr:
                    f.write("\n\nERRORS:\n")
                    f.write(result.stderr)
            
            # Change back to original directory
            os.chdir(orig_dir)
            
            # Check if simulation was successful
            if result.returncode != 0:
                self.logger.error(f"SPICE simulation failed with exit code {result.returncode}")
                if result.stderr:
                    self.logger.error(f"Error message: {result.stderr}")
                return False
            
            self.logger.info("SPICE simulation completed successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error running SPICE simulation: {str(e)}")
            return False
            
    def analyze_thermal_noise(self):
        """
        Analyze thermal noise from simulation results
        
        Returns:
            dict: Analysis results
        """
        self.logger.info("Analyzing thermal noise")
        
        # Get all thermal noise data files
        file_pattern = os.path.join(self.data_dir, "thermal_noise_vgs*.txt")
        files = glob.glob(file_pattern)
        
        if not files:
            self.logger.warning("No thermal noise data files found")
            return {"status": "error", "message": "No thermal noise data files found"}
            
        results = {}
        plots = []
        
        # Process each thermal noise file
        for file in sorted(files):
            try:
                # Extract bias conditions from filename
                match = re.search(r'vgs(\d+\.\d+)_vds(\d+\.\d+)', file)
                if match:
                    vgs = float(match.group(1))
                    vds = float(match.group(2))
                    bias_point = f"Vgs={vgs}V, Vds={vds}V"
                else:
                    bias_point = os.path.basename(file)
                
                # Parse data file
                data = self.parser.read_noise_data(file)
                if data is None or data.empty:
                    continue
                    
                # Extract columns
                freq = data.iloc[:, 0].values
                noise = data.iloc[:, 1].values
                
                # Analyze data
                analysis = self.parser.analyze_thermal_noise(data)
                results[bias_point] = analysis
                
                # Generate plot
                plot_title = f"Thermal Noise Spectrum at {bias_point}"
                plot_file = f"thermal_noise_{vgs:.1f}_{vds:.1f}"
                plot_path = self.plotter.plot_noise_spectrum(freq, noise, plot_title, plot_file)
                plots.append(plot_path)
                
            except Exception as e:
                self.logger.error(f"Error processing thermal noise file {file}: {str(e)}")
                
        # Create composite plot with multiple bias points
        try:
            bias_data = {}
            vgs_values = set()
            vds_values = set()
            
            for file in sorted(files):
                match = re.search(r'vgs(\d+\.\d+)_vds(\d+\.\d+)', file)
                if match:
                    vgs = float(match.group(1))
                    vds = float(match.group(2))
                    vgs_values.add(vgs)
                    vds_values.add(vds)
                    
                    data = self.parser.read_noise_data(file)
                    if data is not None and not data.empty:
                        freq = data.iloc[:, 0].values
                        noise = data.iloc[:, 1].values
                        bias_data[f"Vgs={vgs}V, Vds={vds}V"] = (freq, noise)
            
            # Plot for fixed Vgs, multiple Vds
            vgs_values = sorted(vgs_values)
            vds_values = sorted(vds_values)
            
            if len(vgs_values) > 0 and len(vds_values) > 1:
                vgs_fixed = vgs_values[len(vgs_values) // 2]  # Choose middle Vgs
                vds_data = {}
                
                for file in sorted(files):
                    match = re.search(r'vgs(\d+\.\d+)_vds(\d+\.\d+)', file)
                    if match:
                        vgs = float(match.group(1))
                        vds = float(match.group(2))
                        
                        if abs(vgs - vgs_fixed) < 0.01:  # Match the fixed Vgs
                            data = self.parser.read_noise_data(file)
                            if data is not None and not data.empty:
                                freq = data.iloc[:, 0].values
                                noise = data.iloc[:, 1].values
                                vds_data[f"Vds={vds}V"] = (freq, noise)
                
                if vds_data:
                    plot_title = f"Thermal Noise vs Vds (Vgs={vgs_fixed}V)"
                    plot_file = f"thermal_noise_vds_comparison"
                    plot_path = self.plotter.plot_multiple_noise_spectra(vds_data, plot_title, plot_file)
                    plots.append(plot_path)
            
            # Plot for fixed Vds, multiple Vgs
            if len(vds_values) > 0 and len(vgs_values) > 1:
                vds_fixed = vds_values[len(vds_values) // 2]  # Choose middle Vds
                vgs_data = {}
                
                for file in sorted(files):
                    match = re.search(r'vgs(\d+\.\d+)_vds(\d+\.\d+)', file)
                    if match:
                        vgs = float(match.group(1))
                        vds = float(match.group(2))
                        
                        if abs(vds - vds_fixed) < 0.01:  # Match the fixed Vds
                            data = self.parser.read_noise_data(file)
                            if data is not None and not data.empty:
                                freq = data.iloc[:, 0].values
                                noise = data.iloc[:, 1].values
                                vgs_data[f"Vgs={vgs}V"] = (freq, noise)
                
                if vgs_data:
                    plot_title = f"Thermal Noise vs Vgs (Vds={vds_fixed}V)"
                    plot_file = f"thermal_noise_vgs_comparison"
                    plot_path = self.plotter.plot_multiple_noise_spectra(vgs_data, plot_title, plot_file)
                    plots.append(plot_path)
                    
        except Exception as e:
            self.logger.error(f"Error creating composite thermal noise plots: {str(e)}")
            
        return {
            "status": "success",
            "results": results,
            "plots": plots
        }
        
    def analyze_flicker_noise(self):
        """
        Analyze flicker (1/f) noise from simulation results
        
        Returns:
            dict: Analysis results
        """
        self.logger.info("Analyzing flicker noise")
        
        # Get flicker noise data file
        file_path = os.path.join(self.data_dir, "flicker_noise.txt")
        
        if not os.path.exists(file_path):
            self.logger.warning("Flicker noise data file not found")
            return {"status": "error", "message": "Flicker noise data file not found"}
            
        try:
            # Parse data file
            data = self.parser.read_noise_data(file_path)
            if data is None or data.empty:
                return {"status": "error", "message": "Failed to parse flicker noise data"}
                
            # Extract columns
            freq = data.iloc[:, 0].values
            noise = data.iloc[:, 1].values
            
            # Analyze data
            analysis = self.parser.analyze_flicker_noise(data)
            
            # Generate plot
            plot_title = "Flicker (1/f) Noise Spectrum"
            plot_file = "flicker_noise"
            plot_path = self.plotter.plot_noise_spectrum(freq, noise, plot_title, plot_file)
            
            # Check for output noise file
            output_file = os.path.join(self.data_dir, "output_noise.txt")
            output_data = None
            if os.path.exists(output_file):
                output_data = self.parser.read_noise_data(output_file)
                
            if output_data is not None and not output_data.empty:
                output_freq = output_data.iloc[:, 0].values
                output_noise = output_data.iloc[:, 1].values
                
                # Plot comparison between input and output noise
                plot_title = "Input vs Output Noise"
                plot_file = "input_output_noise"
                
                additional_data = {"Output Noise": output_noise}
                comparison_plot = self.plotter.plot_noise_spectrum(
                    freq, noise, plot_title, plot_file, 
                    additional_data=additional_data
                )
            else:
                comparison_plot = None
                
            plots = [p for p in [plot_path, comparison_plot] if p is not None]
                
            return {
                "status": "success",
                "results": analysis,
                "plots": plots
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing flicker noise: {str(e)}")
            return {"status": "error", "message": str(e)}
            
    def analyze_shot_noise(self):
        """
        Analyze shot noise from simulation results
        
        Returns:
            dict: Analysis results
        """
        self.logger.info("Analyzing shot noise")
        
        # Get shot noise data file
        file_path = os.path.join(self.data_dir, "shot_noise.txt")
        
        if not os.path.exists(file_path):
            self.logger.warning("Shot noise data file not found")
            return {"status": "error", "message": "Shot noise data file not found"}
            
        try:
            # Parse data file
            data = self.parser.read_noise_data(file_path)
            if data is None or data.empty:
                return {"status": "error", "message": "Failed to parse shot noise data"}
                
            # Extract columns
            freq = data.iloc[:, 0].values
            noise = data.iloc[:, 1].values
            
            # Analyze data
            analysis = self.parser.analyze_shot_noise(data)
            
            # Generate plot
            plot_title = "Shot Noise Spectrum"
            plot_file = "shot_noise"
            plot_path = self.plotter.plot_noise_spectrum(freq, noise, plot_title, plot_file)
                
            return {
                "status": "success",
                "results": analysis,
                "plots": [plot_path]
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing shot noise: {str(e)}")
            return {"status": "error", "message": str(e)}
            
    def analyze_temperature_dependence(self):
        """
        Analyze temperature dependence of noise
        
        Returns:
            dict: Analysis results
        """
        self.logger.info("Analyzing temperature dependence of noise")
        
        # Get temperature-dependent noise data files
        file_pattern = os.path.join(self.data_dir, "noise_temp*.txt")
        files = glob.glob(file_pattern)
        
        if not files:
            self.logger.warning("No temperature-dependent noise data files found")
            return {"status": "error", "message": "No temperature-dependent noise data files found"}
            
        try:
            # Extract temperature from filenames and plot multiple spectra
            temp_data = {}
            temperatures = []
            noise_at_1khz = []
            
            for file in sorted(files):
                match = re.search(r'temp(-?\d+)', file)
                if match:
                    temp = int(match.group(1))
                    temperatures.append(temp)
                    
                    data = self.parser.read_noise_data(file)
                    if data is not None and not data.empty:
                        freq = data.iloc[:, 0].values
                        noise = data.iloc[:, 1].values
                        temp_data[f"{temp}°C"] = (freq, noise)
                        
                        # Find noise at approximately 1 kHz for trend analysis
                        if len(freq) > 0:
                            # Use a safer way to find closest index to 1 kHz
                            freq_1khz_idx = 0
                            min_diff = float('inf')
                            for i, f in enumerate(freq):
                                diff = abs(f - 1000)
                                if diff < min_diff:
                                    min_diff = diff
                                    freq_1khz_idx = i
                            noise_at_1khz.append(noise[freq_1khz_idx])
            
            # Plot multiple spectra
            plot_title = "Noise Spectrum vs Temperature"
            plot_file = "noise_vs_temperature"
            spectra_plot = self.plotter.plot_multiple_noise_spectra(temp_data, plot_title, plot_file)
            
            # Plot noise vs temperature trend
            if len(temperatures) > 1 and len(noise_at_1khz) == len(temperatures):
                trend_title = "Noise vs Temperature (at 1 kHz)"
                trend_file = "noise_temp_trend"
                trend_plot = self.plotter.plot_noise_vs_parameter(
                    np.array(temperatures), 
                    np.array(noise_at_1khz), 
                    "Temperature (°C)", 
                    trend_title, 
                    trend_file
                )
                plots = [p for p in [spectra_plot, trend_plot] if p is not None]
            else:
                plots = [spectra_plot] if spectra_plot else []
                
            # Calculate temperature coefficient
            if len(temperatures) > 1 and len(noise_at_1khz) > 1:
                # Calculate slope of noise vs temperature
                slope, intercept = np.polyfit(temperatures, noise_at_1khz, 1)
                temp_coeff = slope
                
                # Calculate correlation coefficient
                corr_coef = np.corrcoef(temperatures, noise_at_1khz)[0, 1]
                
                results = {
                    "temperature_coefficient": temp_coeff,
                    "correlation_coefficient": corr_coef,
                    "temperatures": temperatures,
                    "noise_values": noise_at_1khz
                }
            else:
                results = {
                    "message": "Insufficient data for temperature coefficient calculation"
                }
                
            return {
                "status": "success",
                "results": results,
                "plots": plots
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing temperature dependence: {str(e)}")
            return {"status": "error", "message": str(e)}
            
    def analyze_geometry_dependence(self):
        """
        Analyze device geometry (W, L) dependence of noise
        
        Returns:
            dict: Analysis results
        """
        self.logger.info("Analyzing geometry dependence of noise")
        
        results = {}
        plots = []
        errors = []
        
        # Analyze length dependence
        try:
            self.logger.info("Analyzing channel length dependence")
            
            # Get length-dependent noise data files
            file_pattern = os.path.join(self.data_dir, "noise_length*.txt")
            files = glob.glob(file_pattern)
            
            if files:
                # Extract length from filenames
                def extract_length(filename):
                    match = re.search(r'length(\d+\.\d+e[-+]?\d+)', filename)
                    if match:
                        try:
                            return float(match.group(1))
                        except ValueError:
                            self.logger.warning(f"Could not convert {match.group(1)} to float")
                            return None
                    return None
                    
                lengths, noise_values = self.parser.extract_noise_vs_parameter(file_pattern, extract_length)
                
                if lengths is not None and noise_values is not None and len(lengths) > 1:
                    # Verify that the data shows actual variation with length
                    noise_variation = np.std(noise_values) / np.mean(noise_values)
                    if noise_variation < 1e-6:  # Effectively no variation
                        error_msg = "Length dependence analysis failed: Noise values don't vary with transistor length"
                        self.logger.error(error_msg)
                        errors.append(error_msg)
                        results["length_dependence"] = {
                            "status": "error",
                            "message": error_msg,
                            "lengths": lengths.tolist(),
                            "noise_values": noise_values.tolist(),
                            "noise_variation": noise_variation
                        }
                    else:
                        # Plot noise vs length trend
                        trend_title = "Noise vs Channel Length (at 1 kHz)"
                        trend_file = "noise_length_trend"
                        trend_plot = self.plotter.plot_noise_vs_parameter(
                            lengths, 
                            noise_values, 
                            "Channel Length (m)", 
                            trend_title, 
                            trend_file
                        )
                        
                        if trend_plot:
                            plots.append(trend_plot)
                            
                        # Calculate length scaling factor (expected to be 1/L for flicker noise)
                        # Plot on log-log scale to verify scaling factor
                        plt.figure(figsize=(10, 6))
                        plt.loglog(lengths, noise_values, 'bo-', linewidth=2, markersize=6)
                        
                        # Calculate slope on log-log scale
                        log_lengths = np.log10(lengths)
                        log_noise = np.log10(noise_values)
                        slope, intercept = np.polyfit(log_lengths, log_noise, 1)
                        
                        # Generate fitted line
                        x_fit = np.logspace(np.log10(min(lengths)), np.log10(max(lengths)), 100)
                        y_fit = 10**intercept * x_fit**slope
                        
                        plt.plot(x_fit, y_fit, 'r--', linewidth=1.5, 
                                 label=f'Fit: Noise ∝ L^{slope:.2f}')
                        
                        plt.xlabel('Channel Length (m)')
                        plt.ylabel('Noise (V²/Hz at 1 kHz)')
                        plt.title('Noise Scaling with Channel Length')
                        plt.grid(True, which='both', linestyle='--', alpha=0.6)
                        plt.legend()
                        
                        log_plot_path = os.path.join(self.plots_dir, "noise_length_scaling.png")
                        plt.tight_layout()
                        plt.savefig(log_plot_path, dpi=300)
                        plt.close()
                        
                        plots.append(log_plot_path)
                        
                        results["length_dependence"] = {
                            "status": "success",
                            "scaling_factor": slope,
                            "lengths": lengths.tolist(),
                            "noise_values": noise_values.tolist()
                        }
                else:
                    error_msg = "Insufficient length-dependent data for analysis"
                    self.logger.warning(error_msg)
                    errors.append(error_msg)
                    results["length_dependence"] = {"status": "error", "message": error_msg}
            else:
                error_msg = "No length-dependent noise data files found"
                self.logger.warning(error_msg)
                errors.append(error_msg)
                results["length_dependence"] = {"status": "error", "message": error_msg}
                
        except Exception as e:
            error_msg = f"Error analyzing length dependence: {str(e)}"
            self.logger.error(error_msg)
            errors.append(error_msg)
            results["length_dependence"] = {"status": "error", "message": error_msg}
            
        # Analyze width dependence
        try:
            self.logger.info("Analyzing channel width dependence")
            
            # Get width-dependent noise data files
            file_pattern = os.path.join(self.data_dir, "noise_width*.txt")
            files = glob.glob(file_pattern)
            
            if files:
                # Extract width from filenames
                def extract_width(filename):
                    match = re.search(r'width(\d+\.\d+e[-+]?\d+)', filename)
                    if match:
                        try:
                            return float(match.group(1))
                        except ValueError:
                            self.logger.warning(f"Could not convert {match.group(1)} to float")
                            return None
                    return None
                    
                widths, noise_values = self.parser.extract_noise_vs_parameter(file_pattern, extract_width)
                
                if widths is not None and noise_values is not None and len(widths) > 1:
                    # Verify that the data shows actual variation with width
                    noise_variation = np.std(noise_values) / np.mean(noise_values)
                    if noise_variation < 1e-6:  # Effectively no variation
                        error_msg = "Width dependence analysis failed: Noise values don't vary with transistor width"
                        self.logger.error(error_msg)
                        errors.append(error_msg)
                        results["width_dependence"] = {
                            "status": "error",
                            "message": error_msg,
                            "widths": widths.tolist(),
                            "noise_values": noise_values.tolist(),
                            "noise_variation": noise_variation
                        }
                    else:
                        # Plot noise vs width trend
                        trend_title = "Noise vs Channel Width (at 1 kHz)"
                        trend_file = "noise_width_trend"
                        trend_plot = self.plotter.plot_noise_vs_parameter(
                            widths, 
                            noise_values, 
                            "Channel Width (m)", 
                            trend_title, 
                            trend_file
                        )
                        
                        if trend_plot:
                            plots.append(trend_plot)
                            
                        # Calculate width scaling factor (expected to be 1/W for flicker noise)
                        # Plot on log-log scale to verify scaling factor
                        plt.figure(figsize=(10, 6))
                        plt.loglog(widths, noise_values, 'bo-', linewidth=2, markersize=6)
                        
                        # Calculate slope on log-log scale
                        log_widths = np.log10(widths)
                        log_noise = np.log10(noise_values)
                        slope, intercept = np.polyfit(log_widths, log_noise, 1)
                        
                        # Generate fitted line
                        x_fit = np.logspace(np.log10(min(widths)), np.log10(max(widths)), 100)
                        y_fit = 10**intercept * x_fit**slope
                        
                        plt.plot(x_fit, y_fit, 'r--', linewidth=1.5, 
                                 label=f'Fit: Noise ∝ W^{slope:.2f}')
                        
                        plt.xlabel('Channel Width (m)')
                        plt.ylabel('Noise (V²/Hz at 1 kHz)')
                        plt.title('Noise Scaling with Channel Width')
                        plt.grid(True, which='both', linestyle='--', alpha=0.6)
                        plt.legend()
                        
                        log_plot_path = os.path.join(self.plots_dir, "noise_width_scaling.png")
                        plt.tight_layout()
                        plt.savefig(log_plot_path, dpi=300)
                        plt.close()
                        
                        plots.append(log_plot_path)
                        
                        results["width_dependence"] = {
                            "status": "success",
                            "scaling_factor": slope,
                            "widths": widths.tolist(),
                            "noise_values": noise_values.tolist()
                        }
                else:
                    error_msg = "Insufficient width-dependent data for analysis"
                    self.logger.warning(error_msg)
                    errors.append(error_msg)
                    results["width_dependence"] = {"status": "error", "message": error_msg}
            else:
                error_msg = "No width-dependent noise data files found"
                self.logger.warning(error_msg)
                errors.append(error_msg)
                results["width_dependence"] = {"status": "error", "message": error_msg}
                
        except Exception as e:
            error_msg = f"Error analyzing width dependence: {str(e)}"
            self.logger.error(error_msg)
            errors.append(error_msg)
            results["width_dependence"] = {"status": "error", "message": error_msg}
            
        return {
            "status": "error" if errors else "success",
            "results": results,
            "plots": plots,
            "errors": errors
        }
        
    def analyze_frequency_components(self):
        """
        Analyze frequency-dependent noise components
        
        Returns:
            dict: Analysis results
        """
        self.logger.info("Analyzing frequency-dependent noise components")
        
        # Get frequency component data file
        file_path = os.path.join(self.data_dir, "freq_dependent_noise.txt")
        
        if not os.path.exists(file_path):
            error_msg = "Frequency-dependent noise data file not found"
            self.logger.warning(error_msg)
            return {"status": "error", "message": error_msg}
            
        try:
            # Parse data file
            data = self.parser.read_noise_data(file_path)
            if data is None or data.empty:
                error_msg = "Failed to parse frequency component data"
                self.logger.error(error_msg)
                return {"status": "error", "message": error_msg}
                
            # Check number of columns
            if len(data.columns) < 2:
                error_msg = "Insufficient data columns in frequency component file"
                self.logger.error(error_msg)
                return {"status": "error", "message": error_msg}
            
            # Extract frequency column
            freq = data.iloc[:, 0].values
            
            # Extract total noise column
            if len(data.columns) >= 2:
                total_noise = data.iloc[:, 1].values
            else:
                error_msg = "Total noise data not found in frequency file"
                self.logger.error(error_msg)
                return {"status": "error", "message": error_msg}
            
            # Check if thermal and flicker components are available
            if len(data.columns) >= 4:
                # We have separate thermal and flicker noise components
                thermal = data.iloc[:, 2].values
                flicker = data.iloc[:, 3].values
                
                # Check if these components have actual data (non-zero values)
                if np.sum(thermal) < 1e-20 or np.sum(flicker) < 1e-20:
                    error_msg = "Thermal or flicker noise components contain only zero values"
                    self.logger.warning(error_msg)
                    return {"status": "error", "message": error_msg}
                
                # Generate component plot
                plot_title = "Noise Components Spectrum"
                plot_file = "noise_components"
                plot_path = self.plotter.plot_noise_contrib_components(
                    freq, thermal, flicker, total_noise, plot_title, plot_file
                )
                
                # Find crossover frequency (where thermal = flicker)
                crossover_freq = None
                for i in range(1, len(freq)):
                    if (thermal[i-1] < flicker[i-1] and thermal[i] >= flicker[i]) or \
                       (thermal[i-1] > flicker[i-1] and thermal[i] <= flicker[i]):
                        # Linear interpolation to find exact crossover
                        t1, t2 = thermal[i-1], thermal[i]
                        f1, f2 = flicker[i-1], flicker[i]
                        x1, x2 = freq[i-1], freq[i]
                        
                        if abs(t2-t1) > 1e-10:  # Avoid division by zero
                            frac = (f1 - t1) / (t2 - t1 - (f2 - f1))
                            crossover_freq = x1 + frac * (x2 - x1)
                        break
                
                # Calculate noise contributions
                # Avoid division by zero
                valid_indices = total_noise > 1e-20
                if np.any(valid_indices):
                    thermal_contrib = np.mean(thermal[valid_indices] / total_noise[valid_indices]) * 100
                    flicker_contrib = np.mean(flicker[valid_indices] / total_noise[valid_indices]) * 100
                else:
                    thermal_contrib = 0
                    flicker_contrib = 0
                
                results = {
                    "crossover_frequency": crossover_freq,
                    "thermal_noise_contribution": thermal_contrib,
                    "flicker_noise_contribution": flicker_contrib
                }
            else:
                # Only total noise available - we can't extract components
                error_msg = "Frequency file only contains total noise, separate components not available"
                self.logger.warning(error_msg)
                
                # Still plot the total noise
                plot_title = "Frequency-Dependent Noise Spectrum"
                plot_file = "freq_dependent_noise"
                plot_path = self.plotter.plot_noise_spectrum(freq, total_noise, plot_title, plot_file)
                
                return {
                    "status": "error",
                    "message": error_msg,
                    "plots": [plot_path]
                }
                
            return {
                "status": "success",
                "results": results,
                "plots": [plot_path]
            }
            
        except Exception as e:
            error_msg = f"Error analyzing frequency components: {str(e)}"
            self.logger.error(error_msg)
            return {"status": "error", "message": error_msg}
            
    def run_analysis(self):
        """
        Run the full noise analysis workflow
        
        Returns:
            dict: All analysis results
        """
        self.logger.info("Starting noise analysis workflow")
        
        # Run simulation
        if not self.run_simulation():
            self.logger.error("Simulation failed, cannot proceed with analysis")
            return {"status": "error", "message": "Simulation failed"}
            
        # Run all analyses
        analysis_results = {
            "thermal_noise": self.analyze_thermal_noise(),
            "flicker_noise": self.analyze_flicker_noise(),
            "shot_noise": self.analyze_shot_noise(),
            "temperature_dependence": self.analyze_temperature_dependence(),
            "geometry_dependence": self.analyze_geometry_dependence(),
            "frequency_components": self.analyze_frequency_components()
        }
        
        # Generate report
        report_path = os.path.join(self.output_dir, "REPORT.md")
        self.report_generator.generate_report(analysis_results, report_path)
        
        self.logger.info(f"Analysis complete. Report generated at {report_path}")
        
        return {
            "status": "success",
            "results": analysis_results,
            "report_path": report_path
        } 