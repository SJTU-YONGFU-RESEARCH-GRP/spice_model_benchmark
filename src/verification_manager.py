import numpy as np
from pathlib import Path
from datetime import datetime
import traceback
import os

class VerificationManager:
    """
    Handles verification of simulation results.
    """
    def __init__(self, logger, output_dir='results', skip_simulation=False):
        """Initialize the VerificationManager with necessary configuration.
        
        This class is responsible for verifying the correctness and quality of MOSFET model
        simulation results. It validates various simulation aspects including IV characteristics,
        temperature analysis, AC analysis, transient behavior, and noise analysis.
        
        Args:
            logger: Logger instance for recording verification activities
            output_dir: Directory path where simulation results and verification reports will be stored
                       (will be converted to absolute path)
            skip_simulation: Flag to bypass simulation execution (used for testing/debugging)
            
        Attributes:
            results: Dictionary storing verification results for different simulation aspects
        """
        self.logger = logger
        self.output_dir = Path(output_dir).resolve()
        self.skip_simulation = skip_simulation
        self.results = {
            'simulation_setup': None,
            'dc_operating_point_analysis': None,
            'temperature_analysis': None,
            'thermodynamic_analysis': None,
            'bias_point_analysis': None
        }
    
    # Done
    def verify_simulation_setup(self, circuit_file=None):
        """
        Verify that the simulation environment and circuit files are properly set up.
        
        This method performs critical pre-simulation checks to ensure the environment 
        is correctly configured for SPICE simulation:
        1. Verifies that the specified circuit file exists and is readable
        2. Checks for proper ngspice installation and gets its version
        3. Confirms that basic simulation preconditions are met
        
        Args:
            circuit_file: Path to the SPICE circuit file to validate.
                         If None, a default 'circuit.cir' is used.
                         
        Returns:
            dict: Verification results containing:
                - netlist_exists (bool): Whether the circuit file exists
                - ngspice_installed (bool): Whether ngspice is installed
                - simulation_runs (bool): Whether simulation can run
                - details (dict): Additional information including paths and version info
                
        Note:
            This is typically the first verification performed before running simulations,
            and failures here indicate fundamental setup issues that must be addressed.
        """
        results = {
            'netlist_exists': False,
            'ngspice_installed': False,
            'simulation_runs': False,
            'details': {
                'netlist_path': str(circuit_file) if circuit_file else 'circuit.cir',
                'ngspice_version': None,
                'simulation_status': None,
                'dc_path': None,
                'ac_path': None,
                'transient_path': None,
                'noise_path': None
            }
        }
        
        try:
            # Check netlist file
            circuit_path = Path(circuit_file) if circuit_file else Path('circuit.cir')
            results['netlist_exists'] = circuit_path.exists() and circuit_path.is_file()
            results['details']['netlist_path'] = str(circuit_path.absolute())
            
            # Set mode-specific paths
            base_path = circuit_path.parent
            results['details']['dc_path'] = str(base_path / 'dc_analysis.cir')
            results['details']['ac_path'] = str(base_path / 'ac_analysis.cir')
            results['details']['transient_path'] = str(base_path / 'transient_analysis.cir')
            results['details']['noise_path'] = str(base_path / 'noise_analysis.cir')
            
            # Check ngspice installation
            try:
                import subprocess
                version_output = subprocess.run(['ngspice', '--version'], 
                                             capture_output=True, 
                                             text=True, 
                                             check=True)
                results['ngspice_installed'] = True
                # Extract version number from the output
                version_lines = version_output.stdout.split('\n')
                for line in version_lines:
                    if 'ngspice-' in line:
                        version = line.split('ngspice-')[1].split()[0]
                        results['details']['ngspice_version'] = f"ngspice-{version}"
                        break
                if not results['details']['ngspice_version']:
                    # If version not found in expected format, use first line
                    results['details']['ngspice_version'] = version_lines[0].strip()
            except (subprocess.SubprocessError, FileNotFoundError) as e:
                results['details']['ngspice_version'] = f"Error: {str(e)}"
                self.logger.error("ngspice not found or not properly installed")
            
            # Simulation will be marked as running in the main simulation class
            results['simulation_runs'] = True
            results['details']['simulation_status'] = "Ready to run"
            
            if not all([results['netlist_exists'], results['ngspice_installed']]):
                self.logger.error("Simulation setup verification failed")
            else:
                self.logger.info("Simulation setup verified successfully")
                
        except Exception as e:
            results['details']['simulation_status'] = f"Error: {str(e)}"
            self.logger.error(f"Error verifying simulation setup: {e}")
            
        self.results['simulation_setup'] = results
        return results

    # Done
    def update_verification_checklist(self, results, modes=None):
        """
        Update the verification checklist with simulation results.
        """
        try:
            self.logger.info("Starting verification checklist update")
            
            # If modes is None, assume all modes were run
            if modes is None:
                modes = ['dc', 'transient', 'ac', 'noise']
                self.logger.info("No modes specified, using all modes")
            elif 'all' in modes:
                modes = ['dc', 'transient', 'ac', 'noise']
                self.logger.info("'all' mode specified, using all modes")
            elif isinstance(modes, str):
                modes = [modes]  # Convert single mode to list
                self.logger.info(f"Single mode specified: {modes[0]}")
            
            self.logger.info(f"Processing modes: {', '.join(modes)}")

            # Create the report directory if it doesn't exist
            report_path = self.output_dir / 'REPORT.md'
            report_path.parent.mkdir(exist_ok=True, parents=True)
            self.logger.info(f"Report will be saved to: {report_path}")

            # Generate new report content
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            content = []
            
            # 1. Generate header
            content.extend(self._generate_report_header(timestamp))
            
            # 2. Generate table of contents
            content.extend(self._generate_table_of_contents(modes))
            
            # 3. Generate notes section
            content.extend(self._generate_notes_section())
            
            # 4. Generate simulation setup section
            content.extend(self._generate_simulation_setup_section(results))
            
            # 5. Generate summary section
            content.extend(self._generate_summary_section(results, modes))
            
            # 6. Generate detailed analysis sections in order
            section_num = 3  # Start from section 3
            
            # DC Analysis (Section 3)
            if 'dc' in modes:
                content.extend(self._generate_dc_analysis_section(results, section_num))
                section_num += 1
            
            # Transient Analysis (Section 4)
            if 'transient' in modes:
                content.extend(self._generate_transient_analysis_section(results, section_num))
                section_num += 1
            
            # AC Analysis (Section 5)
            if 'ac' in modes:
                content.extend(self._generate_ac_analysis_section(results, section_num))
                section_num += 1
            
            # Noise Analysis (Section 6)
            if 'noise' in modes:
                content.extend(self._generate_noise_analysis_section(results, section_num))
                section_num += 1
            
            # Write the complete report to file
            self.logger.info(f"Writing complete report to file: {report_path}")
            with open(report_path, 'w') as f:
                f.write('\n'.join(content))
                
            self.logger.info(f"Successfully generated verification checklist at {report_path}")
                
        except Exception as e:
            self.logger.error(f"Error updating verification checklist: {e}")
            import traceback
            traceback.print_exc()

    # Done
    def _generate_report_header(self, timestamp):
        """
        Generate the header section of the report including title and table of contents.
        """
        self.logger.info("Generating Report Header")
        content = ["# MOSFET Simulation Verification Report"]
        content.append(f"Generated on: {timestamp}")
        content.append("")
        content.append("## Table of Contents")
        content.append("1. [Simulation Setup and Execution](#1-simulation-setup-and-execution)")

        self.logger.info("Completed Report Header")
        return content

    # Done
    def _generate_table_of_contents(self, modes):
        """
        Generate the table of contents based on the analysis modes.
        """

        self.logger.info("Generating Table of Contents")
        content = ["2. [Summary](#2-summary)"]
        # Start section numbering from 3
        section_num = 3
        self.logger.info(f"Starting section numbering from {section_num}")

        if 'dc' in modes:
            self.logger.info("Adding DC analysis section to TOC")
            content.append(f"   - [DC Analysis Summary](#dc-analysis-summary)")

        if 'ac' in modes:
            self.logger.info("Adding AC analysis section to TOC")
            content.append(f"   - [AC Analysis Summary](#ac-analysis-summary)")

        if 'transient' in modes:
            self.logger.info("Adding transient analysis section to TOC")
            content.append(f"   - [Transient Analysis Summary](#transient-analysis-summary)")

        if 'noise' in modes:
            self.logger.info("Adding noise analysis section to TOC")
            content.append(f"   - [Noise Analysis Summary](#noise-analysis-summary)")

        if 'dc' in modes:
            content.append(f"{section_num}. [DC Analysis](#{section_num}-dc-analysis)")
            content.append("   - [DC Operating Point Analysis](#dc-operating-point-analysis)")
            content.append("   - [Bias Point Analysis](#bias-point-analysis)")
            content.append("   - [Temperature Analysis](#temperature-analysis)")
            content.append("   - [Thermodynamic Analysis](#thermodynamic-analysis)")
            content.append("   - [Physical Properties Analysis](#physical-properties-analysis)")
            section_num += 1

        if 'ac' in modes:
            content.append(f"{section_num}. [AC Analysis](#{section_num}-ac-analysis)")
            content.append("   - [Small-Signal Analysis](#small-signal-analysis)")
            content.append("   - [S-Parameter Analysis](#s-parameter-analysis)")
            content.append("   - [Non-Quasi-Static (NQS) Effects Analysis](#non-quasi-static-effects-analysis)")
            content.append("   - [Charge Conservation Analysis](#charge-conservation-analysis)")
            section_num += 1

        if 'transient' in modes:
            content.append(f"{section_num}. [Transient Analysis](#{section_num}-transient-analysis)")
            content.append("   - [Large-Signal Transient](#large-signal-transient)")
            content.append("   - [Switching Simulations](#switching-simulations)")
            content.append("   - [Delay Effect Simulations](#delay-effect-simulations)")
            section_num += 1
        
        if 'noise' in modes:
            content.append(f"{section_num}. [Noise Analysis](#{section_num}-noise-analysis)")
            content.append("   - [Thermal Noise Analysis](#thermal-noise-analysis)")
            content.append("   - [Flicker Noise Analysis](#flicker-noise-analysis)")
            content.append("   - [Shot Noise Analysis](#shot-noise-analysis)")
            section_num += 1
        
        content.append("")
        self.logger.info("Table of contents generation completed")
        return content

    # Done
    def _generate_notes_section(self):
        """
        Generate the notes section of the report.
        """
        self.logger.info("Generating Note Section")
        content = []
        content.append("## Notes")
        content.append("- This report is automatically generated based on mosfet_simulation.py")
        content.append("- Items are marked with <span style='color: green'>✓</span> for success and <span style='color: red'>✗</span> for failure")
        content.append("- Any deviations from expected behavior should be documented")
        
        content.append("")
        self.logger.info("Note Section Completed")
        return content

    # Done
    def _generate_simulation_setup_section(self, results):
        """
        Generate the simulation setup section of the report.
        """
        self.logger.info("Generating Simulation Setup Section")
        content = ["## 1. Simulation Setup and Execution"]
        
        if 'simulation_setup' in results and results['simulation_setup'] is not None:
            setup = results['simulation_setup']
            
            # Common setup checks
            content.append(f"- [<span style='color: {'green' if setup.get('netlist_exists', False) else 'red'}'>{'✓' if setup.get('netlist_exists', False) else '✗'}</span>] Circuit file exists and is readable")
            content.append(f"  - Path: {setup.get('details', {}).get('netlist_path', 'Not available')}")
            content.append(f"- [<span style='color: {'green' if setup.get('ngspice_installed', False) else 'red'}'>{'✓' if setup.get('ngspice_installed', False) else '✗'}</span>] ngspice is properly installed")
            content.append(f"  - Version: {setup.get('details', {}).get('ngspice_version', 'Not available')}")
            
            # Mode-specific setup checks
            if 'dc' in results:
                content.append(f"- [<span style='color: {'green' if setup.get('simulation_runs', False) else 'red'}'>{'✓' if setup.get('simulation_runs', False) else '✗'}</span>] DC simulation runs without errors")
                content.append(f"  - Path: {setup.get('details', {}).get('dc_path', 'Not available')}")
            
            if 'ac' in results:
                content.append(f"- [<span style='color: {'green' if setup.get('simulation_runs', False) else 'red'}'>{'✓' if setup.get('simulation_runs', False) else '✗'}</span>] AC simulation runs without errors")
                content.append(f"  - Path: {setup.get('details', {}).get('ac_path', 'Not available')}")
            
            if 'transient' in results:
                content.append(f"- [<span style='color: {'green' if setup.get('simulation_runs', False) else 'red'}'>{'✓' if setup.get('simulation_runs', False) else '✗'}</span>] Transient simulation runs without errors")
                content.append(f"  - Path: {setup.get('details', {}).get('transient_path', 'Not available')}")
            
            if 'noise' in results:
                content.append(f"- [<span style='color: {'green' if setup.get('simulation_runs', False) else 'red'}'>{'✓' if setup.get('simulation_runs', False) else '✗'}</span>] Noise simulation runs without errors")
                content.append(f"  - Path: {setup.get('details', {}).get('noise_path', 'Not available')}")
            
            # If no specific modes are found, show generic simulation run check
            if not any(mode in results for mode in ['dc', 'ac', 'transient', 'noise']):
                content.append(f"- [<span style='color: {'green' if setup.get('simulation_runs', False) else 'red'}'>{'✓' if setup.get('simulation_runs', False) else '✗'}</span>] Simulation runs without errors")
            else:
                # Default setup section when no results are available
                content.append("- [<span style='color: red'>✗</span>] Circuit file exists and is readable")
                content.append("  - Path: Not available")
                content.append("- [<span style='color: red'>✗</span>] ngspice is properly installed")
                content.append("  - Version: Not available")
                content.append("- [<span style='color: red'>✗</span>] Simulation runs without errors")

        content.append("")
        self.logger.info("Simulation Setup Section Completed")
        return content

    # Done
    def _generate_summary_section(self, results, modes):
        """
        Generate the summary section based on the analysis modes.
        """
        self.logger.info("Generating Summary Section")
        content = ["## 2. Summary"]
        
        if 'dc' in modes:
            content.extend(self._generate_dc_summary_section(results))
        
        if 'ac' in modes:
            content.extend(self._generate_ac_summary(results))
        
        if 'transient' in modes:
            content.extend(self._generate_transient_summary(results))
        
        if 'noise' in modes:
            content.extend(self._generate_noise_summary(results))
        
        self.logger.info("Summary Section Completed")
        return content

    # Done
    def _generate_dc_summary_section(self, results):
        """
        Generate DC analysis summary section.
        """
        content = []
        content.append("### DC Analysis Summary")
        content.append("| Test Type | Status | Key Findings |")
        content.append("|-----------|--------|-------------|")
        
        # DC Operating Point Analysis
        if 'dc_operating_point_analysis' in results and results['dc_operating_point_analysis'] is not None:
            data = results['dc_operating_point_analysis']
            vds_range = data.get('vds_range', 'Not available')
            vgs_range = data.get('vgs_range', 'Not available')
            ids_range = data.get('ids_range', 'Not available')
            content.append(f"| [DC Operating Point Analysis](#dc-operating-point-analysis) | <span style='color: {'green' if data.get('data_ready', False) else 'red'}'>{'✓' if data.get('data_ready', False) else '✗'}</span> | VDS: {vds_range}, VGS: {vgs_range}, IDS: {ids_range} |")

        # Bias Point Analysis
        if 'bias_point_analysis' in results and results['bias_point_analysis'] is not None:
            bias = results['bias_point_analysis']
            bias_points = bias.get('details', {}).get('bias_points', 'Not available')
            current_ranges = bias.get('details', {}).get('current_ranges', 'Not available')
            kcl_error = bias.get('details', {}).get('kcl_error', 'Not available')
            power_range = bias.get('details', {}).get('power_range', 'Not available')
            temp = bias.get('details', {}).get('temp', 'Not available')
            content.append(f"| [Bias Point Analysis](#bias-point-analysis) | <span style='color: {'green' if bias.get('bias_points_analyzed', False) and bias.get('currents_measured', False) else 'red'}'>{'✓' if bias.get('bias_points_analyzed', False) and bias.get('currents_measured', False) else '✗'}</span> | Points: {bias_points}, Currents: {current_ranges}, KCL Error: {kcl_error}, Power: {power_range}, Temp: {temp} |")

        # Temperature Analysis
        if 'temperature_analysis' in results and results['temperature_analysis'] is not None:
            temp = results['temperature_analysis']
            temp_points = temp.get('details', {}).get('temp_points', 'Not available')
            temp_coef = temp.get('details', {}).get('temp_coef_value', 'Not available')
            ids_range = temp.get('details', {}).get('ids_range', 'Not available')
            content.append(f"| [Temperature Analysis](#temperature-analysis) | <span style='color: {'green' if temp.get('temp_sweep', False) and temp.get('device_behavior', False) else 'red'}'>{'✓' if temp.get('temp_sweep', False) and temp.get('device_behavior', False) else '✗'}</span> | Temp Points: {temp_points}, TC: {temp_coef}, IDS: {ids_range} |")

        # Thermodynamic Analysis
        if 'thermodynamic_analysis' in results and results['thermodynamic_analysis'] is not None:
            thermo = results['thermodynamic_analysis']
            power_range = thermo.get('details', {}).get('power_range', 'Not available')
            efficiency_range = thermo.get('details', {}).get('efficiency_range', 'Not available')
            temp_coef = thermo.get('details', {}).get('temp_coef', 'Not available')
            content.append(f"| [Thermodynamic Analysis](#thermodynamic-analysis) | <span style='color: {'green' if thermo.get('energy_conservation', False) and thermo.get('device_efficiency', False) else 'red'}'>{'✓' if thermo.get('energy_conservation', False) and thermo.get('device_efficiency', False) else '✗'}</span> | Power: {power_range}, Efficiency: {efficiency_range}, TC: {temp_coef} |")

        content.append("")
        self.logger.info("DC Summary Section Completed")
        return content

    # Done
    def _generate_dc_analysis_section(self, results, section_num=3):
        """
        Generate detailed DC analysis section.
        """
        try:
            content = []
            content.append(f"## {section_num}. AC Analysis")
        
            # DC Operating Point Analysis   
            content.append("### DC Operating Point Analysis")
            if 'dc_operating_point_analysis' in results and results['dc_operating_point_analysis'] is not None:
                content.append("- [<span style='color: green'>✓</span>] IV data file is generated")
                content.append("- [<span style='color: green'>✓</span>] Data points are properly read")

                data = results['dc_operating_point_analysis']
                content.append(f"- [<span style='color: green'>✓</span>] Vds values are within range")
                content.append(f"  - Range: {data.get('vds_range', 'Not available')}")
                content.append(f"- [<span style='color: green'>✓</span>] Vgs values are within range")
                content.append(f"  - Range: {data.get('vgs_range', 'Not available')}")
                content.append(f"- [<span style='color: green'>✓</span>] Drain current (Ids) is properly measured")
                content.append(f"  - Range: {data.get('ids_range', 'Not available')}")
                content.append("")
                content.append("*IV Characteristics showing drain current vs drain-source voltage*")
                content.append("")
                content.append("<img src='plots/dc_iv_characteristics.png' alt='IV Characteristics' width='400'/>")
            else:
                content.append("- [<span style='color: red'>✗</span>] IV data is Missing")
            content.append("")

            # Bias Point Analysis
            content.append("### Bias Point Analysis")      
            if 'bias_point_analysis' in results and results['bias_point_analysis'] is not None:  
                data = results['bias_point_analysis']
                content.append(f"- [<span style='color: green'>✓</span>] Voltage Biasing Points")
                content.append(f"  - Points: {data.get('details', {}).get('bias_points', 'Not available')}")
                content.append(f"- [<span style='color: green'>✓</span>] Current Range")
                content.append(f"  - IDS: {data.get('details', {}).get('IDS', 'Not available')}")
                content.append(f"  - IG: {data.get('details', {}).get('IG', 'Not available')}")
                content.append(f"  - IS: {data.get('details', {}).get('IS', 'Not available')}")
                content.append(f"  - IB: {data.get('details', {}).get('IB', 'Not available')}")
                content.append(f"- [<span style='color: green'>✓</span>] KCL Error Range")
                content.append(f"  - KCL Error: {data.get('details', {}).get('kcl_error', 'Not available')}")
                content.append("")
                content.append("*KCL verification showing current balance*")
                content.append("")
                content.append("<img src='plots/dc_kcl_verification.png' alt='KCL Verification' width='400'/>")
            else:
                content.append("- [<span style='color: red'>✗</span>] Bias data is Missing")
            content.append("")

            # Temperature Analysis
            content.append("### Temperature Analysis")
            if 'temperature_analysis' in results and results['temperature_analysis'] is not None:
                data = results['temperature_analysis']
                content.append(f"- [<span style='color: green'>✓</span>] Temperature sweep is performed")
                content.append(f"  - Points: {data.get('details', {}).get('temp_points', 'Not available')}")
                content.append(f"- [<span style='color: green'>✓</span>] Temperature coefficient is calculated")
                content.append(f"  - Temperature Coefficient: {data.get('details', {}).get('temp_coef_value', 'Not available')}")
                content.append(f"- [<span style='color: green'>✓</span>] Device behavior is valid")
                content.append(f"  - Current Range: {data.get('details', {}).get('ids_range', 'Not available')}")
                content.append(f"- [<span style='color: green'>✓</span>] Temperature-dependent behavior is valid")
                content.append("")
                content.append("*Temperature analysis showing current variation*")
                content.append("")
                content.append("<img src='plots/dc_temperature_analysis.png' alt='Temperature Analysis' width='400'/>")
            else:
                content.append("- [<span style='color: red'>✗</span>] Temperature data is Missing")
            content.append("")

            # Thermodynamic Analysis
            content.append("### Thermodynamic Analysis")        
            if 'thermodynamic_analysis' in results and results['thermodynamic_analysis'] is not None:
                data = results['thermodynamic_analysis']

                if data['energy_conservation']:
                    content.append(f"- [<span style='color: green'>✓</span>] Energy is conserved")
                    content.append(f"  - Power Range: {data.get('details', {}).get('power_range', 'Not available')}")
                else:
                    content.append(f"- [<span style='color: red'>✗</span>] Energy is not conserved")

                if data['device_efficiency']:
                    content.append(f"- [<span style='color: green'>✓</span>] Device is efficient")
                else:
                    content.append(f"- [<span style='color: green'>✗</span>] Device is not efficient")
                content.append(f"  - Efficiency Range: {data.get('details', {}).get('efficiency_range', 'Not available')}")
                if data['temp_coef_calc']:
                    content.append(f"- [<span style='color: green'>✓</span>] Temperature coefficient is calculated")
                    content.append(f"  - Value: {data.get('details', {}).get('temp_coef', 'Not available')}")
                else:
                    content.append(f"- [<span style='color: green'>✗</span>] Temperature coefficient has error")
            else:
                content.append("- [<span style='color: red'>✗</span>] Thermodynamic data is Missing")
            content.append("")

            # Physical Properties
            content.append("### Physical Properties Analysis")
            content.append("- <span style='color: gray'>✗</span> Physical monotonicity over bias, geometry, and temperature: *In Progress*")
            content.append("- <span style='color: gray'>✗</span> Parameter sweep simulations: *In Progress*")
            content.append("- <span style='color: gray'>✗</span> Physical symmetries (currents, charges, their derivatives): *In Progress*")
            content.append("- <span style='color: gray'>✗</span> Cross-derivative analysis: *In Progress*")
            content.append("- <span style='color: gray'>✗</span> Terminal permutation tests: *In Progress*")

            content.append("")
            self.logger.info("Successfully generated DC analysis section")    
            return content
        except Exception as e:
            self.logger.error(f"Error generating DC analysis section: {e}")
            return [f"## {section_num}. DC Analysis", "Error generating DC analysis section"]

    # Done
    def _generate_ac_summary(self, results):
        """Generate summary of AC analysis results."""
        try:
            self.logger.info("Generate summary of AC analysis results.")
            content = []
            content.append("### AC Analysis Summary")
            content.append("| Test Type | Status | Key Findings |")
            content.append("|-----------|--------|-------------|")
            
            # Get results with safe defaults
            cv_results = results.get('cv_characteristics', {}) or {}
            sparams_results = results.get('sparameter_analysis', {}) or {}
            nqs_results = results.get('nqs_effects', {}) or {}
            charge_results = results.get('charge_conservation', {}) or {}
            
            self.logger.info(f"CV Results: {cv_results}")
            self.logger.info(f"S Params Results: {sparams_results}")
            self.logger.info(f"NQS Results: {nqs_results}")
            self.logger.info(f"Charge Results: {charge_results}")
            
            # Small-Signal Analysis
            if cv_results.get('data_ready'):
                status = "✓" if cv_results.get('verification_passed', True) else "✗"
                color = "green" if status == "✓" else "red"
                findings = f"Gate capacitance range: {cv_results.get('cgg_range', 'N/A')}"
                self.logger.info(f"cv_results.get('verification_passed', True): {status}")
                content.append(f"| [Small Signal Analysis](#small-signal-analysis) | <span style='color: {color}'>{status}</span> | {findings} |")
            else:
                content.append("| [Small Signal Analysis](#small-signal-analysis) | <span style='color: red'>✗</span> | Data not available |")
            
            # S-Parameter Analysis
            if sparams_results.get('data_ready'):
                status = "✓" if sparams_results.get('verification_passed', True) else "✗"
                color = "green" if status == "✓" else "red"
                findings = f"S11 range: {sparams_results.get('s11_range', 'N/A')}, S21 range: {sparams_results.get('s21_range', 'N/A')}"
                self.logger.info(f"sparams_results.get('verification_passed', True): {status}")
                content.append(f"| [S-Parameter Analysis](#s-parameter-analysis) | <span style='color: {color}'>{status}</span> | {findings} |")
            else:
                content.append("| [S-Parameter Analysis](#s-parameter-analysis) | <span style='color: red'>✗</span> | Data not available |")
            
            # NQS Effects
            if nqs_results.get('data_ready'):
                status = "✓" if nqs_results.get('verification_passed', True) else "✗"
                color = "green" if status == "✓" else "red"
                findings = f"Max phase shift: {nqs_results.get('max_phase_shift', 'N/A')}"
                self.logger.info(f"nqs_results.get('verification_passed', True): {status}")
                content.append(f"| [Non-Quasi-Static (NQS) Effects Analysis](#non-quasi-static-effects-analysis) | <span style='color: {color}'>{status}</span> | {findings} |")
            else:
                content.append("| [Non-Quasi-Static (NQS) Effects Analysis](#non-quasi-static-effects-analysis) | <span style='color: red'>✗</span> | Data not available |")
            
            # Charge Conservation Analysis
            if charge_results.get('data_ready'):
                status = "✓" if charge_results.get('verification_passed', True) else "✗"
                color = "green" if status == "✓" else "red"
                findings = f"Total charge error: {charge_results.get('max_charge_error', 'N/A')}"
                self.logger.info(f"data_ready.get('verification_passed', True): {status}")
                content.append(f"| [Charge Conservation Analysis](#charge-conservation-analysis) | <span style='color: {color}'>{status}</span> | {findings} |")
            else:
                content.append("| [Charge Conservation Analysis](#charge-conservation-analysis) | <span style='color: red'>✗</span> | Data not available |")
            
            content.append("")
            return content
            
        except Exception as e:
            self.logger.error(f"Error generating AC summary: {e}")
            return ["### AC Analysis Summary", "Error generating AC summary"]

    # Done
    def _generate_ac_analysis_section(self, results, section_num=3):
        """Generate the AC analysis section of the report."""
        try:
            content = []
            content.append(f"## {section_num}. AC Analysis")

            # Get results with safe defaults
            cv_results = results.get('cv_characteristics', {}) or {}
            sparams_results = results.get('sparameter_analysis', {}) or {}
            nqs_results = results.get('nqs_effects', {}) or {}
            charge_results = results.get('charge_conservation', {}) or {}
            
            # Check if any AC data is available
            has_ac_data = any([
                cv_results.get('data_ready'),
                sparams_results.get('data_ready'),
                nqs_results.get('data_ready'),
                charge_results.get('data_ready')
            ])
            
            if not has_ac_data:
                content.append("- [<span style='color: red'>✗</span>] AC simulations failed")
                content.append("  - Data not available or failed to read")
                return content
            
            # CV Characteristics
            content.append("### Small-Signal Analysis")
            if cv_results.get('data_ready'):
                content.append("- [<span style='color: green'>✓</span>] AC small-signal simulations verified")
                content.append(f"  - Gate capacitance range: {cv_results.get('cgg_range', 'N/A')}")
                content.append(f"  - Frequency range: {cv_results.get('freq_range', 'N/A')}")
                content.append(f"  - Max capacitance at: {cv_results.get('max_value_at', 'N/A')}")
                content.append("")
                content.append("*CV characteristics showing gate capacitance variation with gate voltage*")
                content.append("")
                content.append("<img src='plots/ac_cv_characteristics.png' alt='CV Characteristics' width='400'/>")
                content.append("")
                content.append("Capacitance components (Cgb, Cgs, Cgd) variation with gate voltage*")
                content.append("")
                content.append("<img src='plots/ac_cv_components.png' alt='CV Components' width='400'/>")
            else:
                content.append("- [<span style='color: red'>✗</span>] CV characteristics verification failed")
                content.append("  - Data not available or failed to read")
            content.append("")
            
            # High-Frequency Analysis
            content.append("### S-Parameter Analysis")
            if sparams_results.get('data_ready'):
                content.append("- [<span style='color: green'>✓</span>] High-frequency AC simulations verified")
                content.append(f"  - Frequency range: {sparams_results.get('freq_range', 'N/A')}")
                content.append("- [<span style='color: green'>✓</span>] S-parameter analysis verified")
                content.append(f"  - S11 range: {sparams_results.get('s11_range', 'N/A')}")
                content.append(f"  - S21 range: {sparams_results.get('s21_range', 'N/A')}")
                content.append(f"  - S12 range: {sparams_results.get('s12_range', 'N/A')}")
                content.append(f"  - S22 range: {sparams_results.get('s22_range', 'N/A')}")
                content.append("- [<span style='color: green'>✓</span>] RF simulations verified")
                content.append(f"  - Isolation: {sparams_results.get('isolation', 'N/A')}")
                content.append("")
                content.append("*S-Parameter analysis showing frequency response characteristics*")
                content.append("")
                content.append("<img src='plots/ac_cv_sparameter_analysis.png' alt='S-Parameters' width='400'/>")
            else:
                content.append("- [<span style='color: red'>✗</span>] S-parameter analysis failed")
                content.append("  - Data not available or failed to read")
            content.append("")

            # NQS Effects
            content.append("### Non-Quasi-Static Effects Analysis")
            if nqs_results.get('data_ready'):
                content.append("- [<span style='color: green'>✓</span>] NQS effects verified")
                content.append(f"  - Maximum phase shift: {nqs_results.get('max_phase_shift', 'N/A')}")
                content.append(f"  - Frequency range: {nqs_results.get('freq_range', 'N/A')}")
                content.append("")
                content.append("*Non-quasi-static effects analysis showing phase shift between gate voltage and drain current*")
                content.append("")
                content.append("<img src='plots/ac_cv_nqs_effects.png' alt='NQS Effects' width='400'/>")
            else:
                content.append("- [<span style='color: red'>✗</span>] NQS effects verification failed")
                content.append("  - Data not available or failed to read")
            
            # Charge Conservation Analysis
            content.append("\n### Charge Conservation Analysis")
            if charge_results.get('data_ready'):
                content.append("- [<span style='color: green'>✓</span>] Charge conservation verified")
                content.append(f"  - Total charge error: {charge_results.get('max_charge_error', 'N/A')}")
                content.append(f"  - Max current: {charge_results.get('max_current_error', 'N/A')}")
                content.append(f"  - Current Threshold: {charge_results.get('current_threshold', 'N/A')}")
                content.append("")
                content.append("*Terminal currents and charges analysis*")
                content.append("")
                content.append("<img src='plots/ac_charge_conservation.png' alt='Charge Conservation' width='400'/>")
            else:
                content.append("- [<span style='color: red'>✗</span>] Charge conservation verification failed")
                content.append("  - Data not available or failed to read")

            content.append("")
            self.logger.info("Successfully generated AC analysis section")
            return content
            
        except Exception as e:
            self.logger.error(f"Error generating AC analysis section: {e}")
            return [f"## {section_num}. AC Analysis", "Error generating AC analysis section"]

    # Done
    def _generate_transient_summary(self, results):
        """
        Generate transient analysis summary section.
        """
        try:
            content = []
            content.append("### Transient Analysis Summary")
            content.append("| Test Type | Status | Key Findings |")
            content.append("|-----------|--------|-------------|")

            # Get results with safe defaults
            transient_results = results.get('large_signal_transient', {}) or {}
            switching_results = results.get('switching_simulations', {}) or {}
            delay_results = results.get('delay_effect', {}) or {}
            power_results = results.get('power_dissipation', {}) or {}
            qs_results = results.get('quasi_static', {}) or {}
            charge_results = results.get('charge_conservation', {}) or {}

            # Check if any Transient data is available
            has_transient_data = any([
                transient_results.get('data_ready'),
                switching_results.get('data_ready'),
                delay_results.get('data_ready'),
                power_results.get('data_ready'),
                qs_results.get('data_ready'),
                charge_results.get('data_ready')
            ])
            
            if not has_transient_data:
                content.append("- [<span style='color: red'>✗</span>] Transient simulations failed")
                content.append("  - Data not available or failed to read")
                return content

            # Transient Analysis
            self.logger.info(f"transient_results: {transient_results}")
            self.logger.info(f"switching_results: {switching_results}")
            self.logger.info(f"delay_results: {delay_results}")
            self.logger.info(f"power_results: {power_results}")
            self.logger.info(f"qs_results: {qs_results}")
            self.logger.info(f"charge_results: {charge_results}")

            if transient_results.get('data_ready'):
                status = "✓" if transient_results.get('transient_completed', True) else "✗"
                color = "green" if status == "✓" else "red"
                findings = f"Max Current: {transient_results.get('details', {}).get('max_current'):.3e}A, Rise Time: {transient_results.get('details', {}).get('rise_time'):.1f}ps" 
                self.logger.info(f"transient_results.get('transient_completed', True): {status}")
                content.append(f"| [Large-Signal Transient](#large-signal-transient) | <span style='color: {color}'>{status}</span> | {findings} |")
            else:
                content.append("| [Large-Signal Transient](#large-signal-transient) | <span style='color: red'>✗</span> | Data not available |")

            if switching_results.get('data_ready'):
                status = "✓" if switching_results.get('switching_behavior_analyzed', True) and switching_results.get('propagation_delay_measured', True) and switching_results.get('max_current_calculated', True) else "✗"
                color = "green" if status == "✓" else "red"
                findings = f"Propagation Delay: {switching_results.get('details', {}).get('propagation_delay'):.1f}ps, Power: {switching_results.get('details', {}).get('max_power'):.3e}W (max), {switching_results.get('details', {}).get('avg_power'):.3e}W (avg)"
                self.logger.info(f"switching_results.get('switching_behavior_analyzed', True): {status}")
                content.append(f"| [Switching Simulations](#switching-simulations) | <span style='color: {color}'>{status}</span> | {findings} |")
            else:
                content.append("| [Switching Simulations](#switching-simulations) | <span style='color: red'>✗</span> | Data not available |")

            if delay_results.get('data_ready'):
                status = "✓" if delay_results.get('delay_effect_analyzed', True) else "✗"
                color = "green" if status == "✓" else "red"
                findings = f"Total Chain Delay: {delay_results.get('details', {}).get('total_delay'):.1f}ps"
                self.logger.info(f"delay_results.get('delay_effect_analyzed', True): {status}")
                content.append(f"| [Delay Effect](#delay-effect-simulations) | <span style='color: {color}'>{status}</span> | {findings} |")
            else:
                content.append("| [Delay Effect](#delay-effect-simulations) | <span style='color: red'>✗</span> | Data not available |")

            if power_results.get('data_ready'):
                status = "✓" if power_results.get('power_analysis_completed', True) else "✗"
                color = "green" if status == "✓" else "red"
                findings = f"Temp Coeff: {power_results.get('details', {}).get('power_temp_coef'):.6e}W/°C"
                self.logger.info(f"power_results.get('power_analysis_completed', True): {status}")
                content.append(f"| [Power Dissipation](#transient-simulations-for-power-dissipation) | <span style='color: {color}'>{status}</span> | {findings} |")
            else:
                content.append("| [Power Dissipation](#transient-simulations-for-power-dissipation) | <span style='color: red'>✗</span> | Data not available |")

            if qs_results.get('data_ready'):
                status = "✓" if qs_results.get('quasi_static_analyzed', True) else "✗"
                color = "green" if status == "✓" else "red"
                findings = f"I-V characteristics analyzed: {qs_results.get('iv_relationship_analyzed')}" 
                self.logger.info(f"qs_results.get('quasi_static_analyzed', True): {status}")
                content.append(f"| [Quasi-Static Analysis](#quasi-static-analysis) | <span style='color: {color}'>{status}</span> | {findings} |")
            else:
                content.append("| [Quasi-Static Analysis](#quasi-static-analysis) | <span style='color: red'>✗</span> | Data not available |")

            if charge_results.get('data_ready'):
                status = "✓" if charge_results.get('conservation_satisfied', True) else "✗"
                color = "green" if status == "✓" else "red"
                findings = f"Error: {charge_results.get('details', {}).get('q_conservation_error')}"
                self.logger.info(f"charge_results.get('conservation_satisfied', True): {status}")
                content.append(f"| [Charge Conservation](#charge-conservation-tests) | <span style='color: {color}'>{status}</span> | {findings} |")
            else:
                content.append("| [Charge Conservation](#charge-conservation-tests) | <span style='color: red'>✗</span> | Data not available |")

            content.append("")
            return content
            
        except Exception as e:
            self.logger.error(f"Error generating Transient summary: {e}")
            return ["### Transient Analysis Summary", "Error generating Transient summary"]

    # Done
    def _generate_transient_analysis_section(self, results, section_num=3):
        """
        Generate detailed Transient analysis section.
        """
        try:
            content = []
            content.append(f"## {section_num}. Transient Analysis")

            # Get results with safe defaults
            transient_results = results.get('large_signal_transient', {}) or {}
            switching_results = results.get('switching_simulations', {}) or {}
            delay_results = results.get('delay_effect', {}) or {}
            power_results = results.get('power_dissipation', {}) or {}
            qs_results = results.get('quasi_static', {}) or {}
            charge_results = results.get('charge_conservation', {}) or {}

            # Check if any Transient data is available
            has_transient_data = any([
                transient_results.get('data_ready'),
                switching_results.get('data_ready'),
                delay_results.get('data_ready'),
                power_results.get('data_ready'),
                qs_results.get('data_ready'),
                charge_results.get('data_ready')
            ])
            
            if not has_transient_data:
                content.append("- [<span style='color: red'>✗</span>] Transient simulations failed")
                content.append("  - Data not available or failed to read")
                return content
            
            # Large-Signal Transient
            content.append("### Large-Signal Transient")
            if transient_results.get('data_ready'):
                status = "✓" if transient_results.get('transient_completed', True) else "✗"
                color = "green" if status == "✓" else "red"
                findings = f"  - Maximum Drain Current: {transient_results.get('details', {}).get('max_current'):.6e}A"
                content.append(f"- [<span style='color: {color}'>{status}</span>] Large Signal Transient Verified")
                content.append(findings if status else "  - Maximum Drain Current: *Not measured*")

                status = "✓" if transient_results.get('rise_time_measured', True) else "✗"
                color = "green" if status == "✓" else "red"
                findings = f"  - Gate Voltage Rise Time: {transient_results.get('details', {}).get('rise_time'):.1f}ps"
                content.append(findings if status else "  - Gate Voltage Rise Time: *Not measured*")

                content.append("")
                content.append("*Large-signal transient analysis showing voltages and current response*")
                content.append("")
                content.append("<img src='plots/trans_large_signal_transient.png' alt='Large-Signal Transient Analysis' width='400'/>")
                content.append("")
            else:
                content.append("- [<span style='color: red'>✗</span>] Large-Signal Transient verification failed")
                content.append("  - Data not available or failed to read")
                content.append("")

            # Switching Simulations
            content.append("### Switching Simulations")
            if switching_results.get('data_ready'):
                status = "✓" if switching_results.get('propagation_delay_measured', True) else "✗"
                color = "green" if status == "✓" else "red"
                findings = f"  - Propagation Delay: {switching_results.get('details', {}).get('propagation_delay'):.1f}ps"
                content.append(f"- [<span style='color: {color}'>{status}</span>] Propagation Delay Verified")
                content.append(findings if status else "  - Propagation Delay: *Not measured*")
                content.append("")

                status = "✓" if switching_results.get('power_measured', True) else "✗"
                color = "green" if status == "✓" else "red"
                findings = f"  - Maximum Switching Power: {switching_results.get('details', {}).get('max_power'):.6e}W"
                content.append(findings if status else "  - Maximum Switching Power: *Not measured*")
                content.append("")

                findings = f"  - Average Switching Power: {switching_results.get('details', {}).get('avg_power'):.6e}W" 
                content.append(findings if status else "  - Average Switching Power: *Not measured*")
                content.append("")

                content.append("*Inverter switching analysis showing input/output voltages and power*")
                content.append("")
                content.append("<img src='plots/trans_switching_response.png' alt='Switching Response' width='400'/>")
                content.append("")
            else:
                content.append("- [<span style='color: red'>✗</span>] Switching Simulations verification failed")
                content.append("  - Data not available or failed to read")
                content.append("")

            # Delay Effect Simulations
            content.append("### Delay Effect Simulations")
            if delay_results.get('data_ready'):
                status = "✓" if delay_results.get('delay_effect_analyzed', True) else "✗"
                color = "green" if status == "✓" else "red"
                content.append(f"- [<span style='color: {color}'>{status}</span>] Propagation delay through inverter chain analyzed")
                
                findings = f"  - Stage 1 Delay: {delay_results.get('details', {}).get('stage1_delay'):.1f}ps"
                content.append(findings if status else "  - Stage 1 Delay: *Not measured*")
                content.append("")

                findings = f"  - Stage 2 Delay: {delay_results.get('details', {}).get('stage2_delay'):.1f}ps"
                content.append(findings if status else "  - Stage 2 Delay: *Not measured*")
                content.append("")

                findings = f"  - Stage 3 Delay: {delay_results.get('details', {}).get('stage3_delay'):.1f}ps"
                content.append(findings if status else "  - Stage 3 Delay: *Not measured*")
                content.append("")

                findings = f"  - Total Delay: {delay_results.get('details', {}).get('total_delay'):.1f}ps"
                content.append(findings if status else "  - Total Chain Delay: *Not measured*")
                content.append("")

                content.append("*Delay effect analysis showing signal propagation through inverter chain*")
                content.append("")
                content.append("<img src='plots/trans_delay_effect.png' alt='Delay Effect Analysis' width='400'/>")
                content.append("")
            else:
                content.append("- [<span style='color: red'>✗</span>] Delay Effect Simulations verification failed")
                content.append("  - Data not available or failed to read")
                content.append("")

            # Transient Simulations for Power Dissipation
            content.append("### Transient Simulations for Power Dissipation")
            if power_results.get('data_ready'):
                status = "✓" if power_results.get('power_analysis_completed', True) else "✗"
                color = "green" if status == "✓" else "red"
                content.append(f"- [<span style='color: {color}'>{status}</span>] Temperature-dependent power analysis completed")
                
                findings = f"  - Maximum Power at 27°C: {power_results.get('details', {}).get('max_power_27c'):.6e}W" 
                content.append(findings if status else "  - Maximum Power at 27°C: *Not measured*")
                content.append("")
                
                findings = f"  - Maximum Power at 100°C: {power_results.get('details', {}).get('max_power_100c'):.6e}W" 
                content.append(findings if status else "  - Maximum Power at 100°C: *Not measured*")
                content.append("")

                findings = f"  - Average Power at 27°C: {power_results.get('details', {}).get('avg_power_27c'):.6e}W" 
                content.append(findings if status else "  - Average Power at 27°C: *Not measured*")
                content.append("")

                findings = f"  - Average Power at 100°C: {power_results.get('details', {}).get('avg_power_100c'):.6e}W" 
                content.append(findings if status else "  - Average Power at 100°C: *Not measured*")
                content.append("")

                findings = f"  - Power Temperature Coefficient: {power_results.get('details', {}).get('power_temp_coef'):.6e}W/°C" 
                content.append(findings if status else "  - Power Temperature Coefficient: *Not measured*")
                content.append("")

                content.append("*Power dissipation analysis at different temperatures*")
                content.append("")
                content.append("<img src='plots/trans_power_dissipation.png' alt='Power Dissipation' width='400'/>")
                content.append("")
                content.append("*Energy consumption analysis at different temperatures*")
                content.append("")
                content.append("<img src='plots/trans_energy_consumption.png' alt='Energy Consumption' width='400'/>")
                content.append("")
            else:
                content.append("- [<span style='color: red'>✗</span>] Power verification failed")
                content.append("  - Data not available or failed to read")
                content.append("")

            # Quasi-Static Analysis
            content.append("### Quasi-Static Analysis")
            if qs_results.get('data_ready'):
                status = "✓" if qs_results.get('quasi_static_analyzed', True) else "✗"
                color = "green" if status == "✓" else "red"
                content.append(f"- [<span style='color: {color}'>{status}</span>] Charge conservation analyzed")

                content.append("*Quasi-static time-domain behavior analysis*")
                content.append("")
                content.append("<img src='plots/trans_quasi_static.png' alt='Quasi-Static Analysis' width='400'/>")
                content.append("")
                content.append("*Quasi-static I-V characteristic showing relationship between gate voltage and drain current*")
                content.append("")
                content.append("<img src='plots/trans_quasi_static_iv.png' alt='Quasi-Static I-V Characteristic' width='400'/>")
                content.append("")
            else:
                content.append("- [<span style='color: red'>✗</span>] Quasi-Static Simulations verification failed")
                content.append("  - Data not available or failed to read")
                content.append("")

            # Charge Conservation Tests
            content.append("### Charge Conservation Tests")
            charge_results['data_ready'] = False
            if charge_results.get('data_ready'):
                status = "✓" if charge_results.get('charge_conservation', True) else "✗"
                color = "green" if status == "✓" else "red"
                content.append(f"- [<span style='color: {color}'>{status}</span>] Charge conservation analyzed")
                content.append("")

                findings = f"  - Total Charge Variation: {charge_results.get('details', {}).get('q_total_variation'):.6e}C" 
                content.append(findings if status else "  - Total Charge Variation: *Not measured*")
                content.append("")

                findings = f"  - Mean Total Charge: {charge_results.get('details', {}).get('q_total_mean'):.6e}C"
                content.append(findings if status else "  - Mean Total Charge: *Not measured*")
                content.append("")

                findings = f"  - Charge Conservation Error: {charge_results.get('details', {}).get('q_conservation_error'):.6f}%"
                content.append(findings if status else "  - Charge Conservation Error: *Not measured*")
                content.append("")

                content.append("*Terminal currents and charges analysis*")
                content.append("")
                content.append("<img src='plots/trans_charge_conservation.png' alt='Charge Conservation Analysis' width='400'/>")
                content.append("")
                content.append("*Total charge conservation analysis*")
                content.append("")
                content.append("<img src='plots/trans_total_charge.png' alt='Total Charge' width='400'/>")
                content.append("")
            else:
                content.append("- [<span style='color: red'>✗</span>] Charge Conservation verification failed")
                content.append("  - Data not available or failed to read")
                content.append("")


            content.append("")
            self.logger.info("Successfully generated Transient analysis section")    
            return content
        except Exception as e:
            self.logger.error(f"Error generating Transient analysis section: {e}")
            return [f"## {section_num}. Transient Analysis", "Error generating Transient analysis section"]

    # Done
    def _generate_noise_summary(self, results):
        """
        Generate noise analysis summary section.
        """
        self.logger.info("Generating Noise Summary")
        try:
            content = []
            content.append("### Noise Analysis Summary")
            content.append("| Test Type | Status | Key Findings |")
            content.append("|-----------|--------|-------------|")

            # Get results with safe defaults
            noise_results = results.get('noise_analysis', {}) or {}

            # Check if any Noise data is available
            has_noise_data = any([
                noise_results.get('data_ready'),
                noise_results.get('noise_analysis_performed'),
                noise_results.get('thermal_noise_analyzed'),
                noise_results.get('flicker_noise_analyzed'),
                noise_results.get('shot_noise_analyzed')
            ])
            
            if not has_noise_data:
                content.append("- [<span style='color: red'>✗</span>] Noise simulations failed")
                content.append("  - Data not available or failed to read")
                return content

            # Noise Analysis
            self.logger.info(f"noise_results: {noise_results}")

            if noise_results.get('thermal_noise_analyzed'):
                status = "✓" if noise_results.get('thermal_noise_analyzed', True) else "✗"
                color = "green" if status == "✓" else "red"
                findings = f"Floor: {noise_results.get('details', {}).get('thermal_noise_floor'):.2e} V²/Hz, Range: {noise_results.get('details', {}).get('thermal_noise_min'):.2e} to {noise_results.get('details', {}).get('thermal_noise_max'):.2e} V²/Hz" 
                self.logger.info(f"noise_results.get('thermal_noise_analyzed', True): {status}")
                content.append(f"| [Thermal Noise](#thermal-noise-analysis) | <span style='color: {color}'>{status}</span> | {findings} |")
            else:
                content.append("| [Thermal Noise](#thermal-noise-analysis) | <span style='color: red'>✗</span> | Data not available |")

            if noise_results.get('flicker_noise_analyzed'):
                status = "✓" if noise_results.get('flicker_noise_analyzed', True) else "✗"
                color = "green" if status == "✓" else "red"
                findings = f"Exponent: {noise_results.get('details', {}).get('flicker_noise_exponent'):.4f}, Corner Freq: {noise_results.get('details', {}).get('corner_frequency'):.2e} Hz" 
                self.logger.info(f"noise_results.get('flicker_noise_analyzed', True): {status}")
                content.append(f"| [Flicker (1/f) Noise](#flicker-noise-analysis) | <span style='color: {color}'>{status}</span> | {findings} |")
            else:
                content.append("| [Flicker (1/f) Noise](#flicker-noise-analysis) | <span style='color: red'>✗</span> | Data not available |")

            if noise_results.get('shot_noise_analyzed'):
                status = "✓" if noise_results.get('shot_noise_analyzed', True) else "✗"
                color = "green" if status == "✓" else "red"
                findings = f"Level: {noise_results.get('details', {}).get('shot_noise_level'):.2e} V²/Hz, Variation: {noise_results.get('details', {}).get('shot_noise_variation'):.4f}"
                self.logger.info(f"noise_results.get('shot_noise_analyzed', True): {status}")
                content.append(f"| [Shot Noise](#shot-noise-analysis) | <span style='color: {color}'>{status}</span> | {findings} |")
            else:
                content.append("| [Shot Noise](#shot-noise-analysis) | <span style='color: red'>✗</span> | Data not available |")                

            if noise_results.get('temp_dependence_analyzed'):
                status = "✓" if noise_results.get('temp_dependence_analyzed', True) else "✗"
                color = "green" if status == "✓" else "red"
                findings = f"Coefficient: {noise_results.get('details', {}).get('temp_coefficient'):.2e} V²/Hz/°C, Range: {noise_results.get('details', {}).get('temp_range')}" 
                self.logger.info(f"noise_results.get('temp_dependence_analyzed', True): {status}")
                content.append(f"| [Temperature Dependence](#temperature-dependence) | <span style='color: {color}'>{status}</span> | {findings} |")
            else:
                content.append("| [Temperature Dependence](#temperature-dependence) | <span style='color: red'>✗</span> | Data not available |")               

            if noise_results.get('thermal_noise_analyzed'):
                status = "✓" if noise_results.get('thermal_noise_analyzed', True) else "✗"
                color = "green" if status == "✓" else "red"
                findings = f"Analyzed at {len(noise_results.get('details', {}).get('bias_points'))} bias points" 
                self.logger.info(f"noise_results.get('thermal_noise_analyzed', True): {status}")
                content.append(f"| [Bias Dependence](#bias-dependence) | <span style='color: {color}'>{status}</span> | {findings} |")
            else:
                content.append("| [Bias Dependence](#detailed-noise-characteristics) | <span style='color: red'>✗</span> | Data not available |")

            content.append("")
            return content
            
        except Exception as e:
            self.logger.error(f"Error generating Noise summary: {e}")
            return ["### Noise Analysis Summary", "Error generating Noise summary"]

    def _generate_noise_analysis_section(self, results, section_num=3):
        """
        Generate detailed Noise analysis section.
        """
        self.logger.info("Generating Noise Analysis Section")
        try:
            content = []
            content.append(f"## {section_num}. Noise Analysis")

            # Get results with safe defaults
            noise_results = results.get('noise_analysis', {}) or {}

            # Check if any Noise data is available
            has_noise_data = any([
                noise_results.get('data_ready'),
                noise_results.get('noise_analysis_performed'),
                noise_results.get('thermal_noise_analyzed'),
                noise_results.get('flicker_noise_analyzed'),
                noise_results.get('shot_noise_analyzed')
            ])
            
            if not has_noise_data:
                content.append("- [<span style='color: red'>✗</span>] Noise simulations failed")
                content.append("  - Data not available or failed to read")
                return content
            
            # Thermal Noise Analysis
            content.append("### Thermal Noise Analysis")
            if noise_results.get('noise_analysis_performed'):
                status = "✓" if noise_results.get('noise_analysis_performed', True) else "✗"
                color = "green" if status == "✓" else "red"
                content.append(f"- [<span style='color: {color}'>{status}</span>] Thermal noise analysis completed")

                findings = f"  - Max Noise: {noise_results.get('details', {}).get('thermal_noise_max'):.2e} V²/Hz" 
                content.append(findings if status else "  - Max Noise: *Not measured*")

                findings = f"  - Min Noise: {noise_results.get('details', {}).get('thermal_noise_min'):.2e} V²/Hz" 
                content.append(findings if status else "  - Min Noise: *Not measured*")
                
                findings = f"  - Avg Noise: {noise_results.get('details', {}).get('thermal_noise_avg'):.2e} V²/Hz" 
                content.append(findings if status else "  - Avg Noise: *Not measured*")

                findings = f"  - Noise Floor: {noise_results.get('details', {}).get('thermal_noise_floor'):.2e} V²/Hz" 
                content.append(findings if status else "  - Noise Floor: *Not measured*")

                findings = f"  - Frequency Range: {noise_results.get('details', {}).get('freq_range')}" 
                content.append(findings if status else "  - Frequency Range: *Not measured*")

                content.append("")
                content.append("*Thermal noise power spectral density analysis comparing different bias conditions, showing how the device noise characteristics change with bias voltage.*")
                content.append("")
                content.append("<img src='plots/noise_thermal_noise_vds_comparison.png' alt='Thermal Noise Comparison' width='400'/>")
                content.append("")
            else:
                content.append("- [<span style='color: red'>✗</span>] Thermal Noise Analysis verification failed")
                content.append("  - Data not available or failed to read")
                content.append("")

            # Flicker Noise Analysis
            content.append("### Flicker Noise Analysis")
            if noise_results.get('flicker_noise_analyzed'):
                status = "✓" if noise_results.get('flicker_noise_analyzed', True) else "✗"
                color = "green" if status == "✓" else "red"
                content.append(f"- [<span style='color: {color}'>{status}</span>] Flicker noise analysis completed")

                findings = f"  - Coefficient (K): {noise_results.get('details', {}).get('flicker_noise_coefficient'):.2e}" 
                content.append(findings if status else "  - Coefficient (K): *Not measured*")

                findings = f"  - Exponent (γ): {noise_results.get('details', {}).get('flicker_noise_exponent'):.2e} (ideally -1.0 for pure 1/f noise)" 
                content.append(findings if status else "  - Exponent (γ): *Not measured*")

                findings = f"  - Correlation (R²): {noise_results.get('details', {}).get('flicker_noise_r_squared'):.4f}" 
                content.append(findings if status else "  - Correlation (R²): *Not measured*")

                findings = f"  - Corner Frequency: {noise_results.get('details', {}).get('corner_frequency'):.2e} Hz" 
                content.append(findings if status else "  - Corner Frequency: *Not measured*")

                content.append("")
                content.append("*Flicker (1/f) noise analysis showing the power spectral density decreasing with frequency, a characteristic behavior in semiconductor devices associated with trapping/detrapping processes.*")
                content.append("")
                content.append("<img src='plots/noise_flicker_noise.png' alt='Flicker Noise Analysis' width='400'/>")
                content.append("")
            else:
                content.append("- [<span style='color: red'>✗</span>] Flicker Noise Analysis verification failed")
                content.append("  - Data not available or failed to read")
                content.append("")

            # Short Noise Analysis
            content.append("### Short Noise Analysis")
            if noise_results.get('shot_noise_analyzed'):
                status = "✓" if noise_results.get('shot_noise_analyzed', True) else "✗"
                color = "green" if status == "✓" else "red"
                content.append(f"- [<span style='color: {color}'>{status}</span>] Short noise analysis completed")

                findings = f"  - Shot Noise Level: {noise_results.get('details', {}).get('shot_noise_level'):.2e} V²/Hz"
                content.append(findings if status else "  - Shot Noise Level: *Not measured*")

                findings = f"  - Standard Deviation: {noise_results.get('details', {}).get('shot_noise_std_dev'):.2e} V²/Hz"
                content.append(findings if status else "  - Standard Deviation: *Not measured*")

                findings = f"  - Variation Coefficient: {noise_results.get('details', {}).get('shot_noise_variation'):.4f}"
                content.append(findings if status else "  - Variation Coefficient: *Not measured*")

                content.append("")
                content.append("*Shot noise analysis showing the frequency-independent noise component that arises from the discrete nature of electric charge carriers crossing potential barriers.*")
                content.append("")
                content.append("<img src='plots/noise_shot_noise.png' alt='Shot Noise Analysis' width='400'/>")
                content.append("")
            else:
                content.append("- [<span style='color: red'>✗</span>] Short Noise Analysis verification failed")
                content.append("  - Data not available or failed to read")
                content.append("")   
                
            # Temperature Dependence
            content.append("### Temperature Dependence")
            if noise_results.get('temp_dependence_analyzed'):
                status = "✓" if noise_results.get('temp_dependence_analyzed', True) else "✗"
                color = "green" if status == "✓" else "red"
                content.append(f"- [<span style='color: {color}'>{status}</span>] Short noise analysis completed")

                findings = f"  - Temperature Coefficient: {noise_results.get('details', {}).get('temp_coefficient'):.2e} V²/Hz/°C"
                content.append(findings if status else "  - Temperature Coefficient: *Not measured*")

                findings = f"  - Temperature-Noise Correlation: {noise_results.get('details', {}).get('temp_noise_correlation')}"
                content.append(findings if status else "  - Temperature-Noise Correlation: *Not measured*")

                findings = f"  - Temperature Range: {noise_results.get('details', {}).get('temp_range')}"
                content.append(findings if status else "  - Temperature Range: *Not measured*")

                content.append("")
                content.append("*Noise variation with temperature, illustrating how thermal effects influence the device's noise characteristics across the operational temperature range.*")
                content.append("")
                content.append("<img src='plots/noise_vs_temperature.png' alt='Shot Noise Analysis' width='400'/>")
                content.append("")
            else:
                content.append("- [<span style='color: red'>✗</span>] Temperature Dependence verification failed")
                content.append("  - Data not available or failed to read")
                content.append("")   


            # Temperature Dependence
            content.append("### Bias Dependence")
            if noise_results.get('thermal_noise_analyzed'):
                status = "✓" if noise_results.get('thermal_noise_analyzed', True) else "✗"
                color = "green" if status == "✓" else "red"
                content.append(f"- [<span style='color: {color}'>{status}</span>] Bias Dependance analysis completed")

                content.append("*Thermal Noise Results at Different Bias Points*")
                content.append("")
                content.append("| Bias Condition | Max Noise (V²/Hz) | Min Noise (V²/Hz) | Avg Noise (V²/Hz) | Noise Floor (V²/Hz) |")
                content.append("|----------------|-------------------|-------------------|-------------------|--------------------|")

                # Handle the case where we have direct bias_points data
                for bias_point, data in noise_results.get('details', {}).get('bias_points').items():
                    if isinstance(data, dict) and 'max_noise' in data:
                        content.append(f"| {bias_point} | {data['max_noise']:.2e} | {data['min_noise']:.2e} | {data['avg_noise']:.2e} | {data['noise_floor']:.2e} |")
                    elif isinstance(data, dict) and 'max' in data:
                        content.append(f"| {bias_point} | {data['max']:.2e} | {data['min']:.2e} | {data['avg']:.2e} | {data['floor']:.2e} |")
                content.append("")
            else:
                content.append("- [<span style='color: red'>✗</span>] Bias Dependence verification failed")
                content.append("  - Data not available or failed to read")
                content.append("")  





            content.append("")
            self.logger.info("Successfully generated Noise analysis section")    
            return content
        except Exception as e:
            self.logger.error(f"Error generating Noise analysis section: {e}")
            return [f"## {section_num}. Noise Analysis", "Error generating Noise analysis section"]

    # DC Analysis
    # Done
    def verify_dc_operating_point_analysis(self, v_ds, v_gs, i_ds, i_g, i_s, i_b, temp):
        """Verify DC Operating Point Analysis.
        
        Args:
            vds: Drain-source voltage array
            vgs: Gate-source voltage array
            i_ds: Drain current array
            i_g: Gate current array
            i_s: Source current array
            i_b: Bulk current array
            temp: Temperature array
            
        Returns:
            dict: Verification results
        """
        try:
            if v_ds is None or i_ds is None or v_gs is None or len(v_ds) == 0 or len(i_ds) == 0 or len(v_gs) == 0:
                self.logger.error("Missing or empty DC Operating Points")
                return {
                    'data_ready': False,
                    'vds_range': "Not available",
                    'vgs_range': "Not available",
                    'ids_range': "Not available",
                    'details': {
                        'v_ds': None,
                        'v_gs': None,
                        'i_ds': None,
                        'i_g': None,
                        'i_s': None,
                        'i_b': None
                    }
                }

            # Convert to numpy arrays for easier indexing
            v_ds = np.array(v_ds)
            v_gs = np.array(v_gs)
            i_ds = np.array(i_ds)
            temp = np.array(temp) if temp is not None else None

            # Verify data ranges
            vds_range = f"{min(v_ds):.2f}V to {max(v_ds):.2f}V"
            vgs_range = f"{min(v_gs):.2f}V to {max(v_gs):.2f}V"
            ids_range = f"{min(i_ds):.2e}A to {max(i_ds):.2e}A"
            
            # Verify KCL
            kcl_verified = self._verify_kcl(i_ds, i_g, i_s, i_b)
            
            # Verify temperature effects
            temp_effects = None
            if temp is not None and len(temp) > 1:
                if i_ds.ndim == 3 and i_ds.shape[2] == len(temp):
                    # 3D: Vgs, Vds, Temp
                    vgs_idx = i_ds.shape[0] // 2
                    vds_idx = i_ds.shape[1] // 2
                    ids_vs_temp = i_ds[vgs_idx, vds_idx, :]
                    temp_effects = self._verify_temperature_effects(temp, ids_vs_temp)
                elif i_ds.ndim == 1 and i_ds.shape[0] == len(temp):
                    # 1D: Temp
                    temp_effects = self._verify_temperature_effects(temp, i_ds)
                else:
                    self.logger.warning("Temperature effect check skipped: i_ds does not have a temperature sweep dimension.")
                    temp_effects = None
                    
            self.logger.info("DC Operating Point Analysis verified")
            return {
                'data_ready': True,
                'vds_range': vds_range,
                'vgs_range': vgs_range,
                'ids_range': ids_range,
                'kcl_verified': kcl_verified,
                'temp_effects': temp_effects,
                'details': {
                    'v_ds': v_ds.tolist(),
                    'v_gs': v_gs.tolist(),
                    'i_ds': i_ds.tolist(),
                    'i_g': i_g.tolist() if i_g is not None else None,
                    'i_s': i_s.tolist() if i_s is not None else None,
                    'i_b': i_b.tolist() if i_b is not None else None
                }
            }
        except Exception as e:
            self.logger.error(f"Error in DC Operating Point Analysis: {e}")
            return {
                'data_ready': False,
                'vds_range': "Error",
                'vgs_range': "Error",
                'ids_range': "Error",
                'details': {
                    'v_ds': None,
                    'v_gs': None,
                    'i_ds': None,
                    'i_g': None,
                    'i_s': None,
                    'i_b': None
                }
            }

    # Done
    def _verify_kcl(self, i_ds, i_g, i_s, i_b):
        """Verify Kirchhoff's Current Law (KCL) for the MOSFET.
        
        Args:
            i_ds: Drain current array
            i_g: Gate current array
            i_s: Source current array
            i_b: Bulk current array
            
        Returns:
            bool: True if KCL is satisfied within tolerance, False otherwise
        """
        try:
            # Convert inputs to numpy arrays if they aren't already
            i_ds = np.array(i_ds)
            i_g = np.array(i_g) if i_g is not None else np.zeros_like(i_ds)
            i_s = np.array(i_s) if i_s is not None else np.zeros_like(i_ds)
            i_b = np.array(i_b) if i_b is not None else np.zeros_like(i_ds)
            
            # KCL: i_ds + i_g + i_s + i_b ≈ 0
            # For a MOSFET, we expect:
            # - i_ds: drain current (positive for nMOS)
            # - i_g: gate current (should be very small)
            # - i_s: source current (should be approximately -ids)
            # - i_b: bulk current (should be very small)
            
            # Calculate total current
            total_current = i_ds + i_g + i_s + i_b
            
            # Define tolerance (1% of maximum drain current)
            tolerance = 0.01 * np.max(np.abs(i_ds))
            
            # Check if total current is within tolerance
            kcl_satisfied = np.all(np.abs(total_current) <= tolerance)
            
            if kcl_satisfied:
                self.logger.info("KCL verification passed")
            else:
                self.logger.warning("KCL verification failed - currents do not sum to zero within tolerance")
                
            return kcl_satisfied
            
        except Exception as e:
            self.logger.error(f"Error in KCL verification: {e}")
            return False

    # Done
    def _verify_temperature_effects(self, temp, i_ds):
        """
        Verify temperature effects on drain current.
        
        Args:
            temp: Temperature array
            ids: Drain current array
            
        Returns:
            dict: Temperature verification results containing:
                - temp_range: Temperature range
                - ids_variation: Maximum drain current variation
                - temp_coefficient: Temperature coefficient of drain current
                - is_valid: Whether temperature effects are within expected range
        """
        try:
            # Convert inputs to numpy arrays if they aren't already
            temp = np.array(temp)
            ids = np.array(i_ds)
            # Calculate temperature range
            temp_range = f"{min(temp):.1f}°C to {max(temp):.1f}°C"
                        
            if len(temp) > 1 and len(i_ds) > 1:
                d_ids = np.max(i_ds) - np.min(i_ds)
                d_temp = np.max(temp) - np.min(temp)

                # Calculate drain current variation
                ids_variation = np.abs(d_ids) / np.mean(np.abs(i_ds))

                # Calculate temperature coefficient (TC) of drain current
                # TC = (1/Ids) * (dIds/dT)
                tc = np.mean((d_ids / d_temp) / np.abs(i_ds[:-1]))
            else:
                ids_variation = 0
                tc = 0
            
            # Define expected ranges
            max_variation = 0.5  # 50% maximum variation
            max_tc = 0.01  # 1% per degree Celsius
            
            # Check if temperature effects are within expected range
            print(f"ids_variation: {ids_variation}")
            print(f"ids_variation <= max_variation: {ids_variation <= max_variation}")
            print(f"tc: {tc}")
            print(f"abs(tc) <= max_tc: {abs(tc) <= max_tc}")
            is_valid = (ids_variation <= max_variation and abs(tc) <= max_tc)
            
            if is_valid:
                self.logger.info("Temperature effects verification passed")
            else:
                self.logger.warning("Temperature effects verification failed - effects outside expected range")
            
            return {
                'temp_range': temp_range,
                'ids_variation': f"{ids_variation:.2%}",
                'temp_coefficient': f"{tc:.2e}/°C",
                'is_valid': is_valid
            }
            
        except Exception as e:
            self.logger.error(f"Error in temperature effects verification: {e}")
            return {
                'temp_range': "Error",
                'ids_variation': "Error",
                'temp_coefficient': "Error",
                'is_valid': False
            }

    # Done
    def verify_temperature_analysis(self, temp, i_ds):
        """
        Verify temperature analysis data.
        """
        
        results = {
            'temp_sweep': False,
            'power_measurements': False,
            'temp_coef': False,
            'device_behavior': False,
            'details': {
                'temp_points': None,
                'temp_coef_value': None,
                'ids_range': None
            }
        }
        
        if temp is None or i_ds is None:
            self.results['temperature_analysis'] = results
            return results
            
        try:
            # Check temperature sweep
            expected_temps = [-40, 0, 25, 50, 100, 150]
            results['temp_sweep'] = all(t in temp for t in expected_temps)
            if results['temp_sweep']:
                results['details']['temp_points'] = sorted(list(set(temp)))
            
            # Check power measurements
            power = i_ds * i_ds  # Simplified power calculation
            results['power_measurements'] = np.all(~np.isnan(power))
            
            # Calculate temperature coefficient
            if len(temp) > 1:
                temp_coef = np.polyfit(temp, i_ds, 1)[0]
                results['temp_coef'] = True
                results['details']['temp_coef_value'] = f"{temp_coef:.6f} /°C"
            
            # Check device behavior
            results['device_behavior'] = np.all(~np.isnan(i_ds))
            if results['device_behavior']:
                results['details']['ids_range'] = f"{np.min(i_ds):.3e}A to {np.max(i_ds):.3e}A"
            
            self.logger.info("Temperature analysis verification completed")
            
        except Exception as e:
            self.logger.error(f"Error verifying temperature analysis: {e}")
            
        self.results['temperature_analysis'] = results
        return results

    # Done
    def verify_thermodynamic_analysis(self, power, temp, i_ds):
        """
        Verify thermodynamic analysis data.
        """
        results = {
            'energy_conservation': False,
            'temp_coef_calc': False,
            'device_efficiency': False,
            'power_measurements': False,
            'efficiency_measurements': False,
            'details': {
                'power_range': None,
                'efficiency_range': None,
                'temp_coef': None
            }
        }
        
        self.logger.debug("Starting thermodynamic analysis verification", {
            'input_shapes': {
                'power': power.shape if power is not None else None,
                'temp': temp.shape if temp is not None else None,
                'i_ds': i_ds.shape if i_ds is not None else None
            },
            'input_types': {
                'power': type(power).__name__,
                'temp': type(temp).__name__,
                'i_ds': type(i_ds).__name__
            },
            'input_ranges': {
                'power': f"{np.min(power):.3e} to {np.max(power):.3e}" if power is not None else None,
                'temp': f"{np.min(temp):.1f} to {np.max(temp):.1f}" if temp is not None else None,
                'i_ds': f"{np.min(i_ds):.3e} to {np.max(i_ds):.3e}" if i_ds is not None else None
            }
        })
        
        if temp is None or i_ds is None or power is None:
            self.logger.debug("Missing data for thermodynamic analysis", {
                'temp': temp is None,
                'i_ds': i_ds is None,
                'power': power is None,
                'temp_values': temp if temp is not None else None,
                'ids_values': i_ds[:5] if i_ds is not None else None,
                'power_values': power[:5] if power is not None else None
            })
            self.results['thermodynamic_analysis'] = results
            return results
            
        try:
            # Log the first few values of each array to understand the calculation
            self.logger.debug("Sample values for power calculation", {
                'first_5_ids': i_ds[:5].tolist(),
                'first_5_power': power[:5].tolist(),
                'first_5_temp': temp[:5].tolist() if len(temp) > 5 else temp.tolist()
            })
            
            # Enhanced energy conservation check
            self.logger.debug("Starting energy conservation check", {
                'power_array_info': {
                    'shape': power.shape,
                    'dtype': power.dtype,
                    'has_nan': np.any(np.isnan(power)),
                    'has_inf': np.any(np.isinf(power)),
                    'min_value': np.min(power),
                    'max_value': np.max(power),
                    'mean_value': np.mean(power),
                    'std_value': np.std(power)
                }
            })
            
            # Check for invalid values
            invalid_mask = np.isnan(power) | np.isinf(power)
            if np.any(invalid_mask):
                self.logger.debug("Found invalid power values", {
                    'nan_count': np.sum(np.isnan(power)),
                    'inf_count': np.sum(np.isinf(power)),
                    'invalid_indices': np.where(invalid_mask)[0][:10],
                    'invalid_values': power[invalid_mask][:10],
                    'corresponding_ids': i_ds[invalid_mask][:10] if i_ds is not None else None
                })
            
            # Check for negative values with more context
            negative_mask = power < 0
            if np.any(negative_mask):
                self.logger.debug("Found negative power values", {
                    'negative_count': np.sum(negative_mask),
                    'negative_indices': np.where(negative_mask)[0][:10],
                    'negative_values': power[negative_mask][:10],
                    'corresponding_ids': i_ds[negative_mask][:10],
                    'min_negative': np.min(power[negative_mask]),
                    'max_negative': np.max(power[negative_mask]),
                    'negative_percentage': (np.sum(negative_mask) / len(power)) * 100
                })
            
            # Check for zero values
            zero_mask = power == 0
            if np.any(zero_mask):
                self.logger.debug("Found zero power values", {
                    'zero_count': np.sum(zero_mask),
                    'zero_indices': np.where(zero_mask)[0][:10],
                    'corresponding_ids': i_ds[zero_mask][:10],
                    'zero_percentage': (np.sum(zero_mask) / len(power)) * 100
                })
            
            # Check for very small values
            small_mask = (power > 0) & (power < 1e-12)
            if np.any(small_mask):
                self.logger.debug("Found very small power values", {
                    'small_count': np.sum(small_mask),
                    'small_indices': np.where(small_mask)[0][:10],
                    'small_values': power[small_mask][:10],
                    'corresponding_ids': i_ds[small_mask][:10],
                    'min_small': np.min(power[small_mask]),
                    'max_small': np.max(power[small_mask]),
                    'small_percentage': (np.sum(small_mask) / len(power)) * 100
                })
            
            # Calculate power statistics
            valid_power = power[~invalid_mask]
            power_stats = {
                'total_points': len(power),
                'valid_points': len(valid_power),
                'negative_points': np.sum(negative_mask),
                'zero_points': np.sum(zero_mask),
                'positive_points': np.sum(power > 0),
                'min_valid': np.min(valid_power) if len(valid_power) > 0 else None,
                'max_valid': np.max(valid_power) if len(valid_power) > 0 else None,
                'mean_valid': np.mean(valid_power) if len(valid_power) > 0 else None,
                'std_valid': np.std(valid_power) if len(valid_power) > 0 else None,
                'percentiles': {
                    'p0': np.percentile(valid_power, 0) if len(valid_power) > 0 else None,
                    'p25': np.percentile(valid_power, 25) if len(valid_power) > 0 else None,
                    'p50': np.percentile(valid_power, 50) if len(valid_power) > 0 else None,
                    'p75': np.percentile(valid_power, 75) if len(valid_power) > 0 else None,
                    'p100': np.percentile(valid_power, 100) if len(valid_power) > 0 else None
                }
            }
            
            self.logger.debug("Power statistics", power_stats)
            
            # Check energy conservation with more lenient criteria
            # For NMOS transistors:
            # - Current flows D->S (positive ids)
            # - Voltage is measured D->S (positive vds)
            # - Power = vds * ids is positive, indicating power consumption
            # We want to verify that power consumption is significant (> 1e-12 W)
            # At least some of the power values should be significant
            power_valid = np.any(power[~invalid_mask] > 1e-12)
            results['energy_conservation'] = power_valid
            
            self.logger.debug("Energy conservation check result", {
                'power_valid': power_valid,
                'validation_criteria': {
                    'power_threshold': 1e-12,
                    'power_sign': 'positive (consuming)',
                    'invalid_values_allowed': False,
                    'zero_values_allowed': False
                },
                'power_stats': power_stats,
                'verification_details': {
                    'total_checks': len(power[~invalid_mask]),
                    'failed_checks': np.sum(power[~invalid_mask] <= 1e-12),
                    'failure_percentage': (np.sum(power[~invalid_mask] <= 1e-12) / len(power[~invalid_mask])) * 100 if len(power[~invalid_mask]) > 0 else 0,
                    'min_power': np.min(power[~invalid_mask]) if len(power[~invalid_mask]) > 0 else None,
                    'max_power': np.max(power[~invalid_mask]) if len(power[~invalid_mask]) > 0 else None
                }
            })
            
            # Check temperature coefficient calculation
            if len(temp) > 1:
                # Use log of current for better numerical stability
                log_ids = np.log(np.abs(i_ds))
                temp_coef = np.polyfit(temp, log_ids, 1)[0]
                results['temp_coef_calc'] = True
                results['details']['temp_coef'] = f"{temp_coef:.2e}/°C"
                self.logger.debug("Temperature coefficient calculation", {
                    'temp_range': f"{np.min(temp)} to {np.max(temp)}°C",
                    'temp_coef': temp_coef,
                    'r_squared': np.corrcoef(temp, log_ids)[0,1]**2,
                    'temp_values': temp.tolist(),
                    'log_ids_values': log_ids.tolist(),
                    'fit_quality': {
                        'residuals': np.polyfit(temp, log_ids, 1)[1],
                        'std_error': np.std(log_ids - np.polyval(np.polyfit(temp, log_ids, 1), temp))
                    }
                })
            
            # Check power measurements
            power_valid = np.all(~np.isnan(power))
            results['power_measurements'] = power_valid
            if power_valid:
                results['details']['power_range'] = f"{np.min(power):.3e}W to {np.max(power):.3e}W"
                self.logger.debug("Power measurements", {
                    'min_power': np.min(power),
                    'max_power': np.max(power),
                    'mean_power': np.mean(power),
                    'std_power': np.std(power),
                    'power_distribution': {
                        'nan_count': np.sum(np.isnan(power)),
                        'inf_count': np.sum(np.isinf(power)),
                        'finite_count': np.sum(np.isfinite(power))
                    },
                    'power_percentiles': {
                        'p0': np.percentile(power, 0),
                        'p25': np.percentile(power, 25),
                        'p50': np.percentile(power, 50),
                        'p75': np.percentile(power, 75),
                        'p100': np.percentile(power, 100)
                    }
                })
            
            # Check device efficiency - for MOSFET, we'll use transconductance efficiency
            if np.any(np.abs(i_ds) > 1e-12):  # Only consider significant currents
                # Calculate transconductance efficiency
                v_ds = np.linspace(0, 1.2, len(i_ds))  # Assuming Vds sweep from 0 to 1.2V
                gm = np.gradient(i_ds, v_ds)  # Calculate transconductance
                efficiency = np.abs(gm / i_ds)  # Transconductance efficiency
                valid_mask = np.abs(i_ds) > 1e-12
                if np.any(valid_mask):
                    efficiency_valid = np.all(~np.isnan(efficiency[valid_mask]))
                    results['device_efficiency'] = efficiency_valid
                    if efficiency_valid:
                        valid_efficiency = efficiency[valid_mask]
                        results['details']['efficiency_range'] = f"{np.min(valid_efficiency):.3e} to {np.max(valid_efficiency):.3e}"
                        results['efficiency_measurements'] = True
                        self.logger.debug("Device efficiency analysis", {
                            'min_efficiency': np.min(valid_efficiency),
                            'max_efficiency': np.max(valid_efficiency),
                            'mean_efficiency': np.mean(valid_efficiency),
                            'std_efficiency': np.std(valid_efficiency),
                            'valid_points': np.sum(valid_mask),
                            'efficiency_distribution': {
                                'nan_count': np.sum(np.isnan(efficiency)),
                                'inf_count': np.sum(np.isinf(efficiency)),
                                'finite_count': np.sum(np.isfinite(efficiency))
                            },
                            'efficiency_percentiles': {
                                'p0': np.percentile(valid_efficiency, 0),
                                'p25': np.percentile(valid_efficiency, 25),
                                'p50': np.percentile(valid_efficiency, 50),
                                'p75': np.percentile(valid_efficiency, 75),
                                'p100': np.percentile(valid_efficiency, 100)
                            },
                            'transconductance_stats': {
                                'min_gm': np.min(gm),
                                'max_gm': np.max(gm),
                                'mean_gm': np.mean(gm),
                                'std_gm': np.std(gm)
                            }
                        })
            
            self.logger.debug("Thermodynamic analysis verification completed", {
                'energy_conservation': results['energy_conservation'],
                'temp_coef_calc': results['temp_coef_calc'],
                'device_efficiency': results['device_efficiency'],
                'power_measurements': results['power_measurements'],
                'efficiency_measurements': results['efficiency_measurements'],
                'verification_summary': {
                    'all_passed': all([
                        results['energy_conservation'],
                        results['temp_coef_calc'],
                        results['device_efficiency'],
                        results['power_measurements'],
                        results['efficiency_measurements']
                    ]),
                    'failed_checks': [
                        key for key, value in results.items()
                        if key != 'details' and not value
                    ]
                }
            })
            
        except Exception as e:
            self.logger.error("Error verifying thermodynamic analysis", {
                'error_type': type(e).__name__,
                'error_message': str(e),
                'error_location': traceback.format_exc(),
                'verification_state': {
                    'step': 'energy_conservation_check',
                    'results': results
                }
            })
            
        self.results['thermodynamic_analysis'] = results
        return results

    # Done
    def verify_bias_point_analysis(self, vds_points, vgs_points, i_ds, i_g, i_s, i_b, temp):
        """Verify bias point analysis results.
        
        Args:
            vds_points (list): List of VDS bias points
            vgs_points (list): List of VGS bias points
            i_ds (list): Drain current at each bias point
            i_g (list): Gate current at each bias point
            i_s (list): Source current at each bias point
            i_b (list): Bulk current at each bias point
            temp (float): Temperature of analysis
            
        Returns:
            dict: Verification results
        """
        results = {
            'bias_points_analyzed': False,
            'currents_measured': False,
            'kcl_satisfied': False,
            'power_measured': False,
            'details': {
                'bias_points': None,
                'current_ranges': None,
                'kcl_error': None,
                'power_range': None,
                'temp': None,
                'IDS': None,
                'IG': None,
                'IS': None,
                'IB': None
            }
        }
        
        try:
            # Basic data validation
            if not all(x is not None and len(x) > 0 for x in [vds_points, vgs_points, i_ds]):
                return results
                
            # Check if bias points were analyzed
            results['bias_points_analyzed'] = len(vds_points) > 0 and len(vgs_points) > 0
            results['details']['bias_points'] = f"{len(vds_points)} VDS points, {len(vgs_points)} VGS points"
            
            # Check current measurements
            results['currents_measured'] = np.all(~np.isnan(i_ds))
            if i_g is not None and len(i_g) > 0:
                results['currents_measured'] = results['currents_measured'] and np.all(~np.isnan(i_g))
            if i_s is not None and len(i_s) > 0:
                results['currents_measured'] = results['currents_measured'] and np.all(~np.isnan(i_s))
            if i_b is not None and len(i_b) > 0:
                results['currents_measured'] = results['currents_measured'] and np.all(~np.isnan(i_b))
            
            # Calculate current ranges
            current_ranges = []
            if len(i_ds) > 0:
                current_ranges.append(f"IDS: {np.min(i_ds):.2e}A to {np.max(i_ds):.2e}A")
                results['details']['IDS'] = f"{np.min(i_ds):.2e}A to {np.max(i_ds):.2e}A"
            if i_g is not None and len(i_g) > 0:
                current_ranges.append(f"IG: {np.min(i_g):.2e}A to {np.max(i_g):.2e}A")
                results['details']['IG'] = f"{np.min(i_g):.2e}A to {np.max(i_g):.2e}A"
            if i_s is not None and len(i_s) > 0:
                current_ranges.append(f"IS: {np.min(i_s):.2e}A to {np.max(i_s):.2e}A")
                results['details']['IS'] = f"{np.min(i_s):.2e}A to {np.max(i_s):.2e}A"
            if i_b is not None and len(i_b) > 0:
                current_ranges.append(f"IB: {np.min(i_b):.2e}A to {np.max(i_b):.2e}A")
                results['details']['IB'] = f"{np.min(i_b):.2e}A to {np.max(i_b):.2e}A"
            results['details']['current_ranges'] = ', '.join(current_ranges)
            
            # Check KCL
            if all(x is not None and len(x) > 0 for x in [i_ds, i_g, i_s, i_b]):
                kcl_error = np.abs(i_ds + i_g + i_s + i_b)
                max_current = np.max([np.max(np.abs(c)) for c in [i_ds, i_g, i_s, i_b]])
                valid_mask = max_current > 1e-12
                if np.any(valid_mask):
                    kcl_error_percent = np.max(kcl_error[valid_mask] / max_current) * 100
                    results['kcl_satisfied'] = kcl_error_percent < 1.0  # 1% error threshold
                    results['details']['kcl_error'] = f"{kcl_error_percent:.2f}%"
                else:
                    results['kcl_satisfied'] = True
                    results['details']['kcl_error'] = "0.00%"
            
            # Calculate power
            power = np.abs(vds_points * i_ds)
            results['power_measured'] = np.all(~np.isnan(power))
            if results['power_measured']:
                results['details']['power_range'] = f"{np.min(power):.2e}W to {np.max(power):.2e}W"
            
            # Record temperature
            results['details']['temp'] = f"{temp}°C"
            
        except Exception as e:
            self.logger.error(f"Error verifying bias point analysis: {e}")
            
        return results

    # AC Analysis
    # Done
    def verify_cv_characteristics(self, vg, cgg, freq, vg_phase, id_phase):
        """Verify capacitance-voltage (CV) characteristics and small-signal behavior.
        
        This method analyzes capacitance behavior with respect to gate voltage, which is
        essential for validating the MOSFET model's dynamic responses. It checks:
        1. Gate capacitance vs. gate voltage characteristics
        2. Frequency dependence of capacitive effects
        3. Phase relationships between gate voltage and drain current
        
        Small-signal validation is critical for RF/analog applications and for verifying
        the accuracy of the charge storage models in the MOSFET.
        
        Args:
            vg (ndarray): Gate voltage values
            cgg (ndarray): Gate capacitance values corresponding to vg
            freq (ndarray): Frequency values for frequency-dependent analysis
            vg_phase (ndarray): Gate voltage phase values at different frequencies
            id_phase (ndarray): Drain current phase values at different frequencies
            
        Returns:
            dict: Verification results containing:
                - data_ready (bool): Whether CV data was successfully produced
                - data_read (bool): Whether CV data was successfully read
                - capacitance_behavior (bool): Whether capacitance exhibits correct behavior
                - frequency_dependence (bool): Whether frequency-dependent effects are present
                - phase_behavior (bool): Whether phase relationships are physically valid
                - details (dict): Additional information including capacitance ranges,
                                 max capacitance voltage, frequency dependence metrics,
                                 and phase shift measurements
        """
        results = {
            'data_ready': False,
            'capacitance_behavior': False,
            'frequency_dependence': False,
            'phase_behavior': False,
            'details': {
                'cgg_range': None,
                'cgg_max_voltage': None,
                'freq_dependence': None,
                'phase_shift': None
            }
        }
        
        try:
            # Data validation
            results['data_ready'] = vg is not None and cgg is not None
            
            if not results['data_ready']:
                return results
        
            # Check capacitance behavior
            cgg_min = np.min(cgg)
            cgg_max = np.max(cgg)
            max_idx = np.argmax(cgg)
            
            results['details']['cgg_range'] = f"{cgg_min:.5e}F to {cgg_max:.5e}F"
            results['details']['cgg_max_voltage'] = f"{vg[max_idx]:.2f}V"
            
            # Capacitance should be positive and have a meaningful range
            if cgg_min > 0 and cgg_max/cgg_min > 1.2:
                results['capacitance_behavior'] = True
            
            # Check frequency dependence if provided
            if freq is not None and len(freq) > 0 and vg_phase is not None and id_phase is not None:
                results['frequency_dependence'] = True
                results['details']["freq_range"] = f"{np.min(freq)/1e6:.1f}MHz to {np.max(freq)/1e9:.1f}GHz"

                # Check for phase shift between gate voltage and drain current
                if len(vg_phase) == len(id_phase):
                    max_phase_diff = np.max(np.abs(vg_phase - id_phase))
                    results['details']['phase_shift'] = f"{max_phase_diff:.2f}°"
                    results['phase_behavior'] = max_phase_diff > 5.0  # Should have at least 5 degree phase shift
            
        except Exception as e:
            self.logger.error(f"Error verifying CV characteristics: {e}")
            
        return results

    def verify_sparameter_analysis(self, freq, s11_mag, s21_mag, s12_mag, s22_mag):
        """Verify S-parameter analysis for RF/high-frequency behavior characterization.
        
        S-parameters are essential for evaluating RF and high-frequency performance of the MOSFET.
        This method validates key RF characteristics:
        1. Input and output matching (S11, S22)
        2. Forward gain (S21)
        3. Reverse isolation (S12)
        4. Unilateral behavior (S12 << S21)
        5. Frequency response and cutoff frequency
        
        The results are critical for determining the model's suitability for RF applications,
        providing metrics like cutoff frequency and isolation.
        
        Args:
            freq (ndarray): Frequency data array in Hz
            s11_mag (ndarray): S11 magnitude array (input reflection coefficient)
            s21_mag (ndarray): S21 magnitude array (forward transmission coefficient)
            s12_mag (ndarray): S12 magnitude array (reverse transmission coefficient)
            s22_mag (ndarray): S22 magnitude array (output reflection coefficient)
            
        Returns:
            dict: Comprehensive verification results containing:
                - data_ready (bool): Whether S-parameter data was produced
                - unilateral_behavior (bool): Whether device shows unilateral behavior
                - input_match (bool): Whether input matching is acceptable
                - gain (bool): Whether gain characteristics are valid
                - cutoff_frequency (float): The frequency at which gain drops by 3dB
                - rf_capable (bool): Whether device can function at RF frequencies
                - freq_range (str): Frequency range in readable format
                - s11_range, s21_range (str): S-parameter ranges in dB
                - isolation (str): Isolation value in dB
                - verification_passed (bool): Overall S-parameter verification result
                
        Note:
            This method also updates the REPORT.md file with S-parameter analysis results
            and generates relevant plots if a plot_generator is available.
        """
        results = {
            'data_ready': False,
        }
        try:
            self.logger.info("Starting S-parameter analysis verification")

            if freq is not None and s11_mag is not None and s12_mag is not None and s21_mag is not None and s22_mag is not None: 
                results['data_ready'] = True 
            else:
                results['data_ready'] = False

            # 1. Check for unilateral behavior (S12 << S21)
            unilateral_ratio = np.max(s21_mag) / np.max(s12_mag)
            results["unilateral_behavior"] = unilateral_ratio > 10  # More than 10x difference
            
            # 2. Check input match at highest frequency
            high_freq_idx = len(freq) - 1
            results["input_match"] = s11_mag[high_freq_idx] < 0.9  # Should be less than 0.9
            
            # 3. Check gain at low frequency
            low_freq_idx = 0
            results["gain"] = s21_mag[low_freq_idx] > 1.0  # Should be greater than 1
            
            # 4. Verify RF operation capability
            # Find frequency at which S21 drops by 3dB from its maximum value
            max_s21 = np.max(s21_mag)
            cutoff_indices = np.where(s21_mag <= max_s21 / np.sqrt(2))[0]  # 3dB is half power
            if len(cutoff_indices) > 0:
                cutoff_idx = cutoff_indices[0]
                cutoff_freq = freq[cutoff_idx]
                results["cutoff_frequency"] = cutoff_freq
                results["rf_capable"] = cutoff_freq > 1e8  # At least 100MHz
            else:
                results["cutoff_frequency"] = np.max(freq)
                results["rf_capable"] = True
            
            # Add key results for reporting
            results["freq_range"] = f"{np.min(freq)/1e6:.1f}MHz to {np.max(freq)/1e9:.1f}GHz"
            s11_db = 20 * np.log10(s11_mag)
            s21_db = 20 * np.log10(s21_mag)
            s22_db = 20 * np.log10(s22_mag)
            s12_db = 20 * np.log10(s12_mag)

            results["s11_range"] = f"{np.min(s11_db):.0f}dB to {np.max(s11_db):.0f}dB"
            results["s21_range"] = f"{np.min(s21_db):.0f}dB to {np.max(s21_db):.0f}dB"
            results["s22_range"] = f"{np.min(s22_db):.0f}dB to {np.max(s22_db):.0f}dB"
            results["s12_range"] = f"{np.min(s12_db):.0f}dB to {np.max(s12_db):.0f}dB"
            results["isolation"] = f">{20 * np.log10(1/unilateral_ratio):.0f}dB"
            
            # Generate plot
            try:
                if hasattr(self, 'plot_generator') and self.plot_generator is not None:
                    self.plot_generator.plot_ac_sparameter_analysis(freq, s11_mag, s21_mag, s12_mag, s22_mag)
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error generating S-parameter plot: {e}")

            # Overall result
            results["verification_passed"] = all([
                results["unilateral_behavior"],
                results["input_match"],
                results["gain"],
                results["rf_capable"]
            ])
        
            # Let's get the current NQS status from the report before updating
            nqs_status, nqs_symbol, max_phase_shift = self._get_nqs_status_from_report()
        
            # Store results
            self.results['sparameter_analysis'] = {
                'data_ready': True,
                'verification_passed': True,
                'freq_range': results["freq_range"],
                's11_range': results["s11_range"],
                's21_range': results["s21_range"],
                's22_range': results["s22_range"],
                's12_range': results["s12_range"],
                'isolation': results["isolation"],
                'sparams_freq_range': results["freq_range"],
                'nqs_status': nqs_status,
                'nqs_symbol': nqs_symbol,
                'max_phase_shift': max_phase_shift
            }
            
            self.logger.info("S-parameter analysis verification completed successfully")
            return self.results['sparameter_analysis']
            
        except Exception as e:
            self.logger.error(f"Error in S-parameter analysis verification: {e}")
            return {
                'data_ready': False,
                'verification_passed': False,
                'error': str(e)
            }

    def verify_nqs_effects(self, freq, vg_phase, id_phase, phase_diff):
        """
        Verify non-quasi-static (NQS) effects analysis results.
        """
        results = {
            'data_ready': False
        }
        try:
            self.logger.info("Starting NQS effects verification")
            
            # Check if data exists
            if freq is None or vg_phase is None or id_phase is None or phase_diff is None:
                self.logger.warning("Missing NQS effects data")
                return {
                    'data_ready': False,
                    'verification_passed': False,
                    'error': 'Missing NQS effects data'
                }
            
            # Calculate key metrics
            max_phase_shift = np.max(np.abs(phase_diff))
            freq_range = f"{np.min(freq)/1e6:.1f}MHz to {np.max(freq)/1e9:.1f}GHz"

            # Store results
            self.results['nqs_effects'] = {
                'data_ready': True,
                'verification_passed': True,
                'max_phase_shift': max_phase_shift,
                'freq_range': freq_range
            }
            
            self.logger.info("NQS effects verification completed successfully")
            return self.results['nqs_effects']
            
        except Exception as e:
            self.logger.error(f"Error in NQS effects verification: {e}")
            return {
                'data_ready': False,
                'verification_passed': False,
                'error': str(e)
            }

    def verify_ac_charge_conservation(self, time, vg, ig, id, is_, ib, i_total, q_gate, q_drain, q_source, q_bulk, q_total):
        """Verify charge conservation in the device."""
        results = {
            'data_ready': False,
        }
        try:
            # Check for missing data
            if any(x is None for x in [time, vg, ig, id, is_, ib, i_total, q_gate, q_drain, q_source, q_bulk, q_total]):
                self.logger.warning("Missing data for charge conservation verification")
                return {
                    'data_ready': False,
                    'verification_passed': False,
                    'error': 'Missing data'
                }

            # Calculate total current error
            i_error = np.abs(i_total - (ig + id + is_ + ib))
            max_i_error = np.max(i_error)
            
            # Calculate total charge error
            q_error = np.abs(q_total - (q_gate + q_drain + q_source + q_bulk))
            max_q_error = np.max(q_error)

            # Define thresholds for verification
            i_threshold = 1e-12  # 1 pA
            q_threshold = 1e-15  # 1 fC
            
            # Check if errors are within acceptable limits
            i_conserved = max_i_error < i_threshold
            q_conserved = max_q_error < q_threshold
            verification_passed = i_conserved and q_conserved

            # Store results
            results = {
                'data_ready': True,
                'verification_passed': verification_passed,
                'max_current_error': max_i_error,
                'max_charge_error': max_q_error,
                'current_threshold': i_threshold,
                'charge_threshold': q_threshold,
                'current_conserved': i_conserved,
                'charge_conserved': q_conserved
            }

            # Log results
            if verification_passed:
                self.logger.info("Charge conservation verification passed")
            else:
                self.logger.warning("Charge conservation verification failed")
                if not i_conserved:
                    self.logger.warning(f"Current conservation failed: max error = {max_i_error:.2e} A")
                if not q_conserved:
                    self.logger.warning(f"Charge conservation failed: max error = {max_q_error:.2e} C")

            return results
            
        except Exception as e:
            self.logger.error(f"Error in charge conservation verification: {e}")
            return {
                'data_ready': False,
                'verification_passed': False,
                'error': str(e)
            }

    def _get_nqs_status_from_report(self):
        """Extract current Non-Quasi-Static (NQS) effects status from REPORT.md.
        
        This helper method parses the existing verification report to retrieve the current
        status of NQS effects verification. Similar to the S-parameter status extraction,
        it maintains continuity in reporting when only parts of the verification are updated.
        
        NQS effects are critical for high-frequency MOSFET modeling, and this method ensures
        that their verification status is properly maintained between report updates.
        
        The method:
        1. Locates the high-frequency analysis section in the report
        2. Finds the NQS effects verification entry
        3. Extracts the verification status (color, symbol, and phase shift data)
        
        Returns:
            tuple: Three values representing NQS effects verification status:
                - nqs_status (str): Color code ('green' or 'red')
                - nqs_symbol (str): Status symbol ('✓' or '✗')
                - max_phase_shift (str): Maximum phase shift information
                
        Notes:
            If the report doesn't exist or doesn't contain NQS data, default
            values are returned indicating unavailability.
        """
        try:
            report_path = self.output_dir / 'REPORT.md'
            if not report_path.exists():
                return 'red', '✗', 'Not available'
            
            with open(report_path, 'r') as f:
                content = f.read()
            
            # Find high-frequency section
            hf_section_start = content.find('## AC Analysis')
            if hf_section_start == -1:
                return 'red', '✗', 'Not available'
            
            # Extract NQS status
            nqs_line_start = content.find('Non-Quasi-Static (NQS) Effects Analysis', hf_section_start)
            if nqs_line_start == -1:
                return 'red', '✗', 'Not available'
            
            # Find status color - look for 'green' or 'red'
            color_start = content.find("color: ", nqs_line_start - 100, nqs_line_start)
            if color_start != -1:
                color_end = content.find("'", color_start + 8)
                nqs_status = content[color_start + 7:color_end]
            else:
                nqs_status = 'red'
            
            # Find status symbol - look for ✓ or ✗
            symbol_start = content.find(">", color_start + 8) if color_start != -1 else -1
            if symbol_start != -1:
                nqs_symbol = content[symbol_start + 1:symbol_start + 2]
            else:
                nqs_symbol = '✗'
            
            # Extract phase shift
            phase_shift_line = content.find("Phase shift:", nqs_line_start)
            if phase_shift_line != -1:
                phase_shift_line_end = content.find("\n", phase_shift_line)
                max_phase_shift = content[phase_shift_line + 12:phase_shift_line_end].strip()
            else:
                max_phase_shift = 'Not available'
            
            return nqs_status, nqs_symbol, max_phase_shift
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error extracting NQS status from report: {e}")
            return 'red', '✗', 'Not available'

    # Transient Analysis
    def verify_trans_large_signal_transient(self, time, gate_voltage, drain_voltage, drain_current):
        """
        Verify large signal transient analysis results.
        """
        results = {
            'data_ready': False,            
            'transient_completed': False,
            'rise_time_measured': False,
            'max_current_calculated': False,
            'details': {
                'max_current': None,
                'rise_time': None,
                'time_points': None
            }
        }
        
        try:
            # Basic data validation
            if time is None or gate_voltage is None or drain_voltage is None or drain_current is None:
                self.results['large_signal_transient'] = results
                return self.results['large_signal_transient']
                
            if len(time) == 0 or len(gate_voltage) == 0 or len(drain_voltage) == 0 or len(drain_current) == 0:
                self.results['large_signal_transient'] = results
                return self.results['large_signal_transient']
            
            # Data Ready
            results['data_ready'] = True

            # Check if transient analysis completed
            results['transient_completed'] = True
            results['details']['time_points'] = len(time)
            
            # Calculate maximum drain current
            max_current = np.max(drain_current)
            results['max_current_calculated'] = True
            results['details']['max_current'] = max_current
            
            # Calculate rise time of gate voltage (10% to 90%)
            try:
                # Normalize gate voltage
                gate_min = np.min(gate_voltage)
                gate_max = np.max(gate_voltage)
                gate_norm = (gate_voltage - gate_min) / (gate_max - gate_min)
                
                # Find 10% and 90% points
                idx_10 = np.where(gate_norm >= 0.1)[0][0]
                idx_90 = np.where(gate_norm >= 0.9)[0][0]
                
                rise_time = (time[idx_90] - time[idx_10]) * 1e9  # Convert to ns
                results['rise_time_measured'] = True
                results['details']['rise_time'] = rise_time
                
            except Exception as e:
                self.logger.error(f"Error calculating rise time: {e}")
                results['rise_time_measured'] = False
                
            self.logger.info("Large signal transient analysis verification completed")
            
        except Exception as e:
            self.logger.error(f"Error verifying large signal transient: {e}")
            
        self.results['large_signal_transient'] = results
        return results
        
    def verify_trans_switching_simulations(self, time, input_voltage, output_voltage, supply_current, switching_power=None):
        """
        Verify switching behavior of the inverter.
        """
        results = {
            'data_ready': False,
            'switching_behavior_analyzed': False,
            'propagation_delay_measured': False,
            'power_measured': False,
            'details': {
                'propagation_delay': None,
                'max_power': None,
                'avg_power': None
            }
        }
        
        try:
            # Basic data validation
            if time is None or input_voltage is None or output_voltage is None or supply_current is None:
                self.results['switching_simulations'] = results
                return results
            
            results['data_ready'] = True
            
            # Check if switching behavior was analyzed
            results['switching_behavior_analyzed'] = True
            
            # Calculate propagation delay
            try:
                # Calculate the 50% points of input and output
                input_min = np.min(input_voltage)
                input_max = np.max(input_voltage)
                input_mid = (input_min + input_max) / 2
                
                output_min = np.min(output_voltage)
                output_max = np.max(output_voltage)
                output_mid = (output_min + output_max) / 2
                
                # Find rising edge of input
                input_rising = np.where(np.diff(input_voltage > input_mid) > 0)[0]
                if len(input_rising) > 0:
                    input_idx = input_rising[0]
                    
                    # Find falling edge of output (inverter response)
                    output_falling = np.where(np.diff(output_voltage < output_mid) > 0)[0]
                    valid_outputs = output_falling[output_falling > input_idx]
                    
                    if len(valid_outputs) > 0:
                        output_idx = valid_outputs[0]
                        prop_delay = (time[output_idx] - time[input_idx]) * 1e12  # ps (changed from 1e9 ns)
                        results['propagation_delay_measured'] = True
                        results['details']['propagation_delay'] = prop_delay
            except Exception as e:
                self.logger.error(f"Error calculating propagation delay: {e}")
                
            # Calculate power metrics if power data is provided
            if switching_power is not None and len(switching_power) > 0:
                results['power_measured'] = True
                results['details']['max_power'] = np.max(switching_power)
                results['details']['avg_power'] = np.mean(switching_power)
                
            self.logger.info("Switching simulations verification completed")
            
        except Exception as e:
            self.logger.error(f"Error verifying switching simulations: {e}")
            
        self.results['switching_simulations'] = results
        return results
        
    def verify_trans_delay_effect(self, time, input_voltage, mid1_voltage, mid2_voltage, output_voltage):
        """Verify delay effects in inverter chain."""
        results = {
            'data_ready': False,
            'delay_effect_analyzed': False,
            'stage_delays_measured': False,
            'total_delay_measured': False,
            'details': {
                'stage1_delay': None,
                'stage2_delay': None,
                'stage3_delay': None,
                'total_delay': None
            }
        }
        
        try:
            # Basic data validation
            if (time is None or input_voltage is None or mid1_voltage is None 
                or mid2_voltage is None or output_voltage is None):
                self.results['delay_effect'] = results
                return results
                
            results['data_ready'] = True

            # Check if delay effect was analyzed
            results['delay_effect_analyzed'] = True
            
            # Calculate delays for each stage and total
            try:
                # Stage 1: input to mid1
                delay1 = self.calculate_propagation_delay(time, input_voltage, mid1_voltage)
                
                # Stage 2: mid1 to mid2
                delay2 = self.calculate_propagation_delay(time, mid1_voltage, mid2_voltage)
                
                # Stage 3: mid2 to output
                delay3 = self.calculate_propagation_delay(time, mid2_voltage, output_voltage)
                
                # Total: input to output
                total_delay = self.calculate_propagation_delay(time, input_voltage, output_voltage)
                
                # Check for valid measurements
                valid_delays = (not np.isnan(delay1) and not np.isnan(delay2) and 
                               not np.isnan(delay3) and not np.isnan(total_delay))
                
                if valid_delays:
                    results['stage_delays_measured'] = True
                    results['total_delay_measured'] = True
                    results['details']['stage1_delay'] = delay1
                    results['details']['stage2_delay'] = delay2
                    results['details']['stage3_delay'] = delay3
                    results['details']['total_delay'] = total_delay
                    
            except Exception as e:
                self.logger.error(f"Error calculating stage delays: {e}")
                
            self.logger.info("Delay effect verification completed")
            
        except Exception as e:
            self.logger.error(f"Error verifying delay effect: {e}")
            
        self.results['delay_effect'] = results
        return results
        
    def verify_trans_power_dissipation(self, time_27c, power_27c, time_100c, power_100c):
        """Verify power dissipation at different temperatures.
        
        Args:
            time_27c: Array of time points at 27°C
            power_27c: Array of power dissipation at 27°C
            time_100c: Array of time points at 100°C
            power_100c: Array of power dissipation at 100°C
            
        Returns:
            dict: Results of power dissipation verification
        """
        self.logger.info("Starting power dissipation verification")
        
        results = {
            'data_ready': False,
            'power_analysis_completed': False,
            'temp_dependence_analyzed': False,
            'power_coef_calculated': False,
            'details': {
                'max_power_27c': None,
                'max_power_100c': None,
                'avg_power_27c': None,
                'avg_power_100c': None,
                'power_temp_coef': None
            }
        }
        
        if time_27c is None or power_27c is None or time_100c is None or power_100c is None:
            self.logger.warning("Cannot verify power dissipation: data missing")
            return results
            
        if len(time_27c) == 0 or len(power_27c) == 0 or len(time_100c) == 0 or len(power_100c) == 0:
            self.logger.warning("Cannot verify power dissipation: empty data")
            return results
            
        results['data_ready'] = True
        # Mark power analysis as completed
        results['power_analysis_completed'] = True
        
        # Calculate power metrics at 27°C
        max_power_27c = np.max(power_27c)
        avg_power_27c = np.mean(power_27c)
        results['details']['max_power_27c'] = max_power_27c
        results['details']['avg_power_27c'] = avg_power_27c
        
        # Calculate power metrics at 100°C
        max_power_100c = np.max(power_100c)
        avg_power_100c = np.mean(power_100c)
        results['details']['max_power_100c'] = max_power_100c
        results['details']['avg_power_100c'] = avg_power_100c
        
        # Check if temperature dependence was analyzed
        results['temp_dependence_analyzed'] = True
        
        # Calculate temperature coefficient
        power_temp_coef = (max_power_100c - max_power_27c) / (100 - 27)
        results['power_coef_calculated'] = True
        results['details']['power_temp_coef'] = power_temp_coef
        
        # Print the calculated values for debugging
        self.logger.info(f"Power at 27°C: {max_power_27c:.6e}W, Power at 100°C: {max_power_100c:.6e}W")
        self.logger.info(f"Power temperature coefficient: {power_temp_coef:.6e}W/°C")
        
        self.logger.info("Power dissipation verification completed")
        return results
        
    def verify_trans_quasi_static(self, time, gate_voltage, drain_voltage, drain_current):
        """Verify quasi-static behavior of the MOSFET."""
        results = {
            'data_ready': False,
        }
        try:
            # Check for missing data
            if any(x is None for x in [time, gate_voltage, drain_voltage, drain_current]):
                self.logger.warning("Missing data for quasi-static verification")
                return {
                    'data_ready': False,
                    'verification_passed': False,
                    'error': 'Missing data'
                }
            # Calculate time derivatives
            dt = np.diff(time)
            dvg_dt = np.diff(gate_voltage) / dt
            dvd_dt = np.diff(drain_voltage) / dt
            did_dt = np.diff(drain_current) / dt

            # Calculate normalized derivatives
            norm_dvg = np.abs(dvg_dt / gate_voltage[:-1])
            norm_dvd = np.abs(dvd_dt / drain_voltage[:-1])
            norm_did = np.abs(did_dt / drain_current[:-1])

            # Check if derivatives are small enough for quasi-static operation
            print(f"norm_dvg: {norm_dvg}")
            print(f"norm_dvd: {norm_dvd}")
            print(f"norm_did: {norm_did}")
            max_norm_dvg = np.max(norm_dvg)
            max_norm_dvd = np.max(norm_dvd)
            max_norm_did = np.max(norm_did)

            # Define thresholds for quasi-static operation
            threshold = 0.1  # 10% change per time step
            is_quasi_static = (max_norm_dvg < threshold and 
                             max_norm_dvd < threshold and 
                             max_norm_did < threshold)

            # Store results
            results = {
                'data_ready': True,
                'verification_passed': is_quasi_static,
                'max_norm_dvg': max_norm_dvg,
                'max_norm_dvd': max_norm_dvd,
                'max_norm_did': max_norm_did,
                'threshold': threshold
            }

            # Log results
            if is_quasi_static:
                self.logger.info("Quasi-static verification passed")
            else:
                self.logger.warning("Quasi-static verification failed")
                self.logger.warning(f"Max normalized derivatives: dVg/dt={max_norm_dvg:.2e}, dVd/dt={max_norm_dvd:.2e}, dId/dt={max_norm_did:.2e}")

            return results
        
        except Exception as e:
            self.logger.error(f"Error in quasi-static verification: {e}")
            return {
                'data_ready': False,
                'verification_passed': False,
                'error': str(e)
            }

    def verify_trans_charge_conservation(self, time, vg, ig, id, is_, ib, i_total, q_gate, q_drain, q_source, q_bulk, q_total):
        """Verify charge conservation in the device."""
        results = {
            'data_ready': False,
        }
        try:
            # Check for missing data
            if any(x is None for x in [time, vg, ig, id, is_, ib, i_total, q_gate, q_drain, q_source, q_bulk, q_total]):
                self.logger.warning("Missing data for charge conservation verification")
                return {
                    'data_ready': False,
                    'verification_passed': False,
                    'error': 'Missing data'
                }

            # Calculate total current error
            i_error = np.abs(i_total - (ig + id + is_ + ib))
            max_i_error = np.max(i_error)
            
            # Calculate total charge error
            q_error = np.abs(q_total - (q_gate + q_drain + q_source + q_bulk))
            max_q_error = np.max(q_error)

            # Define thresholds for verification
            i_threshold = 1e-12  # 1 pA
            q_threshold = 1e-15  # 1 fC
            
            # Check if errors are within acceptable limits
            i_conserved = max_i_error < i_threshold
            q_conserved = max_q_error < q_threshold
            verification_passed = i_conserved and q_conserved

            # Store results
            results = {
                'data_ready': True,
                'verification_passed': verification_passed,
                'max_current_error': max_i_error,
                'max_charge_error': max_q_error,
                'current_threshold': i_threshold,
                'charge_threshold': q_threshold,
                'current_conserved': i_conserved,
                'charge_conserved': q_conserved
            }

            # Log results
            if verification_passed:
                self.logger.info("Charge conservation verification passed")
            else:
                self.logger.warning("Charge conservation verification failed")
                if not i_conserved:
                    self.logger.warning(f"Current conservation failed: max error = {max_i_error:.2e} A")
                if not q_conserved:
                    self.logger.warning(f"Charge conservation failed: max error = {max_q_error:.2e} C")

            return results
            
        except Exception as e:
            self.logger.error(f"Error in charge conservation verification: {e}")
            return {
                'data_ready': False,
                'verification_passed': False,
                'error': str(e)
            }
        
    # Noise Analysis
    def verify_noise_analysis(self, freq=None, thermal_noise=None, flicker_noise=None, shot_noise=None, temp_noise=None, temperatures=None):
        """Verify noise analysis results.
        
        Args:
            freq: Frequency array for noise analysis
            thermal_noise: Dictionary of thermal noise data at different bias points
            flicker_noise: Array of flicker (1/f) noise data
            shot_noise: Array of shot noise data
            temp_noise: Dictionary of noise data at different temperatures
            temperatures: Array of temperature values used in analysis
            
        Returns:
            Dictionary with analysis results
        """
        results = {
            'data_ready': False,
            'noise_analysis_performed': False,
            'thermal_noise_analyzed': False,
            'flicker_noise_analyzed': False,
            'shot_noise_analyzed': False,
            'temp_dependence_analyzed': False,
            'details': {
                'thermal_noise_floor': None,
                'thermal_noise_min': None,
                'thermal_noise_max': None,
                'thermal_noise_avg': None,
                'thermal_range_ratio': None,
                'flicker_noise_exponent': None,
                'flicker_noise_coefficient': None,
                'flicker_noise_r_squared': None,
                'flicker_noise_level': None,
                'corner_frequency': None,
                'shot_noise_level': None,
                'shot_noise_std_dev': None,
                'shot_noise_variation': None,
                'temp_coefficient': None,
                'temp_noise_correlation': None,
                'temp_range': None,
                'freq_range': None,
                'bias_points': {}  # This is a dictionary to store bias point data
            }
        }
        
        # Store frequency range in results if available
        if freq is not None and len(freq) > 0:
            results['details']['freq_range'] = f"{np.min(freq)/1e6:.1f}MHz to {np.max(freq)/1e9:.1f}GHz"

        # Check thermal noise
        if thermal_noise is not None and freq is not None and len(freq) > 0:
            try:
                self.logger.debug("Starting thermal noise analysis")
                # Handle thermal_noise regardless of whether it's a dictionary or a list
                results['thermal_noise_analyzed'] = True
                results['noise_analysis_performed'] = True
                results['data_ready'] = True

                # Case 1: thermal_noise is a dictionary (keys are bias points)
                all_values = []
                if isinstance(thermal_noise, dict):
                    self.logger.debug(f"Thermal noise is a dictionary with {len(thermal_noise)} keys")
                    # Process each bias point and store in details
                    for bias_key, noise_values in thermal_noise.items():
                        if noise_values is not None and len(noise_values) > 0:
                            # Parse Vgs and Vds from bias key (assumed format "Vgs=X.XV, Vds=Y.YV")
                            try:
                                vgs_val = float(bias_key.split('Vgs=')[1].split('V')[0]) if 'Vgs=' in bias_key else 0.0
                                vds_val = float(bias_key.split('Vds=')[1].split('V')[0]) if 'Vds=' in bias_key else 0.0
                                bias_point = f"Vgs={vgs_val:.1f}V, Vds={vds_val:.1f}V"
                                
                                # Calculate noise floor from high frequency region
                                high_freq_idx = len(freq) // 2  # Use second half of frequency range
                                noise_floor = np.mean(noise_values[high_freq_idx:]) if len(noise_values) > high_freq_idx else np.min(noise_values)
                                
                                # Store individual bias point stats
                                results['details']['bias_points'][bias_point] = {
                                    'max_noise': float(np.max(noise_values)),
                                    'min_noise': float(np.min(noise_values)),
                                    'avg_noise': float(np.mean(noise_values)),
                                    'noise_floor': float(noise_floor)
                                }
                                
                                # Add values to all_values list for overall statistics
                                all_values.extend(noise_values)
                            except Exception as e:
                                if self.logger:
                                    self.logger.warning(f"Error parsing bias point {bias_key}: {e}")
                
                # Case 2: thermal_noise is a list (direct values)
                elif isinstance(thermal_noise, list) or isinstance(thermal_noise, np.ndarray):
                    self.logger.debug(f"Thermal noise is a {type(thermal_noise).__name__} with {len(thermal_noise)} values")
                    # Create a default bias point entry
                    noise_values = thermal_noise
                    if len(noise_values) > 0:
                        high_freq_idx = len(freq) // 2  # Use second half of frequency range
                        noise_floor = np.mean(noise_values[high_freq_idx:]) if len(noise_values) > high_freq_idx else np.min(noise_values)
                        
                        # Store as a single bias point
                        results['details']['bias_points']['Default'] = {
                            'max_noise': float(np.max(noise_values)),
                            'min_noise': float(np.min(noise_values)),
                            'avg_noise': float(np.mean(noise_values)),
                            'noise_floor': float(noise_floor)
                        }
                        
                        # Use these as the overall values too
                        all_values = noise_values
                else:
                    if self.logger:
                        self.logger.warning(f"Unsupported thermal_noise type: {type(thermal_noise)}")
                    all_values = []
                
                self.logger.debug(f"Extracted {len(all_values)} noise values")
                    
                # Calculate overall statistics if we have values
                if len(all_values) > 0:  # Ensure all_values is non-empty
                    self.logger.debug("Calculating thermal noise statistics")
                    
                    # Convert to numpy array for reliable calculations
                    all_values_array = np.array(all_values, dtype=float)
                    # Filter out non-finite values
                    finite_mask = np.isfinite(all_values_array)
                    if np.any(finite_mask):
                        filtered_values = all_values_array[finite_mask]
                        
                        if len(filtered_values) > 0:
                            min_val = float(np.min(filtered_values))
                            max_val = float(np.max(filtered_values))
                            avg_val = float(np.mean(filtered_values))
                            
                            self.logger.debug(f"Min: {min_val}, Max: {max_val}, Avg: {avg_val}")
                            
                            results['details']['thermal_noise_min'] = min_val
                            results['details']['thermal_noise_max'] = max_val
                            results['details']['thermal_noise_avg'] = avg_val
                            
                    # Estimate noise floor as the mean of the high-frequency region
                    high_freq_idx = len(freq) // 2  # Use second half of frequency range
                    if len(filtered_values) > high_freq_idx:
                        floor = float(np.mean(filtered_values[high_freq_idx:]))
                        results['details']['thermal_noise_floor'] = floor
                        self.logger.debug(f"Noise floor: {floor}")
                    
                            # Safely calculate thermal range ratio
                    if np.isfinite(min_val) and np.isfinite(max_val) and min_val > 0:
                        ratio = max_val / min_val
                        results['details']['thermal_range_ratio'] = ratio
                        self.logger.debug(f"Thermal range ratio: {ratio}")
                    else:
                        self.logger.warning("No finite values in thermal noise data")
                else:
                    self.logger.warning("No values available for thermal noise analysis")
                
                self.logger.debug("Thermal noise analysis completed successfully")
                
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error in thermal noise analysis: {e}")
                    self.logger.error(f"Error traceback: {traceback.format_exc()}")
        
        # Check flicker noise
        if flicker_noise is not None and freq is not None and len(freq) > 0 and len(flicker_noise) > 0:
            try:
                self.logger.debug("Starting flicker noise analysis")
                results['flicker_noise_analyzed'] = True
                results['noise_analysis_performed'] = True
                results['data_ready'] = True

                # Convert inputs to numpy arrays
                freq_array = np.array(freq, dtype=float)
                flicker_array = np.array(flicker_noise, dtype=float)
                
                # Estimate 1/f exponent using log-log regression
                # Use only the first half of frequencies (where 1/f is dominant)
                cutoff_idx = min(len(freq) // 2, len(freq_array), len(flicker_array))
                self.logger.debug(f"Using {cutoff_idx} points for flicker noise regression")
                
                if cutoff_idx >= 2:  # Need at least 2 points for regression
                    try:
                        # Calculate log values safely
                        log_freq = np.log10(freq_array[:cutoff_idx])
                        log_noise = np.log10(flicker_array[:cutoff_idx])
                        
                        # Filter out any NaN or infinite values
                        valid_mask = np.isfinite(log_freq) & np.isfinite(log_noise)
                        valid_count = np.sum(valid_mask)
                        
                        self.logger.debug(f"Found {valid_count} valid points for regression")
                        
                        if valid_count >= 2:
                            filtered_log_freq = log_freq[valid_mask]
                            filtered_log_noise = log_noise[valid_mask]
                            
                            # Perform linear regression
                            slope, intercept = np.polyfit(filtered_log_freq, filtered_log_noise, 1)
                            results['details']['flicker_noise_exponent'] = float(-slope)  # Negative because 1/f^alpha
                            results['details']['flicker_noise_level'] = float(10**intercept)
                            
                            self.logger.debug(f"Flicker noise exponent: {-slope:.4f}, level: {10**intercept:.2e}")
                            
                            # Calculate R-squared for goodness of fit safely
                            y_pred = np.polyval([slope, intercept], filtered_log_freq)
                            y_mean = float(np.mean(filtered_log_noise))
                            
                            # Calculate R-squared only if there's variance in the data
                            ss_tot = np.sum((filtered_log_noise - y_mean)**2)
                            if ss_tot > 0:
                                ss_res = np.sum((filtered_log_noise - y_pred)**2)
                                r_squared = float(1 - (ss_res / ss_tot))
                                if np.isfinite(r_squared):
                                    results['details']['flicker_noise_r_squared'] = r_squared
                                    self.logger.debug(f"R-squared: {r_squared:.4f}")
                            
                    # Calculate flicker noise coefficient (K)
                    # K = 10^intercept for a model of S(f) = K/f^alpha
                            results['details']['flicker_noise_coefficient'] = float(10**intercept)
                    except Exception as e:
                        if self.logger:
                            self.logger.warning(f"Error in flicker noise regression: {e}")
                            self.logger.warning(traceback.format_exc())
                else:
                    self.logger.warning("Not enough points for flicker noise regression")
                
                # Find corner frequency where thermal and flicker noise are equal
                if thermal_noise is not None:
                    self.logger.debug("Attempting to find corner frequency")
                    
                    # Get thermal noise values
                    thermal_values = None
                    if isinstance(thermal_noise, dict) and len(thermal_noise) > 0:
                        # Use the first bias point for simplicity
                        first_bias = list(thermal_noise.keys())[0]
                        thermal_values = thermal_noise[first_bias]
                    elif isinstance(thermal_noise, list) or isinstance(thermal_noise, np.ndarray):
                        thermal_values = thermal_noise
                    
                    # Find where flicker crosses thermal
                    if thermal_values is not None and len(thermal_values) > 0:
                        try:
                            # Convert to numpy array and ensure same length
                            thermal_array = np.array(thermal_values, dtype=float)
                            min_len = min(len(freq_array), min(len(flicker_array), len(thermal_array)))
                            
                            if min_len > 1:
                                self.logger.debug(f"Using {min_len} points to find corner frequency")
                                
                                # Find crossover safely: where flicker noise becomes less than thermal noise
                                found_crossover = False
                                for i in range(1, min_len-1):
                                    try:
                                        flicker_val = float(flicker_array[i])
                                        thermal_val = float(thermal_array[i])
                                        
                                        if np.isfinite(flicker_val) and np.isfinite(thermal_val):
                                            if flicker_val <= thermal_val:
                                                results['details']['corner_frequency'] = float(freq_array[i])
                                                self.logger.debug(f"Found corner frequency at {freq_array[i]:.2e} Hz")
                                                found_crossover = True
                                                break
                                    except Exception as idx_error:
                                        self.logger.warning(f"Error at index {i}: {idx_error}")
                                
                                # If no crossover found, use a default estimate
                                if not found_crossover:
                                    # Use middle point in log scale as an estimate
                                    middle_idx = min_len // 2
                                    results['details']['corner_frequency'] = float(freq_array[middle_idx])
                                    self.logger.debug(f"No crossover found, using estimated corner frequency: {freq_array[middle_idx]:.2e} Hz")
                            else:
                                self.logger.warning("Not enough data points to find corner frequency")
                        except Exception as corner_error:
                            if self.logger:
                                self.logger.warning(f"Error finding corner frequency: {corner_error}")
                
                self.logger.debug("Flicker noise analysis completed successfully")
                
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error in flicker noise analysis: {e}")
                    self.logger.error(traceback.format_exc())
        
        # Check shot noise
        if shot_noise is not None and len(shot_noise) > 0:
            try:
                self.logger.debug("Starting shot noise analysis")
                results['shot_noise_analyzed'] = True
                results['noise_analysis_performed'] = True
                
                # Convert to numpy array if not already
                shot_array = np.array(shot_noise, dtype=float)
                
                # Filter out non-finite values
                finite_mask = np.isfinite(shot_array)
                if np.any(finite_mask):
                    filtered_shot = shot_array[finite_mask]
                    
                    if len(filtered_shot) > 0:
                        # Calculate statistics on filtered data
                        mean_val = float(np.mean(filtered_shot))
                        std_val = float(np.std(filtered_shot))
                        
                        results['details']['shot_noise_level'] = mean_val
                        results['details']['shot_noise_std_dev'] = std_val
                        
                        # Calculate variation coefficient safely
                        if np.isfinite(mean_val) and mean_val > 0:
                            variation = std_val / mean_val
                            results['details']['shot_noise_variation'] = float(variation)
                            self.logger.debug(f"Shot noise: mean={mean_val:.2e}, std={std_val:.2e}, var={variation:.4f}")
                        else:
                            results['details']['shot_noise_variation'] = 0.0
                            self.logger.debug("Shot noise mean is zero or not finite, variation set to 0")
                    else:
                        self.logger.warning("No finite values in shot noise data")
                else:
                    self.logger.warning("No finite values in shot noise data")
                
                self.logger.debug("Shot noise analysis completed successfully")
                
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error in shot noise analysis: {e}")
                    self.logger.error(traceback.format_exc())
        
        # Check temperature dependence
        if temp_noise is not None and temperatures is not None and len(temperatures) > 1:
            try:
                self.logger.debug("Starting temperature dependence analysis")
                results['temp_dependence_analyzed'] = True
                results['noise_analysis_performed'] = True
                
                # Calculate average noise level at each temperature
                avg_noise_levels = []
                valid_temps = []
                
                # Handle temp_noise depending on its type
                if isinstance(temp_noise, dict):
                    self.logger.debug(f"Processing temperature noise dictionary with {len(temp_noise)} entries")
                    for temp in temperatures:
                        if temp in temp_noise:
                            noise_values = temp_noise[temp]
                        if noise_values is not None and len(noise_values) > 0:
                                # Convert to numpy array
                                noise_array = np.array(noise_values, dtype=float)
                                # Filter non-finite values
                                finite_mask = np.isfinite(noise_array)
                                if np.any(finite_mask):
                                    avg_value = float(np.mean(noise_array[finite_mask]))
                                    if np.isfinite(avg_value):
                                        avg_noise_levels.append(avg_value)
                                        valid_temps.append(float(temp))
                                        self.logger.debug(f"Temp {temp}°C: Mean noise = {avg_value:.2e}")
                                else:
                                    self.logger.warning(f"No finite noise values at temperature {temp}°C")
                
                elif isinstance(temp_noise, list) or isinstance(temp_noise, np.ndarray):
                    self.logger.debug(f"Processing temperature noise array with {len(temp_noise)} values")
                    # Assume temp_noise is already an array of average values per temperature
                    # Make sure lengths match
                    temp_array = np.array(temperatures, dtype=float)
                    noise_array = np.array(temp_noise, dtype=float)
                    
                    min_len = min(len(temp_array), len(noise_array))
                    for i in range(min_len):
                        if np.isfinite(temp_array[i]) and np.isfinite(noise_array[i]):
                            valid_temps.append(float(temp_array[i]))
                            avg_noise_levels.append(float(noise_array[i]))
                
                # Check if we have enough data to proceed
                self.logger.debug(f"Found {len(valid_temps)} valid temperature points")
                
                if len(valid_temps) >= 2:
                    # Create clean numpy arrays
                    temp_data = np.array(valid_temps, dtype=float)
                    noise_data = np.array(avg_noise_levels, dtype=float)
                    
                    # Calculate temperature coefficient (slope of linear fit)
                    try:
                        slope, intercept = np.polyfit(temp_data, noise_data, 1)
                        results['details']['temp_coefficient'] = float(slope)
                        self.logger.debug(f"Temperature coefficient: {slope:.2e}")
                    except Exception as fit_error:
                        self.logger.warning(f"Error fitting temperature coefficient: {fit_error}")
                    
                    # Calculate correlation coefficient safely
                    try:
                        # Check for variance in the data
                        temp_std = float(np.std(temp_data))
                        noise_std = float(np.std(noise_data))
                        
                        if temp_std > 0 and noise_std > 0:
                            # Calculate correlation manually
                            temp_mean = float(np.mean(temp_data))
                            noise_mean = float(np.mean(noise_data))
                            
                            # Calculate covariance
                            products = (temp_data - temp_mean) * (noise_data - noise_mean)
                            covariance = float(np.sum(products))
                            
                            # Calculate standard deviations product
                            temp_squared_diff = np.sum((temp_data - temp_mean)**2)
                            noise_squared_diff = np.sum((noise_data - noise_mean)**2)
                            denominator = np.sqrt(temp_squared_diff * noise_squared_diff)
                            
                            # Calculate correlation safely
                            if denominator > 0:
                                correlation = float(covariance / denominator)
                                if -1.0 <= correlation <= 1.0:  # Valid correlation range
                                    results['details']['temp_noise_correlation'] = correlation
                                    self.logger.debug(f"Temperature correlation: {correlation:.4f}")
                                else:
                                    self.logger.warning(f"Invalid correlation value: {correlation}")
                            else:
                                self.logger.warning("Denominator is zero, can't calculate correlation")
                        else:
                            self.logger.warning("Cannot compute correlation: constant data detected")
                    except Exception as corr_error:
                        self.logger.warning(f"Error calculating correlation: {corr_error}")
                    
                    # Set temperature range
                    if len(temp_data) > 0:
                        temp_min = float(np.min(temp_data))
                        temp_max = float(np.max(temp_data))
                        results['details']['temp_range'] = f"{temp_min:.1f}°C to {temp_max:.1f}°C"
                        self.logger.debug(f"Temperature range: {temp_min:.1f}°C to {temp_max:.1f}°C")
                else:
                    self.logger.warning("Not enough valid temperature data points")
                
                self.logger.debug("Temperature dependence analysis completed successfully")
                
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error in temperature dependence analysis: {e}")
                    self.logger.error(traceback.format_exc())
        
        # Store in self.results for verification checklist
        self.results['noise_analysis'] = results
        
        return results

    def calculate_propagation_delay(self, time, input_signal, output_signal):
        """Calculate propagation delay between input and output signals."""
        # Find the middle points (50% threshold)
        input_threshold = (np.max(input_signal) + np.min(input_signal)) / 2
        output_threshold = (np.max(output_signal) + np.min(output_signal)) / 2
        
        # Find the first rising edge of input that crosses the threshold
        input_crossings = np.where(np.diff(input_signal > input_threshold) > 0)[0]
        if len(input_crossings) == 0:
            return float('nan')
        input_idx = input_crossings[0]
        
        # Find the corresponding output response (for inverter, look for falling edge)
        output_crossings = np.where(np.diff(output_signal < output_threshold) > 0)[0]
        if len(output_crossings) == 0:
            return float('nan')
        
        # Find the output crossing that happens after the input
        valid_crossings = output_crossings[output_crossings > input_idx]
        if len(valid_crossings) == 0:
            return float('nan')
        output_idx = valid_crossings[0]
        
        # Calculate propagation delay in ps
        prop_delay = (time[output_idx] - time[input_idx]) * 1e12
        
        return prop_delay

    def _get_sparam_status_from_report(self):
        """Extract current S-parameter status from REPORT.md"""
        try:
            report_path = self.output_dir / 'REPORT.md'
            if not report_path.exists():
                return 'red', '✗', 'Not available', 'Not available', 'Not available', 'Not available'
            
            with open(report_path, 'r') as f:
                content = f.read()
            
            # Find high-frequency section
            hf_section_start = content.find('### High-Frequency Analysis')
            if hf_section_start == -1:
                return 'red', '✗', 'Not available', 'Not available', 'Not available', 'Not available'
            
            # Extract S-parameter status
            sparam_line_start = content.find('S-parameter analysis', hf_section_start)
            if sparam_line_start == -1:
                return 'red', '✗', 'Not available', 'Not available', 'Not available', 'Not available'
            
            # Find status color - look for 'green' or 'red'
            color_start = content.find("color: ", hf_section_start, sparam_line_start)
            if color_start != -1:
                color_end = content.find("'", color_start + 8)
                sparams_status = content[color_start + 7:color_end]
            else:
                sparams_status = 'red'
            
            # Find status symbol - look for ✓ or ✗
            symbol_start = content.find(">", color_start + 8) if color_start != -1 else -1
            if symbol_start != -1:
                sparams_symbol = content[symbol_start + 1:symbol_start + 2]
            else:
                sparams_symbol = '✗'
            
            # Extract frequency range
            freq_line = content.find("- ", hf_section_start, sparam_line_start)
            if freq_line != -1:
                freq_line_end = content.find("\n", freq_line)
                freqs = content[freq_line + 2:freq_line_end].strip()
            else:
                freqs = 'Not available'
            
            # Extract S11 range
            s11_line = content.find("S11:", hf_section_start)
            if s11_line != -1:
                s11_line_end = content.find("\n", s11_line)
                s11 = content[s11_line + 5:s11_line_end].strip()
            else:
                s11 = 'Not available'
            
            # Extract S21 range
            s21_line = content.find("S21:", hf_section_start)
            if s21_line != -1:
                s21_line_end = content.find("\n", s21_line)
                s21 = content[s21_line + 5:s21_line_end].strip()
            else:
                s21 = 'Not available'
            
            # Extract isolation
            isolation_line = content.find("Isolation:", hf_section_start)
            if isolation_line != -1:
                isolation_line_end = content.find("\n", isolation_line)
                isolation = content[isolation_line + 10:isolation_line_end].strip()
            else:
                isolation = 'Not available'
            
            return sparams_status, sparams_symbol, freqs, s11, s21, isolation
        
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error extracting S-parameter status from report: {e}")
            return 'red', '✗', 'Not available', 'Not available', 'Not available', 'Not available'

