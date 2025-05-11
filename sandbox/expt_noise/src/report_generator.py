import os
import time
from datetime import datetime

class ReportGenerator:
    """
    Generator for Markdown reports based on noise analysis results
    """
    def __init__(self, logger):
        """
        Initialize the report generator
        
        Args:
            logger: Logger instance for logging messages
        """
        self.logger = logger
        self.logger.info("ReportGenerator initialized")
        
    def generate_report(self, analysis_results, output_path):
        """
        Generate a Markdown report from analysis results
        
        Args:
            analysis_results: Dictionary of analysis results
            output_path: Path to save the report
            
        Returns:
            bool: True if report was generated successfully, False otherwise
        """
        try:
            self.logger.info(f"Generating report at {output_path}")
            
            with open(output_path, 'w') as f:
                # Report header
                f.write("# SPICE Model Noise Analysis Report\n\n")
                f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # Table of Contents
                f.write("## Table of Contents\n\n")
                f.write("1. [Introduction](#introduction)\n")
                f.write("2. [Simulation Setup](#simulation-setup)\n")
                f.write("3. [Noise Characteristics](#noise-characteristics)\n")
                f.write("   - [Thermal Noise](#thermal-noise)\n")
                f.write("   - [Flicker (1/f) Noise](#flicker-noise)\n")
                f.write("   - [Shot Noise](#shot-noise)\n")
                f.write("4. [Frequency Analysis](#frequency-analysis)\n")
                f.write("5. [Temperature Dependence](#temperature-dependence)\n")
                f.write("6. [Geometry Dependence](#geometry-dependence)\n")
                f.write("7. [Conclusions](#conclusions)\n\n")
                
                # Introduction
                f.write("## Introduction\n\n")
                f.write("This report presents the results of noise analysis simulations performed on a 45nm NMOS transistor using the FreePDK45 model. ")
                f.write("The analysis covers various aspects of noise characterization including thermal noise, flicker noise, shot noise, ")
                f.write("and their dependence on frequency, temperature, and device geometry.\n\n")
                
                # Simulation Setup
                f.write("## Simulation Setup\n\n")
                f.write("The simulations were performed using ngspice with the following configuration:\n\n")
                f.write("- **Model:** FreePDK45 NMOS_VTG\n")
                f.write("- **Default Dimensions:** L=45nm, W=10µm\n")
                f.write("- **Bias Conditions:** Various VGS and VDS combinations\n")
                f.write("- **Temperature Range:** -40°C to 150°C\n")
                f.write("- **Frequency Range:** 0.1Hz to 10GHz\n\n")
                
                # Noise Characteristics
                f.write("## Noise Characteristics\n\n")
                
                # Thermal Noise
                f.write("### Thermal Noise\n\n")
                thermal_results = analysis_results.get("thermal_noise", {})
                if thermal_results.get("status") == "success":
                    results = thermal_results.get("results", {})
                    plots = thermal_results.get("plots", [])
                    
                    f.write("Thermal noise analysis was performed at multiple bias points to characterize the noise behavior in different operating regions.\n\n")
                    
                    # Add result details
                    if results:
                        f.write("#### Thermal Noise Results\n\n")
                        f.write("| Bias Condition | Max Noise (V²/Hz) | Min Noise (V²/Hz) | Avg Noise (V²/Hz) | Noise Floor (V²/Hz) |\n")
                        f.write("|----------------|-------------------|-------------------|-------------------|--------------------|\n")
                        
                        for bias, result in results.items():
                            if result.get("status") == "success":
                                max_noise = result.get("max_noise", "N/A")
                                min_noise = result.get("min_noise", "N/A")
                                avg_noise = result.get("avg_noise", "N/A")
                                noise_floor = result.get("noise_floor", "N/A")
                                
                                f.write(f"| {bias} | {max_noise:.2e} | {min_noise:.2e} | {avg_noise:.2e} | {noise_floor:.2e} |\n")
                        
                        f.write("\n")
                    
                    # Add plots
                    if plots:
                        f.write("#### Thermal Noise Plots\n\n")
                        
                        for i, plot in enumerate(plots):
                            if plot:
                                plot_basename = os.path.basename(plot)
                                rel_path = os.path.join("plots", plot_basename)
                                
                                f.write(f"![Thermal Noise Plot {i+1}]({rel_path})\n\n")
                                
                        f.write("\n")
                else:
                    f.write("*Thermal noise analysis failed or produced no results.*\n\n")
                
                # Flicker Noise
                f.write("### Flicker Noise\n\n")
                flicker_results = analysis_results.get("flicker_noise", {})
                if flicker_results.get("status") == "success":
                    results = flicker_results.get("results", {})
                    plots = flicker_results.get("plots", [])
                    
                    f.write("Flicker (1/f) noise analysis was performed to characterize the low-frequency noise behavior of the device.\n\n")
                    
                    # Add result details
                    if results:
                        f.write("#### Flicker Noise Results\n\n")
                        
                        k_avg = results.get("flicker_noise_coefficient", "N/A")
                        k_std = results.get("flicker_noise_coefficient_std", "N/A")
                        gamma = results.get("flicker_noise_exponent", "N/A")
                        corner = results.get("corner_frequency", "N/A")
                        
                        f.write(f"- **Flicker Noise Coefficient (K):** {k_avg:.2e} ± {k_std:.2e}\n")
                        f.write(f"- **Flicker Noise Exponent (γ):** {gamma:.4f} (ideally 1.0 for pure 1/f noise)\n")
                        
                        if corner is not None:
                            f.write(f"- **Estimated Corner Frequency:** {corner:.2e} Hz\n")
                            
                        f.write("\n")
                    
                    # Add plots
                    if plots:
                        f.write("#### Flicker Noise Plots\n\n")
                        
                        for i, plot in enumerate(plots):
                            if plot:
                                plot_basename = os.path.basename(plot)
                                rel_path = os.path.join("plots", plot_basename)
                                
                                f.write(f"![Flicker Noise Plot {i+1}]({rel_path})\n\n")
                                
                        f.write("\n")
                else:
                    f.write("*Flicker noise analysis failed or produced no results.*\n\n")
                
                # Shot Noise
                f.write("### Shot Noise\n\n")
                shot_results = analysis_results.get("shot_noise", {})
                if shot_results.get("status") == "success":
                    results = shot_results.get("results", {})
                    plots = shot_results.get("plots", [])
                    
                    f.write("Shot noise analysis was performed to characterize the random fluctuations due to discrete charge carriers.\n\n")
                    
                    # Add result details
                    if results:
                        f.write("#### Shot Noise Results\n\n")
                        
                        noise_level = results.get("shot_noise_level", "N/A")
                        noise_std = results.get("noise_std", "N/A")
                        variation = results.get("noise_variation", "N/A")
                        correlation = results.get("frequency_correlation", "N/A")
                        
                        f.write(f"- **Shot Noise Level:** {noise_level:.2e} V²/Hz\n")
                        f.write(f"- **Noise Standard Deviation:** {noise_std:.2e} V²/Hz\n")
                        f.write(f"- **Variation Coefficient:** {variation:.4f}\n")
                        f.write(f"- **Frequency Correlation:** {correlation:.4f} (ideally near zero for pure shot noise)\n\n")
                    
                    # Add plots
                    if plots:
                        f.write("#### Shot Noise Plots\n\n")
                        
                        for i, plot in enumerate(plots):
                            if plot:
                                plot_basename = os.path.basename(plot)
                                rel_path = os.path.join("plots", plot_basename)
                                
                                f.write(f"![Shot Noise Plot {i+1}]({rel_path})\n\n")
                                
                        f.write("\n")
                else:
                    f.write("*Shot noise analysis failed or produced no results.*\n\n")
                
                # Frequency Analysis
                f.write("## Frequency Analysis\n\n")
                freq_results = analysis_results.get("frequency_components", {})
                if freq_results.get("status") == "success":
                    results = freq_results.get("results", {})
                    plots = freq_results.get("plots", [])
                    
                    f.write("Frequency analysis was performed to examine how different noise components contribute to the total noise across frequencies.\n\n")
                    
                    # Add result details
                    if results:
                        crossover = results.get("crossover_frequency")
                        thermal_contrib = results.get("thermal_noise_contribution")
                        flicker_contrib = results.get("flicker_noise_contribution")
                        
                        if crossover is not None:
                            f.write(f"- **Crossover Frequency:** {crossover:.2e} Hz (where thermal noise equals flicker noise)\n")
                            
                        if thermal_contrib is not None and flicker_contrib is not None:
                            f.write(f"- **Thermal Noise Contribution:** {thermal_contrib:.2f}%\n")
                            f.write(f"- **Flicker Noise Contribution:** {flicker_contrib:.2f}%\n\n")
                    
                    # Add plots
                    if plots:
                        f.write("#### Frequency Analysis Plots\n\n")
                        
                        for i, plot in enumerate(plots):
                            if plot:
                                plot_basename = os.path.basename(plot)
                                rel_path = os.path.join("plots", plot_basename)
                                
                                f.write(f"![Frequency Analysis Plot {i+1}]({rel_path})\n\n")
                                
                        f.write("\n")
                else:
                    # Check if we have an error message or plots despite the error
                    error_message = freq_results.get("message", "Unknown error")
                    plots = freq_results.get("plots", [])
                    
                    f.write(f"*Frequency component analysis encountered an issue: {error_message}*\n\n")
                    f.write("Only the total noise spectrum could be analyzed without separate thermal and flicker noise components.\n\n")
                    
                    # Still add plots if available
                    if plots:
                        f.write("#### Available Frequency Analysis Plots\n\n")
                        
                        for i, plot in enumerate(plots):
                            if plot:
                                plot_basename = os.path.basename(plot)
                                rel_path = os.path.join("plots", plot_basename)
                                
                                f.write(f"![Frequency Analysis Plot {i+1}]({rel_path})\n\n")
                                
                        f.write("\n")
                
                # Temperature Dependence
                f.write("## Temperature Dependence\n\n")
                temp_results = analysis_results.get("temperature_dependence", {})
                if temp_results.get("status") == "success":
                    results = temp_results.get("results", {})
                    plots = temp_results.get("plots", [])
                    
                    f.write("Temperature dependence analysis was performed to study how noise characteristics vary with temperature.\n\n")
                    
                    # Add result details
                    if results:
                        temp_coeff = results.get("temperature_coefficient")
                        corr_coeff = results.get("correlation_coefficient")
                        
                        if temp_coeff is not None:
                            f.write(f"- **Temperature Coefficient:** {temp_coeff:.2e} V²/Hz/°C\n")
                            
                        if corr_coeff is not None:
                            f.write(f"- **Temperature-Noise Correlation:** {corr_coeff:.4f}\n\n")
                    
                    # Add plots
                    if plots:
                        f.write("#### Temperature Dependence Plots\n\n")
                        
                        for i, plot in enumerate(plots):
                            if plot:
                                plot_basename = os.path.basename(plot)
                                rel_path = os.path.join("plots", plot_basename)
                                
                                f.write(f"![Temperature Dependence Plot {i+1}]({rel_path})\n\n")
                                
                        f.write("\n")
                else:
                    f.write("*Temperature dependence analysis failed or produced no results.*\n\n")
                
                # Geometry Dependence
                self._add_geometry_dependence_section(f, analysis_results)
                
                # Conclusions
                f.write("## Conclusions\n\n")
                
                f.write("Based on the noise analysis results, the following conclusions can be drawn:\n\n")
                
                # Build conclusions based on available results
                conclusions = []
                
                # Check thermal noise results
                thermal_results = analysis_results.get("thermal_noise", {})
                if thermal_results.get("status") == "success" and thermal_results.get("results"):
                    conclusions.append("- Thermal noise characteristics were successfully analyzed at multiple bias points, "
                                     "showing expected behavior with frequency and bias conditions.")
                
                # Check flicker noise results
                flicker_results = analysis_results.get("flicker_noise", {})
                if flicker_results.get("status") == "success" and flicker_results.get("results"):
                    results = flicker_results.get("results", {})
                    gamma = results.get("flicker_noise_exponent")
                    
                    if gamma is not None:
                        if abs(gamma - 1.0) < 0.2:
                            conclusions.append(f"- Flicker noise shows a close-to-ideal 1/f behavior with an exponent of {gamma:.2f}, "
                                              "indicating good model quality for low-frequency noise.")
                        else:
                            conclusions.append(f"- Flicker noise shows a non-ideal 1/f^{gamma:.2f} behavior, "
                                              "which deviates from the theoretical 1/f characteristic.")
                
                # Check temperature dependence
                temp_results = analysis_results.get("temperature_dependence", {})
                if temp_results.get("status") == "success" and temp_results.get("results"):
                    results = temp_results.get("results", {})
                    temp_coeff = results.get("temperature_coefficient")
                    
                    if temp_coeff is not None:
                        if temp_coeff > 0:
                            conclusions.append(f"- Noise increases with temperature (coefficient: {temp_coeff:.2e} V²/Hz/°C), "
                                              "which is consistent with thermally activated noise mechanisms.")
                        else:
                            conclusions.append(f"- Noise decreases with temperature (coefficient: {temp_coeff:.2e} V²/Hz/°C), "
                                              "which is unusual and may indicate model limitations.")
                
                # Check geometry dependence
                geom_results = analysis_results.get("geometry_dependence", {})
                if geom_results.get("status") == "success" and geom_results.get("results"):
                    results = geom_results.get("results", {})
                    
                    length_results = results.get("length_dependence", {})
                    width_results = results.get("width_dependence", {})
                    
                    if length_results and "scaling_factor" in length_results:
                        l_factor = length_results["scaling_factor"]
                        if abs(l_factor + 1.0) < 0.3:
                            conclusions.append(f"- Noise scales approximately as 1/L (scaling factor: {l_factor:.2f}), "
                                              "which is consistent with theoretical expectations for flicker noise.")
                        else:
                            conclusions.append(f"- Noise scaling with length (factor: {l_factor:.2f}) deviates from "
                                              "the theoretical 1/L relationship.")
                    
                    if width_results and "scaling_factor" in width_results:
                        w_factor = width_results["scaling_factor"]
                        if abs(w_factor + 1.0) < 0.3:
                            conclusions.append(f"- Noise scales approximately as 1/W (scaling factor: {w_factor:.2f}), "
                                              "which is consistent with theoretical expectations for flicker noise.")
                        else:
                            conclusions.append(f"- Noise scaling with width (factor: {w_factor:.2f}) deviates from "
                                              "the theoretical 1/W relationship.")
                
                # Add conclusions to report
                for conclusion in conclusions:
                    f.write(f"{conclusion}\n\n")
                
                # Add a general conclusion if specific points are lacking
                if not conclusions:
                    f.write("- The noise analysis provides valuable insights into the behavior of the FreePDK45 NMOS transistor model.\n\n")
                    f.write("- Further investigations may be needed to establish more comprehensive noise characterization across all operating conditions.\n\n")
                
                f.write("---\n\n")
                f.write(f"Report generated on {datetime.now().strftime('%Y-%m-%d')} using ngspice and the FreePDK45 model.\n")
            
            self.logger.info(f"Report generated successfully at {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            return False

    def _add_geometry_dependence_section(self, f, analysis_results):
        """
        Add geometry dependence section to the report
        
        Args:
            f: File handle for the report
            analysis_results: Analysis results dictionary
        """
        f.write("## Geometry Dependence\n\n")
        
        geom_results = analysis_results.get("geometry_dependence", {})
        results = geom_results.get("results", {})
        plots = geom_results.get("plots", [])
        errors = geom_results.get("errors", [])
        
        f.write("Geometry dependence analysis was performed to study how noise characteristics vary with device dimensions.\n\n")
        
        if errors:
            f.write("**Note: The following errors were encountered during geometry dependence analysis:**\n\n")
            for error in errors:
                f.write(f"- ⚠️ {error}\n")
            f.write("\n")
        
        # Channel Length Dependence
        f.write("### Channel Length Dependence\n\n")
        
        length_results = results.get("length_dependence", {})
        length_status = length_results.get("status", "error")
        
        if length_status == "success":
            length_factor = length_results.get("scaling_factor", "N/A")
            
            f.write(f"- **Length Scaling Factor:** {length_factor:.2f} (noise ∝ L^{length_factor:.2f})\n")
            f.write(f"- **Theoretical Expectation:** -1.0 for flicker noise (noise ∝ 1/L)\n\n")
        else:
            error_message = length_results.get("message", "Unknown error")
            f.write(f"- **Analysis Status:** Failed\n")
            f.write(f"- **Error:** {error_message}\n")
            
            # If we have data, show the variation
            if "noise_variation" in length_results:
                variation = length_results.get("noise_variation", 0)
                f.write(f"- **Data Variation:** {variation:.6f} (should be significantly > 1e-6)\n\n")
            else:
                f.write("\n")
        
        # Channel Width Dependence
        f.write("### Channel Width Dependence\n\n")
        
        width_results = results.get("width_dependence", {})
        width_status = width_results.get("status", "error")
        
        if width_status == "success":
            width_factor = width_results.get("scaling_factor", "N/A")
            
            f.write(f"- **Width Scaling Factor:** {width_factor:.2f} (noise ∝ W^{width_factor:.2f})\n")
            f.write(f"- **Theoretical Expectation:** -1.0 for flicker noise (noise ∝ 1/W)\n\n")
        else:
            error_message = width_results.get("message", "Unknown error")
            f.write(f"- **Analysis Status:** Failed\n")
            f.write(f"- **Error:** {error_message}\n")
            
            # If we have data, show the variation
            if "noise_variation" in width_results:
                variation = width_results.get("noise_variation", 0)
                f.write(f"- **Data Variation:** {variation:.6f} (should be significantly > 1e-6)\n\n")
            else:
                f.write("\n")
        
        # Add plots if available
        if plots:
            f.write("#### Geometry Dependence Plots\n\n")
            
            for i, plot_path in enumerate(plots, 1):
                rel_path = os.path.relpath(plot_path, os.path.dirname(os.path.dirname(self.output_dir)))
                f.write(f"![Geometry Dependence Plot {i}]({rel_path})\n\n") 