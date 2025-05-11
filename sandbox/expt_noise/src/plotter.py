import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter

class NoisePlotter:
    """
    Plotter class for generating noise analysis plots
    """
    def __init__(self, logger, output_dir="plots"):
        """
        Initialize the plotter
        
        Args:
            logger: Logger instance for logging messages
            output_dir: Directory to save plots (default: plots)
        """
        self.logger = logger
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        self.logger.info(f"NoisePlotter initialized. Output directory: {output_dir}")
        
    def plot_noise_spectrum(self, freq, noise, title, filename, 
                           log_x=True, log_y=True, additional_data=None):
        """
        Plot noise spectrum
        
        Args:
            freq: Frequency data array
            noise: Noise data array
            title: Plot title
            filename: Output filename (without extension)
            log_x: Use logarithmic X axis (default: True)
            log_y: Use logarithmic Y axis (default: True)
            additional_data: Dictionary of additional data series to plot {label: values}
        """
        try:
            plt.figure(figsize=(10, 6))
            
            # Plot main noise data
            plt.plot(freq, noise, 'b-', linewidth=2, label='Noise Spectrum')
            
            # Plot additional data if provided
            if additional_data:
                colors = ['r-', 'g-', 'm-', 'c-', 'y-']
                for i, (label, data) in enumerate(additional_data.items()):
                    plt.plot(freq, data, colors[i % len(colors)], linewidth=1.5, label=label)
            
            # Set axis scales
            if log_x:
                plt.xscale('log')
            if log_y:
                plt.yscale('log')
                
            # Set labels and title
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Noise Spectral Density (V²/Hz)')
            plt.title(title)
            plt.grid(True, which='both', linestyle='--', alpha=0.6)
            plt.legend()
            
            # Format axes
            ax = plt.gca()
            ax.xaxis.set_major_formatter(ScalarFormatter())
            
            # Save figure
            output_path = os.path.join(self.output_dir, f"{filename}.png")
            plt.tight_layout()
            plt.savefig(output_path, dpi=300)
            plt.close()
            
            self.logger.info(f"Noise spectrum plot saved to {output_path}")
            return output_path
        except Exception as e:
            self.logger.error(f"Error creating noise spectrum plot: {str(e)}")
            return None
            
    def plot_noise_vs_parameter(self, parameter, noise, parameter_name, title, filename):
        """
        Plot noise level against a parameter (temperature, width, length, etc.)
        
        Args:
            parameter: Parameter values array
            noise: Noise values array
            parameter_name: Name of the parameter (for X axis label)
            title: Plot title
            filename: Output filename (without extension)
        """
        try:
            plt.figure(figsize=(10, 6))
            
            # Plot noise vs parameter
            plt.plot(parameter, noise, 'bo-', linewidth=2, markersize=6)
            
            # Set labels and title
            plt.xlabel(parameter_name)
            plt.ylabel('Noise Level (V²/Hz)')
            plt.title(title)
            plt.grid(True, linestyle='--', alpha=0.6)
            
            # Save figure
            output_path = os.path.join(self.output_dir, f"{filename}.png")
            plt.tight_layout()
            plt.savefig(output_path, dpi=300)
            plt.close()
            
            self.logger.info(f"Parameter analysis plot saved to {output_path}")
            return output_path
        except Exception as e:
            self.logger.error(f"Error creating parameter analysis plot: {str(e)}")
            return None
            
    def plot_multiple_noise_spectra(self, data_dict, title, filename, 
                                   log_x=True, log_y=True):
        """
        Plot multiple noise spectra on the same graph
        
        Args:
            data_dict: Dictionary of {label: (freq, noise)} pairs
            title: Plot title
            filename: Output filename (without extension)
            log_x: Use logarithmic X axis (default: True)
            log_y: Use logarithmic Y axis (default: True)
        """
        try:
            plt.figure(figsize=(10, 6))
            
            # Plot each noise spectrum
            colors = ['b', 'r', 'g', 'm', 'c', 'y', 'k', 'orange', 'purple', 'brown']
            for i, (label, (freq, noise)) in enumerate(data_dict.items()):
                color = colors[i % len(colors)]
                plt.plot(freq, noise, f'{color}-', linewidth=1.5, label=label)
                
            # Set axis scales
            if log_x:
                plt.xscale('log')
            if log_y:
                plt.yscale('log')
                
            # Set labels and title
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Noise Spectral Density (V²/Hz)')
            plt.title(title)
            plt.grid(True, which='both', linestyle='--', alpha=0.6)
            plt.legend()
            
            # Format axes
            ax = plt.gca()
            ax.xaxis.set_major_formatter(ScalarFormatter())
            
            # Save figure
            output_path = os.path.join(self.output_dir, f"{filename}.png")
            plt.tight_layout()
            plt.savefig(output_path, dpi=300)
            plt.close()
            
            self.logger.info(f"Multiple noise spectra plot saved to {output_path}")
            return output_path
        except Exception as e:
            self.logger.error(f"Error creating multiple noise spectra plot: {str(e)}")
            return None
            
    def plot_noise_contrib_components(self, freq, thermal, flicker, total, title, filename):
        """
        Plot noise contribution components (thermal, flicker, total)
        
        Args:
            freq: Frequency data array
            thermal: Thermal noise component data
            flicker: Flicker noise component data
            total: Total noise data
            title: Plot title
            filename: Output filename (without extension)
        """
        try:
            plt.figure(figsize=(10, 6))
            
            # Plot each component
            plt.loglog(freq, total, 'k-', linewidth=2, label='Total Noise')
            plt.loglog(freq, thermal, 'r-', linewidth=1.5, label='Thermal Noise')
            plt.loglog(freq, flicker, 'b-', linewidth=1.5, label='Flicker (1/f) Noise')
            
            # Set labels and title
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Noise Spectral Density (V²/Hz)')
            plt.title(title)
            plt.grid(True, which='both', linestyle='--', alpha=0.6)
            plt.legend()
            
            # Format axes
            ax = plt.gca()
            ax.xaxis.set_major_formatter(ScalarFormatter())
            
            # Save figure
            output_path = os.path.join(self.output_dir, f"{filename}.png")
            plt.tight_layout()
            plt.savefig(output_path, dpi=300)
            plt.close()
            
            self.logger.info(f"Noise components plot saved to {output_path}")
            return output_path
        except Exception as e:
            self.logger.error(f"Error creating noise components plot: {str(e)}")
            return None 