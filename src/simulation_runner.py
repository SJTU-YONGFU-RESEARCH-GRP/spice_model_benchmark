import os
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Union, Set
import shutil


class SimulationRunner:
    """Handles running SPICE simulations and managing output files.
    
    This class provides methods to run different types of SPICE simulations
    (DC, AC, transient, and noise) and handles the output file management
    by automatically moving results to the appropriate data directory.
    
    Attributes:
        logger: Logger instance for recording simulation activities
        output_dir: Directory where simulation results will be stored
        data_dir: Subdirectory for simulation data files
        dc_circuit_file: Path to the DC analysis circuit file
        ac_circuit_file: Path to the AC analysis circuit file
        transient_circuit_file: Path to the transient analysis circuit file
        noise_circuit_file: Path to the noise analysis circuit file
    """
    
    # Define file patterns that should be moved to the data directory
    OUTPUT_FILE_PATTERNS: Set[str] = {
        'iv_data_', 'cv_data.txt', 'charge_conservation', 'sparams_data',
        'nqs_effects', 'bias_point_data.txt', 'tran_', 'thermal_noise_',
        'flicker_noise', 'shot_noise', 'noise_temp'
    }
    
    def __init__(self, 
                 logger,
                 output_dir: str = 'results',
                 dc_circuit_file: Optional[str] = None,
                 transient_circuit_file: Optional[str] = None,
                 noise_circuit_file: Optional[str] = None,
                 ac_circuit_file: Optional[str] = None) -> None:
        """Initialize the simulation runner with circuit files and output directory.
        
        Args:
            logger: Logger instance for simulation output
            output_dir: Directory to store simulation results (default: 'results')
            dc_circuit_file: Path to the DC analysis circuit file
            transient_circuit_file: Path to the transient analysis circuit file
            noise_circuit_file: Path to the noise analysis circuit file
            ac_circuit_file: Path to the AC analysis circuit file
        """
        self.logger = logger
        self.output_dir = output_dir
        
        # Convert all paths to Path objects for consistency
        self.dc_circuit_file = Path(dc_circuit_file) if dc_circuit_file else None
        self.transient_circuit_file = Path(transient_circuit_file) if transient_circuit_file else None
        self.noise_circuit_file = Path(noise_circuit_file) if noise_circuit_file else None
        self.ac_circuit_file = Path(ac_circuit_file) if ac_circuit_file else None
        
        # Create output directory structure with absolute path
        self.output_dir_path = Path(output_dir).resolve()
        self.output_dir_path.mkdir(exist_ok=True)
        
        # Create data subdirectory for all simulation output files
        self.data_dir = self.output_dir_path / 'data'
        self.data_dir.mkdir(exist_ok=True)
        
    def run_simulation(self, circuit_file: Union[str, Path]) -> bool:
        """Run the SPICE simulation.
        
        Args:
            circuit_file: Path to the circuit file to run
            
        Returns:
            bool: True if simulation was successful, False otherwise
        """
        try:
            circuit_file_path = Path(circuit_file)
            if not circuit_file_path.exists():
                self.logger.logger.error(f"Circuit file not found: {circuit_file_path}")
                return False
                
            self.logger.logger.info(f"Starting SPICE simulation for {circuit_file_path.name}")
            
            # Get absolute paths
            circuit_path = circuit_file_path.absolute()
            circuit_dir = circuit_path.parent
            
            # Save current directory
            original_dir = Path.cwd()
            
            try:
                # Change to the circuit file directory
                os.chdir(circuit_dir)
                
                # Run ngspice
                cmd = ['ngspice', '-b', circuit_path.name]
                self.logger.logger.info(f"Running command: {' '.join(cmd)}")
                
                process = subprocess.Popen(
                    cmd, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    text=True  # Get strings instead of bytes
                )
                stdout, stderr = process.communicate()
                
                # Log output
                if stdout:
                    self.logger.logger.info(f"Simulation output: {stdout}")
                if stderr:
                    self.logger.logger.warning(f"Simulation warnings: {stderr}")
                
                # Check for errors
                if process.returncode != 0:
                    self.logger.logger.error(f"SPICE simulation failed with return code {process.returncode}: {stderr}")
                    return False
                
                # Move output files to data subdirectory
                self._move_output_files(circuit_dir)
                
                self.logger.logger.info(f"Simulation for {circuit_path.name} completed successfully")
                return True
                
            finally:
                # Always return to original directory
                os.chdir(original_dir)
            
        except Exception as e:
            self.logger.logger.error(f"Error running SPICE simulation: {e}", exc_info=True)
            return False
    
    def _move_output_files(self, source_dir: Union[str, Path]) -> None:
        """Move output files from source directory to data directory.
        
        Args:
            source_dir: Directory containing simulation output files
        """
        source_path = Path(source_dir)
        
        # First, handle text output files
        for filename in os.listdir(source_path):
            # Check if the file matches any of our output patterns
            if any(pattern in filename for pattern in self.OUTPUT_FILE_PATTERNS):
                src_file = source_path / filename
                dst_file = self.data_dir / filename
                self._move_file(src_file, dst_file)
        
        # Then handle raw files
        for filename in os.listdir(source_path):
            if filename.endswith('.raw'):
                src_file = source_path / filename
                dst_file = self.data_dir / filename
                self._move_file(src_file, dst_file)
    
    def _move_file(self, src: Path, dst: Path) -> None:
        """Safely move a file with proper error handling.
        
        Args:
            src: Source file path
            dst: Destination file path
        """
        try:
            if src.exists():
                self.logger.logger.info(f"Moving {src.name} to data directory")
                # Create destination directory if it doesn't exist
                dst.parent.mkdir(exist_ok=True, parents=True)
                # Use shutil.move instead of os.rename for better cross-device support
                shutil.move(str(src), str(dst))
            else:
                self.logger.logger.warning(f"Source file not found: {src}")
        except Exception as e:
            self.logger.logger.warning(f"Failed to move file {src.name}: {e}")
    
    def run_dc_simulation(self) -> bool:
        """Run DC analysis simulation.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.dc_circuit_file or not self.dc_circuit_file.exists():
            self.logger.logger.error(f"DC circuit file not found: {self.dc_circuit_file}")
            return False
            
        self.logger.logger.info("Starting DC analysis simulation")
        return self.run_simulation(self.dc_circuit_file)
    
    def run_ac_simulation(self) -> bool:
        """Run AC analysis simulations including CV characteristics and S-parameters.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.ac_circuit_file or not self.ac_circuit_file.exists():
            self.logger.logger.error(f"AC circuit file not found: {self.ac_circuit_file}")
            return False
            
        self.logger.logger.info("Starting AC analysis simulation")
        return self.run_simulation(self.ac_circuit_file)
            
    def run_transient_simulation(self) -> bool:
        """Run transient analysis simulations.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.transient_circuit_file or not self.transient_circuit_file.exists():
            self.logger.logger.error(f"Transient circuit file not found: {self.transient_circuit_file}")
            return False
            
        self.logger.logger.info("Starting transient analysis simulation")
        return self.run_simulation(self.transient_circuit_file)
            
    def run_noise_simulation(self) -> bool:
        """Run the dedicated noise analysis simulation.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.noise_circuit_file or not self.noise_circuit_file.exists():
            self.logger.logger.error(f"Noise circuit file not found: {self.noise_circuit_file}")
            return False
            
        self.logger.logger.info("Starting dedicated noise analysis simulation")
        return self.run_simulation(self.noise_circuit_file)
        
    def run_all_simulations(self) -> bool:
        """Run all simulations sequentially: DC, AC, transient, and noise circuit files.
        
        Returns:
            bool: True if all simulations succeeded, False if any failed
        """
        # Run DC simulation (IV characteristics, bias point analysis)
        if not self.run_dc_simulation():
            self.logger.logger.error("DC circuit simulation failed")
            return False
        
        # Run AC simulation (CV characteristics, S-parameters) if file exists
        if self.ac_circuit_file and self.ac_circuit_file.exists():
            if not self.run_ac_simulation():
                self.logger.logger.error("AC circuit simulation failed")
                return False
        else:
            self.logger.logger.info("Skipping AC simulation (no circuit file)")
            
        # Run transient simulation
        if not self.run_transient_simulation():
            self.logger.logger.error("Transient circuit simulation failed")
            return False
            
        # Run noise analysis
        if not self.run_noise_simulation():
            self.logger.logger.error("Noise analysis simulation failed")
            return False
            
        self.logger.logger.info("All simulations completed successfully")
        return True
