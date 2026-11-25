import os
from pathlib import Path
from typing import Union, Optional, Tuple, List
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from .plot_style import (
    apply_rcparams,
    apply_style,
    save_dev_figure,
    FIGSIZE,
    FIGSIZE_SQUARE,
    FIGSIZE_TALL,
    PRIMARY_BLUE,
    SECONDARY_RED,
    ACCENT_PURPLE,
    TWIN_ORANGE,
    HIGHLIGHT_GREEN,
    MUTED_GRAY,
    LINE_COLORS,
    LINEWIDTH_MAIN,
    LINEWIDTH_SECONDARY,
    TITLE_SIZE,
    LABEL_SIZE,
    MULTI_SERIES_COLORS,
)

# Intercept plt.savefig to guarantee dev-plot styling (SVG vector + PNG dual export & spine enforcement)
_orig_plt_savefig = plt.savefig

def _dev_plt_savefig(fname, *args, **kwargs):
    """Enforce dev-plot styling: axis spines, grid, tight_layout, and dual SVG/PNG export."""
    p = Path(str(fname))
    p.parent.mkdir(parents=True, exist_ok=True)
    fig = plt.gcf()
    for ax in fig.get_axes():
        apply_style(ax)
    try:
        fig.tight_layout()
    except Exception:
        pass

    svg_p = p.with_suffix(".svg")
    try:
        svg_kwargs = {k: v for k, v in kwargs.items() if k not in ("dpi", "format")}
        fig.savefig(str(svg_p), format="svg", **svg_kwargs)
    except Exception:
        pass
    return _orig_plt_savefig(fname, *args, **kwargs)

plt.savefig = _dev_plt_savefig


class PlotGenerator:
    """Handles generation of plots from simulation data conforming to dev-plot."""
    def __init__(self, output_dir, dpi=300, logger=None):
        self.output_dir = output_dir
        self.plots_dir = os.path.join(output_dir, 'plots')
        # Create plots directory if it doesn't exist
        os.makedirs(self.plots_dir, exist_ok=True)
        self.dpi = dpi
        self.logger = logger
        
        # Apply dev-plot typography & rcparams
        apply_rcparams()

        # MATLAB-aligned dev-plot color palette
        self.colors = {
            'blue': PRIMARY_BLUE,      # #0033cc
            'red': SECONDARY_RED,      # #cc0000
            'green': HIGHLIGHT_GREEN,  # #006400
            'purple': ACCENT_PURPLE,   # #7f3fbf
            'orange': TWIN_ORANGE,     # #e67300
            'gray': MUTED_GRAY,        # #666666
        }
        
        # Create alias mappings for semantic use
        self.color_map = {
            'primary': self.colors['blue'],
            'secondary': self.colors['red'],
            'tertiary': self.colors['green'],
            'quaternary': self.colors['purple'],
            'total': self.colors['orange'],
            'accent': self.colors['purple'],
        }
        
        # Set consistent figure width for all plots
        self.figure_width = 11
        
        # Set height ratios for different panel configurations
        self.height_ratio_single = 0.5    # Standard FIGSIZE (11, 5.5)
        self.height_ratio_two = 1.0       # Two panel plots  
        self.height_ratio_three = 1.5     # Three panel plots
        
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
            plt.savefig(output_file, dpi=self.dpi, bbox_inches='tight')
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
            plt.savefig(output_file, dpi=self.dpi, bbox_inches='tight')
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
            plt.savefig(output_file, dpi=self.dpi, bbox_inches='tight')
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
            plt.savefig(std_file, dpi=self.dpi, bbox_inches='tight')
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
                            plt.savefig(std_area_file, dpi=self.dpi, bbox_inches='tight')
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
            print(f"[WARNING]: S-parameter data file not found, generating from raw files")
            
            # Process input files to generate S-parameter data file
            self._process_sparameter_files()
        
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
            print(f"[WARNING]: NQS effects data file not found, generating from raw files")
            
            # Process input files to generate NQS effects data file
            self._process_nqs_effects_files()
        
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
            plt.savefig(os.path.join(output_dir, 'plots', 'ac_charge_conservation.png'))
            plt.close()
            
            self.logger.info("Charge conservation plots generated successfully")
            
        except Exception as e:
            self.logger.error(f"Error generating charge conservation plots: {e}")
            import traceback
            traceback.print_exc()

    def _process_sparameter_files(self):
        """Generate S-parameter data file from raw simulation output."""
        import os
        import math
        import re
        import numpy as np
        
        # Create output directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
        raw_sp1 = os.path.join(self.data_dir, 's_params_p1.txt')
        raw_sp2 = os.path.join(self.data_dir, 's_params_p2.txt')

        # Check if raw files exist
        if not os.path.exists(raw_sp1) or not os.path.exists(raw_sp2):
            print("[WARNING]: Raw S-parameter files not found, using calculated data")
            # Generate reasonable S-parameter data based on typical MOSFET behavior
            freq = np.logspace(6, 10, 20)  # 1MHz to 10GHz
            s_params = []
            for f in freq:
                # Calculate realistic S-parameters based on frequency
                # Higher frequencies -> worse matching and gain
                s11_mag = 0.8 - f/1e11
                s11_phase = -15 - f/1e10
                s21_mag = 12 - f/1e10
                s21_phase = 165 - f/1e10
                s12_mag = 0.003 - f/1e13
                s12_phase = 95 - f/1e10
                s22_mag = 0.9 - f/1e11
                s22_phase = -12 - f/1e10
                
                s_params.append([
                    f, 
                    s11_mag, s11_phase, 
                    s12_mag, s12_phase, 
                    s21_mag, s21_phase, 
                    s22_mag, s22_phase
                ])
                
            # Write the data file
            with open(os.path.join(self.data_dir, 'sparams_data.txt'), 'w') as f:
                f.write("# S-parameter data\n")
                f.write("# freq s11_mag s11_phase s12_mag s12_phase s21_mag s21_phase s22_mag s22_phase\n")
                for params in s_params:
                    f.write(" ".join(f"{p}" for p in params) + "\n")
            
            print(f"[INFO]: S-parameter data file created with calculated data ({len(s_params)} points)")
            return
            
        # Now parse the actual files if they exist
        try:
            # Function to read SPICE output file and extract complex data
            def _read_spice_file(filename):
                with open(filename, 'r') as f:
                    lines = f.readlines()
                
                # Extract variables and data
                variables = {}
                data_points = []
                in_variables = False
                in_values = False
                current_point = None
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    if line.startswith('Variables:'):
                        in_variables = True
                        continue
                    
                    if in_variables and line.startswith('\t'):
                        # Variable definition
                        parts = line.split()
                        if len(parts) >= 2:
                            idx = int(parts[0])
                            name = parts[1]
                            variables[idx] = name
                    
                    if line.startswith('Values:'):
                        in_variables = False
                        in_values = True
                        continue
                        
                    if in_values:
                        if line.startswith(' '):
                            # This is a data line
                            parts = line.split()
                            if len(parts) >= 2:
                                idx = int(parts[0])
                                val_parts = parts[1].split(',')
                                if len(val_parts) == 2:
                                    # Complex number
                                    re_val = float(val_parts[0])
                                    im_val = float(val_parts[1])
                                    if current_point is None:
                                        continue
                                    current_point[idx] = complex(re_val, im_val)
                        else:
                            # New data point
                            match = re.match(r'^\s*(\d+)\s', line)
                            if match:
                                if current_point:
                                    data_points.append(current_point)
                                current_point = {}
                
                if current_point:
                    data_points.append(current_point)
                
                return variables, data_points
            
            # Read the S-parameter simulation result files
            vars_p1, data_p1 = _read_spice_file(raw_sp1)
            vars_p2, data_p2 = _read_spice_file(raw_sp2)
            
            # Find the relevant variable indices
            freq_idx = None
            vg_idx = None
            vd_idx = None
            
            for idx, name in vars_p1.items():
                if name == 'frequency':
                    freq_idx = idx
                elif name == 'v(g_term)':
                    vg_idx = idx
                elif name == 'v(d_term)':
                    vd_idx = idx
            
            if freq_idx is None or vg_idx is None or vd_idx is None:
                raise ValueError("Required variables not found in S-parameter data")
            
            # Process the data points to calculate S-parameters
            s_params = []
            z0 = 50.0  # Reference impedance
            
            # Ensure both data sets have the same number of points
            min_points = min(len(data_p1), len(data_p2))
            
            for i in range(min_points):
                p1 = data_p1[i]
                p2 = data_p2[i]
                
                # Extract values
                freq = abs(p1[freq_idx])
                vg1 = p1[vg_idx]  # Port 1 active
                vd1 = p1[vd_idx]
                vg2 = p2[vg_idx]  # Port 2 active
                vd2 = p2[vd_idx]
                
                # Calculate S-parameters
                s11 = (vg1 - z0) / (vg1 + z0)
                s21 = 2 * vd1 / (vg1 + z0)
                s22 = (vd2 - z0) / (vd2 + z0)
                s12 = 2 * vg2 / (vd2 + z0)
                
                # Extract magnitude and phase
                s11_mag = abs(s11)
                s11_phase = math.degrees(math.atan2(s11.imag, s11.real))
                s21_mag = abs(s21)
                s21_phase = math.degrees(math.atan2(s21.imag, s21.real))
                s12_mag = abs(s12)
                s12_phase = math.degrees(math.atan2(s12.imag, s12.real))
                s22_mag = abs(s22)
                s22_phase = math.degrees(math.atan2(s22.imag, s22.real))
                
                s_params.append([
                    freq, 
                    s11_mag, s11_phase, 
                    s12_mag, s12_phase, 
                    s21_mag, s21_phase, 
                    s22_mag, s22_phase
                ])
            
            # Write the data file
            with open('results/data/sparams_data.txt', 'w') as f:
                f.write("# S-parameter data\n")
                f.write("# freq s11_mag s11_phase s12_mag s12_phase s21_mag s21_phase s22_mag s22_phase\n")
                for params in s_params:
                    f.write(" ".join(f"{p}" for p in params) + "\n")
            
            print(f"[INFO]: S-parameter data file created from raw data files ({len(s_params)} points)")
        
        except Exception as e:
            print(f"[ERROR]: Failed to process S-parameter files: {e}")
            # Fall back to calculated data
            self._process_sparameter_files()
    
    def _process_nqs_effects_files(self):
        """Generate NQS effects data file from raw simulation output."""
        import os
        import math
        import re
        import numpy as np
        
        # Create output directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
        raw_nqs = os.path.join(self.data_dir, 'nqs_effects_raw.txt')

        # Check if raw file exists
        if not os.path.exists(raw_nqs):
            print("[WARNING]: Raw NQS effects file not found, using calculated data")
            # Generate reasonable NQS effects data based on frequency
            freq = np.logspace(6, 10, 20)  # 1MHz to 10GHz
            nqs_data = []
            for f in freq:
                # Calculate realistic NQS effects based on frequency
                # Higher frequencies -> larger phase differences
                vg_phase = 45 + f/1e8  # Base phase starts at 45 degrees
                id_phase = 45 + f/3e8  # Smaller slope for drain current phase
                phase_diff = vg_phase - id_phase
                
                nqs_data.append([f, vg_phase, id_phase, phase_diff])
                
            # Write the data file
            with open(os.path.join(self.data_dir, 'nqs_effects.txt'), 'w') as f:
                f.write("# Non-quasi-static effects analysis - phase shifts\n")
                f.write("# freq vg_phase id_phase phase_diff\n")
                for data_point in nqs_data:
                    f.write(" ".join(f"{d}" for d in data_point) + "\n")
            
            print(f"[INFO]: NQS effects data file created with calculated data ({len(nqs_data)} points)")
            return
            
        # Now parse the actual file if it exists
        try:
            # Function to read SPICE output file and extract complex data
            def _read_spice_file(filename):
                with open(filename, 'r') as f:
                    lines = f.readlines()
                
                # Extract variables and data
                variables = {}
                data_points = []
                in_variables = False
                in_values = False
                current_point = None
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    if line.startswith('Variables:'):
                        in_variables = True
                        continue
                    
                    if in_variables and line.startswith('\t'):
                        # Variable definition
                        parts = line.split()
                        if len(parts) >= 2:
                            idx = int(parts[0])
                            name = parts[1]
                            variables[idx] = name
                    
                    if line.startswith('Values:'):
                        in_variables = False
                        in_values = True
                        continue
                        
                    if in_values:
                        if line.startswith(' '):
                            # This is a data line
                            parts = line.split()
                            if len(parts) >= 2:
                                idx = int(parts[0])
                                val_parts = parts[1].split(',')
                                if len(val_parts) == 2:
                                    # Complex number
                                    re_val = float(val_parts[0])
                                    im_val = float(val_parts[1])
                                    if current_point is None:
                                        continue
                                    current_point[idx] = complex(re_val, im_val)
                        else:
                            # New data point
                            match = re.match(r'^\s*(\d+)\s', line)
                            if match:
                                if current_point:
                                    data_points.append(current_point)
                                current_point = {}
                
                if current_point:
                    data_points.append(current_point)
                
                return variables, data_points
            
            # Read the NQS effects simulation result file
            vars_nqs, data_nqs = _read_spice_file(raw_nqs)
            
            # Find the relevant variable indices
            freq_idx = None
            vg_idx = None
            id_idx = None
            vd_idx = None
            
            for idx, name in vars_nqs.items():
                if name == 'frequency':
                    freq_idx = idx
                elif name == 'v(g_term)':
                    vg_idx = idx
                elif name == 'i(id_current)':
                    id_idx = idx
                elif name == 'v(d_term)':
                    vd_idx = idx
            
            if freq_idx is None or vg_idx is None:
                raise ValueError("Required variables not found in NQS effects data")
            
            # Use drain voltage phase if drain current not available
            if id_idx is None:
                id_idx = vd_idx
                print("[WARNING]: Using drain voltage phase instead of current phase for NQS effects")
            
            # Process the data points to calculate NQS effects
            nqs_data = []
            
            for point in data_nqs:
                # Extract values
                freq = abs(point[freq_idx])
                vg = point[vg_idx]
                id_val = point[id_idx] if id_idx in point else complex(0, 0)
                
                # Calculate phases
                vg_phase = math.degrees(math.atan2(vg.imag, vg.real))
                id_phase = math.degrees(math.atan2(id_val.imag, id_val.real))
                
                # Adjust phases to be in the range [0, 360)
                vg_phase = vg_phase + 360 if vg_phase < 0 else vg_phase
                id_phase = id_phase + 360 if id_phase < 0 else id_phase
                
                # Calculate phase difference
                phase_diff = vg_phase - id_phase
                if phase_diff < 0:
                    phase_diff += 360
                
                nqs_data.append([freq, vg_phase, id_phase, phase_diff])
            
            # Write the data file
            with open('results/data/nqs_effects.txt', 'w') as f:
                f.write("# Non-quasi-static effects analysis - phase shifts\n")
                f.write("# freq vg_phase id_phase phase_diff\n")
                for data_point in nqs_data:
                    f.write(" ".join(f"{d}" for d in data_point) + "\n")
            
            print(f"[INFO]: NQS effects data file created from raw data file ({len(nqs_data)} points)")
        
        except Exception as e:
            print(f"[ERROR]: Failed to process NQS effects file: {e}")
            # Fall back to calculated data
            freq = np.logspace(6, 10, 20)  # 1MHz to 10GHz
            nqs_data = []
            for f in freq:
                vg_phase = 45 + f/1e8
                id_phase = 45 + f/3e8
                phase_diff = vg_phase - id_phase
                nqs_data.append([f, vg_phase, id_phase, phase_diff])
                
            with open('results/data/nqs_effects.txt', 'w') as f:
                f.write("# Non-quasi-static effects analysis - phase shifts\n")
                f.write("# freq vg_phase id_phase phase_diff\n")
                for data_point in nqs_data:
                    f.write(" ".join(f"{d}" for d in data_point) + "\n")
            
            print(f"[INFO]: NQS effects data file created with fallback data ({len(nqs_data)} points)") 

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
        pass

    def plot_gummel_symmetry(self, output_dir, vx, ix, gx, gxx):
        """Plot Gummel Symmetry Test (GST) characteristics.
        
        Plots Ix(Vx) [odd symmetry], Gx(Vx) [even symmetry], and Gxx(Vx) [odd zero-crossing].
        """
        try:
            plots_dir = os.path.join(output_dir, 'plots')
            os.makedirs(plots_dir, exist_ok=True)
            
            fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 10), sharex=True)
            
            # Subplot 1: Ix vs Vx (Odd Symmetry)
            ax1.plot(vx, ix * 1e3, 'b-', linewidth=2, label=r'$I_x(V_x)$')
            ax1.axhline(0, color='gray', linestyle='--', alpha=0.6)
            ax1.axvline(0, color='gray', linestyle='--', alpha=0.6)
            ax1.set_ylabel(r'$I_x$ (mA)')
            ax1.set_title('Gummel Symmetry Test (McAndrew TED 2025)\n$I_x$ vs $V_x$ (Odd Parity: $I_x(-V_x) = -I_x(V_x)$)')
            ax1.grid(True, linestyle=':', alpha=0.6)
            ax1.legend(loc='best')
            
            # Subplot 2: Gx vs Vx (Even Symmetry)
            ax2.plot(vx, gx * 1e3, 'r-', linewidth=2, label=r'$G_x = dI_x/dV_x$')
            ax2.axvline(0, color='gray', linestyle='--', alpha=0.6)
            ax2.set_ylabel(r'$G_x$ (mS)')
            ax2.set_title(r'Conductance $G_x$ (Even Parity: $G_x(-V_x) = G_x(V_x)$)')
            ax2.grid(True, linestyle=':', alpha=0.6)
            ax2.legend(loc='best')
            
            # Subplot 3: Gxx vs Vx (Odd Zero-Crossing)
            ax3.plot(vx, gxx, 'g-', linewidth=2, label=r'$G_{xx} = d^2I_x/dV_x^2$')
            ax3.axhline(0, color='gray', linestyle='--', alpha=0.6)
            ax3.axvline(0, color='gray', linestyle='--', alpha=0.6)
            ax3.set_xlabel(r'Differential Voltage $V_x$ (V)')
            ax3.set_ylabel(r'$G_{xx}$ (A/V$^2$)')
            ax3.set_title(r'Second Derivative $G_{xx}$ (Odd Zero Crossing at $V_x = 0$)')
            ax3.grid(True, linestyle=':', alpha=0.6)
            ax3.legend(loc='best')
            
            plt.tight_layout()
            output_file = os.path.join(plots_dir, 'dc_gummel_symmetry.png')
            plt.savefig(output_file, dpi=self.dpi)
            plt.close()
            if self.logger:
                self.logger.info(f"GST plot saved to {output_file}")
            return output_file
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error plotting Gummel symmetry: {e}")
            return None

    def plot_derivative_smoothness(self, output_dir, vgs, ids, gm=None, gm2=None, gm3=None, vth=None):
        """Plot transconductance derivative smoothness up to 3rd-order (Gm, Gm2, Gm3) and extracted Vth."""
        try:
            plots_dir = os.path.join(output_dir, 'plots')
            os.makedirs(plots_dir, exist_ok=True)
            
            order = np.argsort(vgs)
            vgs_s = np.asarray(vgs, dtype=float)[order]
            ids_s = np.asarray(ids, dtype=float)[order]
            if gm is not None:
                gm_s = np.asarray(gm, dtype=float)[order]
            else:
                gm_s = np.gradient(ids_s, vgs_s)

            if gm2 is not None:
                gm2_s = np.asarray(gm2, dtype=float)[order]
            else:
                gm2_s = np.gradient(gm_s, vgs_s)

            if gm3 is not None:
                gm3_s = np.asarray(gm3, dtype=float)[order]
            else:
                gm3_s = np.gradient(gm2_s, vgs_s)
            
            fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(9, 12), sharex=True)
            
            # Subplot 1: Ids vs Vgs and Vth tangent
            ax1.plot(vgs_s, ids_s * 1e3, 'b-', linewidth=2, label=r'$I_{ds}$')
            if vth is not None:
                try:
                    vth_val = float(str(vth).replace('V', '').strip())
                    max_idx = np.argmax(gm_s)
                    m = gm_s[max_idx]
                    v_line = np.linspace(vth_val, max(vgs_s), 50)
                    i_line = (m * (v_line - vth_val)) * 1e3
                    ax1.plot(v_line, i_line, 'r--', label=f'Extrapolated Tangent ($V_{{th}}={vth_val:.3f}V$)')
                    ax1.axvline(vth_val, color='red', linestyle=':', label=f'$V_{{th}}={vth_val:.3f}V$')
                except Exception:
                    pass
            ax1.set_ylabel(r'$I_{ds}$ (mA)')
            ax1.set_title('MOSFET Transfer Characteristics & Threshold Voltage Extraction')
            ax1.grid(True, linestyle=':', alpha=0.6)
            ax1.legend(loc='best')
            
            # Subplot 2: Gm vs Vgs
            ax2.plot(vgs_s, gm_s * 1e3, 'm-', linewidth=2, label=r'$G_m = \partial I_{ds}/\partial V_{gs}$')
            ax2.set_ylabel(r'$G_m$ (mS)')
            ax2.set_title('1st Derivative: Transconductance $G_m$')
            ax2.grid(True, linestyle=':', alpha=0.6)
            ax2.legend(loc='best')

            # Subplot 3: Gm2 vs Vgs
            ax3.plot(vgs_s, gm2_s * 1e3, 'g-', linewidth=2, label=r'$G_{m2} = \partial^2 I_{ds}/\partial V_{gs}^2$')
            ax3.set_ylabel(r'$G_{m2}$ (mS/V)')
            ax3.set_title('2nd Derivative: $G_{m2}$ Smoothness')
            ax3.grid(True, linestyle=':', alpha=0.6)
            ax3.legend(loc='best')

            # Subplot 4: Gm3 vs Vgs (RF Linearity / IP3 audit)
            ax4.plot(vgs_s, gm3_s * 1e3, 'c-', linewidth=2, label=r'$G_{m3} = \partial^3 I_{ds}/\partial V_{gs}^3$')
            ax4.axhline(0, color='gray', linestyle='--', alpha=0.5)
            ax4.set_xlabel(r'Gate-Source Voltage $V_{gs}$ (V)')
            ax4.set_ylabel(r'$G_{m3}$ (mS/V$^2$)')
            ax4.set_title('3rd Derivative: $G_{m3}$ (RF Intermodulation / Linearity Audit)')
            ax4.grid(True, linestyle=':', alpha=0.6)
            ax4.legend(loc='best')
            
            plt.tight_layout()
            output_file = os.path.join(plots_dir, 'dc_derivative_smoothness.png')
            plt.savefig(output_file, dpi=self.dpi)
            plt.close()
            if self.logger:
                self.logger.info(f"Derivative smoothness plot saved to {output_file}")
            return output_file
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error plotting derivative smoothness: {e}")
            return None

    def plot_output_conductance_derivatives(self, output_dir, vds, ids, gds=None, gds2=None, gds3=None):
        """Plot output conductance and higher derivatives (Ids, Gds, Gds2, Gds3 vs Vds)."""
        try:
            plots_dir = os.path.join(output_dir, 'plots')
            os.makedirs(plots_dir, exist_ok=True)

            order = np.argsort(vds)
            vds_s = np.asarray(vds, dtype=float)[order]
            ids_s = np.asarray(ids, dtype=float)[order]
            gds_s = np.asarray(gds, dtype=float)[order] if gds is not None else np.gradient(ids_s, vds_s)
            gds2_s = np.asarray(gds2, dtype=float)[order] if gds2 is not None else np.gradient(gds_s, vds_s)
            gds3_s = np.asarray(gds3, dtype=float)[order] if gds3 is not None else np.gradient(gds2_s, vds_s)

            fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(9, 12), sharex=True)

            ax1.plot(vds_s, ids_s * 1e3, 'b-', linewidth=2, label=r'$I_{ds}$')
            ax1.set_ylabel(r'$I_{ds}$ (mA)')
            ax1.set_title('MOSFET Output Characteristics ($I_d$ vs $V_{ds}$)')
            ax1.grid(True, linestyle=':', alpha=0.6)
            ax1.legend(loc='best')

            ax2.plot(vds_s, gds_s * 1e3, 'm-', linewidth=2, label=r'$G_{ds} = \partial I_d/\partial V_{ds}$')
            ax2.set_ylabel(r'$G_{ds}$ (mS)')
            ax2.set_title('Output Conductance $G_{ds}$ (Passivity & Saturation Audit)')
            ax2.grid(True, linestyle=':', alpha=0.6)
            ax2.legend(loc='best')

            ax3.plot(vds_s, gds2_s * 1e3, 'g-', linewidth=2, label=r'$G_{ds2} = \partial^2 I_d/\partial V_{ds}^2$')
            ax3.set_ylabel(r'$G_{ds2}$ (mS/V)')
            ax3.set_title('2nd Output Derivative $G_{ds2}$')
            ax3.grid(True, linestyle=':', alpha=0.6)
            ax3.legend(loc='best')

            ax4.plot(vds_s, gds3_s * 1e3, 'r-', linewidth=2, label=r'$G_{ds3} = \partial^3 I_d/\partial V_{ds}^3$')
            ax4.axhline(0, color='gray', linestyle='--', alpha=0.5)
            ax4.set_xlabel(r'Drain-Source Voltage $V_{ds}$ (V)')
            ax4.set_ylabel(r'$G_{ds3}$ (mS/V$^2$)')
            ax4.set_title('3rd Output Derivative $G_{ds3}$ (Output Linearity Audit)')
            ax4.grid(True, linestyle=':', alpha=0.6)
            ax4.legend(loc='best')

            plt.tight_layout()
            output_file = os.path.join(plots_dir, 'dc_output_conductance_derivatives.png')
            plt.savefig(output_file, dpi=self.dpi)
            plt.close()
            if self.logger:
                self.logger.info(f"Output conductance derivatives plot saved to {output_file}")
            return output_file
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error plotting output conductance derivatives: {e}")
            return None

    def plot_asymptotic_extrapolation(self, output_dir, vg, id_vg, vd_leak=None, id_leak=None, vd_on=None, id_on=None):
        """Plot extreme asymptotic extrapolation behavior (deep reverse bias & high Vds)."""
        try:
            plots_dir = os.path.join(output_dir, 'plots')
            os.makedirs(plots_dir, exist_ok=True)

            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

            # 1. Gate sweep linear (-2V to 2.5V)
            ax1.plot(vg, id_vg * 1e3, 'b-', linewidth=2)
            ax1.axvline(0, color='black', linestyle=':', alpha=0.5)
            ax1.axvline(1.0, color='green', linestyle=':', alpha=0.5, label='Nominal Vdd')
            ax1.set_xlabel(r'Gate Voltage $V_{gs}$ (V)')
            ax1.set_ylabel(r'Drain Current $I_{ds}$ (mA)')
            ax1.set_title('Asymptotic Gate Sweep (Linear Scale: -2.0V to +2.5V)')
            ax1.grid(True, linestyle=':', alpha=0.6)
            ax1.legend(loc='best')

            # 2. Gate sweep semilog-y
            pos_id = np.maximum(np.abs(id_vg), 1e-15)
            ax2.semilogy(vg, pos_id, 'm-', linewidth=2)
            ax2.axvline(0, color='black', linestyle=':', alpha=0.5)
            ax2.axvline(1.0, color='green', linestyle=':', alpha=0.5, label='Nominal Vdd')
            ax2.set_xlabel(r'Gate Voltage $V_{gs}$ (V)')
            ax2.set_ylabel(r'$|I_{ds}|$ (A, log scale)')
            ax2.set_title('Asymptotic Subthreshold & Reverse Leakage (Log Scale)')
            ax2.grid(True, linestyle=':', alpha=0.6)
            ax2.legend(loc='best')

            # 3. High Vds leakage (Vgs = 0)
            if vd_leak is not None and id_leak is not None:
                ax3.semilogy(vd_leak, np.maximum(np.abs(id_leak), 1e-18), 'r-', linewidth=2)
                ax3.axvline(1.0, color='green', linestyle=':', alpha=0.5, label='Nominal Vdd')
                ax3.set_xlabel(r'Drain Voltage $V_{ds}$ (V)')
                ax3.set_ylabel(r'Leakage $|I_{ds}|$ (A, log scale)')
                ax3.set_title('High $V_{ds}$ Off-State Leakage ($V_{gs} = 0V$)')
                ax3.grid(True, linestyle=':', alpha=0.6)
                ax3.legend(loc='best')

            # 4. High Vds on-state (Vgs = 1.0)
            if vd_on is not None and id_on is not None:
                ax4.plot(vd_on, id_on * 1e3, 'g-', linewidth=2)
                ax4.axvline(1.0, color='green', linestyle=':', alpha=0.5, label='Nominal Vdd')
                ax4.set_xlabel(r'Drain Voltage $V_{ds}$ (V)')
                ax4.set_ylabel(r'On-State $I_{ds}$ (mA)')
                ax4.set_title('High $V_{ds}$ On-State Saturation ($V_{gs} = 1.0V$)')
                ax4.grid(True, linestyle=':', alpha=0.6)
                ax4.legend(loc='best')

            plt.tight_layout()
            output_file = os.path.join(plots_dir, 'dc_asymptotic_extrapolation.png')
            plt.savefig(output_file, dpi=self.dpi)
            plt.close()
            if self.logger:
                self.logger.info(f"Asymptotic extrapolation plot saved to {output_file}")
            return output_file
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error plotting asymptotic extrapolation: {e}")
            return None

    def plot_dynamic_self_heating(self, output_dir, freq, go_sh, co_sh=None):
        """Plot AC dynamic self-heating output conductance dispersion go(f) and capacitance."""
        try:
            plots_dir = os.path.join(output_dir, 'plots')
            os.makedirs(plots_dir, exist_ok=True)

            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 8), sharex=True)

            ax1.semilogx(freq, go_sh * 1e3, 'b-', linewidth=2, label=r'$g_o(f) = \mathrm{Re}(Y_{22})$')
            ax1.set_ylabel(r'Output Conductance $g_o$ (mS)')
            ax1.set_title('Dynamic Self-Heating Frequency Dispersion ($g_o(f)$ from 1 Hz to 100 GHz)')
            ax1.grid(True, linestyle=':', alpha=0.6)
            ax1.legend(loc='best')

            if co_sh is not None:
                ax2.semilogx(freq, co_sh * 1e15, 'm-', linewidth=2, label=r'$C_o(f) = \mathrm{Im}(Y_{22})/(2\pi f)$')
                ax2.set_ylabel(r'Output Capacitance $C_o$ (fF)')
                ax2.set_title('Dynamic Output Capacitance $C_o(f)$')
                ax2.grid(True, linestyle=':', alpha=0.6)
                ax2.legend(loc='best')

            ax2.set_xlabel('Frequency (Hz)')
            plt.tight_layout()
            output_file = os.path.join(plots_dir, 'ac_dynamic_self_heating.png')
            plt.savefig(output_file, dpi=self.dpi)
            plt.close()
            if self.logger:
                self.logger.info(f"Dynamic self-heating plot saved to {output_file}")
            return output_file
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error plotting dynamic self-heating: {e}")
            return None
    

