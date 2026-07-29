import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os
import matplotlib.gridspec as gridspec

class PlotGenerator:
    """Handles generation of plots from simulation data."""
    def __init__(self, output_dir, dpi=300, logger=None):
        self.output_dir = output_dir
        self.plots_dir = os.path.join(output_dir, 'plots')
        # Create plots directory if it doesn't exist
        os.makedirs(self.plots_dir, exist_ok=True)
        self.dpi = dpi
        self.logger = logger
        
        # Define a minimal color palette with just 5 colors
        self.colors = {
            'blue': '#0000FF',    # Primary color (gates, inputs) - Pure blue
            'red': '#FF0000',     # Secondary color (drains, outputs) - Pure red
            'green': '#00AA00',   # Tertiary color (sources, other signals) - Pure green
            'purple': '#AA00AA',  # Quaternary color (for bulk, bias points) - Rich purple
            'orange': '#FF8000'   # For total/reference values - Rich orange
        }
        
        # Create alias mappings for semantic use
        self.color_map = {
            'primary': self.colors['blue'],
            'secondary': self.colors['red'],
            'tertiary': self.colors['green'],
            'quaternary': self.colors['purple'],
            'total': self.colors['orange']
        }
        
        # Set consistent figure width for all plots
        self.figure_width = 10
        
        # Set height ratios for different panel configurations
        self.height_ratio_single = 0.9    # Height ratio for single panel plots
        self.height_ratio_two = 1.6       # Height ratio for two panel plots  
        self.height_ratio_three = 2.4     # Height ratio for three panel plots
        
        # Calculate actual heights
        self.single_plot_height = self.figure_width * self.height_ratio_single
        self.two_panel_height = self.figure_width * self.height_ratio_two
        self.three_panel_height = self.figure_width * self.height_ratio_three
    
    # DC Analysis
    def plot_dc_iv_characteristics(self, output_dir, vds, vgs, ids, colors=None):
        """Plot IV characteristics with subthreshold and saturation regions."""
        try:
            plt.figure(figsize=(self.figure_width, self.single_plot_height))
            
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
            color_keys = list(self.color_map.keys())
            for i, vg in enumerate(selected_vgs):
                mask = np.isclose(vgs, vg)
                if np.any(mask):
                    vds_curve = vds[mask]
                    ids_curve = ids[mask]
                    print(f"Vgs={vg:.3f}V: Ids range {np.min(ids_curve):.3e}A to {np.max(ids_curve):.3e}A")
                    # Use color from our limited palette, cycling as needed
                    color_key = color_keys[i % len(color_keys)]
                    plt.plot(vds_curve, ids_curve, color=self.color_map[color_key], label=f'Vgs={vg:.1f}V')
            
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
            for i, vg in enumerate(selected_vgs):
                mask = np.isclose(vgs, vg)
                if np.any(mask):
                    vds_curve = vds[mask]
                    ids_curve = ids[mask]
                    # Use same color as main plot for consistency
                    color_key = color_keys[i % len(color_keys)]
                    ax_inset.semilogy(vds_curve, np.abs(ids_curve), color=self.color_map[color_key], label=f'Vgs={vg:.1f}V')
            
            ax_inset.set_xlabel('Vds (V)')
            ax_inset.set_ylabel('|Ids| (A)')
            ax_inset.set_title('Subthreshold Region')
            ax_inset.grid(True)
            
            # Save to plots subdirectory
            output_file = Path(self.plots_dir) / 'dc_iv_characteristics.png'
            plt.savefig(output_file, dpi=self.dpi)
            plt.close()
            
            if self.logger:
                self.logger.info(f"IV characteristics plot saved to {output_file}")
                
            return output_file
            
        except Exception as e:
            self.logger.error(f"Error plotting IV characteristics: {e}")
            raise

    def plot_dc_kcl_verification(self, output_dir, ids, ig, is_, ib):
        """Plot KCL verification showing current balance."""
        if any(x is None for x in [ids, ig, is_, ib]):
            return None
            
        try:
            plt.figure(figsize=(self.figure_width, self.single_plot_height))
            
            # Calculate total current
            total = ids + ig + is_ + ib
            
            # Plot individual currents with consistent colors
            plt.plot(ids, color=self.color_map['secondary'], label='Ids')
            plt.plot(ig, color=self.color_map['primary'], label='Ig')
            plt.plot(is_, color=self.color_map['tertiary'], label='Is')
            plt.plot(ib, color=self.color_map['quaternary'], label='Ib')
            plt.plot(total, '--', color=self.color_map['total'], label='Total (KCL)')
            
            plt.xlabel('Measurement Point')
            plt.ylabel('Current (A)')
            plt.title('KCL Verification')
            plt.grid(True)
            plt.legend()
            
            # Save plot
            output_file = Path(self.plots_dir) / 'dc_kcl_verification.png'
            plt.savefig(output_file, dpi=self.dpi)
            plt.close()
            
            if self.logger:
                self.logger.info(f"KCL verification plot saved to {output_file}")
                
            return output_file
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error creating KCL verification plot: {e}")
            return None

    def plot_dc_temperature_analysis(self, output_dir, temp, ids):
        """Plot temperature analysis with current variation."""
        if temp is None or ids is None:
            return None
            
        try:
            plt.figure(figsize=(self.figure_width, self.single_plot_height))
            
            # Plot temperature dependence
            plt.plot(temp, ids, 'o-', color=self.color_map['primary'], label='Ids')
            
            # Add trend line
            z = np.polyfit(temp, ids, 1)
            p = np.poly1d(z)
            plt.plot(temp, p(temp), '--', color=self.color_map['total'], label=f'Trend (slope: {z[0]:.2e}A/°C)')
            
            plt.xlabel('Temperature (°C)')
            plt.ylabel('Ids (A)')
            plt.title('Temperature Analysis')
            plt.grid(True)
            plt.legend()
            
            # Save plot
            output_file = Path(self.plots_dir) / 'dc_temperature_analysis.png'
            plt.savefig(output_file, dpi=self.dpi)
            plt.close()
            
            if self.logger:
                self.logger.info(f"Temperature analysis plot saved to {output_file}")
                
            return output_file
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error creating temperature analysis plot: {e}")
            return None

    # AC Analysis
    def plot_ac_cv_characteristics(self, output_dir, vg=None, ig=None, freq=None):
        """
        Generate comprehensive CV plots based on data in results/data/cv_data.txt.
        Creates both component analysis and frequency-dependent plots.
        """
        try:
            results = []
            # Make sure plots directory exists
            plots_dir = Path(output_dir) / 'plots'
            plots_dir.mkdir(exist_ok=True)
            
            # Check if file exists
            data_file = os.path.join(output_dir, 'data', 'cv_data.txt')
            if not os.path.exists(data_file):
                if self.logger:
                    self.logger.error(f"CV data file {data_file} not found")
                return None
                
            if self.logger:
                self.logger.info(f"Loading CV data from {data_file}")
            
            # Read file and handle potential header lines
            with open(data_file, 'r') as f:
                lines = f.readlines()
                
            # Skip header lines
            data_lines = lines[1:] if len(lines) > 1 else []
            if len(data_lines) == 0:
                if self.logger:
                    self.logger.error("No valid data found in CV data file")
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
                        self.logger.warning(f"Error parsing line: {line.strip()}, {e}")
                    continue
                    
            if not data:
                if self.logger:
                    self.logger.error("No valid data could be parsed from CV file")
                return None
                
            data = np.array(data)
            if self.logger:
                self.logger.info(f"CV data shape: {data.shape}")
            
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
                raise ValueError(
                    "CV component plots require measured Cgb/Cgs/Cgd columns"
                )
            
            # Create the components plot
            plt.figure(figsize=(12, 8))
            
            # Plot capacitance components
            plt.plot(vg, cgg, '-', linewidth=2.5, color=self.color_map['total'], label='Total Gate Cap (Cgg)')
            plt.plot(vg, cgb, '--', linewidth=2, color=self.color_map['primary'], label='Gate-Bulk Cap (Cgb)')
            plt.plot(vg, cgs, '--', linewidth=2, color=self.color_map['secondary'], label='Gate-Source Cap (Cgs)')
            plt.plot(vg, cgd, '--', linewidth=2, color=self.color_map['tertiary'], label='Gate-Drain Cap (Cgd)')
            
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
            
            # Set y-axis limits - modified to include all components
            # Find the maximum of all capacitance components to ensure all are visible
            all_cap_values = np.concatenate((cgg, cgb, cgs, cgd))
            max_cap = np.max(all_cap_values) if len(all_cap_values) > 0 else np.max(cgg)
            plt.ylim(0, max_cap*1.2)  # Add 20% margin to ensure all components are visible
            
            # Add x and y axis lines at origin
            plt.axhline(y=0, color='k', linestyle='-', alpha=0.2)
            plt.axvline(x=0, color='k', linestyle='-', alpha=0.2)
            
            # Save the figure
            plt.tight_layout()
            comp_file = Path(self.plots_dir) / 'ac_cv_components.png'
            plt.savefig(comp_file, dpi=self.dpi)
            plt.close()
            
            if self.logger:
                self.logger.info(f"CV components plot saved to {comp_file}")
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
                raise ValueError(
                    "multi-frequency CV plot requires four measured "
                    "frequency columns"
                )
            
            # Create the multifrequency plot
            plt.figure(figsize=(12, 8))
            
            # Plot for each frequency
            plt.plot(vg, cgg_1k, '-', linewidth=2.5, color=self.color_map['primary'], label='1 kHz')
            plt.plot(vg, cgg_10k, '-', linewidth=2, color=self.color_map['secondary'], label='10 kHz')
            plt.plot(vg, cgg_100k, '-', linewidth=2, color=self.color_map['tertiary'], label='100 kHz')
            plt.plot(vg, cgg_1m, '-', linewidth=2, color=self.color_map['quaternary'], label='1 MHz')
            
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
            freq_file = Path(self.plots_dir) / 'ac_v_multifreq_characteristics.png'
            plt.savefig(freq_file, dpi=self.dpi)
            plt.close()
            
            if self.logger:
                self.logger.info(f"CV multifrequency plot saved to {freq_file}")
            results.append(freq_file)
            
            # Also generate the standard CV plot that the other code is expecting
            plt.figure(figsize=(12, 8))
            plt.plot(vg, cgg_1m, '-', linewidth=2, color=self.color_map['primary'], label='Gate Capacitance (1MHz)')
            plt.xlabel('Gate Voltage (V)', fontsize=12)
            plt.ylabel('Capacitance (fF)', fontsize=12)
            plt.title('CV Characteristics', fontsize=14)
            plt.grid(True)
            plt.axvline(x=vth, color='gray', linestyle='--', linewidth=1.5, label=f'Vth ≈ {vth}V')
            plt.legend()
            
            # Save standard plot for compatibility
            std_file = Path(self.plots_dir) / 'ac_cv_characteristics.png'
            plt.savefig(std_file, dpi=self.dpi)
            plt.close()
            
            if self.logger:
                self.logger.info(f"CV plot saved to {std_file}")
            results.append(std_file)

            # ---------- Plot 3: Per-gate-area (W*L) normalized CV at 1MHz ----------
            # This plot is generated if MOSFETSimulation produced the per-area table.
            per_area_file = os.path.join(output_dir, 'data', 'ac_cv_caps_1MHz_per_gate_area.csv')
            if os.path.exists(per_area_file):
                try:
                    arr = np.genfromtxt(per_area_file, delimiter=',', names=True, dtype=float, encoding=None)
                    if arr.size > 0 and 'Vg' in arr.dtype.names:
                        vg_a = np.atleast_1d(arr['Vg']).astype(float)
                        order_a = np.argsort(vg_a)
                        vg_a = vg_a[order_a]

                        def _col(name: str):
                            if name in arr.dtype.names:
                                return np.atleast_1d(arr[name]).astype(float)[order_a]
                            return None

                        cgg_a = _col('Cgg_fF_per_um2')
                        cgs_a = _col('Cgs_fF_per_um2')
                        cgd_a = _col('Cgd_fF_per_um2')
                        cgb_a = _col('Cgb_fF_per_um2')

                        # Plot Cgg per area
                        if cgg_a is not None:
                            plt.figure(figsize=(12, 8))
                            plt.plot(
                                vg_a,
                                cgg_a,
                                '-',
                                linewidth=2.5,
                                color=self.color_map['primary'],
                                label='Cgg / Area (1MHz)'
                            )
                            plt.xlabel('Gate Voltage (V)', fontsize=12)
                            plt.ylabel('Capacitance Density (fF/µm²)', fontsize=12)
                            plt.title('CV Characteristics per Gate Area (1MHz)', fontsize=14)
                            plt.grid(True, alpha=0.3)
                            plt.axvline(x=vth, color='gray', linestyle='--', linewidth=1.5, label=f'Vth ≈ {vth}V')
                            plt.legend()

                            plt.tight_layout()
                            std_area_file = Path(self.plots_dir) / 'ac_cv_characteristics_per_gate_area.png'
                            plt.savefig(std_area_file, dpi=self.dpi)
                            plt.close()
                            if self.logger:
                                self.logger.info(f"CV per-area plot saved to {std_area_file}")
                            results.append(std_area_file)

                        # Plot components per area
                        if all(x is not None for x in [cgg_a, cgb_a, cgs_a, cgd_a]):
                            plt.figure(figsize=(12, 8))
                            plt.plot(vg_a, cgg_a, '-', linewidth=2.5, color=self.color_map['total'], label='Cgg / Area')
                            plt.plot(vg_a, cgb_a, '--', linewidth=2, color=self.color_map['primary'], label='Cgb / Area')
                            plt.plot(vg_a, cgs_a, '--', linewidth=2, color=self.color_map['secondary'], label='Cgs / Area')
                            plt.plot(vg_a, cgd_a, '--', linewidth=2, color=self.color_map['tertiary'], label='Cgd / Area')
                            plt.axvline(x=vth, color='gray', linestyle='--', linewidth=1.5, label=f'Vth ≈ {vth}V')

                            plt.xlabel('Gate Voltage (V)', fontsize=12)
                            plt.ylabel('Capacitance Density (fF/µm²)', fontsize=12)
                            plt.title('MOSFET Capacitance Components per Gate Area (1MHz)', fontsize=14)
                            plt.grid(True, alpha=0.3)
                            plt.legend(loc='best')

                            # Make sure negative components are visible
                            all_vals = np.concatenate((cgg_a, cgb_a, cgs_a, cgd_a))
                            y_min = float(np.min(all_vals))
                            y_max = float(np.max(all_vals))
                            pad = 0.1 * (y_max - y_min) if y_max > y_min else (abs(y_max) * 0.1 + 1.0)
                            plt.ylim(y_min - pad, y_max + pad)

                            plt.axhline(y=0, color='k', linestyle='-', alpha=0.2)
                            plt.axvline(x=0, color='k', linestyle='-', alpha=0.2)

                            plt.tight_layout()
                            comp_area_file = Path(self.plots_dir) / 'ac_cv_components_per_gate_area.png'
                            plt.savefig(comp_area_file, dpi=self.dpi)
                            plt.close()
                            if self.logger:
                                self.logger.info(f"CV components per-area plot saved to {comp_area_file}")
                            results.append(comp_area_file)
                except Exception as e:
                    if self.logger:
                        self.logger.warning(f"Per-area CV plot skipped: {e}")
            
            return results
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error creating CV plots: {e}")
            import traceback
            traceback.print_exc()
            return None

    def plot_ac_sparameter_analysis(self, output_dir, freq=None, s11_mag=None, s21_mag=None, s12_mag=None, s22_mag=None):
        """Plot S-parameters analysis.
        
        Args:
            freq: Frequency array in Hz
            s11_mag: S11 magnitude array
            s21_mag: S21 magnitude array (forward gain)
            s12_mag: S12 magnitude array (reverse isolation)
            s22_mag: S22 magnitude array
            
        Returns:
            Path to the saved plot file
        """
        import os
        import math
        import numpy as np

        # Make sure plots directory exists
        plots_dir = Path(output_dir) / 'plots'
        plots_dir.mkdir(exist_ok=True)
            
        # Check if S-parameter data file exists
        data_file = os.path.join(self.output_dir, 'data', 'sparams_data.txt')

        if not os.path.exists(data_file) or os.path.getsize(data_file) == 0:
            raise FileNotFoundError(
                "S-parameter plot requires measured data/sparams_data.txt"
            )
        
        # Read S-parameter data from file
        data = []
        headers = []
        with open(data_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#'):
                    if len(headers) == 0:
                        headers = line.strip('# ').split()
                    continue
                values = line.split()
                if len(values) >= 9:  # At least freq + 4 S-params with mag and phase
                    data.append([float(v) for v in values])
        
        if not data:
            print("[ERROR]: No valid S-parameter data found")
            return None
        
        # Convert to numpy array for easier processing
        data = np.array(data)
        freq = data[:, 0]
        s11_mag = data[:, 1]
        s11_phase = data[:, 2]
        s12_mag = data[:, 3]
        s12_phase = data[:, 4]
        s21_mag = data[:, 5]
        s21_phase = data[:, 6]
        s22_mag = data[:, 7]
        s22_phase = data[:, 8]
        
        # Create high-frequency S-parameter plot
        plt.figure(figsize=(self.figure_width, 2 * self.single_plot_height))
        
        # Top panel: Magnitude plot (dB scale)
        plt.subplot(2, 1, 1)
        plt.semilogx(freq, 20 * np.log10(s11_mag), 'r-', label='S11 (Input Return Loss)')
        plt.semilogx(freq, 20 * np.log10(s21_mag), 'g-', label='S21 (Forward Gain)')
        plt.semilogx(freq, 20 * np.log10(s12_mag), 'b-', label='S12 (Reverse Isolation)')
        plt.semilogx(freq, 20 * np.log10(s22_mag), 'm-', label='S22 (Output Return Loss)')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude (dB)')
        plt.title('S-Parameters Magnitude')
        plt.grid(True, which='both', linestyle='--', alpha=0.6)
        plt.legend(loc='best')
        
        # Bottom panel: Phase plot
        plt.subplot(2, 1, 2)
        plt.semilogx(freq, s11_phase, 'r-', label='S11 Phase')
        plt.semilogx(freq, s21_phase, 'g-', label='S21 Phase')
        plt.semilogx(freq, s12_phase, 'b-', label='S12 Phase')
        plt.semilogx(freq, s22_phase, 'm-', label='S22 Phase')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Phase (degrees)')
        plt.title('S-Parameters Phase')
        plt.grid(True, which='both', linestyle='--', alpha=0.6)
        plt.legend(loc='best')
        
        plt.tight_layout()
        
        # Save plot
        plot_file = os.path.join(plots_dir, 'ac_cv_sparameter_analysis.png')
        plt.savefig(plot_file, dpi=self.dpi)
        plt.close()
        
        print(f"[INFO]: S-parameter analysis plot saved to {plot_file}")
        return plot_file

    def plot_ac_nqs_effects(self, output_dir, freq=None, vg_phase=None, id_phase=None, phase_diff=None):
        """Plot non-quasi-static effects analysis.
        
        Args:
            freq: Frequency array in Hz
            vg_phase: Gate voltage phase in degrees
            id_phase: Drain current phase in degrees
            phase_diff: Phase difference in degrees
            
        Returns:
            Path to the saved plot file
        """
        import os
        import math
        import numpy as np

        # Make sure plots directory exists
        plots_dir = Path(output_dir) / 'plots'
        plots_dir.mkdir(exist_ok=True)
            
        # Check if NQS effects data file exists
        data_file = os.path.join(self.output_dir, 'data', 'nqs_effects.txt')
        
        if not os.path.exists(data_file) or os.path.getsize(data_file) == 0:
            raise FileNotFoundError(
                "NQS plot requires measured data/nqs_effects.txt"
            )
        
        # Read NQS effects data from file
        data = []
        headers = []
        with open(data_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#'):
                    if len(headers) == 0:
                        headers = line.strip('# ').split()
                    continue
                values = line.split()
                if len(values) >= 4:  # freq, vg_phase, id_phase, phase_diff
                    data.append([float(v) for v in values])
        
        if not data:
            print("[ERROR]: No valid NQS effects data found")
            return None
        
        # Convert to numpy array for easier processing
        data = np.array(data)
        freq = data[:, 0]
        vg_phase = data[:, 1]
        id_phase = data[:, 2]
        phase_diff = data[:, 3]
        
        # Create NQS effects plot
        plt.figure(figsize=(self.figure_width, 2 * self.single_plot_height))
        
        # Top panel: Phase values
        plt.subplot(2, 1, 1)
        plt.semilogx(freq, vg_phase, 'r-', label='Gate Voltage Phase')
        plt.semilogx(freq, id_phase, 'b-', label='Drain Current Phase')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Phase (degrees)')
        plt.title('Non-Quasi-Static Effect: Signal Phases')
        plt.grid(True, which='both', linestyle='--', alpha=0.6)
        plt.legend(loc='best')
        
        # Bottom panel: Phase difference (key NQS indicator)
        plt.subplot(2, 1, 2)
        plt.semilogx(freq, phase_diff, 'g-', linewidth=2)
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Phase Difference (degrees)')
        plt.title('Gate-Drain Phase Shift (NQS Effect)')
        plt.grid(True, which='both', linestyle='--', alpha=0.6)
        plt.tight_layout()
        
        # Save plot
        plot_file = os.path.join(plots_dir, 'ac_cv_nqs_effects.png')
        plt.savefig(plot_file, dpi=self.dpi)
        plt.close()
            
        print(f"[INFO]: NQS effects plot saved to {plot_file}")
        return plot_file

    def plot_ac_charge_conservation(self, output_dir, time, vg, ig, id, is_, ib, i_total, q_gate, q_drain, q_source, q_bulk, q_total):
        """Plot charge conservation test results.
        
        Args:
            time (np.ndarray): Time points
            vg (np.ndarray): Gate voltage
            ig (np.ndarray): Gate current
            id (np.ndarray): Drain current
            is_ (np.ndarray): Source current
            ib (np.ndarray): Bulk current
            i_total (np.ndarray): Total current
            q_gate (np.ndarray): Gate charge
            q_drain (np.ndarray): Drain charge
            q_source (np.ndarray): Source charge
            q_bulk (np.ndarray): Bulk charge
            q_total (np.ndarray): Total charge
        """
        try:
            # Create figure with subplots
            fig = plt.figure(figsize=(15, 10))
            gs = gridspec.GridSpec(4, 1)
            plt.figure(figsize=(self.figure_width, 4 * self.single_plot_height))
        
            # Plot currents
            plt.subplot(4, 1, 1)
            plt.plot(time, ig, 'b-', label='Gate')
            plt.plot(time, id, 'r-', label='Drain')
            plt.plot(time, is_, 'g-', label='Source')
            plt.plot(time, ib, 'm-', label='Bulk')
            plt.plot(time, i_total, 'k--', label='Total')
            plt.xlabel('Time (s)')
            plt.ylabel('Current (A)')
            plt.title('Terminal Currents')
            plt.grid(True)
            plt.legend()
            
            # Plot charges
            plt.subplot(4, 1, 2)
            plt.plot(time, q_gate, 'b-', label='Gate')
            plt.plot(time, q_drain, 'r-', label='Drain')
            plt.plot(time, q_source, 'g-', label='Source')
            plt.plot(time, q_bulk, 'm-', label='Bulk')
            plt.plot(time, q_total, 'k--', label='Total')
            plt.xlabel('Time (s)')
            plt.ylabel('Charge (C)')
            plt.title('Terminal Charges')
            plt.grid(True)
            plt.legend()
            
            # Plot charge vs voltage
            plt.subplot(4, 1, 3)
            plt.plot(vg, q_gate, 'b-', label='Gate')
            plt.plot(vg, q_drain, 'r-', label='Drain')
            plt.plot(vg, q_source, 'g-', label='Source')
            plt.plot(vg, q_bulk, 'm-', label='Bulk')
            plt.xlabel('Gate Voltage (V)')
            plt.ylabel('Charge (C)')
            plt.title('Charge vs Gate Voltage')
            plt.grid(True)
            plt.legend()
            
            # Plot total charge error
            plt.subplot(4, 1, 4)
            plt.plot(time, q_total, 'k-')
            plt.xlabel('Time (s)')
            plt.ylabel('Total Charge (C)')
            plt.title('Total Charge Error')
            plt.grid(True)
            
            # Adjust layout and save
            plt.tight_layout()
            plt.savefig(
                os.path.join(
                    output_dir, 'plots', 'ac_charge_conservation.png'
                ),
                dpi=self.dpi,
            )
            plt.close()
            
            self.logger.info("Charge conservation plots generated successfully")
            
        except Exception as e:
            self.logger.error(f"Error generating charge conservation plots: {e}")
            import traceback
            traceback.print_exc()

    def _process_sparameter_files(self):
        """Reject plot-time construction of simulator measurements."""
        raise RuntimeError(
            "plot-time S-parameter generation is disabled; data must come "
            "from the simulator post-processor"
        )

    def _process_nqs_effects_files(self):
        """Reject plot-time construction of simulator measurements."""
        raise RuntimeError(
            "plot-time NQS generation is disabled; data must come from the "
            "simulator post-processor"
        )

    # Transient Analysis
    def plot_trans_large_signal_transient(self, output_dir, time, gate_voltage, drain_voltage, drain_current):
        """Plot large signal transient analysis results."""
        try:
            # Make sure plots directory exists
            plots_dir = Path(output_dir) / 'plots'
            plots_dir.mkdir(exist_ok=True)
                
            output_file = os.path.join(plots_dir, 'trans_large_signal_transient.png')

            plt.figure(figsize=(self.figure_width, self.two_panel_height))
            plt.subplot(2, 1, 1)
            plt.plot(time*1e9, gate_voltage, color=self.color_map['primary'], label='Gate Voltage (V)')
            plt.plot(time*1e9, drain_voltage, color=self.color_map['secondary'], label='Drain Voltage (V)')
            plt.xlabel('Time (ns)')
            plt.ylabel('Voltage (V)')
            plt.legend()
            plt.grid(True)
            plt.title('Large-Signal Transient Analysis - Voltages')
            
            plt.subplot(2, 1, 2)
            plt.plot(time*1e9, drain_current*1e3, color=self.color_map['secondary'], label='Drain Current (mA)')
            plt.xlabel('Time (ns)')
            plt.ylabel('Current (mA)')
            plt.legend()
            plt.grid(True)
            
            plt.tight_layout()
            
            plt.savefig(output_file, dpi=self.dpi)
            plt.close()
            
            if self.logger:
                self.logger.info(f"Large signal transient plot saved to {output_file}")
                
            return output_file
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error creating large signal transient plot: {e}")
            return None
    
    def plot_trans_switching_response(self, output_dir, time, input_voltage, output_voltage, supply_current, switching_power=None):
        """Plot switching behavior of the inverter."""
        try:
            # Make sure plots directory exists
            plots_dir = Path(output_dir) / 'plots'
            plots_dir.mkdir(exist_ok=True)
                
            output_file = os.path.join(plots_dir, 'trans_switching_response.png')

            plt.figure(figsize=(self.figure_width, self.three_panel_height))
            
            # Plot voltages
            plt.subplot(3, 1, 1)
            plt.plot(time*1e9, input_voltage, color=self.color_map['primary'], label='Input Voltage (V)')
            plt.plot(time*1e9, output_voltage, color=self.color_map['secondary'], label='Output Voltage (V)')
            plt.xlabel('Time (ns)')
            plt.ylabel('Voltage (V)')
            plt.legend()
            plt.grid(True)
            plt.title('Inverter Switching Response')
            
            # Plot current
            plt.subplot(3, 1, 2)
            plt.plot(time*1e9, supply_current*1e3, color=self.color_map['tertiary'], label='Supply Current (mA)')
            plt.xlabel('Time (ns)')
            plt.ylabel('Current (mA)')
            plt.legend()
            plt.grid(True)
            
            # Plot power if available
            if switching_power is not None:
                plt.subplot(3, 1, 3)
                plt.plot(time*1e9, switching_power*1e3, color=self.color_map['quaternary'], label='Power Dissipation (mW)')
                plt.xlabel('Time (ns)')
                plt.ylabel('Power (mW)')
                plt.legend()
                plt.grid(True)
            
            plt.tight_layout()
            
            plt.savefig(output_file, dpi=self.dpi)
            plt.close()
            
            if self.logger:
                self.logger.info(f"Switching response plot saved to {output_file}")
                
            return output_file
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error creating switching response plot: {e}")
            return None
    
    def plot_trans_delay_effect(self, output_dir, time, input_voltage, mid1_voltage, mid2_voltage, output_voltage):
        """Plot delay effects in inverter chain."""
        try:
            # Make sure plots directory exists
            plots_dir = Path(output_dir) / 'plots'
            plots_dir.mkdir(exist_ok=True)
                
            output_file = os.path.join(plots_dir, 'trans_delay_effect.png')

            plt.figure(figsize=(self.figure_width, self.single_plot_height))
            plt.plot(time*1e12, input_voltage, color=self.color_map['primary'], label='Input')
            plt.plot(time*1e12, mid1_voltage, color=self.color_map['tertiary'], label='Mid1')
            plt.plot(time*1e12, mid2_voltage, color=self.color_map['quaternary'], label='Mid2')
            plt.plot(time*1e12, output_voltage, color=self.color_map['secondary'], label='Output')
            plt.xlabel('Time (ps)')
            plt.ylabel('Voltage (V)')
            plt.legend()
            plt.grid(True)
            plt.title('Delay Effect Analysis - Inverter Chain')
            
            plt.savefig(output_file, dpi=self.dpi)
            plt.close()
            
            if self.logger:
                self.logger.info(f"Delay effect plot saved to {output_file}")
                
            return output_file
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error creating delay effect plot: {e}")
            return None
    
    def plot_trans_power_dissipation(self, output_dir, time_27c, power_27c, time_100c, power_100c):
        """Plot power dissipation at different temperatures."""
        try:
            # Make sure plots directory exists
            plots_dir = Path(output_dir) / 'plots'
            plots_dir.mkdir(exist_ok=True)
                
            output_file = os.path.join(plots_dir, 'trans_power_dissipation.png')

            plt.figure(figsize=(self.figure_width, self.single_plot_height))
            plt.plot(time_27c*1e9, power_27c*1e3, color=self.color_map['primary'], label='27°C')
            plt.plot(time_100c*1e9, power_100c*1e3, color=self.color_map['secondary'], label='100°C')
            plt.xlabel('Time (ns)')
            plt.ylabel('Power (mW)')
            plt.legend()
            plt.grid(True)
            plt.title('Power Dissipation at Different Temperatures')
            
            plt.savefig(output_file, dpi=self.dpi)
            plt.close()
            
            if self.logger:
                self.logger.info(f"Power dissipation plot saved to {output_file}")
                
            return output_file
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error creating power dissipation plot: {e}")
            return None
    
    def plot_trans_energy_consumption(self, output_dir, time_27c, energy_27c, time_100c, energy_100c):
        """Plot energy consumption at different temperatures."""
        try:
            # Make sure plots directory exists
            plots_dir = Path(output_dir) / 'plots'
            plots_dir.mkdir(exist_ok=True)
                
            output_file = os.path.join(plots_dir, 'trans_energy_consumption.png')

            plt.figure(figsize=(self.figure_width, self.single_plot_height))
            plt.plot(time_27c*1e9, energy_27c*1e12, color=self.color_map['primary'], label='27°C')
            plt.plot(time_100c*1e9, energy_100c*1e12, color=self.color_map['secondary'], label='100°C')
            plt.xlabel('Time (ns)')
            plt.ylabel('Energy (pJ)')
            plt.legend()
            plt.grid(True)
            plt.title('Energy Consumption at Different Temperatures')
            
            plt.savefig(output_file, dpi=self.dpi)
            plt.close()
            
            if self.logger:
                self.logger.info(f"Energy consumption plot saved to {output_file}")
                
            return output_file
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error creating energy consumption plot: {e}")
            return None

    def plot_trans_quasi_static(self, output_dir, time, gate_voltage, drain_voltage, drain_current):
        """Plot quasi-static behavior."""
        try:
            # Time-domain plot
            # Make sure plots directory exists
            plots_dir = Path(output_dir) / 'plots'
            plots_dir.mkdir(exist_ok=True)
                
            time_plot_file = os.path.join(plots_dir, 'trans_quasi_static_time.png')
            iv_plot_file = os.path.join(plots_dir, 'trans_quasi_static_iv.png')

            plt.figure(figsize=(self.figure_width, self.two_panel_height))
            
            # Plot voltages
            plt.subplot(2, 1, 1)
            plt.plot(time*1e9, gate_voltage, color=self.color_map['primary'], label='Gate Voltage (V)')
            plt.plot(time*1e9, drain_voltage, color=self.color_map['secondary'], label='Drain Voltage (V)')
            plt.xlabel('Time (ns)')
            plt.ylabel('Voltage (V)')
            plt.legend()
            plt.grid(True)
            plt.title('Quasi-Static Analysis')
            
            # Plot drain current - Use tertiary color (green) for current in bottom panel
            plt.subplot(2, 1, 2)
            plt.plot(time*1e9, drain_current*1e3, color=self.color_map['tertiary'], label='Drain Current (mA)')
            plt.xlabel('Time (ns)')
            plt.ylabel('Current (mA)')
            plt.legend()
            plt.grid(True)
            
            plt.tight_layout()
            
            plt.savefig(time_plot_file, dpi=self.dpi)
            plt.close()
            
            # I-V characteristic plot
            plt.figure(figsize=(self.figure_width, self.single_plot_height))
            plt.plot(gate_voltage, drain_current*1e3, color=self.color_map['tertiary'])
            plt.xlabel('Gate Voltage (V)')
            plt.ylabel('Drain Current (mA)')
            plt.grid(True)
            plt.title('Quasi-Static I-V Characteristic')

            plt.savefig(iv_plot_file, dpi=self.dpi)
            plt.close()
            
            if self.logger:
                self.logger.logger.info(f"Quasi-static plots saved to {time_plot_file} and {iv_plot_file}")
                
            return {"time_plot": time_plot_file, "iv_plot": iv_plot_file}
            
        except Exception as e:
            if self.logger:
                self.logger.logger.error(f"Error creating quasi-static plots: {e}")
            return None

    def plot_trans_charge_conservation(
        self,
        output_dir,
        time,
        vg,
        ig,
        id,
        is_,
        ib,
        i_total,
        q_gate,
        q_drain,
        q_source,
        q_bulk,
        q_total,
    ):
        """Render transient charge artifacts from the supplied result arrays.

        Integration and residual calculation remain the responsibility of the
        existing simulation/verification pipeline.  This method only maps
        those arrays to two distinct report images.
        """
        try:
            plots_dir = Path(output_dir) / "plots"
            plots_dir.mkdir(exist_ok=True)
            terminal_path = plots_dir / "trans_charge_conservation.png"
            total_path = plots_dir / "trans_total_charge.png"

            plt.figure(
                figsize=(self.figure_width, 3 * self.single_plot_height)
            )
            plt.subplot(3, 1, 1)
            plt.plot(time, ig, label="Gate")
            plt.plot(time, id, label="Drain")
            plt.plot(time, is_, label="Source")
            plt.plot(time, ib, label="Bulk")
            plt.plot(time, i_total, "k--", label="Total")
            plt.xlabel("Time (s)")
            plt.ylabel("Current (A)")
            plt.title("Transient Terminal Currents")
            plt.grid(True)
            plt.legend()

            plt.subplot(3, 1, 2)
            plt.plot(time, q_gate, label="Gate")
            plt.plot(time, q_drain, label="Drain")
            plt.plot(time, q_source, label="Source")
            plt.plot(time, q_bulk, label="Bulk")
            plt.xlabel("Time (s)")
            plt.ylabel("Charge (C)")
            plt.title("Transient Terminal Charges")
            plt.grid(True)
            plt.legend()

            plt.subplot(3, 1, 3)
            plt.plot(vg, q_gate, label="Gate")
            plt.plot(vg, q_drain, label="Drain")
            plt.plot(vg, q_source, label="Source")
            plt.plot(vg, q_bulk, label="Bulk")
            plt.xlabel("Gate Voltage (V)")
            plt.ylabel("Charge (C)")
            plt.title("Terminal Charge vs Gate Voltage")
            plt.grid(True)
            plt.legend()
            plt.tight_layout()
            plt.savefig(terminal_path, dpi=self.dpi)
            plt.close()

            plt.figure(figsize=(self.figure_width, self.single_plot_height))
            plt.plot(time, q_total, color="black")
            plt.xlabel("Time (s)")
            plt.ylabel("Total Charge (C)")
            plt.title("Transient Total Charge Conservation")
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(total_path, dpi=self.dpi)
            plt.close()

            if self.logger:
                self.logger.info(
                    "Transient charge plots saved to "
                    f"{terminal_path} and {total_path}"
                )
            return {
                "terminal_plot": str(terminal_path),
                "total_plot": str(total_path),
            }
        except Exception as e:
            if self.logger:
                self.logger.error(
                    f"Error creating transient charge plots: {e}"
                )
            return None

    # Noise
    
    def plot_noise_spectrum(self, output_dir, freq, noise, title, filename, 
                           log_x=True, log_y=True, additional_data=None):
        """Plot noise spectrum.
        
        Args:
            freq: Frequency array
            noise: Noise power spectral density array
            title: Plot title
            filename: Output filename (without extension)
            log_x: Use logarithmic scale for x-axis
            log_y: Use logarithmic scale for y-axis
            additional_data: Optional dictionary with additional data to plot
        
        Returns:
            str: Path to the saved plot file
        """
        try:
            plt.figure(figsize=(self.figure_width, self.single_plot_height))
            
            # Main noise data
            plt.plot(freq, noise, color=self.color_map['primary'], label='Noise PSD')
            
            # Additional data if provided
            if additional_data:
                for i, (label, (x_data, y_data)) in enumerate(additional_data.items()):
                    color_key = list(self.color_map.keys())[min(i+1, len(self.color_map)-1)]
                    plt.plot(x_data, y_data, color=self.color_map[color_key], label=label)
            
            # Set axis scales
            if log_x:
                plt.xscale('log')
            if log_y:
                plt.yscale('log')
                
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Noise Power Spectral Density (V²/Hz)')
            plt.title(title)
            plt.grid(True, which='both', linestyle='--', alpha=0.6)
            plt.legend()

            # Make sure plots directory exists
            plots_dir = Path(output_dir) / 'plots'
            plots_dir.mkdir(exist_ok=True)

            output_file = Path(self.plots_dir) / f'{filename}.png'
            plt.savefig(output_file, dpi=self.dpi)
            plt.close()
            
            if self.logger:
                self.logger.info(f"Noise spectrum plot saved to {output_file}")
                
            return output_file
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error creating noise spectrum plot: {e}")
            return None
    
    def plot_multiple_noise_spectra(self, output_dir, data_dict, title, filename):
        """Plot multiple noise spectra on the same figure.
        
        Args:
            data_dict: Dictionary with keys as labels and values as (freq, noise) tuples
            title: Plot title
            filename: Output filename (without extension)
        
        Returns:
            str: Path to the saved plot file
        """
        try:
            plt.figure(figsize=(self.figure_width, self.single_plot_height))
            
            # Use our limited color set instead of a colormap
            color_keys = list(self.color_map.keys())
            
            for i, (label, (freq, noise)) in enumerate(data_dict.items()):
                # Cycle through our color set
                color_key = color_keys[i % len(color_keys)]
                plt.plot(freq, noise, label=label, color=self.color_map[color_key])
            
            plt.xscale('log')
            plt.yscale('log')
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Noise Power Spectral Density (V²/Hz)')
            plt.title(title)
            plt.grid(True, which='both', linestyle='--', alpha=0.6)
            plt.legend()
            
            output_file = Path(self.plots_dir) / f'{filename}.png'
            plt.savefig(output_file, dpi=self.dpi)
            plt.close()
            
            if self.logger:
                self.logger.info(f"Multiple noise spectra plot saved to {output_file}")
                
            return output_file
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error creating multiple noise spectra plot: {e}")
            return None
    
    def plot_noise_vs_temperature(self, output_dir, temps, noise_levels, title="Noise vs Temperature"):
        """Plot noise level variation with temperature.
        
        Args:
            temps: List of temperature values
            noise_levels: List of corresponding noise levels or dictionary of temp->noise pairs
            title: Plot title
        
        Returns:
            str: Path to the saved plot file
        """
        try:
            plt.figure(figsize=(self.figure_width, self.single_plot_height))
            
            # Convert inputs to numpy arrays if they aren't already
            temps = np.array(temps)
            
            # Check the type of noise_levels
            if isinstance(noise_levels, dict):
                # Extract values from dictionary for temperatures we have
                noise_values = []
                valid_temps = []
                for temp in temps:
                    if temp in noise_levels:
                        valid_temps.append(temp)
                        # Get average noise level if it's an array
                        noise_data = noise_levels[temp]
                        if isinstance(noise_data, tuple) and len(noise_data) == 2:
                            # It's (freq, noise) tuple, calculate average
                            noise_values.append(np.mean(noise_data[1]))
                        else:
                            noise_values.append(np.mean(noise_data))
                temps = np.array(valid_temps)
                noise_levels = np.array(noise_values)
            else:
                # It's already an array, just make sure both arrays have same length
                noise_levels = np.array(noise_levels)
                if len(temps) != len(noise_levels):
                    if self.logger:
                        self.logger.warning(f"Mismatch in data dimensions: temps {temps.shape}, noise {noise_levels.shape}")
                    # Use only the data points we have for both
                    min_len = min(len(temps), len(noise_levels))
                    temps = temps[:min_len]
                    noise_levels = noise_levels[:min_len]
            
            if len(temps) == 0 or len(noise_levels) == 0:
                if self.logger:
                    self.logger.error("No valid temperature-noise data pairs found")
                return None
            
            plt.plot(temps, noise_levels, 'o-', color=self.color_map['primary'])
            
            # Linear fit
            if len(temps) > 1:
                z = np.polyfit(temps, noise_levels, 1)
                p = np.poly1d(z)
                plt.plot(temps, p(temps), '--', color=self.color_map['secondary'], 
                         label=f'Slope: {z[0]:.2e} V²/Hz/°C')
            
            plt.xlabel('Temperature (°C)')
            plt.ylabel('Noise Power Spectral Density (V²/Hz)')
            plt.title(title)
            plt.grid(True)
            plt.legend()
            
            output_file = Path(self.plots_dir) / 'noise_vs_temperature.png'
            plt.savefig(output_file, dpi=self.dpi)
            plt.close()
            
            if self.logger:
                self.logger.info(f"Noise vs temperature plot saved to {output_file}")
                
            return output_file
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error creating noise vs temperature plot: {e}")
            return None
    
    def plot_noise_components(self, output_dir, freq, thermal_noise, flicker_noise, shot_noise):
        """Plot different noise components on the same figure.
        
        Args:
            freq: Frequency array
            thermal_noise: Thermal noise array
            flicker_noise: Flicker noise array
            shot_noise: Shot noise array
        
        Returns:
            str: Path to the saved plot file
        """
        try:
            plt.figure(figsize=(self.figure_width, self.single_plot_height))
            
            plt.loglog(freq, thermal_noise, label='Thermal Noise', color=self.color_map['primary'])
            plt.loglog(freq, flicker_noise, label='Flicker Noise', color=self.color_map['secondary'])
            plt.loglog(freq, shot_noise, label='Shot Noise', color=self.color_map['tertiary'])
            
            # Calculate and plot total noise
            total_noise = thermal_noise + flicker_noise + shot_noise
            plt.loglog(freq, total_noise, label='Total Noise', color=self.color_map['total'], 
                      linestyle='--', linewidth=2)
            
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Noise Power Spectral Density (V²/Hz)')
            plt.title('Noise Components Analysis')
            plt.grid(True, which='both', linestyle='--', alpha=0.6)
            plt.legend()
            
            output_file = Path(self.plots_dir) / 'noise_components.png'
            plt.savefig(output_file, dpi=self.dpi)
            plt.close()
            
            if self.logger:
                self.logger.info(f"Noise components plot saved to {output_file}")
                
            return output_file
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error creating noise components plot: {e}")
            return None

    def calculate_rise_time(self, time, signal, low_threshold=0.1, high_threshold=0.9):
        """Calculate rise time (10% to 90%) of a signal."""
        # Normalize the signal
        normalized_signal = (signal - np.min(signal)) / (np.max(signal) - np.min(signal))
        
        # Find crossing points
        low_idx = np.where(normalized_signal >= low_threshold)[0][0]
        high_idx = np.where(normalized_signal >= high_threshold)[0][0]
        
        # Calculate rise time in ps
        rise_time = (time[high_idx] - time[low_idx]) * 1e12
        
        return rise_time

    def plot_noise_vs_parameter(self, output_dir, parameter, noise, parameter_name, title, filename):
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
            plt.figure(figsize=(self.figure_width, self.single_plot_height))
            
            # Plot noise vs parameter
            plt.plot(parameter, noise, 'o-', linewidth=2, markersize=6, color=self.color_map['primary'])
            
            # Set labels and title
            plt.xlabel(parameter_name)
            plt.ylabel('Noise Level (V²/Hz)')
            plt.title(title)
            plt.grid(True, linestyle='--', alpha=0.6)
            
            # Save figure
            output_path = Path(self.plots_dir) / f"{filename}.png"
            plt.tight_layout()
            plt.savefig(output_path, dpi=self.dpi)
            plt.close()
            
            if self.logger:
                self.logger.info(f"Parameter analysis plot saved to {output_path}")
            return output_path
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error creating parameter analysis plot: {e}")
            return None

    def plot_noise_contrib_components(self, freq, thermal, flicker, total, title, filename):
        """Plot noise contribution components."""
        # Implementation details
        # ...
    
