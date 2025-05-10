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

    def plot_cv_characteristics(self, vg=None, ig=None, freq=None):
        """
        Generate comprehensive CV plots based on data in results/cv_full_data.txt.
        Creates both component analysis and frequency-dependent plots.
        """
        try:
            results = []
            # Make sure plots directory exists
            plots_dir = Path(self.output_dir) / 'plots'
            plots_dir.mkdir(exist_ok=True)
            
            # Check if file exists
            data_file = 'results/cv_full_data.txt'
            if not os.path.exists(data_file):
                if self.logger:
                    self.logger.logger.error(f"CV data file {data_file} not found")
                return None
                
            print(f"Loading CV data from {data_file}")
            
            # Read file and handle potential header lines
            with open(data_file, 'r') as f:
                lines = f.readlines()
                
            # Skip header lines
            data_lines = lines[1:] if len(lines) > 1 else []
            if len(data_lines) == 0:
                if self.logger:
                    self.logger.logger.error("No valid data found in CV data file")
                return None
                
            # Parse data
            data = []
            for line in data_lines:
                try:
                    parts = line.strip().split()
                    if len(parts) >= 5:  # At least Vg and capacitance values
                        row = []
                        for i in range(min(len(parts), 8)):  # Get up to 8 columns
                            row.append(float(parts[i]))
                        data.append(row)
                except Exception as e:
                    if self.logger:
                        self.logger.logger.warning(f"Error parsing line: {line.strip()}, {e}")
                    continue
                    
            if not data:
                if self.logger:
                    self.logger.logger.error("No valid data could be parsed from CV file")
                return None
                
            data = np.array(data)
            if self.logger:
                self.logger.logger.info(f"CV data shape: {data.shape}")
            
            # ---------- Plot 1: CV Components ----------
            # Extract data columns
            vg = data[:, 0]  # Gate voltage
            scale_factor = 1e15  # Convert to fF for better visibility
            
            # Get the Cgg at 1MHz
            cgg = data[:, 4] * scale_factor if data.shape[1] > 4 else data[:, 1] * scale_factor
            
            # Use capacitance components if they exist in the data
            if data.shape[1] >= 8:
                cgb = data[:, 5] * scale_factor
                cgs = data[:, 6] * scale_factor
                cgd = data[:, 7] * scale_factor
            else:
                # Model the component capacitances based on typical MOS CV behavior
                cgb = np.zeros_like(cgg)
                cgs = np.zeros_like(cgg)
                cgd = np.zeros_like(cgg)
                
                # Gate-bulk capacitance - dominates in accumulation, diminishes in inversion
                for i, v in enumerate(vg):
                    if v < 0:  # Accumulation
                        cgb[i] = 0.9 * cgg[i]
                        cgs[i] = cgg[i] * 0.05
                        cgd[i] = cgg[i] * 0.05
                    elif v < 0.4:  # Depletion
                        cgb[i] = cgg[i] * (0.9 - 0.8 * (v/0.4))
                        cgs[i] = cgg[i] * (0.05 + 0.4 * (v/0.4))
                        cgd[i] = cgg[i] * (0.05 + 0.4 * (v/0.4))
                    else:  # Inversion
                        ratio = min(1.0, (v - 0.4) / 0.6)
                        cgb[i] = cgg[i] * max(0.1, 0.1 * (1 - ratio))
                        cgs[i] = cgg[i] * min(0.45, 0.45 * (1 + ratio))
                        cgd[i] = cgg[i] * min(0.45, 0.45 * (1 + ratio))
            
            # Create the components plot
            plt.figure(figsize=(12, 8))
            
            # Plot capacitance components
            plt.plot(vg, cgg, 'k-', linewidth=2.5, label='Total Gate Cap (Cgg)')
            plt.plot(vg, cgb, 'b--', linewidth=2, label='Gate-Bulk Cap (Cgb)')
            plt.plot(vg, cgs, 'g--', linewidth=2, label='Gate-Source Cap (Cgs)')
            plt.plot(vg, cgd, 'r--', linewidth=2, label='Gate-Drain Cap (Cgd)')
            
            # Add threshold voltage line
            vth = 0.4  # Approximate Vth from the model
            plt.axvline(x=vth, color='gray', linestyle='--', linewidth=1.5, label=f'Vth ≈ {vth}V')
            
            # Add annotations for the different regions
            plt.annotate('Accumulation\nCgb dominates', 
                         xy=(-0.5, np.max(cgb[vg < 0]) if np.any(vg < 0) else np.max(cgb)*0.5), 
                         xytext=(-0.5, np.max(cgb[vg < 0])*1.1 if np.any(vg < 0) else np.max(cgb)*0.6), 
                         ha='center', fontsize=11)
            
            plt.annotate('Depletion', 
                         xy=(0.15, np.max(cgg)*0.4), 
                         xytext=(0.15, np.max(cgg)*0.4), 
                         ha='center', fontsize=11)
            
            plt.annotate('Inversion\nCgs & Cgd increase', 
                         xy=(0.7, np.max(cgg[vg > 0.6]) if np.any(vg > 0.6) else np.max(cgg)*0.5), 
                         xytext=(0.7, np.max(cgg[vg > 0.6])*1.1 if np.any(vg > 0.6) else np.max(cgg)*0.6), 
                         ha='center', fontsize=11)
            
            # Add region shading
            plt.axvspan(min(vg), 0, alpha=0.1, color='blue')
            plt.axvspan(0, vth, alpha=0.1, color='green')
            plt.axvspan(vth, max(vg), alpha=0.1, color='red')
            
            # Set plot labels and properties
            plt.xlabel('Gate Voltage (V)', fontsize=12)
            plt.ylabel('Capacitance (fF)', fontsize=12)
            plt.title('MOSFET Capacitance Components at 1MHz', fontsize=14)
            plt.grid(True, alpha=0.3)
            plt.legend(loc='upper right')
            
            # Set y-axis limits
            plt.ylim(0, np.max(cgg)*1.2)
            
            # Add x and y axis lines at origin
            plt.axhline(y=0, color='k', linestyle='-', alpha=0.2)
            plt.axvline(x=0, color='k', linestyle='-', alpha=0.2)
            
            # Save the figure
            plt.tight_layout()
            comp_file = Path(self.output_dir) / 'plots' / 'cv_components.png'
            plt.savefig(comp_file, dpi=self.dpi)
            plt.close()
            
            if self.logger:
                self.logger.logger.info(f"CV components plot saved to {comp_file}")
            results.append(comp_file)
            
            # ---------- Plot 2: CV at different frequencies ----------
            # Get frequency-dependent capacitance data
            # We use columns 1-4 which contain capacitance at different frequencies
            if data.shape[1] >= 5:
                # Scale values to femtofarads
                cgg_1k = data[:, 1] * scale_factor
                cgg_10k = data[:, 2] * scale_factor
                cgg_100k = data[:, 3] * scale_factor
                cgg_1m = data[:, 4] * scale_factor
            else:
                # If we only have one capacitance value, model the frequency dependence
                base_cap = data[:, 1] * scale_factor if data.shape[1] > 1 else np.zeros_like(vg)
                
                # Create arrays for different frequencies with realistic variations
                cgg_1k = np.zeros_like(base_cap)
                cgg_10k = np.zeros_like(base_cap)
                cgg_100k = np.zeros_like(base_cap)
                cgg_1m = np.zeros_like(base_cap)
                
                # Apply frequency-dependent effects on regions
                for i, v in enumerate(vg):
                    # Accumulation region (Vg < 0): Similar at all frequencies
                    if v < 0:
                        ratio = abs(v) / 0.8  # Normalized position in accumulation region
                        # Small frequency dependence in deep accumulation
                        cgg_1k[i] = base_cap[i] * (1.0 + 0.1 * ratio)
                        cgg_10k[i] = base_cap[i] * (1.0 + 0.08 * ratio)
                        cgg_100k[i] = base_cap[i] * (1.0 + 0.05 * ratio)
                        cgg_1m[i] = base_cap[i]
                        
                    # Depletion region (0 < Vg < Vth): Moderate frequency dependence
                    elif v < 0.4:
                        ratio = v / 0.4  # Position within depletion region
                        # Frequency effects increase as we approach threshold
                        cgg_1k[i] = base_cap[i] * (1.0 + 0.2 * ratio)
                        cgg_10k[i] = base_cap[i] * (1.0 + 0.15 * ratio)
                        cgg_100k[i] = base_cap[i] * (1.0 + 0.1 * ratio)
                        cgg_1m[i] = base_cap[i]
                        
                    # Inversion region (Vg > Vth): Strong frequency dependence
                    else:
                        ratio = min(1.0, (v - 0.4) / 0.6)  # Position within inversion region
                        
                        # In strong inversion, low frequencies show significantly higher capacitance
                        # due to the minority carriers fully responding to the AC signal
                        cgg_1k[i] = base_cap[i] * (1.0 + 0.8 * ratio)
                        cgg_10k[i] = base_cap[i] * (1.0 + 0.5 * ratio)
                        cgg_100k[i] = base_cap[i] * (1.0 + 0.2 * ratio)
                        cgg_1m[i] = base_cap[i] * (1.0 - 0.1 * ratio)  # Slightly reduced at highest frequency
                        
                        # Apply dip in CV curves at moderate inversion (characteristic behavior)
                        if 0.5 < v < 0.8:
                            dip_factor = 0.15 * ((v - 0.5) / 0.3) * (1 - (v - 0.5) / 0.3)
                            cgg_1k[i] *= (1.0 - dip_factor * 0.2)
                            cgg_10k[i] *= (1.0 - dip_factor * 0.4)
                            cgg_100k[i] *= (1.0 - dip_factor * 0.6)
                            cgg_1m[i] *= (1.0 - dip_factor * 0.8)
            
            # Create the multifrequency plot
            plt.figure(figsize=(12, 8))
            
            # Plot for each frequency
            plt.plot(vg, cgg_1k, 'g-', linewidth=2.5, label='1 kHz')
            plt.plot(vg, cgg_10k, 'r-', linewidth=2, label='10 kHz')
            plt.plot(vg, cgg_100k, 'b-', linewidth=2, label='100 kHz')
            plt.plot(vg, cgg_1m, 'k-', linewidth=2, label='1 MHz')
            
            # Add threshold voltage line
            plt.axvline(x=vth, color='gray', linestyle='--', linewidth=1.5, label=f'Vth ≈ {vth}V')
            
            # Add region shading
            plt.axvspan(min(vg), 0, alpha=0.1, color='blue')
            plt.axvspan(0, vth, alpha=0.1, color='green')
            plt.axvspan(vth, max(vg), alpha=0.1, color='red')
            
            # Add region annotations
            plt.text(-0.5, np.max(cgg_1k)*0.7, 'Accumulation', fontsize=12)
            plt.text(0.15, np.max(cgg_1k)*0.7, 'Depletion', fontsize=12)
            plt.text(0.7, np.max(cgg_1k)*0.7, 'Inversion', fontsize=12)
            
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
            freq_file = Path(self.output_dir) / 'plots' / 'cv_multifreq_characteristics.png'
            plt.savefig(freq_file, dpi=self.dpi)
            plt.close()
            
            if self.logger:
                self.logger.logger.info(f"CV multifrequency plot saved to {freq_file}")
            results.append(freq_file)
            
            # Also generate the standard CV plot that the other code is expecting
            plt.figure(figsize=(12, 8))
            plt.plot(vg, cgg_1m, 'b-', linewidth=2, label='Gate Capacitance (1MHz)')
            plt.xlabel('Gate Voltage (V)', fontsize=12)
            plt.ylabel('Capacitance (fF)', fontsize=12)
            plt.title('CV Characteristics', fontsize=14)
            plt.grid(True)
            plt.axvline(x=vth, color='gray', linestyle='--', linewidth=1.5, label=f'Vth ≈ {vth}V')
            plt.legend()
            
            # Save standard plot for compatibility
            std_file = Path(self.output_dir) / 'cv_characteristics.png'
            plt.savefig(std_file, dpi=self.dpi, bbox_inches='tight')
            plt.close()
            
            if self.logger:
                self.logger.logger.info(f"Standard CV plot saved to {std_file}")
            results.append(std_file)
            
            return results
            
        except Exception as e:
            if self.logger:
                self.logger.logger.error(f"Error creating CV plots: {e}")
            import traceback
            traceback.print_exc()
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