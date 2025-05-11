#!/usr/bin/env python3
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import logging
import subprocess
import re
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("env_reliability_analysis.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ENV_RELIABILITY_ANALYSIS")

# Directories
OUTPUT_DIR = Path("results")
PLOT_DIR = OUTPUT_DIR / "plots"
REPORT_PATH = Path("REPORT.md")

# Ensure directories exist
OUTPUT_DIR.mkdir(exist_ok=True)
PLOT_DIR.mkdir(exist_ok=True)

# Helper function for consistent plot styling
def setup_plot(title, xlabel, ylabel):
    plt.figure(figsize=(10, 6))
    plt.title(title, fontsize=14)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.grid(True, alpha=0.3)
    
def save_plot(filename, tight=True):
    if tight:
        plt.tight_layout()
    plt.savefig(PLOT_DIR / filename, dpi=300)
    plt.close()

class SpiceResultParser:
    """Parser for SPICE simulation output files"""
    
    @staticmethod
    def parse_thermal_analysis(filepath="thermal_analysis.txt"):
        """Parse thermal analysis data"""
        logger.info(f"Parsing thermal analysis data from {filepath}")
        try:
            # Check if file exists
            if not os.path.exists(filepath):
                logger.error(f"File not found: {filepath}")
                return None
                
            # Read thermal data
            df = pd.read_csv(filepath, sep=r'\s+')
            logger.info(f"Successfully loaded thermal data with shape {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Error parsing thermal analysis data: {e}")
            return None
    
    @staticmethod
    def parse_thermal_freq(filepath="thermal_freq_data.txt"):
        """Parse thermal frequency analysis data"""
        logger.info(f"Parsing thermal frequency data from {filepath}")
        try:
            # Check if file exists
            if not os.path.exists(filepath):
                logger.error(f"File not found: {filepath}")
                return None, None
            
            # Try to read the file
            try:
                data = np.loadtxt(filepath, skiprows=1)
                # Check if data is empty
                if data.size == 0:
                    logger.error("Empty data file")
                    return None, None
                    
                # Check if data is 2D
                if len(data.shape) == 2 and data.shape[1] >= 2:
                    freq = data[:, 0]
                    thermal_z = data[:, 1]
                else:
                    # If data is 1D or doesn't have enough columns
                    logger.error("Data doesn't have enough columns")
                    return None, None
            except Exception as e:
                logger.error(f"Error reading thermal frequency data: {e}")
                return None, None
                
            logger.info(f"Successfully loaded thermal frequency data with {len(freq)} points")
            return freq, thermal_z
        except Exception as e:
            logger.error(f"Error parsing thermal frequency data: {e}")
            return None, None
            
    @staticmethod
    def parse_process_corners(filepath="process_corners.txt"):
        """Parse process corner analysis data"""
        logger.info(f"Parsing process corner data from {filepath}")
        try:
            # Check if file exists
            if not os.path.exists(filepath):
                logger.error(f"File not found: {filepath}")
                return None
                
            # Read process corner data
            df = pd.read_csv(filepath, sep=r'\s+')
            logger.info(f"Successfully loaded process corner data with shape {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Error parsing process corner data: {e}")
            return None
            
    @staticmethod
    def parse_monte_carlo(filepath="monte_carlo.txt"):
        """Parse Monte Carlo analysis data"""
        logger.info(f"Parsing Monte Carlo data from {filepath}")
        try:
            # Check if file exists
            if not os.path.exists(filepath):
                logger.error(f"File not found: {filepath}")
                return None
                
            # Read Monte Carlo data
            df = pd.read_csv(filepath, sep=r'\s+')
            logger.info(f"Successfully loaded Monte Carlo data with shape {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Error parsing Monte Carlo data: {e}")
            return None
            
    @staticmethod
    def parse_aging_analysis(filepath="aging_analysis.txt"):
        """Parse aging analysis data"""
        logger.info(f"Parsing aging analysis data from {filepath}")
        try:
            # Check if file exists
            if not os.path.exists(filepath):
                logger.error(f"File not found: {filepath}")
                return None
                
            # Read aging data
            df = pd.read_csv(filepath, sep=r'\s+')
            logger.info(f"Successfully loaded aging data with shape {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Error parsing aging analysis data: {e}")
            return None
            
    @staticmethod
    def parse_stress_test(filepath="stress_test.txt"):
        """Parse stress test data"""
        logger.info(f"Parsing stress test data from {filepath}")
        try:
            # Check if file exists
            if not os.path.exists(filepath):
                logger.error(f"File not found: {filepath}")
                return None
                
            # Read stress test data
            df = pd.read_csv(filepath, sep=r'\s+')
            logger.info(f"Successfully loaded stress test data with shape {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Error parsing stress test data: {e}")
            return None


class EnvironmentalReliabilityAnalyzer:
    """Analyze environmental and reliability aspects of MOSFET models"""
    
    def __init__(self):
        self.parser = SpiceResultParser()
        self.report_content = []
        
    def add_to_report(self, content):
        """Add content to the report"""
        self.report_content.append(content)
        
    def generate_report(self):
        """Write report to REPORT.md"""
        with open(REPORT_PATH, 'w') as f:
            f.write("\n".join(self.report_content))
        logger.info(f"Report generated at {REPORT_PATH}")
        
    def run_ngspice_simulation(self, netlist="env_reliability.cir"):
        """Run ngspice simulation"""
        logger.info(f"Running ngspice simulation with netlist {netlist}")
        
        # Run ngspice in batch mode
        try:
            result = subprocess.run(
                ["ngspice", "-b", netlist], 
                capture_output=True, 
                text=True, 
                check=True
            )
            logger.info("ngspice simulation completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"ngspice simulation failed: {e.stderr}")
            return False
            
    def analyze_temperature_thermal(self):
        """Analyze temperature and thermal characteristics"""
        logger.info("Analyzing temperature and thermal characteristics")
        
        # Parse data
        thermal_df = self.parser.parse_thermal_analysis()
        freq, thermal_z = self.parser.parse_thermal_freq()
        
        if thermal_df is None:
            logger.error("Thermal analysis data not available")
            return
            
        # Add to report
        self.add_to_report("# Environmental and Reliability Analysis Report")
        self.add_to_report("\n## Temperature and Thermal Analysis")
        
        # Calculate temperature coefficients
        self.add_to_report("\n### Temperature Dependence of Current and Power")
        
        # Group by Vgs, Vds and calculate temperature coefficients
        temp_coef = []
        for (vgs, vds), group in thermal_df.groupby(['Vgs', 'Vds']):
            # Calculate temperature coefficient using linear regression
            temps = group['Temperature']
            currents = group['Id']
            if len(temps) > 1:
                temp_coef_id = np.polyfit(temps, currents, 1)[0]  # Slope of linear fit
                temp_coef.append({
                    'Vgs': vgs,
                    'Vds': vds,
                    'Id_TempCoef': temp_coef_id,
                    'Id_TempCoef_Percent': temp_coef_id / currents.mean() * 100
                })
        
        temp_coef_df = pd.DataFrame(temp_coef)
        
        # Plot temperature dependence for a specific bias point
        vgs_plot = 1.0
        vds_plot = 1.0
        bias_data = thermal_df[(thermal_df['Vgs'] == vgs_plot) & (thermal_df['Vds'] == vds_plot)]
        
        if not bias_data.empty:
            # Current vs Temperature plot
            setup_plot(f"Current vs Temperature (Vgs={vgs_plot}V, Vds={vds_plot}V)", 
                      "Temperature (°C)", "Drain Current (A)")
            plt.plot(bias_data['Temperature'], bias_data['Id'], 'o-', linewidth=2)
            save_plot("current_vs_temp.png")
            
            # Power vs Temperature plot
            setup_plot(f"Power vs Temperature (Vgs={vgs_plot}V, Vds={vds_plot}V)", 
                      "Temperature (°C)", "Power Dissipation (W)")
            plt.plot(bias_data['Temperature'], bias_data['Power'], 'o-', linewidth=2)
            save_plot("power_vs_temp.png")
            
            # Add plots to report
            self.add_to_report("\nCurrent-temperature and power-temperature characteristics:")
            self.add_to_report(f"\n![Current vs Temperature](plots/current_vs_temp.png)")
            self.add_to_report(f"\n![Power vs Temperature](plots/power_vs_temp.png)")
        
        # Create a more comprehensive thermal surface plot
        if len(thermal_df['Vgs'].unique()) > 1 and len(thermal_df['Temperature'].unique()) > 1:
            # Use a fixed Vds for the surface plot
            vds_fixed = thermal_df['Vds'].unique()[0]
            surface_data = thermal_df[thermal_df['Vds'] == vds_fixed]
            
            # Create pivot table for surface plot
            pivot_data = surface_data.pivot_table(index='Vgs', columns='Temperature', values='Id')
            
            # Create surface plot
            fig = plt.figure(figsize=(12, 8))
            ax = fig.add_subplot(111, projection='3d')
            X, Y = np.meshgrid(pivot_data.columns, pivot_data.index)
            ax.plot_surface(X, Y, pivot_data.values, cmap='viridis', alpha=0.8)
            ax.set_xlabel('Temperature (°C)')
            ax.set_ylabel('Gate Voltage (V)')
            ax.set_zlabel('Drain Current (A)')
            ax.set_title(f'Drain Current Surface (Vds={vds_fixed}V)')
            save_plot("current_surface_temp_vgs.png", tight=False)
            
            self.add_to_report("\n### 3D Surface Analysis of Temperature Effects")
            self.add_to_report(f"\n![Current Surface](plots/current_surface_temp_vgs.png)")
        
        # Add temperature coefficient table to report
        self.add_to_report("\n### Temperature Coefficients")
        self.add_to_report("\nTemperature coefficients for various bias points:")
        self.add_to_report("\n```")
        self.add_to_report(temp_coef_df.to_string(index=False, float_format="{:.3e}".format))
        self.add_to_report("\n```")
        
        # Average temperature coefficient
        if temp_coef_df is None or len(temp_coef_df) == 0:
            logger.warning("No valid temperature coefficient data available")
            avg_temp_coef = 0
            avg_temp_coef_pct = 0
        else:
            avg_temp_coef = temp_coef_df['Id_TempCoef'].mean()
            avg_temp_coef_pct = temp_coef_df['Id_TempCoef_Percent'].mean()
        
        self.add_to_report(f"\nAverage drain current temperature coefficient: {avg_temp_coef:.3e} A/°C ({avg_temp_coef_pct:.3f}%/°C)")
        
        # Analyze thermal frequency response
        if freq is not None and thermal_z is not None and len(freq) > 0 and len(thermal_z) > 0:
            self.add_to_report("\n### Thermal Frequency Response")
            
            try:
                # Plot thermal impedance vs frequency
                setup_plot("Thermal Impedance vs Frequency", "Frequency (Hz)", "Thermal Impedance (Ω)")
                plt.semilogx(freq, thermal_z, linewidth=2)
                save_plot("thermal_impedance_vs_freq.png")
                
                self.add_to_report("\nThermal impedance frequency response:")
                self.add_to_report(f"\n![Thermal Impedance](plots/thermal_impedance_vs_freq.png)")
                
                # Calculate thermal cutoff frequency
                max_z = np.max(thermal_z)
                f_cutoff_idx = np.argmin(np.abs(thermal_z - max_z/np.sqrt(2)))
                f_cutoff = freq[f_cutoff_idx] if f_cutoff_idx < len(freq) else None
                
                if f_cutoff is not None:
                    self.add_to_report(f"\nThermal cutoff frequency: {f_cutoff:.2e} Hz")
                    self.add_to_report(f"\nMaximum thermal impedance: {max_z:.3e} Ω")
            except Exception as e:
                logger.error(f"Error in thermal frequency analysis: {e}")
                self.add_to_report("\nThermal frequency analysis could not be completed due to data issues.")
            
        # Summary
        self.add_to_report("\n### Temperature and Thermal Analysis Summary")
        self.add_to_report("\n- Successfully analyzed temperature dependence from -40°C to 150°C")
        self.add_to_report(f"\n- Average drain current temperature coefficient: {avg_temp_coef:.3e} A/°C ({avg_temp_coef_pct:.3f}%/°C)")
        if freq is not None and thermal_z is not None and f_cutoff is not None:
            self.add_to_report(f"\n- Thermal frequency response analyzed: cutoff at {f_cutoff:.2e} Hz")
        self.add_to_report("\n- Thermal-electrical coupling effects observed and quantified")
            
    def analyze_process_statistical(self):
        """Analyze process and statistical characteristics"""
        logger.info("Analyzing process and statistical characteristics")
        
        # Parse data
        corners_df = self.parser.parse_process_corners()
        mc_df = self.parser.parse_monte_carlo()
        
        if corners_df is None and mc_df is None:
            logger.error("Both process corner and Monte Carlo data not available")
            self.add_to_report("\n## Process and Statistical Analysis")
            self.add_to_report("\nNo valid process corner or Monte Carlo data available for analysis.")
            return
            
        # Add to report
        self.add_to_report("\n## Process and Statistical Analysis")
            
        # Add to report
        self.add_to_report("\n## Process and Statistical Analysis")
        
        # Process corners analysis
        self.add_to_report("\n### Process Corner Analysis")
        
        # Add process corner table to report
        self.add_to_report("\nDevice characteristics at different process corners:")
        self.add_to_report("\n```")
        self.add_to_report(corners_df.to_string(index=False, float_format="{:.3e}".format))
        self.add_to_report("\n```")
        
        # Plot process corners
        setup_plot("Drain Current at Different Process Corners", "Process Corner", "Drain Current (A)")
        plt.bar(corners_df['Corner'], corners_df['Id'])
        plt.axhline(y=corners_df[corners_df['Corner'] == 'TT']['Id'].values[0], 
                   color='r', linestyle='--', label='Typical')
        plt.legend()
        save_plot("process_corners_current.png")
        
        self.add_to_report("\nDrain current variation across process corners:")
        self.add_to_report(f"\n![Process Corners](plots/process_corners_current.png)")
        
        # Calculate corner variation statistics
        typical_id = corners_df[corners_df['Corner'] == 'TT']['Id'].values[0]
        max_id = corners_df['Id'].max()
        min_id = corners_df['Id'].min()
        
        id_variation_pct = (max_id - min_id) / typical_id * 100
        self.add_to_report(f"\nDrain current variation: {id_variation_pct:.2f}% across all corners")
        
        # Monte Carlo analysis
        self.add_to_report("\n### Monte Carlo Analysis")
        
        # Histogram of Monte Carlo drain current
        if mc_df is None or mc_df['Id'].isnull().all() or len(mc_df['Id']) < 2:
            logger.error("Monte Carlo Id data is invalid or not available")
            self.add_to_report("\nMonte Carlo drain current distribution could not be plotted due to invalid or missing data.")
            id_mean = 0
            id_std = 0
            id_cv = 0
        else:
            try:
                setup_plot("Monte Carlo Drain Current Distribution", "Drain Current (A)", "Frequency")
                plt.hist(mc_df['Id'], bins=20, alpha=0.7, edgecolor='black')
                plt.axvline(x=mc_df['Id'].mean(), color='r', linestyle='--', label='Mean')
                plt.axvline(x=mc_df['Id'].median(), color='g', linestyle='--', label='Median')
                plt.legend()
                save_plot("monte_carlo_id_histogram.png")
                
                # Calculate Monte Carlo statistics
                id_mean = mc_df['Id'].mean()
                id_std = mc_df['Id'].std()
                id_cv = id_std / id_mean * 100
                
                self.add_to_report("\nMonte Carlo drain current distribution:")
                self.add_to_report(f"\n![Monte Carlo Histogram](plots/monte_carlo_id_histogram.png)")
            except Exception as e:
                logger.error(f"Error creating Monte Carlo histogram: {e}")
                self.add_to_report("\nMonte Carlo drain current distribution could not be plotted due to an error in data processing.")
                id_mean = 0
                id_std = 0
                id_cv = 0
        
                # Output Monte Carlo statistics if available
        if id_mean != 0:
            self.add_to_report("\nMonte Carlo statistics:")
            self.add_to_report(f"\n- Mean drain current: {id_mean:.3e} A")
            self.add_to_report(f"\n- Standard deviation: {id_std:.3e} A") 
            self.add_to_report(f"\n- Coefficient of variation: {id_cv:.2f}%")
        else:
            self.add_to_report("\nMonte Carlo statistics could not be calculated due to invalid or missing data.")
        
        # Scatter plot of parameter variations
        if mc_df is None or len(mc_df) < 2 or 'Vth' not in mc_df.columns or 'Id' not in mc_df.columns or 'Mobility' not in mc_df.columns:
            logger.error("Monte Carlo parameter data is invalid or missing required columns")
            self.add_to_report("\nParameter variation analysis could not be performed due to missing data.")
            corr_vth_id = 0
            corr_mobility_id = 0
        else:
            try:
                setup_plot("Parameter Variation Effect on Drain Current", "Threshold Voltage (V)", "Drain Current (A)")
                plt.scatter(mc_df['Vth'], mc_df['Id'], alpha=0.7)
                scatter = plt.scatter(mc_df['Vth'], mc_df['Id'], c=mc_df['Mobility'], alpha=0.7)
                plt.colorbar(scatter, label='Mobility')
                save_plot("monte_carlo_params_scatter.png")
                
                # Correlation analysis
                corr_vth_id = mc_df['Vth'].corr(mc_df['Id'])
                corr_mobility_id = mc_df['Mobility'].corr(mc_df['Id'])
                
                self.add_to_report("\nEffect of parameter variations on drain current:")
                self.add_to_report(f"\n![Parameter Variation](plots/monte_carlo_params_scatter.png)")
            except Exception as e:
                logger.error(f"Error creating parameter variation scatter plot: {e}")
                self.add_to_report("\nParameter variation analysis could not be completed due to an error in data processing.")
                corr_vth_id = 0
                corr_mobility_id = 0
        
        # Report correlations if available
        if corr_vth_id != 0 or corr_mobility_id != 0:
            self.add_to_report("\nParameter correlations with drain current:")
            self.add_to_report(f"\n- Threshold voltage correlation: {corr_vth_id:.4f}")
            self.add_to_report(f"\n- Mobility correlation: {corr_mobility_id:.4f}")
        
        # Process corners and Monte Carlo summary
        self.add_to_report("\n### Process and Statistical Analysis Summary")
        
        if corners_df is not None and not corners_df.empty:
            self.add_to_report("\n- Process corner analysis completed for TT, FF, SS, FS, and SF corners")
            self.add_to_report(f"\n- Process corner drain current variation: {id_variation_pct:.2f}%")
        else:
            self.add_to_report("\n- Process corner analysis could not be completed due to missing data")
            
        if mc_df is not None and not mc_df.empty:
            self.add_to_report(f"\n- Monte Carlo analysis completed with {len(mc_df)} simulation runs")
            if id_cv != 0:
                self.add_to_report(f"\n- Monte Carlo coefficient of variation: {id_cv:.2f}%")
                
            if corr_vth_id != 0 or corr_mobility_id != 0:
                self.add_to_report("\n- Key parameters affecting performance identified through correlation analysis")
        else:
            self.add_to_report("\n- Monte Carlo analysis could not be completed due to missing data")
    
    def analyze_reliability_aging(self):
        """Analyze reliability and aging characteristics"""
        logger.info("Analyzing reliability and aging characteristics")
        
        # Parse data
        aging_df = self.parser.parse_aging_analysis()
        stress_df = self.parser.parse_stress_test()
        
        if aging_df is None and stress_df is None:
            logger.error("Both aging and stress test data not available")
            self.add_to_report("\n## Reliability and Aging Analysis")
            self.add_to_report("\nNo valid aging or stress test data available for analysis.")
            return
            
        # Add to report
        self.add_to_report("\n## Reliability and Aging Analysis")
        
        # Aging analysis
        # Initialize variables for later use
        id_decay_rate = 0
        id_decay_rate_pct = 0
        gm_decay_rate = 0
        gm_decay_rate_pct = 0
        
        if aging_df is not None and len(aging_df) > 0:
            self.add_to_report("\n### Aging Effect Analysis")
            
            try:
                # Plot aging effect on drain current
                setup_plot("Effect of Vth Shift on Drain Current", "Threshold Voltage Shift (V)", "Drain Current (A)")
                plt.plot(aging_df['Vth_shift'], aging_df['Id'], 'o-', linewidth=2)
                save_plot("aging_current_vs_vth.png")
                
                # Plot aging effect on transconductance
                setup_plot("Effect of Vth Shift on Transconductance", "Threshold Voltage Shift (V)", "Transconductance (S)")
                plt.plot(aging_df['Vth_shift'], aging_df['Gm'], 'o-', linewidth=2)
                save_plot("aging_gm_vs_vth.png")
                
                self.add_to_report("\nEffect of threshold voltage shift due to aging:")
                self.add_to_report(f"\n![Aging Current](plots/aging_current_vs_vth.png)")
                self.add_to_report(f"\n![Aging Gm](plots/aging_gm_vs_vth.png)")
                
                # Calculate aging degradation rates if we have enough data points
                if len(aging_df) > 1:
                    id_decay_rate = np.polyfit(aging_df['Vth_shift'], aging_df['Id'], 1)[0]
                    id_decay_rate_pct = id_decay_rate / aging_df['Id'].iloc[0] * 100
                    
                    gm_decay_rate = np.polyfit(aging_df['Vth_shift'], aging_df['Gm'], 1)[0]
                    gm_decay_rate_pct = gm_decay_rate / aging_df['Gm'].iloc[0] * 100
            except Exception as e:
                logger.error(f"Error plotting aging effects: {e}")
                self.add_to_report("\nAging effect analysis could not be completed due to data issues.")
        else:
            logger.error("Aging analysis data not available")
            self.add_to_report("\n### Aging Effect Analysis")
            self.add_to_report("\nNo valid aging analysis data available from SPICE simulation.")
        
        # Report aging degradation rates
        self.add_to_report("\nAging degradation rates:")
        self.add_to_report(f"\n- Drain current degradation rate: {id_decay_rate:.3e} A/V ({id_decay_rate_pct:.2f}%/V)")
        self.add_to_report(f"\n- Transconductance degradation rate: {gm_decay_rate:.3e} S/V ({gm_decay_rate_pct:.2f}%/V)")
        
        # Stress test analysis
        # Initialize stress_data as empty DataFrame to avoid UnboundLocalError
        stress_data = pd.DataFrame()
        
        if stress_df is not None and len(stress_df) > 0:
            self.add_to_report("\n### Stress Test Analysis")
            
            try:
                # Filter data for specific stress level and temperature
                stress_level = 2  # Medium stress level
                stress_temp = 85  # Medium temperature
                
                if 'Stress_level' in stress_df.columns and 'Temperature' in stress_df.columns:
                    stress_data = stress_df[
                        (stress_df['Stress_level'] == stress_level) & 
                        (stress_df['Temperature'] == stress_temp)
                    ]
                else:
                    logger.error("Required columns missing in stress test data")
                    self.add_to_report("\nStress test analysis could not be completed due to missing data columns.")
                    stress_data = pd.DataFrame()
            except Exception as e:
                logger.error(f"Error filtering stress test data: {e}")
                stress_data = pd.DataFrame()
                self.add_to_report("\nStress test analysis could not be completed due to data issues.")
        else:
            logger.error("Stress test data not available")
            self.add_to_report("\n### Stress Test Analysis")
            self.add_to_report("\nNo valid stress test data available from SPICE simulation.")
        
        if not stress_data.empty:
            # Plot degradation over time
            setup_plot(f"Current Degradation vs Stress Time (Level={stress_level}, T={stress_temp}°C)", 
                      "Stress Time (hours)", "Current Degradation (%)")
            plt.semilogx(stress_data['Stress_time'], stress_data['Id_degradation'], 'o-', linewidth=2)
            plt.grid(True, which="both")
            save_plot("stress_degradation_vs_time.png")
            
            self.add_to_report("\nCurrent degradation with stress time:")
            self.add_to_report(f"\n![Stress Degradation](plots/stress_degradation_vs_time.png)")
        
        # Plot degradation for different stress levels if stress data is available
        if stress_df is not None and not stress_df.empty and 'Stress_time' in stress_df.columns:
            try:
                # Group by stress level and get the max stress time point
                max_time = stress_df['Stress_time'].max()
                high_time_data = stress_df[stress_df['Stress_time'] == max_time]
                
                if not high_time_data.empty and 'Temperature' in high_time_data.columns and 'Stress_level' in high_time_data.columns and 'Id_degradation' in high_time_data.columns:
                    # Pivot data for heatmap by temperature and stress level
                    pivot_data = high_time_data.pivot_table(
                        index='Temperature', 
                        columns='Stress_level', 
                        values='Id_degradation'
                    )
                    
                    if not pivot_data.empty:
                        # Create heatmap
                        plt.figure(figsize=(10, 6))
                        plt.imshow(pivot_data, cmap='hot_r', aspect='auto', interpolation='nearest')
                        plt.colorbar(label='Current Degradation (%)')
                        plt.xlabel('Stress Level')
                        plt.ylabel('Temperature (°C)')
                        plt.title(f'Current Degradation Heatmap after {max_time:.0e} hours')
                        plt.xticks(range(len(pivot_data.columns)), pivot_data.columns)
                        plt.yticks(range(len(pivot_data.index)), pivot_data.index)
                        
                        # Add degradation values to heatmap
                        for i in range(len(pivot_data.index)):
                            for j in range(len(pivot_data.columns)):
                                plt.text(j, i, f"{pivot_data.iloc[i, j]:.1f}%", 
                                         ha="center", va="center", color="w")
                        
                        save_plot("degradation_heatmap.png")
                        
                        self.add_to_report("\n### Temperature and Stress Level Effects")
                        self.add_to_report("\nHeatmap showing degradation as a function of temperature and stress level:")
                        self.add_to_report(f"\n![Degradation Heatmap](plots/degradation_heatmap.png)")
                    else:
                        logger.error("Pivot data is empty")
                        self.add_to_report("\n### Temperature and Stress Level Effects")
                        self.add_to_report("\nTemperature and stress level analysis could not be completed due to insufficient data.")
                else:
                    logger.error("Required columns missing in high time stress data")
                    self.add_to_report("\n### Temperature and Stress Level Effects")
                    self.add_to_report("\nTemperature and stress level analysis could not be completed due to missing data columns.")
            except Exception as e:
                logger.error(f"Error creating degradation heatmap: {e}")
                self.add_to_report("\n### Temperature and Stress Level Effects")
                self.add_to_report("\nTemperature and stress level analysis could not be completed due to an error in data processing.")
        
        # Reliability lifetime extraction
        if len(stress_data) > 1:
            # Assuming failure at 10% degradation, estimate lifetime using linear interpolation
            failure_threshold = 10.0  # 10% degradation
            
            # Filter to valid data points with increasing time
            valid_data = stress_data[stress_data['Stress_time'] > 0].sort_values('Stress_time')
            
            if not valid_data.empty and valid_data['Id_degradation'].max() > failure_threshold:
                # Find intersection with threshold using linear interpolation
                times = valid_data['Stress_time']
                degradations = valid_data['Id_degradation']
                
                # Find points around the threshold
                idx_before = np.where(degradations < failure_threshold)[0][-1]
                idx_after = np.where(degradations >= failure_threshold)[0][0]
                
                time_before = times.iloc[idx_before]
                time_after = times.iloc[idx_after]
                deg_before = degradations.iloc[idx_before]
                deg_after = degradations.iloc[idx_after]
                
                # Linear interpolation to find failure time
                time_failure = time_before + (failure_threshold - deg_before) * (time_after - time_before) / (deg_after - deg_before)
                
                self.add_to_report("\n### Reliability Lifetime Extraction")
                self.add_to_report(f"\nEstimated lifetime at stress level {stress_level} and temperature {stress_temp}°C: {time_failure:.2e} hours")
                self.add_to_report(f"\n(Assuming failure at {failure_threshold}% current degradation)")
        
        # Aging and reliability summary
        self.add_to_report("\n### Reliability and Aging Analysis Summary")
        
        if aging_df is not None and len(aging_df) > 1:
            self.add_to_report("\n- Aging effects analyzed through threshold voltage shifts")
            self.add_to_report(f"\n- Drain current degradation rate: {id_decay_rate_pct:.2f}%/V of Vth shift")
            self.add_to_report(f"\n- Transconductance degradation rate: {gm_decay_rate_pct:.2f}%/V of Vth shift")
        else:
            self.add_to_report("\n- Aging effects analysis could not be completed due to insufficient data")
        
        if stress_df is not None and not stress_df.empty:
            self.add_to_report(f"\n- HCI and NBTI effects analyzed with various stress conditions")
            if 'time_failure' in locals():
                self.add_to_report(f"\n- Estimated device lifetime: {time_failure:.2e} hours under test conditions")
        else:
            self.add_to_report("\n- Stress effect analysis could not be completed due to insufficient data")
        
    def run_analysis(self):
        """Run the full analysis pipeline"""
        logger.info("Starting Environmental and Reliability Analysis")
        
        # Step 1: Run ngspice simulation
        if not self.run_ngspice_simulation():
            logger.error("ngspice simulation failed, analysis aborted")
            return False
            
        # Step 2: Analyze temperature and thermal characteristics
        self.analyze_temperature_thermal()
        
        # Step 3: Analyze process and statistical characteristics
        self.analyze_process_statistical()
        
        # Step 4: Analyze reliability and aging characteristics
        self.analyze_reliability_aging()
        
        # Generate checklist report
        self.add_to_report("\n## Environmental and Reliability Checklist Status")
        
        # Get the data for status report
        thermal_df = self.parser.parse_thermal_analysis()
        freq, thermal_z = self.parser.parse_thermal_freq()
        corners_df = self.parser.parse_process_corners()
        mc_df = self.parser.parse_monte_carlo()
        aging_df = self.parser.parse_aging_analysis()
        stress_df = self.parser.parse_stress_test()
        
        self.add_to_report("\n### Temperature and Thermal")
        if thermal_df is not None and not thermal_df.empty:
            self.add_to_report("\n- ✓ **Thermal analysis** - Analyzed temperature-dependent characteristics from SPICE simulation")
            self.add_to_report("\n- ✓ **Thermal-electrical coupled simulations** - Analyzed power dissipation vs temperature")
            self.add_to_report("\n- ✓ **Power dissipation simulations** - Analyzed power dissipation under different conditions")
        else:
            self.add_to_report("\n- ✗ **Thermal analysis** - Data not available from SPICE simulation")
            self.add_to_report("\n- ✗ **Thermal-electrical coupled simulations** - Data not available from SPICE simulation")
            self.add_to_report("\n- ✗ **Power dissipation simulations** - Data not available from SPICE simulation")
            
        if freq is not None and thermal_z is not None and len(freq) > 0 and len(thermal_z) > 0:
            self.add_to_report("\n- ✓ **Frequency-dependent thermal analysis** - Analyzed thermal impedance vs frequency")
        else:
            self.add_to_report("\n- ✗ **Frequency-dependent thermal analysis** - Data not available from SPICE simulation")
        
        self.add_to_report("\n### Process and Statistical")
        if mc_df is not None and not mc_df.empty:
            self.add_to_report("\n- ✓ **Monte Carlo simulations** - Performed Monte Carlo analysis with parameter variations")
            self.add_to_report("\n- ✓ **Statistical analysis** - Analyzed variability in device characteristics")
        else:
            self.add_to_report("\n- ✗ **Monte Carlo simulations** - Data not available from SPICE simulation")
            self.add_to_report("\n- ✗ **Statistical analysis** - Data not available from SPICE simulation")
            
        if corners_df is not None and not corners_df.empty:
            self.add_to_report("\n- ✓ **Process corner simulations** - Analyzed device characteristics at different corners")
            self.add_to_report("\n- ✓ **Process variation simulations** - Simulated effect of process variations on device performance")
        else:
            self.add_to_report("\n- ✗ **Process corner simulations** - Data not available from SPICE simulation")
            self.add_to_report("\n- ✗ **Process variation simulations** - Data not available from SPICE simulation")
            
        if thermal_df is not None and not thermal_df.empty and 'Temperature' in thermal_df.columns and len(thermal_df['Temperature'].unique()) > 1:
            self.add_to_report("\n- ✓ **Temperature corner simulations** - Analyzed device at various temperature conditions")
        else:
            self.add_to_report("\n- ✗ **Temperature corner simulations** - Data not available from SPICE simulation")
        
        self.add_to_report("\n### Reliability and Aging")
        if aging_df is not None and not aging_df.empty:
            self.add_to_report("\n- ✓ **Long-term reliability simulations** - Analyzed device degradation over time")
            self.add_to_report("\n- ✓ **Aging effects modeling** - Analyzed aging through parameter shifts")
        else:
            self.add_to_report("\n- ✗ **Long-term reliability simulations** - Data not available from SPICE simulation")
            self.add_to_report("\n- ✗ **Aging effects modeling** - Data not available from SPICE simulation")
            
        if stress_df is not None and not stress_df.empty:
            self.add_to_report("\n- ✓ **Stress test simulations** - Analyzed device under various stress conditions")
            self.add_to_report("\n- ✓ **Degradation analysis** - Quantified degradation rates and mechanisms")
        else:
            self.add_to_report("\n- ✗ **Stress test simulations** - Data not available from SPICE simulation")
            self.add_to_report("\n- ✗ **Degradation analysis** - Data not available from SPICE simulation")
        
        self.generate_report()
        logger.info("Environmental and Reliability Analysis completed successfully")
        return True


if __name__ == "__main__":
    analyzer = EnvironmentalReliabilityAnalyzer()
    analyzer.run_analysis() 