import numpy as np
from pathlib import Path
import os
import re
import shutil

class DataReader:
    """Handles reading and parsing simulation data files.
    
    This class provides functionality to read various types of semiconductor device 
    simulation data from files output by circuit simulators such as NGSpice.
    
    The DataReader is organized into several categories of methods:
    
    1. Helper methods (prefixed with _) that provide common functionality:
       - _find_file: Locates files in various directories
       - _parse_data_file: Reads and parses data files
       - _read_ngspice_raw: Reads NGSpice raw format files
       - _read_noise_data_file: Specialized reader for noise data files
       
    2. IV and CV characteristic data methods:
       - read_iv_data: Reads IV curves across different temperatures
       - read_cv_data: Reads capacitance-voltage characteristics
       
    3. Transient analysis methods:
       - read_large_signal_transient_data: Reads large signal transient responses
       - read_switching_response_data: Reads switching time characteristics
       - read_delay_effect_data: Reads propagation delay data
       
    4. Power and energy analysis methods:
       - read_power_dissipation_data: Reads power consumption data
       - read_energy_consumption_data: Reads energy usage data
       
    5. Noise analysis methods:
       - read_thermal_noise_data: Reads thermal noise characteristics
       - read_flicker_noise_data: Reads flicker (1/f) noise characteristics
       - read_shot_noise_data: Reads shot noise characteristics
       
    6. Other specialized analysis methods:
       - read_temperature_data: Extracts temperature-dependent characteristics
       - read_bias_point_data: Reads DC bias point data
       - read_sparameter_data: Reads S-parameter data
       - read_nqs_effects_data: Reads non-quasi-static effects data
       - read_charge_conservation_data: Reads charge conservation test data
       
    Each method handles file location, data parsing, and error handling consistently.
    """
    def __init__(self, logger, output_dir='results'):
        self.logger = logger
        self.output_dir = output_dir
        # Create data directory path
        self.data_dir = os.path.join(self.output_dir, 'data')
    
    def _find_file(self, filename, fallback_dirs=None):
        """Helper method to find a file in the data directory or fallback locations.
        
        Args:
            filename: Name of the file to find
            fallback_dirs: List of other directories to check (default: output_dir and netlists)
            
        Returns:
            str: Path to the file if found, None otherwise
        """
        if fallback_dirs is None:
            fallback_dirs = [self.output_dir, 'netlists']
        
        # First check in data directory
        file_path = os.path.join(self.data_dir, filename)
        if os.path.exists(file_path):
            return file_path
        
        # Check in fallback directories
        for dir_path in fallback_dirs:
            file_path = os.path.join(dir_path, filename)
            if os.path.exists(file_path):
                return file_path
        
        return None
    
    def _copy_file_to_data_dir(self, src_path, dest_filename=None):
        """Copy a file to the data directory.
        
        Args:
            src_path: Source path of the file
            dest_filename: Optional destination filename (default: use original filename)
            
        Returns:
            str: Path to the copied file
        """
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir, exist_ok=True)
        
        dest_filename = dest_filename or os.path.basename(src_path)
        dest_path = os.path.join(self.data_dir, dest_filename)
        
        shutil.copy(src_path, dest_path)
        self.logger.logger.info(f"Copied file from {src_path} to {dest_path}")
        
        return dest_path
    
    def _parse_data_file(self, file_path, skiprows=2, expected_cols=None, col_names=None):
        """Parse a data file using numpy loadtxt with appropriate error handling.
        
        Args:
            file_path: Path to the data file
            skiprows: Number of header rows to skip
            expected_cols: Expected number of columns
            col_names: Column names to map in the file (header must be available)
            
        Returns:
            np.ndarray: Data array if successful, None otherwise
        """
        try:
            if not os.path.exists(file_path):
                self.logger.logger.warning(f"Data file not found: {file_path}")
                return None
            
            # If col_names is provided, read the header to map column positions
            col_map = None
            if col_names:
                with open(file_path, 'r') as f:
                    header = f.readline().strip().split()
                    col_map = {name: i for i, name in enumerate(header)}
            
            # Load data with numpy
            data = np.loadtxt(file_path, skiprows=skiprows)
            
            # Validate data shape if expected_cols is provided
            if expected_cols and (len(data) == 0 or data.shape[1] < expected_cols):
                self.logger.logger.warning(f"Data file {file_path} has incorrect format. Expected at least {expected_cols} columns.")
                return None
            
            return data, col_map
        except Exception as e:
            self.logger.logger.error(f"Error parsing data file {file_path}: {e}")
            return None, None
    
    def _read_ngspice_raw(self, file_path):
        """Read NGSpice raw files and extract data.
        
        Args:
            file_path: Path to the raw file
            
        Returns:
            tuple: (frequency, inoise_spectrum) if successful, else (None, None)
        """
        try:
            if not os.path.exists(file_path):
                self.logger.logger.warning(f"NGSpice raw file not found: {file_path}")
                return None, None
            
            # Parse the raw file format - very simple parser since we need specific data
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            # Find where the data section starts
            data_start = None
            for i, line in enumerate(lines):
                if line.strip() == 'Values:':
                    data_start = i + 1
                    break
            
            if data_start is None:
                self.logger.logger.warning(f"Could not find data section in raw file: {file_path}")
                return None, None
            
            # Extract the data
            freq_data = []
            noise_data = []
            
            for i in range(data_start, len(lines), 3):  # 3 lines per data point: index, frequency, noise
                if i + 2 < len(lines):
                    try:
                        freq = float(lines[i+1].strip())
                        noise = float(lines[i+2].strip())
                        freq_data.append(freq)
                        noise_data.append(noise)
                    except (ValueError, IndexError):
                        self.logger.logger.warning(f"Error parsing data at line {i+1} in file {file_path}")
                        continue
            
            if not freq_data:
                self.logger.logger.warning(f"No valid data extracted from {file_path}")
                return None, None
            
            return np.array(freq_data), np.array(noise_data)
            
        except Exception as e:
            self.logger.logger.error(f"Error reading NGSpice raw file {file_path}: {e}")
            return None, None

    def _read_noise_data_file(self, file_path):
        """Read noise data files with robust parsing to handle text headers and complex formats.
        
        Args:
            file_path: Path to the noise data file
            
        Returns:
            tuple: (frequency, noise) if successful, else (None, None)
        """
        try:
            if not os.path.exists(file_path):
                self.logger.logger.warning(f"Noise data file not found: {file_path}")
                return None, None

            # Try multiple parsing approaches
            # 1. First try our custom triplet parser
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            # Find Values: section
            values_index = None
            for i, line in enumerate(lines):
                if line.strip() == 'Values:':
                    values_index = i
                    break
            
            if values_index is not None:
                # Process the data section using triplet format
                freq_data = []
                noise_data = []
                i = values_index + 1
                
                while i < len(lines) - 2:  # Need at least 3 more lines for a complete triplet
                    # Each triplet has: index, frequency, noise
                    if lines[i].strip() and not lines[i].strip().startswith(' '):
                        i += 1  # Skip index line
                        
                        # Read frequency
                        if i < len(lines):
                            try:
                                freq = float(lines[i].strip())
                                freq_data.append(freq)
                                i += 1
                                
                                # Read noise
                                if i < len(lines):
                                    try:
                                        noise = float(lines[i].strip())
                                        noise_data.append(noise)
                                    except ValueError:
                                        # Skip this triplet if we can't parse the noise value
                                        pass
                            except ValueError:
                                # Skip this triplet if we can't parse the frequency
                                pass
                    i += 1
                
                # Check if we have valid data
                if len(freq_data) > 0 and len(noise_data) > 0:
                    # Ensure the arrays have the same length
                    min_len = min(len(freq_data), len(noise_data))
                    freq_array = np.array(freq_data[:min_len])
                    noise_array = np.array(noise_data[:min_len])
                    return freq_array, noise_array
            
            # 2. Try numpy parsing with different skiprows values
            for skiprows in [9, 10, 8, 11]:
                try:
                    data = np.loadtxt(file_path, skiprows=skiprows)
                    if len(data) > 0 and data.shape[1] >= 3:
                        freq = data[:, 0]  # First column is frequency
                        noise = data[:, 2]  # Third column is noise
                        return freq, noise
                except Exception:
                    continue
            
            # 3. Last resort - try a more flexible line-by-line parsing
            freq_data = []
            noise_data = []
            data_started = False
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                # If we see 'Values:', data will start soon
                if line == 'Values:':
                    data_started = True
                    continue
                    
                if data_started:
                    # Split by whitespace and try to extract values
                    parts = line.split()
                    if len(parts) == 1:
                        try:
                            # This might be a frequency or noise value
                            value = float(parts[0])
                            # If this is the first value we've seen, assume it's frequency
                            if len(freq_data) > len(noise_data):
                                noise_data.append(value)
                            else:
                                freq_data.append(value)
                        except ValueError:
                            # Not a numeric value, skip
                            pass
            
            # Check if we have matching data
            if len(freq_data) == len(noise_data) and len(freq_data) > 0:
                return np.array(freq_data), np.array(noise_data)
            
            # No valid data found
            self.logger.logger.warning(f"Could not extract valid data from {file_path}")
            return None, None
            
        except Exception as e:
            self.logger.logger.error(f"Error reading noise data file {file_path}: {e}")
            return None, None

    def read_iv_data(self):
        """Read IV characteristics data from the ASCII file."""
        try:
            self.logger.logger.info("Reading IV characteristics data")
            
            temp_files = {
                -40: 'iv_data_-40.txt',
                0: 'iv_data_0.txt',
                25: 'iv_data_25.txt',
                50: 'iv_data_50.txt',
                100: 'iv_data_100.txt',
                150: 'iv_data_150.txt'
            }
            
            vds_list, vgs_list, ids_list, ig_list, is_list, ib_list, temp_list = [], [], [], [], [], [], []
            
            for temp, filename in temp_files.items():
                file_path = self._find_file(filename)
                if not file_path:
                    self.logger.logger.warning(f"IV data file not found: {filename}")
                    continue
                    
                self.logger.logger.debug(f"Reading data for temperature {temp}°C from {filename}")
                
                try:
                    # Read data with column names
                    data, col_map = self._parse_data_file(file_path, skiprows=2, col_names=True)
                    if data is None or col_map is None:
                        continue
                    
                    # Map columns based on header names
                    vds_list.extend(data[:, col_map['v(drain_iv)']])
                    vgs_list.extend(data[:, col_map['v(gate_iv)']])
                    ids_list.extend(data[:, col_map['id']])
                    is_list.extend(data[:, col_map['is']])
                    ib_list.extend(data[:, col_map['ib']])
                    ig_list.extend(data[:, col_map['ig']])
                    temp_list.extend([temp] * len(data))
                except Exception as e:
                    self.logger.logger.warning(f"Error reading {filename}: {e}")
                    continue
            
            if not vds_list:
                self.logger.logger.error("No valid data found in any IV data file")
                return None, None, None, None, None, None, None
            
            return (np.array(vds_list), np.array(vgs_list), np.array(ids_list),
                   np.array(ig_list), np.array(is_list), np.array(ib_list),
                   np.array(temp_list))
            
        except Exception as e:
            self.logger.logger.error(f"Error reading IV data: {e}")
            return None, None, None, None, None, None, None

    def read_cv_data(self):
        """Read CV characteristics data from the output file."""
        try:
            filename = 'cv_data.txt'
            file_path = self._find_file(filename)
            
            if not file_path:
                self.logger.logger.warning(f"CV data file not found")
                return None, None, None, None, None
                
            self.logger.logger.info(f"Reading CV data from {file_path}")
            
            # Parse data file
            data, _ = self._parse_data_file(file_path, skiprows=1, expected_cols=5)
            if data is None:
                return None, None, None, None, None
            
            # Extract data columns
            vg = data[:, 0]  # Gate voltage column
            
            # For capacitance values, use the 1MHz data (column 4)
            # For currents, calculate from capacitance values
            cgg = data[:, 4] if data.shape[1] > 4 else data[:, 1]  # Total gate capacitance at 1MHz
            
            # Calculate terminal currents from capacitances
            w = 2 * np.pi * 1e6  # Angular frequency at 1MHz
            ig = w * cgg  # Gate current
            
            # Extract component capacitances if available
            if data.shape[1] >= 8:
                cgb = data[:, 5]  # Gate-bulk capacitance
                cgs = data[:, 6]  # Gate-source capacitance
                cgd = data[:, 7]  # Gate-drain capacitance
                
                # Calculate terminal currents
                ib = w * cgb  # Bulk current
                is_ = w * cgs  # Source current 
            else:
                # If component capacitances not available, use estimated values
                ib = ig * 0.2  # Approximate bulk current as 20% of gate current
                is_ = ig * 0.4  # Approximate source current as 40% of gate current
            
            self.logger.logger.info(f"CV data read successfully: {len(vg)} data points")
            return vg, ig, is_, ib, cgg
            
        except Exception as e:
            self.logger.logger.error(f"Error reading CV data: {e}")
            import traceback
            traceback.print_exc()
            return None, None, None, None, None
    
    def read_temperature_data(self):
        """Read temperature data from IV characteristics files."""
        try:
            self.logger.logger.info("Reading temperature data")
            
            temp_files = {
                -40: 'iv_data_-40.txt',
                0: 'iv_data_0.txt',
                25: 'iv_data_25.txt',
                50: 'iv_data_50.txt',
                100: 'iv_data_100.txt',
                150: 'iv_data_150.txt'
            }
            
            temp_list = []
            
            for temp, filename in temp_files.items():
                file_path = self._find_file(filename)
                if not file_path:
                    self.logger.logger.warning(f"Temperature data file not found: {filename}")
                    continue
                    
                try:
                    data, _ = self._parse_data_file(file_path, skiprows=2)
                    if data is None:
                        continue
                    
                    temp_list.extend([temp] * len(data))
                except Exception as e:
                    self.logger.logger.warning(f"Error reading {filename}: {e}")
                    continue
            
            if not temp_list:
                self.logger.logger.error("No valid temperature data found")
                return None
            
            self.logger.logger.info("Temperature data read successfully")
            return np.array(temp_list)
            
        except Exception as e:
            self.logger.logger.error(f"Error reading temperature data: {e}")
            return None

    def read_bias_point_data(self):
        """Read bias point analysis data from output files.
        
        Returns:
            tuple: (vds_points, vgs_points, ids, ig, is_, ib) arrays of bias point data
        """
        try:
            # Find bias point data file
            bias_file = None
            
            # Look for bias point files in data directory first
            for filename in os.listdir(self.data_dir) if os.path.exists(self.data_dir) else []:
                if filename == 'bias_point_data.txt' or filename.startswith('bias_point_data_'):
                    bias_file = os.path.join(self.data_dir, filename)
                    break
            
            # If not found, check in output directory
            if bias_file is None:
                for filename in os.listdir(self.output_dir):
                    if filename == 'bias_point_data.txt' or filename.startswith('bias_point_data_'):
                        bias_file = os.path.join(self.output_dir, filename)
                        break
            
            # Try netlists directory as last resort
            if bias_file is None:
                netlists_dir = 'netlists'
                if os.path.exists(netlists_dir):
                    for filename in os.listdir(netlists_dir):
                        if filename == 'bias_point_data.txt' or filename.startswith('bias_point_data_'):
                            bias_file = os.path.join(netlists_dir, filename)
                            # Copy to data directory for future use
                            os.makedirs(self.data_dir, exist_ok=True)
                            dest_file = os.path.join(self.data_dir, filename)
                            shutil.copy(bias_file, dest_file)
                            bias_file = dest_file
                            self.logger.logger.info(f"Copied bias point data from {bias_file} to {dest_file}")
                            break
            
            if bias_file is None:
                self.logger.logger.info("No bias point data file found - skipping bias point analysis")
                return None, None, None, None, None, None
            
            # Read data from file
            data, _ = self._parse_data_file(bias_file, skiprows=1, expected_cols=6)
            if data is None:
                return None, None, None, None, None, None
            
            # Extract columns
            vds_points = data[:, 0]  # VDS column
            vgs_points = data[:, 1]  # VGS column
            ids = data[:, 2]         # Drain current
            ig = data[:, 3]          # Gate current
            is_ = data[:, 4]         # Source current
            ib = data[:, 5]          # Bulk current
            
            self.logger.logger.info(f"Read bias point data from {bias_file}")
            return vds_points, vgs_points, ids, ig, is_, ib
            
        except Exception as e:
            self.logger.logger.error(f"Error reading bias point data: {e}")
            return None, None, None, None, None, None

    # Transient analysis data reading methods
    def read_large_signal_transient_data(self):
        """Read large signal transient analysis data from file.
        
        Returns:
            tuple: (time, vgate, vdrain, idrain) arrays of large signal transient data
        """
        try:
            filename = 'tran_large_signal.txt'
            file_path = self._find_file(filename, fallback_dirs=[self.output_dir, 'netlists'])
            
            if not file_path:
                self.logger.logger.warning("Large signal transient data file not found in any location")
                return None, None, None, None
            
            # Read and parse data
            data, _ = self._parse_data_file(file_path, skiprows=2, expected_cols=5)
            if data is None:
                self.logger.logger.warning("No large signal transient data found in file")
                return None, None, None, None
                
            # Extract columns by position rather than by name
            time = data[:, 0]    # First time column
            vgate = data[:, 2]   # v(gate_tran)
            vdrain = data[:, 3]  # v(drain_tran)
            idrain = data[:, 4]  # i(Vds_tran)
            
            self.logger.logger.info("Large signal transient data read successfully")
            return time, vgate, vdrain, idrain
            
        except Exception as e:
            self.logger.logger.error(f"Error reading large signal transient data: {e}")
            return None, None, None, None
            
    def read_switching_response_data(self):
        """Read switching response data from file.
        
        Returns:
            tuple: (time, vin, vout, idrain) arrays of switching response data
        """
        try:
            filename = 'tran_switching.txt'
            file_path = self._find_file(filename, fallback_dirs=[self.output_dir, 'netlists'])
            
            if not file_path:
                self.logger.logger.warning("Switching response data file not found in any location")
                return None, None, None, None
            
            # Read and parse data
            data, _ = self._parse_data_file(file_path, skiprows=2, expected_cols=5)
            if data is None:
                self.logger.logger.warning("No switching response data found in file")
                return None, None, None, None
                
            # Extract columns by position rather than by name
            time = data[:, 0]   # First time column
            vin = data[:, 2]    # v(in_inv)
            vout = data[:, 3]   # v(out_inv)
            idrain = data[:, 4]  # i(Vdd_inv)
            
            self.logger.logger.info("Switching response data read successfully")
            return time, vin, vout, idrain
            
        except Exception as e:
            self.logger.logger.error(f"Error reading switching response data: {e}")
            return None, None, None, None
            
    def read_switching_power_data(self):
        """Read switching power data from file.
        
        Returns:
            tuple: (time, power) arrays of switching power data
        """
        try:
            filename = 'tran_switching_power.txt'
            file_path = self._find_file(filename, fallback_dirs=[self.output_dir, 'netlists'])
            
            if not file_path:
                self.logger.logger.warning("Switching power data file not found in any location")
                return None, None
            
            # Read and parse data
            data, _ = self._parse_data_file(file_path, skiprows=2, expected_cols=3)
            if data is None:
                self.logger.logger.warning("No switching power data found in file")
                return None, None
                
            # Extract columns by position rather than by name
            time = data[:, 0]   # First time column
            power = data[:, 2]  # Power column
            
            self.logger.logger.info("Switching power data read successfully")
            return time, power
            
        except Exception as e:
            self.logger.logger.error(f"Error reading switching power data: {e}")
            return None, None

    def read_delay_effect_data(self):
        """Read delay effect data from file.
        
        Returns:
            tuple: (time, vin, v_mid1, v_mid2, vout) arrays of delay effect data
        """
        try:
            filename = 'tran_delay.txt'
            file_path = self._find_file(filename, fallback_dirs=[self.output_dir, 'netlists'])
            
            if not file_path:
                self.logger.logger.warning("Delay effect data file not found in any location")
                return None, None, None, None, None
            
            # Read and parse data
            data, _ = self._parse_data_file(file_path, skiprows=2, expected_cols=6)
            if data is None:
                self.logger.logger.warning("No delay effect data found in file")
                return None, None, None, None, None
                
            # Extract columns by position rather than by name
            time = data[:, 0]    # First time column
            vin = data[:, 2]     # v(in_delay)
            v_mid1 = data[:, 3]  # v(mid1_delay)
            v_mid2 = data[:, 4]  # v(mid2_delay)
            vout = data[:, 5]    # v(out_delay)
            
            self.logger.logger.info("Delay effect data read successfully")
            return time, vin, v_mid1, v_mid2, vout
            
        except Exception as e:
            self.logger.logger.error(f"Error reading delay effect data: {e}")
            return None, None, None, None, None
            
    def read_power_dissipation_data(self, temperature=27):
        """Read power dissipation data from file.
        
        Args:
            temperature: Temperature in degrees Celsius for the power data to read
            
        Returns:
            tuple: (time, power) arrays of power dissipation data
        """
        try:
            filename = f'tran_power_{temperature}C.txt'
            file_path = self._find_file(filename, fallback_dirs=[self.output_dir, 'netlists'])
            
            if not file_path:
                self.logger.logger.warning(f"Power dissipation data file at {temperature}°C not found in any location")
                return None, None
            
            # Read and parse data
            data, _ = self._parse_data_file(file_path, skiprows=2, expected_cols=5)
            if data is None:
                self.logger.logger.warning(f"No power dissipation data at {temperature}°C found in file")
                return None, None
                
            # Extract columns by position rather than by name
            time = data[:, 0]    # First time column
            power = data[:, 4]   # Power column (4th column, 0-indexed)
            
            self.logger.logger.info(f"Power dissipation data for {temperature}°C read successfully")
            return time, power
            
        except Exception as e:
            self.logger.logger.error(f"Error reading power dissipation data at {temperature}°C: {e}")
            return None, None
            
    def read_energy_consumption_data(self, temperature=27):
        """Read energy consumption data from file.
        
        Args:
            temperature: Temperature in degrees Celsius for the energy data to read
            
        Returns:
            tuple: (time, energy) arrays of energy consumption data
        """
        try:
            filename = f'tran_power_{temperature}C.txt'
            file_path = self._find_file(filename, fallback_dirs=[self.output_dir, 'netlists'])
            
            if not file_path:
                self.logger.logger.warning(f"Energy consumption data file at {temperature}°C not found in any location")
                return None, None
            
            # Read and parse data
            data, _ = self._parse_data_file(file_path, skiprows=2, expected_cols=6)
            if data is None:
                self.logger.logger.warning(f"No energy consumption data at {temperature}°C found in file")
                return None, None
                
            # Extract columns by position rather than by name
            time = data[:, 0]    # First time column
            energy = data[:, 5]  # Energy column (5th column, 0-indexed)
            
            self.logger.logger.info(f"Energy consumption data for {temperature}°C read successfully")
            return time, energy
            
        except Exception as e:
            self.logger.logger.error(f"Error reading energy consumption data at {temperature}°C: {e}")
            return None, None
    
    def read_quasi_static_data(self):
        """Read quasi-static analysis data from file.
        
        Returns:
            tuple: (time, vgate, vdrain, idrain) arrays of quasi-static data
        """
        try:
            filename = 'tran_quasi_static.txt'
            file_path = self._find_file(filename, fallback_dirs=[self.output_dir, 'netlists'])
            
            if not file_path:
                self.logger.logger.warning("Quasi-static data file not found in any location")
                return None, None, None, None
            
            # Read and parse data
            data, _ = self._parse_data_file(file_path, skiprows=2, expected_cols=5)
            if data is None:
                self.logger.logger.warning("No quasi-static data found in file")
                return None, None, None, None
                
            # Extract columns by position rather than by name
            time = data[:, 0]    # First time column
            vgate = data[:, 2]   # v(gate_qs)
            vdrain = data[:, 3]  # v(drain_qs)
            idrain = data[:, 4]  # id_qs
            
            self.logger.logger.info("Quasi-static data read successfully")
            return time, vgate, vdrain, idrain
            
        except Exception as e:
            self.logger.logger.error(f"Error reading quasi-static data: {e}")
            return None, None, None, None
            
    def read_charge_conservation_data(self):
        """Read charge conservation test data from output file.
        
        Returns:
            tuple: (time, vg, ig, id, is_, ib) arrays of charge conservation data
        """
        try:
            # First check for tran_charge.txt which contains all charge data
            file_path = os.path.join(self.output_dir, 'data', 'tran_charge.txt')
            if os.path.exists(file_path):
                self.logger.logger.info(f"Reading charge conservation data from {file_path}")
                
                # Read the file with numpy - skip the first two comment lines
                try:
                    data = np.loadtxt(file_path, skiprows=2)
                    if len(data) > 0 and data.shape[1] >= 7:
                        # Extract columns
                        time = data[:, 0]   # Time
                        vg = data[:, 2]     # Gate voltage
                        ig = data[:, 3]     # Gate current
                        id = data[:, 4]     # Drain current
                        is_ = data[:, 5]    # Source current
                        ib = data[:, 6]     # Bulk current
                        
                        self.logger.logger.info(f"Charge conservation data read successfully from tran_charge.txt: {len(time)} time points")
                        return time, vg, ig, id, is_, ib
                except Exception as e:
                    self.logger.logger.warning(f"Error parsing tran_charge.txt: {e}. Trying alternative files.")
            
            # If tran_charge.txt can't be used, fall back to charge_conservation.txt
            file_path = os.path.join(self.output_dir, 'data', 'charge_conservation.txt')
            if not os.path.exists(file_path):
                # If not there, check in main output directory as fallback
                file_path = os.path.join(self.output_dir, 'charge_conservation.txt')
                if not os.path.exists(file_path):
                    # Check if the file exists in the netlists directory
                    netlists_file = os.path.join('netlists', 'charge_conservation.txt')
                    if os.path.exists(netlists_file):
                        # Create data directory if it doesn't exist
                        data_dir = os.path.join(self.output_dir, 'data')
                        os.makedirs(data_dir, exist_ok=True)
                        
                        # Copy file to results/data directory
                        shutil.copy(netlists_file, file_path)
                        self.logger.logger.info(f"Copied charge conservation data from {netlists_file} to {file_path}")
                    else:
                        self.logger.logger.warning(f"Charge conservation data file not found: {file_path}")
                        return None, None, None, None, None, None
            
            self.logger.logger.info(f"Reading charge conservation data from {file_path}")
            
            # First try to load data directly with numpy
            try:
                data = np.loadtxt(file_path, skiprows=1)
                if len(data) > 0 and data.shape[1] >= 6:
                    # Extract columns
                    time = data[:, 0]  # Time
                    vg = data[:, 1]    # Gate voltage
                    ig = data[:, 2]    # Gate current
                    id = data[:, 3]    # Drain current
                    is_ = data[:, 4]   # Source current
                    ib = data[:, 5]    # Bulk current
                    
                    self.logger.logger.info(f"Charge conservation data read successfully: {len(time)} time points")
                    return time, vg, ig, id, is_, ib
            except Exception as e:
                self.logger.logger.warning(f"Standard parsing failed, attempting to parse ngspice raw file format: {e}")
            
            # If standard parsing fails, try to parse the ngspice raw file format
            try:
                # Read the file and parse the ngspice raw format
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                
                # Find the 'Values:' line that indicates the start of data
                values_index = -1
                variables_index = -1
                for i, line in enumerate(lines):
                    if line.strip() == 'Variables:':
                        variables_index = i
                    if line.strip() == 'Values:':
                        values_index = i
                        break
                
                if values_index == -1:
                    self.logger.logger.error("Could not find 'Values:' in charge conservation file")
                    return None, None, None, None, None, None
                
                # Parse data from the Values section
                time_data = []
                vg_data = []
                ig_data = []
                id_data = []
                is_data = []
                ib_data = []
                
                # Extract column indices from Variables section
                var_map = {}
                if variables_index != -1:
                    for i in range(variables_index + 1, values_index):
                        parts = lines[i].strip().split()
                        if len(parts) >= 3:
                            idx = int(parts[0])
                            var_name = parts[1]
                            var_map[idx] = var_name
                
                # Process data rows - each data point spans multiple lines
                i = values_index + 1
                while i < len(lines):
                    # First line has the index and time value
                    row_match = re.match(r'^ *([0-9]+)\t([-0-9.e+]+)', lines[i].strip())
                    if row_match:
                        index = int(row_match.group(1))
                        time_val = float(row_match.group(2))
                        time_data.append(time_val)
                        
                        # Next lines contain the voltage and currents
                        # We need to parse the next 5 values, skipping empty lines
                        values = []
                        j = i + 1
                        while j < len(lines) and len(values) < 5:
                            line = lines[j].strip()
                            if line and line[0] == '\t':
                                try:
                                    val = float(line.strip())
                                    values.append(val)
                                except ValueError:
                                    pass
                            j += 1
                        
                        # If we found all 5 values, add them to our data arrays
                        if len(values) >= 5:
                            vg_data.append(values[0])  # Gate voltage
                            ig_data.append(values[1])  # Gate current
                            id_data.append(values[2])  # Drain current
                            is_data.append(values[3])  # Source current
                            ib_data.append(values[4])  # Bulk current
                            i = j - 1  # Continue from where we left off
                    i += 1
                
                # Check if we extracted valid data
                if len(time_data) > 0 and len(time_data) == len(vg_data) == len(ig_data) == len(id_data) == len(is_data) == len(ib_data):
                    # Convert to numpy arrays
                    time_array = np.array(time_data)
                    vg_array = np.array(vg_data)
                    ig_array = np.array(ig_data)
                    id_array = np.array(id_data)
                    is_array = np.array(is_data)
                    ib_array = np.array(ib_data)
                    
                    self.logger.logger.info(f"Charge conservation data parsed from ngspice raw format: {len(time_array)} time points")
                    return time_array, vg_array, ig_array, id_array, is_array, ib_array
                else:
                    self.logger.logger.error("Failed to extract consistent data from ngspice raw format")
                    return None, None, None, None, None, None
                
            except Exception as e:
                self.logger.logger.error(f"Error parsing charge conservation data from ngspice raw format: {e}")
                import traceback
                traceback.print_exc()
                return None, None, None, None, None, None
                
        except Exception as e:
            self.logger.logger.error(f"Error reading charge conservation data: {e}")
            import traceback
            traceback.print_exc()
            return None, None, None, None, None, None
    
    # Noise analysis data reading methods
    def read_thermal_noise_data(self, vgs=0.3, vds=0.3):
        """Read thermal noise data from file.
        
        Args:
            vgs: Gate-source voltage for the specific thermal noise data file
            vds: Drain-source voltage for the specific thermal noise data file
            
        Returns:
            tuple: (freq, noise, temp, temps) arrays of thermal noise data
                   where temp is the default temperature and temps is an array of all temperatures
        """
        try:
            # Try the text file first
            txt_filename = f'thermal_noise_vgs{vgs:.1f}_vds{vds:.1f}.txt'
            txt_file_path = self._find_file(txt_filename)
            
            if txt_file_path:
                # Use custom parser
                freq, noise = self._read_noise_data_file(txt_file_path)
                if freq is not None and noise is not None:
                    self.logger.logger.info(f"Thermal noise data for Vgs={vgs}V, Vds={vds}V read successfully from txt file")
                    # Default temperature is 27°C unless specified otherwise
                    temp = 27
                    # Return a list of temperatures used (usually just the default in this case)
                    temps = np.array([temp])
                    return freq, noise, temp, temps
            
            # Try the raw file if txt file doesn't exist or couldn't be read
            raw_filename = f'thermal_noise_vgs{vgs:.1f}_vds{vds:.1f}.raw'
            raw_file_path = self._find_file(raw_filename, fallback_dirs=['netlists'])
            
            if not raw_file_path:
                self.logger.logger.warning(f"Thermal noise data file not found for Vgs={vgs}V, Vds={vds}V")
                return None, None, None, None
            
            # Read the raw file
            freq, noise = self._read_ngspice_raw(raw_file_path)
            if freq is not None and noise is not None:
                self.logger.logger.info(f"Thermal noise data for Vgs={vgs}V, Vds={vds}V read successfully from raw file")
                # Default temperature is 27°C unless specified otherwise
                temp = 27
                # Return a list of temperatures used (usually just the default in this case)
                temps = np.array([temp])
                return freq, noise, temp, temps
            
            return None, None, None, None
                
        except Exception as e:
            self.logger.logger.error(f"Error reading thermal noise data: {e}")
            return None, None, None, None
    
    def read_all_thermal_noise_data(self):
        """Read all thermal noise data files for different bias points.
        
        Returns:
            dict: Dictionary with keys as bias points and values as (freq, noise) tuples
        """
        # Common bias points used in the simulation
        bias_points = [
            (0.3, 0.3), (0.3, 0.6), (0.3, 0.9), (0.3, 1.2),
            (0.6, 0.3), (0.6, 0.6)
        ]
        
        thermal_noise_data = {}
        
        for vgs, vds in bias_points:
            freq, noise, _, _ = self.read_thermal_noise_data(vgs, vds)
            if freq is not None and noise is not None:
                key = f"Vgs={vgs:.1f}V, Vds={vds:.1f}V"
                thermal_noise_data[key] = (freq, noise)
                self.logger.logger.debug(f"Added thermal noise data for {key}")
        
        if not thermal_noise_data:
            self.logger.logger.warning("No thermal noise data found for any bias point")
        else:
            self.logger.logger.info(f"Read thermal noise data for {len(thermal_noise_data)} bias points")
            
        return thermal_noise_data
    
    def read_flicker_noise_data(self):
        """Read flicker noise data from file.
        
        Returns:
            tuple: (freq, noise) arrays of flicker noise data
        """
        try:
            # Try the text file first
            txt_filename = 'flicker_noise.txt'
            txt_file_path = self._find_file(txt_filename)
            
            if txt_file_path:
                # Use custom parser
                freq, noise = self._read_noise_data_file(txt_file_path)
                if freq is not None and noise is not None:
                    self.logger.logger.info("Flicker noise data read successfully from txt file")
                    return freq, noise
            
            # Try the raw file if txt file doesn't exist or couldn't be read
            raw_filename = 'flicker_noise.raw'
            raw_file_path = self._find_file(raw_filename, fallback_dirs=['netlists'])
            
            if not raw_file_path:
                self.logger.logger.warning("Flicker noise data file not found")
                return None, None
            
            # Read the raw file
            freq, noise = self._read_ngspice_raw(raw_file_path)
            if freq is not None and noise is not None:
                self.logger.logger.info("Flicker noise data read successfully from raw file")
                return freq, noise
            
            return None, None
            
        except Exception as e:
            self.logger.logger.error(f"Error reading flicker noise data: {e}")
            return None, None
    
    def read_shot_noise_data(self):
        """Read shot noise data from file.
        
        Returns:
            tuple: (freq, noise) arrays of shot noise data
        """
        try:
            # Try the text file first
            txt_filename = 'shot_noise.txt'
            txt_file_path = self._find_file(txt_filename)
            
            if txt_file_path:
                # Use custom parser
                freq, noise = self._read_noise_data_file(txt_file_path)
                if freq is not None and noise is not None:
                    self.logger.logger.info("Shot noise data read successfully from txt file")
                    return freq, noise
            
            # Try the raw file if txt file doesn't exist or couldn't be read
            raw_filename = 'shot_noise.raw'
            raw_file_path = self._find_file(raw_filename, fallback_dirs=['netlists'])
            
            if not raw_file_path:
                self.logger.logger.warning("Shot noise data file not found")
                return None, None
            
            # Read the raw file
            freq, noise = self._read_ngspice_raw(raw_file_path)
            if freq is not None and noise is not None:
                self.logger.logger.info("Shot noise data read successfully from raw file")
                return freq, noise
            
            return None, None
            
        except Exception as e:
            self.logger.logger.error(f"Error reading shot noise data: {e}")
            return None, None
    
    def read_temperature_noise_data(self):
        """Read temperature-dependent noise data from files.
        
        Returns:
            tuple: (temperatures, noise_data) where temperatures is a list and
                  noise_data is a dictionary of temperature -> (freq, noise) mappings
        """
        try:
            # Temperature points typically measured
            temperatures = [-40, 0, 27, 50, 100, 150]
            noise_data = {}
            
            for temp in temperatures:
                # First try reading from .txt file in data directory
                txt_file_path = os.path.join(self.output_dir, 'data', f'noise_temp{temp}.txt')
                if os.path.exists(txt_file_path):
                    # Use custom parser instead of np.loadtxt
                    freq, noise = self._read_noise_data_file(txt_file_path)
                    if freq is not None and noise is not None:
                        noise_data[temp] = (freq, noise)
                        self.logger.logger.debug(f"Temperature noise data at {temp}°C read successfully from txt file")
                        continue
                
                # If txt file doesn't exist or couldn't be read, try raw file
                raw_file_path = os.path.join(self.output_dir, 'data', f'noise_temp{temp}.raw')
                if not os.path.exists(raw_file_path):
                    # Try in netlists directory as fallback
                    raw_file_path = os.path.join('netlists', f'noise_temp{temp}.raw')
                    if not os.path.exists(raw_file_path):
                        self.logger.logger.warning(f"Temperature noise data file not found for {temp}°C")
                        continue
                
                # Read the raw file
                freq, noise = self._read_ngspice_raw(raw_file_path)
                if freq is not None and noise is not None:
                    noise_data[temp] = (freq, noise)
                    self.logger.logger.debug(f"Temperature noise data at {temp}°C read successfully from raw file")
            
            # Check if we have any data
            if not noise_data:
                self.logger.logger.warning("No temperature noise data found")
                return None, None
            
            # Return only the temperatures for which we have data
            valid_temps = list(noise_data.keys())
            self.logger.logger.info(f"Temperature noise data read successfully for temperatures: {valid_temps}")
            return valid_temps, noise_data
            
        except Exception as e:
            self.logger.logger.error(f"Error reading temperature noise data: {e}")
            return None, None
    
    def read_sparameter_data(self):
        """Read S-parameter data from output file.
        
        Returns:
            tuple: (freq, s11_mag, s21_mag, s12_mag, s22_mag) arrays of S-parameter data
        """
        try:
            # First check in data directory
            filename = 'sparams_data.txt'
            file_path = os.path.join(self.output_dir, 'data', filename)
            
            if not os.path.exists(file_path):
                # If not there, check in main output directory as fallback
                file_path = os.path.join(self.output_dir, filename)
                if not os.path.exists(file_path):
                    # Check if the S-parameter raw files exist in the netlists directory
                    s_params_p1_file = os.path.join('netlists', 's_params_p1.txt')
                    s_params_p2_file = os.path.join('netlists', 's_params_p2.txt')
                    
                    if os.path.exists(s_params_p1_file) and os.path.exists(s_params_p2_file):
                        # Create data directory if it doesn't exist
                        data_dir = os.path.join(self.output_dir, 'data')
                        os.makedirs(data_dir, exist_ok=True)
                        
                        # Copy files to results directory for processing
                        dest_p1 = os.path.join(data_dir, 's_params_p1.txt')
                        dest_p2 = os.path.join(data_dir, 's_params_p2.txt')
                        shutil.copy(s_params_p1_file, dest_p1)
                        shutil.copy(s_params_p2_file, dest_p2)
                        self.logger.logger.info(f"Copied S-parameter data files from netlists to {data_dir}")
                        
                        # Also check for sparams_data.txt in netlists directory
                        sparams_data_file = os.path.join('netlists', filename)
                        if os.path.exists(sparams_data_file):
                            shutil.copy(sparams_data_file, file_path)
                            self.logger.logger.info(f"Copied S-parameter data file from netlists/{filename} to {file_path}")
                    else:
                        self.logger.logger.error(f"S-parameter data file {filename} not found")
                        return None, None, None, None, None, None, None, None, None
            
            self.logger.logger.info(f"Reading S-parameter data from {file_path}")
            
            # Read file, skipping header lines (starting with #)
            data = []
            with open(file_path, 'r') as f:
                for line in f:
                    if line.startswith('#'):
                        continue
                    try:
                        parts = line.strip().split()
                        if len(parts) >= 9:  # freq and 8 S-parameter values
                            row = [float(parts[0])]  # Frequency
                            # S11, S12, S21, S22 magnitudes and phases
                            for i in range(1, 9):
                                row.append(float(parts[i]))
                            data.append(row)
                    except Exception as e:
                        self.logger.logger.warning(f"Error parsing S-parameter line: {line.strip()}, {e}")
                        continue
            
            if not data:
                self.logger.logger.error("No valid S-parameter data could be parsed")
                return None, None, None, None, None, None, None, None, None
            
            data = np.array(data)
            
            # Extract data columns
            freq = data[:, 0]       # Frequency
            s11_mag = data[:, 1]    # S11 magnitude
            s11_phase = data[:, 2]  # S11 phase (degrees)
            s12_mag = data[:, 3]    # S12 magnitude
            s12_phase = data[:, 4]  # S12 phase (degrees)
            s21_mag = data[:, 5]    # S21 magnitude
            s21_phase = data[:, 6]  # S21 phase (degrees)
            s22_mag = data[:, 7]    # S22 magnitude
            s22_phase = data[:, 8]  # S22 phase (degrees)
            
            self.logger.logger.info(f"S-parameter data read successfully: {len(freq)} frequency points")
            return freq, s11_mag, s11_phase, s12_mag, s12_phase, s21_mag, s21_phase, s22_mag, s22_phase
            
        except Exception as e:
            self.logger.logger.error(f"Error reading S-parameter data: {e}")
            return None, None, None, None, None, None, None, None, None
    
    def read_nqs_effects_data(self):
        """Read non-quasi-static effects data from output file.
        
        Returns:
            tuple: (freq, vg_phase, id_phase, phase_diff) arrays of NQS effect data
        """
        try:
            # First check in data directory
            filename = 'nqs_effects.txt'
            file_path = os.path.join(self.output_dir, 'data', filename)
            
            if not os.path.exists(file_path):
                # If not there, check in main output directory as fallback
                file_path = os.path.join(self.output_dir, filename)
                if not os.path.exists(file_path):
                    # Check if the NQS effects raw file exists in the netlists directory
                    nqs_raw_file = os.path.join('netlists', 'nqs_effects_raw.txt')
                    
                    if os.path.exists(nqs_raw_file):
                        # Create data directory if it doesn't exist
                        data_dir = os.path.join(self.output_dir, 'data')
                        os.makedirs(data_dir, exist_ok=True)
                        
                        # Copy file to results directory for processing
                        dest_raw = os.path.join(data_dir, 'nqs_effects_raw.txt')
                        shutil.copy(nqs_raw_file, dest_raw)
                        self.logger.logger.info(f"Copied NQS effects raw data file from netlists to {data_dir}")
                        
                        # Also check for nqs_effects.txt in netlists directory
                        nqs_effects_file = os.path.join('netlists', filename)
                        if os.path.exists(nqs_effects_file):
                            shutil.copy(nqs_effects_file, file_path)
                            self.logger.logger.info(f"Copied NQS effects data file from netlists/{filename} to {file_path}")
                    else:
                        self.logger.logger.warning(f"Non-quasi-static effects data file not found: {file_path}")
                        return None, None, None, None
            
            self.logger.logger.info(f"Reading NQS effects data from {file_path}")
            
            # Read file, skipping header lines (starting with #)
            data = []
            with open(file_path, 'r') as f:
                for line in f:
                    if line.startswith('#'):
                        continue
                    try:
                        parts = line.strip().split()
                        if len(parts) >= 4:  # freq, vg_phase, id_phase, phase_diff
                            row = []
                            for i in range(4):
                                row.append(float(parts[i]))
                            data.append(row)
                    except Exception as e:
                        self.logger.logger.warning(f"Error parsing NQS line: {line.strip()}, {e}")
                        continue
            
            if not data:
                self.logger.logger.error("No valid NQS effects data could be parsed")
                return None, None, None, None
            
            data = np.array(data)
            
            # Extract data columns
            freq = data[:, 0]        # Frequency
            vg_phase = data[:, 1]    # Gate voltage phase
            id_phase = data[:, 2]    # Drain current phase
            phase_diff = data[:, 3]  # Phase difference (vg_phase - id_phase)
            
            self.logger.logger.info(f"NQS effects data read successfully: {len(freq)} frequency points")
            return freq, vg_phase, id_phase, phase_diff
            
        except Exception as e:
            self.logger.logger.error(f"Error reading NQS effects data: {e}")
            return None, None, None, None 