import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os

class PlotGenerator:
    """Handles generation of plots from simulation data."""
    def __init__(self, output_dir, dpi=300, logger=None):
        self.output_dir = output_dir
        self.dpi = dpi
        self.logger = logger
        self.colors = plt.cm.viridis(np.linspace(0, 1, 6))  # 6 colors for different temperatures
        
    def plot_iv_characteristics(self, vds, vgs, ids, output_dir, colors=None):
        """Plot IV characteristics with subthreshold and saturation regions."""
        try:
            plt.figure(figsize=(10, 8))
            
            # Debug logging
            print(f"Vgs range: {np.min(vgs):.3f}V to {np.max(vgs):.3f}V")
            print(f"Ids range: {np.min(ids):.3e}A to {np.max(ids):.3e}A")
            
            # Select subset of Vgs values for clearer plot
            unique_vgs = np.unique(vgs)
            if len(unique_vgs) > 10:
                # Keep first, last, and evenly spaced middle values
                indices = np.linspace(0, len(unique_vgs)-1, 10, dtype=int)
                selected_vgs = unique_vgs[indices]
            else:
                selected_vgs = unique_vgs
                
            print(f"Selected Vgs values: {selected_vgs}")
            
            # Plot IV curves for selected Vgs values
            for vg in selected_vgs:
                mask = np.isclose(vgs, vg)
                if np.any(mask):
                    vds_curve = vds[mask]
                    ids_curve = ids[mask]
                    print(f"Vgs={vg:.3f}V: Ids range {np.min(ids_curve):.3e}A to {np.max(ids_curve):.3e}A")
                    plt.plot(vds_curve, ids_curve, label=f'Vgs={vg:.1f}V')
            
            plt.xlabel('Drain-Source Voltage (V)')
            plt.ylabel('Drain Current (A)')
            plt.title('MOSFET IV Characteristics')
            plt.grid(True)
            plt.legend()
            
            # Add subthreshold and saturation region markers
            plt.axvline(x=0.1, color='gray', linestyle='--', alpha=0.5)
            plt.axvline(x=0.5, color='gray', linestyle='--', alpha=0.5)
            plt.text(0.15, plt.ylim()[1]*0.9, 'Subthreshold', rotation=90)
            plt.text(0.55, plt.ylim()[1]*0.9, 'Saturation', rotation=90)
            
            # Add log scale inset for subthreshold region
            ax_inset = plt.axes([0.2, 0.2, 0.3, 0.3])
            for vg in selected_vgs:
                mask = np.isclose(vgs, vg)
                if np.any(mask):
                    vds_curve = vds[mask]
                    ids_curve = ids[mask]
                    ax_inset.semilogy(vds_curve, np.abs(ids_curve), label=f'Vgs={vg:.1f}V')
            
            ax_inset.set_xlabel('Vds (V)')
            ax_inset.set_ylabel('|Ids| (A)')
            ax_inset.set_title('Subthreshold Region')
            ax_inset.grid(True)
            
            # Use self.output_dir instead of the passed output_dir
            output_file = Path(self.output_dir) / 'iv_characteristics.png'
            plt.savefig(output_file, dpi=self.dpi, bbox_inches='tight')
            plt.close()
            
            if self.logger:
                self.logger.logger.info(f"IV characteristics plot saved to {output_file}")
                
            return output_file
            
        except Exception as e:
            self.logger.logger.error(f"Error plotting IV characteristics: {e}")
            raise

    def plot_cv_characteristics(self, vg, ig, freq=None):
        """Plot CV characteristics with frequency response."""
        if vg is None or ig is None:
            return None
            
        try:
            plt.figure(figsize=(12, 8))
            
            # Plot CV curve
            plt.plot(vg, np.abs(ig), 'b-', label='|Ig|')
            
            # Add frequency response if available
            if freq is not None:
                ax2 = plt.gca().twinx()
                ax2.semilogx(freq, np.abs(ig), 'r--', label='Frequency Response')
                ax2.set_ylabel('|Ig| (A)')
                ax2.legend(loc='upper right')
            
            plt.xlabel('Vg (V)')
            plt.ylabel('|Ig| (A)')
            plt.title('CV Characteristics')
            plt.grid(True)
            plt.legend(loc='upper left')
            
            # Save plot
            output_file = Path(self.output_dir) / 'cv_characteristics.png'
            plt.savefig(output_file, dpi=self.dpi, bbox_inches='tight')
            plt.close()
            
            if self.logger:
                self.logger.logger.info(f"CV characteristics plot saved to {output_file}")
                
            return output_file
            
        except Exception as e:
            if self.logger:
                self.logger.logger.error(f"Error creating CV characteristics plot: {e}")
            return None

    def plot_temperature_analysis(self, temp, ids):
        """Plot temperature analysis with current variation."""
        if temp is None or ids is None:
            return None
            
        try:
            plt.figure(figsize=(12, 8))
            
            # Plot temperature dependence
            plt.plot(temp, ids, 'bo-', label='Ids')
            
            # Add trend line
            z = np.polyfit(temp, ids, 1)
            p = np.poly1d(z)
            plt.plot(temp, p(temp), 'r--', label=f'Trend (slope: {z[0]:.2e}A/°C)')
            
            plt.xlabel('Temperature (°C)')
            plt.ylabel('Ids (A)')
            plt.title('Temperature Analysis')
            plt.grid(True)
            plt.legend()
            
            # Save plot
            output_file = Path(self.output_dir) / 'temperature_analysis.png'
            plt.savefig(output_file, dpi=self.dpi, bbox_inches='tight')
            plt.close()
            
            if self.logger:
                self.logger.logger.info(f"Temperature analysis plot saved to {output_file}")
                
            return output_file
            
        except Exception as e:
            if self.logger:
                self.logger.logger.error(f"Error creating temperature analysis plot: {e}")
            return None

    def plot_kcl_verification(self, ids, ig, is_, ib):
        """Plot KCL verification showing current balance."""
        if any(x is None for x in [ids, ig, is_, ib]):
            return None
            
        try:
            plt.figure(figsize=(12, 8))
            
            # Calculate total current
            total = ids + ig + is_ + ib
            
            # Plot individual currents
            plt.plot(ids, 'b-', label='Ids')
            plt.plot(ig, 'g-', label='Ig')
            plt.plot(is_, 'r-', label='Is')
            plt.plot(ib, 'y-', label='Ib')
            plt.plot(total, 'k--', label='Total (KCL)')
            
            plt.xlabel('Measurement Point')
            plt.ylabel('Current (A)')
            plt.title('KCL Verification')
            plt.grid(True)
            plt.legend()
            
            # Save plot
            output_file = Path(self.output_dir) / 'kcl_verification.png'
            plt.savefig(output_file, dpi=self.dpi, bbox_inches='tight')
            plt.close()
            
            if self.logger:
                self.logger.logger.info(f"KCL verification plot saved to {output_file}")
                
            return output_file
            
        except Exception as e:
            if self.logger:
                self.logger.logger.error(f"Error creating KCL verification plot: {e}")
            return None 