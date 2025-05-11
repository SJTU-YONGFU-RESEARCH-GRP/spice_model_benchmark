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
                    # Move IV and CV data files
                    if filename.startswith('iv_data_') or filename == 'cv_data.txt':
                        src = os.path.join(circuit_dir, filename)
                        dst = os.path.join(output_path, filename)
                        if os.path.exists(src):
                            self.logger.logger.info(f"Moving {filename} to results directory")
                            os.rename(src, dst)
                    
                    # Also move transient data files
                    if filename.startswith('tran_'):
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
