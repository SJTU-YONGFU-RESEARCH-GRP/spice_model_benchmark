import os
import subprocess
from pathlib import Path

class SimulationRunner:
    """Handles running SPICE simulations and managing output files."""
    def __init__(self, logger, output_dir='results', 
                 dc_circuit_file=None, transient_circuit_file=None, 
                 noise_circuit_file=None, ac_circuit_file=None):
        self.logger = logger
        self.output_dir = output_dir
        
        # Store circuit file paths directly
        self.dc_circuit_file = dc_circuit_file
        self.transient_circuit_file = transient_circuit_file
        self.noise_circuit_file = noise_circuit_file
        self.ac_circuit_file = ac_circuit_file
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Create data subdirectory for all simulation output files
        self.data_dir = os.path.join(output_dir, 'data')
        os.makedirs(self.data_dir, exist_ok=True)
        
    def run_simulation(self, circuit_file):
        """Run the SPICE simulation.
        
        Args:
            circuit_file: Path to the circuit file to run
            
        Returns:
            bool: True if simulation was successful, False otherwise
        """
        try:
            self.logger.logger.info(f"Starting SPICE simulation for {os.path.basename(circuit_file)}")
            
            # Get absolute paths
            circuit_path = os.path.abspath(circuit_file)
            output_path = os.path.abspath(self.output_dir)
            data_path = os.path.abspath(self.data_dir)
            
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
                
                # Move output files to data subdirectory
                for filename in os.listdir(circuit_dir):
                    # Check if the file is a SPICE output file (text format)
                    if (filename.startswith('iv_data_') or 
                        filename == 'cv_data.txt' or 
                        filename.startswith('charge_conservation') or
                        filename.startswith('sparams_data') or
                        filename.startswith('nqs_effects') or
                        filename == 'bias_point_data.txt' or
                        filename.startswith('tran_') or
                        filename.startswith('thermal_noise_') or
                        filename.startswith('flicker_noise') or
                        filename.startswith('shot_noise') or
                        filename.startswith('noise_temp')):
                        
                        src = os.path.join(circuit_dir, filename)
                        
                        # For all text files, store them in the data subdirectory
                        dst = os.path.join(data_path, filename)
                            
                        if os.path.exists(src):
                            self.logger.logger.info(f"Moving {filename} to data directory")
                            os.rename(src, dst)
                
                # Handle raw files separately to store in data directory too
                for filename in os.listdir(circuit_dir):
                    if filename.endswith('.raw'):
                        src = os.path.join(circuit_dir, filename)
                        dst = os.path.join(data_path, filename)
                        
                        if os.path.exists(src):
                            self.logger.logger.info(f"Moving raw file {filename} to data directory")
                            os.rename(src, dst)
                
                self.logger.logger.info(f"Simulation for {os.path.basename(circuit_file)} completed successfully")
                return True
                
            finally:
                # Always return to original directory
                os.chdir(original_dir)
            
        except Exception as e:
            self.logger.logger.error(f"Error running SPICE simulation: {e}")
            return False
    
    def run_dc_simulation(self):
        """Run DC analysis simulation.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not os.path.exists(self.dc_circuit_file):
            self.logger.logger.error(f"DC circuit file not found: {self.dc_circuit_file}")
            return False
            
        self.logger.logger.info("Starting DC analysis simulation")
        return self.run_simulation(self.dc_circuit_file)
    
    def run_ac_simulation(self):
        """Run AC analysis simulations including CV characteristics and S-parameters.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not os.path.exists(self.ac_circuit_file):
            self.logger.logger.error(f"AC circuit file not found: {self.ac_circuit_file}")
            return False
            
        self.logger.logger.info("Starting AC analysis simulation")
        return self.run_simulation(self.ac_circuit_file)
            
    def run_transient_simulation(self):
        """Run transient analysis simulations.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not os.path.exists(self.transient_circuit_file):
            self.logger.logger.error(f"Transient circuit file not found: {self.transient_circuit_file}")
            return False
            
        self.logger.logger.info("Starting transient analysis simulation")
        return self.run_simulation(self.transient_circuit_file)
            
    def run_noise_simulation(self):
        """Run the dedicated noise analysis simulation.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not os.path.exists(self.noise_circuit_file):
            self.logger.logger.error(f"Noise circuit file not found: {self.noise_circuit_file}")
            return False
            
        self.logger.logger.info("Starting dedicated noise analysis simulation")
        return self.run_simulation(self.noise_circuit_file)
        
    def run_all_simulations(self):
        """Run all simulations sequentially: DC, AC, transient, and noise circuit files.
        
        Returns:
            bool: True if all simulations succeeded, False if any failed
        """
        # First run the DC circuit simulation (IV characteristics, bias point analysis)
        if not self.run_dc_simulation():
            self.logger.logger.error("DC circuit simulation failed")
            return False
        
        # Run the AC circuit simulation (CV characteristics, S-parameters)
        if self.ac_circuit_file and os.path.exists(self.ac_circuit_file):
            if not self.run_ac_simulation():
                self.logger.logger.error("AC circuit simulation failed")
                return False
            
        # Then run the transient circuit simulation
        if not self.run_transient_simulation():
            self.logger.logger.error("Transient circuit simulation failed")
            return False
            
        # Finally run the noise analysis
        if not self.run_noise_simulation():
            self.logger.logger.error("Noise analysis simulation failed")
            return False
            
        self.logger.logger.info("All simulations completed successfully")
        return True
