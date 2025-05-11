import os
import subprocess
from pathlib import Path

class SimulationRunner:
    """Handles running SPICE simulations and managing output files."""
    def __init__(self, circuit_file, logger, output_dir='results'):
        self.circuit_file = circuit_file
        self.logger = logger
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
    def run_simulation(self):
        """Run the SPICE simulation."""
        try:
            self.logger.logger.info("Starting SPICE simulation")
            
            # Get absolute paths
            circuit_path = os.path.abspath(self.circuit_file)
            output_path = os.path.abspath(self.output_dir)
            
            # Save current directory
            original_dir = os.getcwd()
            
            try:
                # Change to the circuit file directory
                circuit_dir = os.path.dirname(circuit_path)
                os.chdir(circuit_dir)
                
                # Run ngspice
                cmd = ['ngspice', '-b', os.path.basename(circuit_path)]
                self.logger.logger.info(f"Running command: {' '.join(cmd)}")
                
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                
                # Log output
                if stdout:
                    self.logger.logger.info(f"Simulation output: {stdout.decode()}")
                if stderr:
                    self.logger.logger.warning(f"Simulation warnings: {stderr.decode()}")
                
                # Check for errors
                if process.returncode != 0:
                    self.logger.logger.error(f"SPICE simulation failed: {stderr.decode()}")
                    return False
                
                # Move output files to results directory
                for filename in os.listdir(circuit_dir):
                    if filename.startswith('iv_data_') or filename == 'cv_data.txt':
                        src = os.path.join(circuit_dir, filename)
                        dst = os.path.join(output_path, filename)
                        if os.path.exists(src):
                            self.logger.logger.info(f"Moving {filename} to results directory")
                            os.rename(src, dst)
                
                self.logger.logger.info("Simulation completed successfully")
                return True
                
            finally:
                # Always return to original directory
                os.chdir(original_dir)
            
        except Exception as e:
            self.logger.logger.error(f"Error running SPICE simulation: {e}")
            return False

    def run_bias_point_analysis(self, vds_points=None, vgs_points=None, temp=27):
        """Run bias point analysis at specified operating points.
        
        Args:
            vds_points (list): List of VDS bias points to analyze
            vgs_points (list): List of VGS bias points to analyze
            temp (float): Temperature in Celsius for the analysis
            
        Returns:
            bool: True if analysis completed successfully, False otherwise
        """
        try:
            self.logger.logger.info("Starting bias point analysis")
            
            # Default bias points if none provided
            if vds_points is None:
                vds_points = [0.0, 0.6, 1.2]  # Typical bias points
            if vgs_points is None:
                vgs_points = [0.0, 0.6, 1.2]  # Typical bias points
            
            # Get absolute paths
            circuit_path = os.path.abspath(self.circuit_file)
            output_path = os.path.abspath(self.output_dir)
            
            # Save current directory
            original_dir = os.getcwd()
            
            try:
                # Change to the circuit file directory
                circuit_dir = os.path.dirname(circuit_path)
                os.chdir(circuit_dir)
                
                # Create temporary netlist for bias point analysis
                with open(circuit_path, 'r') as f:
                    netlist_lines = f.readlines()
                
                # Find the .end line
                end_index = -1
                for i, line in enumerate(netlist_lines):
                    if line.strip().lower() == '.end':
                        end_index = i
                        break
                
                if end_index == -1:
                    raise ValueError("Could not find .end in netlist")
                
                # Add bias point analysis commands before .end
                bias_commands = []
                for vds in vds_points:
                    for vgs in vgs_points:
                        bias_commands.append(f".dc Vds_bias {vds} {vds} 1 Vgs_bias {vgs} {vgs} 1")
                        bias_commands.append(f".temp {temp}")
                        bias_commands.append(f".print dc v(drain_bias) v(gate_bias) i(Vds_bias) i(Vgs_bias) i(Vs_bias) i(Vb_bias)")
                
                # Insert commands before .end
                modified_netlist = netlist_lines[:end_index] + bias_commands + netlist_lines[end_index:]
                
                # Write modified netlist
                temp_netlist = os.path.join(circuit_dir, 'bias_point_analysis.cir')
                with open(temp_netlist, 'w') as f:
                    f.writelines(modified_netlist)
                
                # Run ngspice with modified netlist
                cmd = ['ngspice', '-b', 'bias_point_analysis.cir']
                self.logger.logger.info(f"Running bias point analysis: {' '.join(cmd)}")
                
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                
                # Log output
                if stdout:
                    self.logger.logger.info(f"Bias point analysis output: {stdout.decode()}")
                if stderr:
                    self.logger.logger.warning(f"Bias point analysis warnings: {stderr.decode()}")
                
                # Check for errors
                if process.returncode != 0:
                    self.logger.logger.error(f"Bias point analysis failed: {stderr.decode()}")
                    return False
                
                # Move output files to results directory
                for filename in os.listdir(circuit_dir):
                    if filename.startswith('bias_point_data_'):
                        src = os.path.join(circuit_dir, filename)
                        dst = os.path.join(output_path, filename)
                        if os.path.exists(src):
                            self.logger.logger.info(f"Moving {filename} to results directory")
                            os.rename(src, dst)
                
                # Clean up temporary netlist
                if os.path.exists(temp_netlist):
                    os.remove(temp_netlist)
                
                self.logger.logger.info("Bias point analysis completed successfully")
                return True
                
            finally:
                # Always return to original directory
                os.chdir(original_dir)
            
        except Exception as e:
            self.logger.logger.error(f"Error running bias point analysis: {e}")
            return False 