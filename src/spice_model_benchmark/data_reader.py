import numpy as np
from pathlib import Path
import os
import re
import shutil
import pandas as pd

class DataReader:
    """Handles reading and parsing simulation data files.
    
    This class provides functionality to read various types of semiconductor device 
    simulation data from files output by circuit simulators such as NGSpice.
    
    The DataReader is organized into several categories of methods:
    
    1. Helper methods (prefixed with _) that provide common functionality:
       - _find_file: Locates files in various directories
       - _copy_file_to_data_dir:
       - _parse_data_file: Reads and parses data files
       - _parse_data_file_with_comments: 
       - _read_ngspice_raw: Reads NGSpice raw format files
       - _read_noise_data_file: Specialized reader for noise data files
       
    2. DC data methods:
       - read_iv_data: Reads IV curves across different temperatures
       - read_temperature_data: Extracts temperature-dependent characteristics
       - read_bias_point_data: Reads DC bias point data
       
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
       
    6. AC Analysis methods:
       - read_cv_data: Reads capacitance-voltage characteristics
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
    
    def _find_file(self, filename, output_dir, fallback_dirs=None):
        """Helper method to find a file in the data directory or fallback locations.
        
        Args:
            filename: Name of the file to find
            fallback_dirs: List of other directories to check (default: output_dir and netlists)
            
        Returns:
            str: Path to the file if found, None otherwise
        """
        if fallback_dirs is None:
            fallback_dirs = [output_dir, 'netlists']
        
        # First check in data directory
        data_dir = os.path.join(output_dir, 'data')
        file_path = os.path.join(data_dir, filename)
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
        self.logger.info(f"Copied file from {src_path} to {dest_path}")
        
        return dest_path
    
    def _parse_data_file(self, file_path, skiprows=1, expected_cols=None, col_names=None):
        """Parse a data file with a single header line using numpy loadtxt.
        
        Args:
            file_path: Path to the data file
            skiprows: Number of header rows to skip (default: 1)
            expected_cols: Expected number of columns
            col_names: Column names to map in the file (header must be available)
            
        Returns:
            tuple: (data array, column mapping) if successful, else (None, None)
        """
        try:
            if not os.path.exists(file_path):
                self.logger.warning(f"Data file not found: {file_path}")
                return None, None
            
            # If col_names is provided, read the header to map column positions
            col_map = None
            if col_names:
                with open(file_path, 'r') as f:
                    # Read first line (column names)
                    header = f.readline().strip().split()
                    # Remove '#' if present at the start
                    if header and header[0].startswith('#'):
                        header = header[1:]
                    col_map = {name: i for i, name in enumerate(header)}
            
            # Load data with numpy
            data = np.loadtxt(file_path, skiprows=skiprows)
            
            # Validate data shape if expected_cols is provided
            if expected_cols and (len(data) == 0 or data.shape[1] < expected_cols):
                self.logger.warning(f"Data file {file_path} has incorrect format. Expected at least {expected_cols} columns.")
                return None, None
            
            return data, col_map
        except Exception as e:
            self.logger.error(f"Error parsing data file {file_path}: {e}")
            return None, None

    def _parse_data_file_with_comments(self, file_path, expected_cols=None, col_names=None):
        """Parse a data file with two comment lines using numpy loadtxt.
        
        Args:
            file_path: Path to the data file
            expected_cols: Expected number of columns
            col_names: Column names to map in the file (header must be available)
            
        Returns:
            tuple: (data array, column mapping) if successful, else (None, None)
        """
        try:
            if not os.path.exists(file_path):
                self.logger.warning(f"Data file not found: {file_path}")
                return None, None
            
            # If col_names is provided, read the header to map column positions
            col_map = None
            if col_names:
                with open(file_path, 'r') as f:
                    # Skip first comment line
                    f.readline()
                    # Read second line (column names)
                    header = f.readline().strip().split()
                    # Remove '#' if present at the start
                    if header and header[0].startswith('#'):
                        header = header[1:]
                    col_map = {name: i for i, name in enumerate(header)}
            
            # Load data with numpy
            data = np.loadtxt(file_path, skiprows=2)  # Skip both comment lines
            
            # Validate data shape if expected_cols is provided
            if expected_cols and (len(data) == 0 or data.shape[1] < expected_cols):
                self.logger.warning(f"Data file {file_path} has incorrect format. Expected at least {expected_cols} columns.")
                return None, None
            
            return data, col_map
        except Exception as e:
            self.logger.error(f"Error parsing data file {file_path}: {e}")
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
                self.logger.warning(f"NGSpice raw file not found: {file_path}")
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
                self.logger.warning(f"Could not find data section in raw file: {file_path}")
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
                        self.logger.warning(f"Error parsing data at line {i+1} in file {file_path}")
                        continue
            
            if not freq_data:
                self.logger.warning(f"No valid data extracted from {file_path}")
                return None, None
            
            return np.array(freq_data), np.array(noise_data)
            
        except Exception as e:
            self.logger.error(f"Error reading NGSpice raw file {file_path}: {e}")
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

    # DC analysis data reading methods
    def read_dc_iv_data(self, output_dir):
        """Read IV characteristics data from the ASCII file."""
        try:
            self.logger.info("Reading IV characteristics data")
            
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
                file_path = self._find_file(filename, output_dir)
                if not file_path:
                    self.logger.warning(f"IV data file not found: {filename}")
                else:
                    self.logger.info(f"IV data file found: {file_path}")

                self.logger.debug(f"Reading data for temperature {temp}°C from {filename}")
                
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
                    self.logger.warning(f"Error reading {filename}: {e}")
                    continue
            
            if not vds_list:
                self.logger.error("No valid data found in any IV data file")
                return None, None, None, None, None, None, None
            
            return (np.array(vds_list), np.array(vgs_list), np.array(ids_list),
                   np.array(ig_list), np.array(is_list), np.array(ib_list),
                   np.array(temp_list))
            
        except Exception as e:
            self.logger.error(f"Error reading IV data: {e}")
            return None, None, None, None, None, None, None

    def read_dc_temperature_data(self, output_dir):
        """Read temperature data from IV characteristics files."""
        try:
            self.logger.info("Reading temperature data")
            
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
                file_path = self._find_file(filename, output_dir)
                if not file_path:
                    self.logger.warning(f"Temperature data file not found: {filename}")
                else:
                    self.logger.info(f"Temperature data file found: {file_path}")

                try:
                    data, _ = self._parse_data_file(file_path, skiprows=2)
                    if data is None:
                        continue
                    
                    temp_list.extend([temp] * len(data))
                except Exception as e:
                    self.logger.warning(f"Error reading {filename}: {e}")
                    continue
            
            if not temp_list:
                self.logger.error("No valid temperature data found")
                return None
            
            self.logger.info("Temperature data read successfully")
            return np.array(temp_list)
            
        except Exception as e:
            self.logger.error(f"Error reading temperature data: {e}")
            return None

    def read_dc_bias_point_data(self, output_dir):
        """Read bias point analysis data from output files.
        
        Returns:
            tuple: (vds_points, vgs_points, i_ds, i_g, i_s, i_b) arrays of bias point data
        """
        try:
            self.logger.info("Reading Bias Point data")
            # Find bias point data file
            bias_file = None
            
            # Look for bias point files in data directory first
            filename = 'bias_point_data.txt'
            bias_file = self._find_file(filename, output_dir)
            if not bias_file:
                self.logger.warning(f"Bias Point data file not found: {filename}")
                return None, None, None, None, None, None
            else:
                self.logger.info(f"Bias file found: {bias_file}")
            
            # Read data from file
            data, _ = self._parse_data_file(bias_file, skiprows=1, expected_cols=6)
            if data is None:
                self.logger.warning("Data is None during parsing process")
                return None, None, None, None, None, None

            # Extract columns
            vds_points = data[:, 0]  # VDS column
            vgs_points = data[:, 1]  # VGS column
            i_ds = data[:, 2]         # Drain current
            i_g = data[:, 3]          # Gate current
            i_s = data[:, 4]         # Source current
            i_b = data[:, 5]          # Bulk current
                
            self.logger.info(f"Read bias point data from {bias_file}")
            return vds_points, vgs_points, i_ds, i_g, i_s, i_b
                
        except Exception as e:
            self.logger.error(f"Error reading bias point data: {e}")
            return None, None, None, None, None, None

    # Transient analysis data reading methods
    def read_trans_large_signal_transient_data(self, output_dir):
        """Read large signal transient analysis data from file.
        
        Returns:
            tuple: (time, vgate, vdrain, idrain) arrays of large signal transient data
        """
        try:
            filename = 'tran_large_signal.txt'
            file_path = self._find_file(filename, output_dir, fallback_dirs=[output_dir, 'netlists'])
            
            if not file_path:
                self.logger.warning("Large signal transient data file not found in any location")
                return None, None, None, None
            
            # Read and parse data
            data, _ = self._parse_data_file(file_path, skiprows=2, expected_cols=5)
            if data is None:
                self.logger.warning("No large signal transient data found in file")
                return None, None, None, None
                
            # Extract columns by position rather than by name
            time = data[:, 0]    # First time column
            vgate = data[:, 2]   # v(gate_tran)
            vdrain = data[:, 3]  # v(drain_tran)
            idrain = data[:, 4]  # i(Vds_tran)
            
            self.logger.info("Large signal transient data read successfully")
            return time, vgate, vdrain, idrain
            
        except Exception as e:
            self.logger.error(f"Error reading large signal transient data: {e}")
            return None, None, None, None
            
    def read_trans_switching_response_data(self, output_dir):
        """Read switching response data from file.
        
        Returns:
            tuple: (time, vin, vout, idrain) arrays of switching response data
        """
        try:
            filename = 'tran_switching.txt'
            file_path = self._find_file(filename, output_dir, fallback_dirs=[output_dir, 'netlists'])
            
            if not file_path:
                self.logger.warning("Switching response data file not found in any location")
                return None, None, None, None
            
            # Read and parse data
            data, _ = self._parse_data_file(file_path, skiprows=2, expected_cols=5)
            if data is None:
                self.logger.warning("No switching response data found in file")
                return None, None, None, None
                
            # Extract columns by position rather than by name
            time = data[:, 0]   # First time column
            vin = data[:, 2]    # v(in_inv)
            vout = data[:, 3]   # v(out_inv)
            idrain = data[:, 4]  # i(Vdd_inv)
            
            self.logger.info("Switching response data read successfully")
            return time, vin, vout, idrain
            
        except Exception as e:
            self.logger.error(f"Error reading switching response data: {e}")
            return None, None, None, None
            
    def read_trans_switching_power_data(self, output_dir):
        """Read switching power data from file.
        
        Returns:
            tuple: (time, power) arrays of switching power data
        """
        try:
            filename = 'tran_switching_power.txt'
            file_path = self._find_file(filename, output_dir, fallback_dirs=[self.output_dir, 'netlists'])
            
            if not file_path:
                self.logger.warning("Switching power data file not found in any location")
                return None, None
            
            # Read and parse data
            data, _ = self._parse_data_file(file_path, skiprows=2, expected_cols=3)
            if data is None:
                self.logger.warning("No switching power data found in file")
                return None, None
                
            # Extract columns by position rather than by name
            time = data[:, 0]   # First time column
            power = data[:, 2]  # Power column
            
            self.logger.info("Switching power data read successfully")
            return time, power
            
        except Exception as e:
            self.logger.error(f"Error reading switching power data: {e}")
            return None, None

    def read_trans_delay_effect_data(self, output_dir):
        """Read delay effect data from file.
        
        Returns:
            tuple: (time, vin, v_mid1, v_mid2, vout) arrays of delay effect data
        """
        try:
            filename = 'tran_delay.txt'
            file_path = self._find_file(filename, output_dir, fallback_dirs=[self.output_dir, 'netlists'])
            
            if not file_path:
                self.logger.warning("Delay effect data file not found in any location")
                return None, None, None, None, None
            
            # Read and parse data
            data, _ = self._parse_data_file(file_path, skiprows=2, expected_cols=6)
            if data is None:
                self.logger.warning("No delay effect data found in file")
                return None, None, None, None, None
                
            # Extract columns by position rather than by name
            time = data[:, 0]    # First time column
            vin = data[:, 2]     # v(in_delay)
            v_mid1 = data[:, 3]  # v(mid1_delay)
            v_mid2 = data[:, 4]  # v(mid2_delay)
            vout = data[:, 5]    # v(out_delay)
            
            self.logger.info("Delay effect data read successfully")
            return time, vin, v_mid1, v_mid2, vout
            
        except Exception as e:
            self.logger.error(f"Error reading delay effect data: {e}")
            return None, None, None, None, None
            
    def read_trans_power_dissipation_data(self, output_dir, temperature=27):
        """Read power dissipation data from file.
        
        Args:
            temperature: Temperature in degrees Celsius for the power data to read
            
        Returns:
            tuple: (time, power) arrays of power dissipation data
        """
        try:
            filename = f'tran_power_{temperature}C.txt'
            file_path = self._find_file(filename, output_dir, fallback_dirs=[self.output_dir, 'netlists'])
            
            if not file_path:
                self.logger.warning(f"Power dissipation data file at {temperature}°C not found in any location")
                return None, None
            
            # Read and parse data
            data, _ = self._parse_data_file(file_path, skiprows=2, expected_cols=5)
            if data is None:
                self.logger.warning(f"No power dissipation data at {temperature}°C found in file")
                return None, None
                
            # Extract columns by position rather than by name
            time = data[:, 0]    # First time column
            power = data[:, 4]   # Power column (4th column, 0-indexed)
            
            self.logger.info(f"Power dissipation data for {temperature}°C read successfully")
            return time, power
            
        except Exception as e:
            self.logger.error(f"Error reading power dissipation data at {temperature}°C: {e}")
            return None, None
            
    def read_trans_energy_consumption_data(self, output_dir, temperature=27):
        """Read energy consumption data from file.
        
        Args:
            temperature: Temperature in degrees Celsius for the energy data to read
            
        Returns:
            tuple: (time, energy) arrays of energy consumption data
        """
        try:
            filename = f'tran_power_{temperature}C.txt'
            file_path = self._find_file(filename, output_dir, fallback_dirs=[self.output_dir, 'netlists'])
            
            if not file_path:
                self.logger.warning(f"Energy consumption data file at {temperature}°C not found in any location")
                return None, None
            
            # Read and parse data
            data, _ = self._parse_data_file(file_path, skiprows=2, expected_cols=6)
            if data is None:
                self.logger.warning(f"No energy consumption data at {temperature}°C found in file")
                return None, None
                
            # Extract columns by position rather than by name
            time = data[:, 0]    # First time column
            energy = data[:, 5]  # Energy column (5th column, 0-indexed)
            
            self.logger.info(f"Energy consumption data for {temperature}°C read successfully")
            return time, energy
            
        except Exception as e:
            self.logger.error(f"Error reading energy consumption data at {temperature}°C: {e}")
            return None, None
    
    def read_trans_quasi_static_data(self, output_dir):
        """Read quasi-static analysis data from file.
        
        Returns:
            tuple: (time, vgate, vdrain, idrain) arrays of quasi-static data
        """
        try:
            filename = 'tran_quasi_static.txt'
            file_path = self._find_file(filename, output_dir, fallback_dirs=[output_dir, 'netlists'])
            
            if not file_path:
                self.logger.warning("Quasi-static data file not found in any location")
                return None, None, None, None
            
            # Read and parse data
            data, _ = self._parse_data_file(file_path, skiprows=2, expected_cols=5)
            if data is None:
                self.logger.warning("No quasi-static data found in file")
                return None, None, None, None
                
            # Extract columns by position rather than by name
            time = data[:, 0]    # First time column
            vgate = data[:, 2]   # v(gate_qs)
            vdrain = data[:, 3]  # v(drain_qs)
            idrain = data[:, 4]  # id_qs
            
            self.logger.info("Quasi-static data read successfully")
            return time, vgate, vdrain, idrain
            
        except Exception as e:
            self.logger.error(f"Error reading quasi-static data: {e}")
            return None, None, None, None

    def read_trans_charge_conservation_data(self, output_dir):
        """Read charge conservation test data from output file.
        
        Returns:
            tuple: (time, vg, ig, id, is_, ib) arrays of charge conservation data
        """
        try:
            # First check for tran_charge.txt which contains all charge data
            file_path = os.path.join(output_dir, 'data', 'tran_charge.txt')
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

    def read_trans_charge_conservation_full_data(self, output_dir):
        try:
            file_path = os.path.join(output_dir, 'data', 'tran_charge.txt')
            if not os.path.exists(file_path):
                return (None, None, None, None, None, None, None, None, None, None, None, None)

            data = None
            for skiprows in (2, 1):
                try:
                    candidate = np.loadtxt(file_path, skiprows=skiprows)
                    if len(candidate) > 0 and candidate.shape[1] >= 13:
                        data = candidate
                        break
                except Exception:
                    continue

            if data is None:
                return (None, None, None, None, None, None, None, None, None, None, None, None)

            time = data[:, 0]
            vg = data[:, 2]
            ig = data[:, 3]
            id_ = data[:, 4]
            is_ = data[:, 5]
            ib = data[:, 6]
            i_total = data[:, 7]
            q_gate = data[:, 8]
            q_drain = data[:, 9]
            q_source = data[:, 10]
            q_bulk = data[:, 11]
            q_total = data[:, 12]

            return time, vg, ig, id_, is_, ib, i_total, q_gate, q_drain, q_source, q_bulk, q_total
        except Exception as e:
            self.logger.logger.error(f"Error reading full transient charge conservation data: {e}")
            return (None, None, None, None, None, None, None, None, None, None, None, None)

    # Noise analysis data reading methods
    def read_thermal_noise_data(self, output_dir, vgs=0.3, vds=0.3):
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
            txt_file_path = self._find_file(txt_filename, output_dir)
            
            if txt_file_path:
                # Use custom parser
                freq, noise = self._read_noise_data_file(txt_file_path)
                if freq is not None and noise is not None:
                    self.logger.info(f"Thermal noise data for Vgs={vgs}V, Vds={vds}V read successfully from txt file")
                    # Default temperature is 27°C unless specified otherwise
                    temp = 27
                    # Return a list of temperatures used (usually just the default in this case)
                    temps = np.array([temp])
                    return freq, noise, temp, temps
            
            # Try the raw file if txt file doesn't exist or couldn't be read
            raw_filename = f'thermal_noise_vgs{vgs:.1f}_vds{vds:.1f}.raw'
            raw_file_path = self._find_file(raw_filename, output_dir, fallback_dirs=['netlists'])
            
            if not raw_file_path:
                self.logger.warning(f"Thermal noise data file not found for Vgs={vgs}V, Vds={vds}V")
                return None, None, None, None
            
            # Read the raw file
            freq, noise = self._read_ngspice_raw(raw_file_path)
            if freq is not None and noise is not None:
                self.logger.info(f"Thermal noise data for Vgs={vgs}V, Vds={vds}V read successfully from raw file")
                # Default temperature is 27°C unless specified otherwise
                temp = 27
                # Return a list of temperatures used (usually just the default in this case)
                temps = np.array([temp])
                return freq, noise, temp, temps
            
            return None, None, None, None
                
        except Exception as e:
            self.logger.error(f"Error reading thermal noise data: {e}")
            return None, None, None, None
    
    def read_all_thermal_noise_data(self, output_dir):
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
            freq, noise, _, _ = self.read_thermal_noise_data(output_dir, vgs, vds)
            if freq is not None and noise is not None:
                key = f"Vgs={vgs:.1f}V, Vds={vds:.1f}V"
                thermal_noise_data[key] = (freq, noise)
                self.logger.debug(f"Added thermal noise data for {key}")
        
        if not thermal_noise_data:
            self.logger.warning("No thermal noise data found for any bias point")
        else:
            self.logger.info(f"Read thermal noise data for {len(thermal_noise_data)} bias points")
            
        return thermal_noise_data
    
    def read_flicker_noise_data(self, output_dir):
        """Read flicker noise data from file.
        
        Returns:
            tuple: (freq, noise) arrays of flicker noise data
        """
        try:
            # Try the text file first
            txt_filename = 'flicker_noise.txt'
            txt_file_path = self._find_file(txt_filename, output_dir)
            
            if txt_file_path:
                # Use custom parser
                freq, noise = self._read_noise_data_file(txt_file_path)
                if freq is not None and noise is not None:
                    self.logger.info("Flicker noise data read successfully from txt file")
                    return freq, noise
            
            # Try the raw file if txt file doesn't exist or couldn't be read
            raw_filename = 'flicker_noise.raw'
            raw_file_path = self._find_file(raw_filename, output_dir, fallback_dirs=['netlists'])
            
            if not raw_file_path:
                self.logger.warning("Flicker noise data file not found")
                return None, None
            
            # Read the raw file
            freq, noise = self._read_ngspice_raw(raw_file_path)
            if freq is not None and noise is not None:
                self.logger.info("Flicker noise data read successfully from raw file")
                return freq, noise
            
            return None, None
            
        except Exception as e:
            self.logger.error(f"Error reading flicker noise data: {e}")
            return None, None
    
    def read_shot_noise_data(self, output_dir):
        """Read shot noise data from file.
        
        Returns:
            tuple: (freq, noise) arrays of shot noise data
        """
        try:
            # Try the text file first
            txt_filename = 'shot_noise.txt'
            txt_file_path = self._find_file(txt_filename, output_dir)
            
            if txt_file_path:
                # Use custom parser
                freq, noise = self._read_noise_data_file(txt_file_path)
                if freq is not None and noise is not None:
                    self.logger.info("Shot noise data read successfully from txt file")
                    return freq, noise
            
            # Try the raw file if txt file doesn't exist or couldn't be read
            raw_filename = 'shot_noise.raw'
            raw_file_path = self._find_file(raw_filename, output_dir, fallback_dirs=['netlists'])
            
            if not raw_file_path:
                self.logger.warning("Shot noise data file not found")
                return None, None
            
            # Read the raw file
            freq, noise = self._read_ngspice_raw(raw_file_path)
            if freq is not None and noise is not None:
                self.logger.info("Shot noise data read successfully from raw file")
                return freq, noise
            
            return None, None
            
        except Exception as e:
            self.logger.error(f"Error reading shot noise data: {e}")
            return None, None
    
    def read_temperature_noise_data(self, output_dir):
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
                txt_filename = f'noise_temp{temp}.txt'
                txt_file_path = self._find_file(txt_filename, output_dir)

                if os.path.exists(txt_file_path):
                    # Use custom parser instead of np.loadtxt
                    freq, noise = self._read_noise_data_file(txt_file_path)
                    if freq is not None and noise is not None:
                        noise_data[temp] = (freq, noise)
                        self.logger.debug(f"Temperature noise data at {temp}°C read successfully from txt file")
                        continue
                
                # If txt file doesn't exist or couldn't be read, try raw file
                raw_file_path = os.path.join(self.output_dir, 'data', f'noise_temp{temp}.raw')
                if not os.path.exists(raw_file_path):
                    # Try in netlists directory as fallback
                    raw_file_path = os.path.join('netlists', f'noise_temp{temp}.raw')
                    if not os.path.exists(raw_file_path):
                        self.logger.warning(f"Temperature noise data file not found for {temp}°C")
                        continue
                
                # Read the raw file
                freq, noise = self._read_ngspice_raw(raw_file_path)
                if freq is not None and noise is not None:
                    noise_data[temp] = (freq, noise)
                    self.logger.debug(f"Temperature noise data at {temp}°C read successfully from raw file")
            
            # Check if we have any data
            if not noise_data:
                self.logger.warning("No temperature noise data found")
                return None, None
            
            # Return only the temperatures for which we have data
            valid_temps = list(noise_data.keys())
            self.logger.info(f"Temperature noise data read successfully for temperatures: {valid_temps}")
            return valid_temps, noise_data
            
        except Exception as e:
            self.logger.error(f"Error reading temperature noise data: {e}")
            return None, None

    def read_noise_data_file(self, output_dir):
        """Read noise data files with robust parsing to handle text headers and complex formats.
        
        Args:
            file_path: Path to the noise data file
            
        Returns:
            tuple: (frequency, noise) if successful, else (None, None)
        """
        try:
            if not os.path.exists(file_path):
                self.logger.warning(f"Noise data file not found: {file_path}")
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
            self.logger.warning(f"Could not extract valid data from {file_path}")
            return None, None
            
        except Exception as e:
            self.logger.error(f"Error reading noise data file {file_path}: {e}")
            return None, None

    # AC analysis data reading methods
    def read_cv_data(self, output_dir):
        """Read capacitance-voltage characteristics data.
        
        Returns:
            tuple: (vg, cv_ig, cv_is, cv_ib, cgg) if successful, else (None, None, None, None, None)
        """
        try:
            file_path = self._find_file('cv_data.txt', output_dir)
            if not file_path:
                self.logger.warning("CV data file not found")
                return None, None, None, None, None
            
            # Read CV characteristics data
            vg, cgg, freq, vg_phase, id_phase = self.read_cv_characteristics_data(file_path)
            if vg is None or cgg is None:
                return None, None, None, None, None
            
            # Calculate currents from capacitances
            # For AC analysis, current = jωCV
            # We'll use a reference frequency of 1MHz
            freq = 1e6  # 1MHz
            omega = 2 * np.pi * freq
            
            # Calculate currents
            cv_ig = omega * cgg * vg  # Gate current
            cv_is = omega * cgg * vg  # Source current (using Cgg as approximation)
            cv_ib = omega * cgg * vg  # Bulk current (using Cgg as approximation)
            
            return vg, cv_ig, cv_is, cv_ib, cgg
            
        except Exception as e:
            self.logger.error(f"Error reading CV data: {e}")
            return None, None, None, None, None 

    def read_cv_characteristics_data(self, file_path):
        """Read CV characteristics data from the simulation output."""
        try:
            self.logger.info(f"Reading CV characteristics data from {file_path}")
            
            # Check if file exists
            if not os.path.exists(file_path):
                self.logger.error(f"CV characteristics file not found: {file_path}")
                return None, None, None, None, None
            
            # Try to read the data
            try:
                # Try reading with pandas, which will handle column headers
                data = pd.read_csv(file_path, delim_whitespace=True)
                columns = list(data.columns)
                # If the expected columnar format is present, use it
                if 'Vg' in columns and 'Cgg_1MHz' in columns:
                    vg = data['Vg'].values
                    cgg = data['Cgg_1MHz'].values
                    # For compatibility, fill freq, vg_phase, id_phase with dummy arrays
                    freq = np.full_like(vg, 1e6, dtype=float)  # 1 MHz
                    vg_phase = np.zeros_like(vg, dtype=float)
                    id_phase = np.zeros_like(vg, dtype=float)
                    self.logger.info("Successfully read CV characteristics data (columnar format)")
                    return vg, cgg, freq, vg_phase, id_phase
                # Otherwise, fall through to the next logic
            except Exception as e:
                self.logger.warning(f"Standard parsing failed, attempting to parse ngspice raw file format: {e}")
                data = None
            
            # Try to parse ngspice raw format (previous logic)
            try:
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                data_start = 0
                for i, line in enumerate(lines):
                    if line.strip().startswith('Values:'):
                        data_start = i + 1
                        break
                if data_start == 0:
                    raise ValueError("Could not find data section in ngspice raw file")
                data_lines = []
                for line in lines[data_start:]:
                    line = line.strip()
                    if line and not line.startswith('Date:'):
                        try:
                            values = [float(x) for x in line.split()]
                            if len(values) >= 5:
                                data_lines.append(values)
                        except ValueError:
                            continue
                if not data_lines:
                    raise ValueError("No valid data found in ngspice raw file")
                data = pd.DataFrame(data_lines, columns=['vg', 'cgg', 'freq', 'vg_phase', 'id_phase'])
            except Exception as e:
                self.logger.error(f"Failed to parse ngspice raw format: {e}")
                return None, None, None, None, None
            # Verify we have the required columns
            required_columns = ['vg', 'cgg', 'freq', 'vg_phase', 'id_phase']
            if not all(col in data.columns for col in required_columns):
                self.logger.error(f"Missing required columns in CV data. Found columns: {data.columns}")
                return None, None, None, None, None
            # Extract the data
            vg = data['vg'].values
            cgg = data['cgg'].values
            freq = data['freq'].values
            vg_phase = data['vg_phase'].values
            id_phase = data['id_phase'].values
            self.logger.info("Successfully read CV characteristics data (ngspice raw format)")
            return vg, cgg, freq, vg_phase, id_phase
        except Exception as e:
            self.logger.error(f"Error reading CV characteristics data: {e}")
            return None, None, None, None, None

    def read_sparameter_data(self, output_dir):
        """Read S-parameter data from simulation output.
        
        Returns:
            tuple: (freq, s11_mag, s11_phase, s12_mag, s12_phase, s21_mag, s21_phase, s22_mag, s22_phase)
                   if successful, else tuple of Nones
        """
        try:
            file_path = self._find_file('sparams_data.txt', output_dir)
            if not file_path:
                self.logger.warning("S-parameter data file not found")
                return None, None, None, None, None, None, None, None, None
            
            # Read data with column mapping using two-comment-line parser
            data, col_map = self._parse_data_file_with_comments(
                file_path,
                expected_cols=9,  # freq and 8 S-parameter values (mag and phase)
                col_names=['freq', 's11_mag', 's11_phase', 's12_mag', 's12_phase', 's21_mag', 's21_phase', 's22_mag', 's22_phase']
            )
            
            if data is None or col_map is None:
                return None, None, None, None, None, None, None, None, None
            
            # Extract frequency and S-parameters
            freq = data[:, col_map['freq']]
            s11_mag = data[:, col_map['s11_mag']]
            s11_phase = data[:, col_map['s11_phase']]
            s12_mag = data[:, col_map['s12_mag']]
            s12_phase = data[:, col_map['s12_phase']]
            s21_mag = data[:, col_map['s21_mag']]
            s21_phase = data[:, col_map['s21_phase']]
            s22_mag = data[:, col_map['s22_mag']]
            s22_phase = data[:, col_map['s22_phase']]
            
            return freq, s11_mag, s11_phase, s12_mag, s12_phase, s21_mag, s21_phase, s22_mag, s22_phase
            
        except Exception as e:
            self.logger.error(f"Error reading S-parameter data: {e}")
            return None, None, None, None, None, None, None, None, None

    def read_nqs_effects_data(self, output_dir):
        """Read non-quasi-static effects data from simulation output.
        
        Returns:
            tuple: (nqs_freq, vg_phase, id_phase, phase_diff) if successful, else tuple of Nones
        """
        try:
            file_path = self._find_file('nqs_effects.txt', output_dir)
            if not file_path:
                self.logger.warning("NQS effects data file not found")
                return None, None, None, None
            
            # Read data with column mapping using two-comment-line parser
            data, col_map = self._parse_data_file_with_comments(
                file_path,
                expected_cols=4,  # freq, vg_phase, id_phase, phase_diff
                col_names=['freq', 'vg_phase', 'id_phase', 'phase_diff']
            )
            
            if data is None or col_map is None:
                return None, None, None, None
            
            # Extract data using column mapping
            nqs_freq = data[:, col_map['freq']]
            vg_phase = data[:, col_map['vg_phase']]
            id_phase = data[:, col_map['id_phase']]
            phase_diff = data[:, col_map['phase_diff']]
            
            return nqs_freq, vg_phase, id_phase, phase_diff
            
        except Exception as e:
            self.logger.error(f"Error reading NQS effects data: {e}")
            return None, None, None, None

    def read_charge_conservation_data(self, output_dir):
        """
        Read charge conservation test data from output file.

        Returns:
            tuple: (time, vg, ig, id, is_, ib) arrays of charge conservation data
        """
        try:
            file_path = self._find_file('charge_conservation.txt', output_dir)
            if not file_path:
                file_path = self._find_file('charge_conservation.txt', fallback_dirs=[output_dir, 'netlists'])
            if not file_path:
                self.logger.warning(f"Charge conservation data file not found: {file_path}")
                return None, None, None, None, None, None

            self.logger.info(f"Reading charge conservation data from {file_path}")

            # Robustly parse ngspice raw format: skip to 'Values:', then read blocks
            with open(file_path, 'r') as f:
                lines = f.readlines()
            values_idx = None
            for i, line in enumerate(lines):
                if line.strip() == 'Values:':
                    values_idx = i
                    break
            if values_idx is None:
                self.logger.error("Could not find 'Values:' in charge conservation file")
                return None, None, None, None, None, None
            # Parse data blocks
            time, vg, ig, id, is_, ib = [], [], [], [], [], []
            i = values_idx + 1
            while i < len(lines):
                if lines[i].strip() == '':
                    i += 1
                    continue
                # index and time
                parts = lines[i].strip().split()
                if len(parts) == 2:
                    time.append(float(parts[1]))
                    # next 5 lines: vg, ig, id, is_, ib
                    try:
                        vg.append(float(lines[i+1].strip()))
                        ig.append(float(lines[i+2].strip()))
                        id.append(float(lines[i+3].strip()))
                        is_.append(float(lines[i+4].strip()))
                        ib.append(float(lines[i+5].strip()))
                        i += 6
                        continue
                    except Exception as e:
                        self.logger.warning(f"Error parsing data block at line {i}: {e}")
                        break
                i += 1
            if len(time) > 0:
                return (np.array(time), np.array(vg), np.array(ig), np.array(id), np.array(is_), np.array(ib))
            else:
                self.logger.error("No valid charge conservation data parsed.")
                return None, None, None, None, None, None
        except Exception as e:
            self.logger.error(f"Error reading charge conservation data: {e}")
            import traceback
            traceback.print_exc()
            return None, None, None, None, None, None

    def verify_sparameter_data(self, freq, s11_mag, s12_mag, s21_mag, s22_mag):
        """Verify S-parameter data consistency.
        
        Args:
            freq: Frequency array
            s11_mag: S11 magnitude array
            s12_mag: S12 magnitude array
            s21_mag: S21 magnitude array
            s22_mag: S22 magnitude array
            
        Returns:
            bool: True if data is consistent, False otherwise
        """
        try:
            # Check array lengths
            if not all(len(x) == len(freq) for x in [s11_mag, s12_mag, s21_mag, s22_mag]):
                self.logger.warning("S-parameter arrays have inconsistent lengths")
                return False
            
            # Check for NaN or infinite values
            if any(np.isnan(x).any() or np.isinf(x).any() for x in [freq, s11_mag, s12_mag, s21_mag, s22_mag]):
                self.logger.warning("S-parameter data contains NaN or infinite values")
                return False
            
            # Check frequency is monotonically increasing
            if not np.all(np.diff(freq) > 0):
                self.logger.warning("Frequency array is not monotonically increasing")
                return False
            
            # Check S-parameter magnitudes are between 0 and 1
            if any((x > 1).any() for x in [s11_mag, s12_mag, s21_mag, s22_mag]):
                self.logger.warning("S-parameter magnitudes exceed 1")
                return False
            
            # Check reciprocity (S12 ≈ S21 for passive devices)
            if not np.allclose(s12_mag, s21_mag, rtol=0.1):  # 10% tolerance
                self.logger.warning("S-parameter reciprocity check failed")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error verifying S-parameter data: {e}")
            return False
    
    def verify_cv_data(self, vg, cgg, cgd, cgs, cgb):
        """Verify CV data consistency.
        
        Args:
            vg: Gate voltage array
            cgg: Gate-gate capacitance array
            cgd: Gate-drain capacitance array
            cgs: Gate-source capacitance array
            cgb: Gate-bulk capacitance array
            
        Returns:
            bool: True if data is consistent, False otherwise
        """
        try:
            # Check array lengths
            if not all(len(x) == len(vg) for x in [cgg, cgd, cgs, cgb]):
                self.logger.warning("CV data arrays have inconsistent lengths")
                return False
            
            # Check for NaN or infinite values
            if any(np.isnan(x).any() or np.isinf(x).any() for x in [vg, cgg, cgd, cgs, cgb]):
                self.logger.warning("CV data contains NaN or infinite values")
                return False
            
            # Check capacitance values are positive
            if any((x < 0).any() for x in [cgg, cgd, cgs, cgb]):
                self.logger.warning("CV data contains negative capacitance values")
                return False
            
            # Check total capacitance consistency
            # Cgg should be approximately equal to Cgd + Cgs + Cgb
            total_cap = cgd + cgs + cgb
            if not np.allclose(cgg, total_cap, rtol=0.1):  # 10% tolerance
                self.logger.warning("CV data total capacitance mismatch")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error verifying CV data: {e}")
            return False
