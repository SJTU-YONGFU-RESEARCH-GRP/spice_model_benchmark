import numpy as np
from pathlib import Path
import os
import re

class DataReader:
    """Handles reading and parsing simulation data files."""
    def __init__(self, logger, output_dir='results'):
        self.logger = logger
        self.output_dir = output_dir
    
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
                # First check in data directory
                file_path = os.path.join(self.output_dir, 'data', filename)
                if not os.path.exists(file_path):
                    # If not there, check in main output directory as fallback
                    file_path = os.path.join(self.output_dir, filename)
                    if not os.path.exists(file_path):
                        self.logger.logger.warning(f"IV data file not found at {file_path}")
                        continue
                    
                self.logger.logger.debug(f"Reading data for temperature {temp}°C from {filename}")
                
                try:
                    # Read data with column names
                    with open(file_path, 'r') as f:
                        header = f.readline().strip().split()
                        data = np.loadtxt(file_path, skiprows=2)  # Skip header and column names
                    
                    if len(data) > 0:
                        # Map columns based on header names
                        col_map = {name: i for i, name in enumerate(header)}
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
            # First check in data directory
            cv_file = os.path.join(self.output_dir, 'data', 'cv_data.txt')
            if not os.path.exists(cv_file):
                # If not there, check in main output directory as fallback
                cv_file = os.path.join(self.output_dir, 'cv_data.txt')
                if not os.path.exists(cv_file):
                    self.logger.logger.warning(f"CV data file not found: {cv_file}")
                    return None, None, None, None, None
                
            self.logger.logger.info(f"Reading CV data from {cv_file}")
            
            # Read data file
            with open(cv_file, 'r') as f:
                lines = f.readlines()
            
            # Parse the header to determine columns
            header = lines[0].strip().split()
            
            # Parse data
            data = []
            for line in lines[1:]:  # Skip header
                try:
                    parts = line.strip().split()
                    if len(parts) >= 5:  # At least Vg and 4 capacitance values
                        row = []
                        for i in range(min(len(parts), 8)):  # Get up to 8 columns
                            row.append(float(parts[i]))
                        data.append(row)
                except Exception as e:
                    self.logger.logger.warning(f"Error parsing line in CV data: {line.strip()}, {e}")
                    continue
            
            if not data:
                self.logger.logger.error("No valid CV data could be parsed")
                return None, None, None, None, None
                
            data = np.array(data)
            
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
                # First check in data directory
                file_path = os.path.join(self.output_dir, 'data', filename)
                if not os.path.exists(file_path):
                    # If not there, check in main output directory as fallback
                    file_path = os.path.join(self.output_dir, filename)
                    if not os.path.exists(file_path):
                        self.logger.logger.warning(f"Temperature data file not found at {file_path}")
                        continue
                    
                try:
                    data = np.loadtxt(file_path, skiprows=2)  # Skip header and column names
                    if len(data) > 0:
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
            
            # First check in data directory
            data_dir_path = os.path.join(self.output_dir, 'data')
            if os.path.exists(data_dir_path):
                for filename in os.listdir(data_dir_path):
                    if filename == 'bias_point_data.txt' or filename.startswith('bias_point_data_'):
                        bias_file = os.path.join(data_dir_path, filename)
                        break
            
            # If not found, check in output directory
            if bias_file is None:
                for filename in os.listdir(self.output_dir):
                    if filename == 'bias_point_data.txt' or filename.startswith('bias_point_data_'):
                        bias_file = os.path.join(self.output_dir, filename)
                        break
            
            if bias_file is None:
                self.logger.logger.info("No bias point data file found - skipping bias point analysis")
                return None, None, None, None, None, None
            
            # Read data from file
            data = np.loadtxt(bias_file, skiprows=1)
            
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
            # First check in data directory
            file_path = os.path.join(self.output_dir, 'data', 'tran_large_signal.txt')
            if not os.path.exists(file_path):
                # If not there, check in main output directory
                file_path = os.path.join(self.output_dir, 'tran_large_signal.txt')
                if not os.path.exists(file_path):
                    # As a last resort, try in netlists directory
                    file_path = os.path.join('netlists', 'tran_large_signal.txt')
                    if not os.path.exists(file_path):
                        self.logger.logger.warning(f"Large signal transient data file not found in any location")
                        return None, None, None, None
                    else:
                        self.logger.logger.info(f"Found large signal transient data in netlists directory")
                
            # Read data directly with numpy
            try:
                data = np.loadtxt(file_path, skiprows=2)
                if len(data) == 0:
                    self.logger.logger.warning("No large signal transient data found in file")
                    return None, None, None, None
                    
                # Extract columns by position rather than by name
                time = data[:, 0]  # First time column
                vgate = data[:, 2]  # v(gate_tran)
                vdrain = data[:, 3]  # v(drain_tran)
                idrain = data[:, 4]  # i(Vds_tran)
                
                self.logger.logger.info("Large signal transient data read successfully")
                return time, vgate, vdrain, idrain
            except Exception as e:
                self.logger.logger.error(f"Error parsing large signal transient data: {e}")
                return None, None, None, None
            
        except Exception as e:
            self.logger.logger.error(f"Error reading large signal transient data: {e}")
            return None, None, None, None
            
    def read_switching_response_data(self):
        """Read switching response data from file.
        
        Returns:
            tuple: (time, vin, vout, idrain) arrays of switching response data
        """
        try:
            # First check in data directory
            file_path = os.path.join(self.output_dir, 'data', 'tran_switching.txt')
            if not os.path.exists(file_path):
                # If not there, check in main output directory
                file_path = os.path.join(self.output_dir, 'tran_switching.txt')
                if not os.path.exists(file_path):
                    # As a last resort, try in netlists directory
                    file_path = os.path.join('netlists', 'tran_switching.txt')
                    if not os.path.exists(file_path):
                        self.logger.logger.warning(f"Switching response data file not found in any location")
                        return None, None, None, None
                    else:
                        self.logger.logger.info(f"Found switching response data in netlists directory")
                
            # Read data directly with numpy
            try:
                data = np.loadtxt(file_path, skiprows=2)
                if len(data) == 0:
                    self.logger.logger.warning("No switching response data found in file")
                    return None, None, None, None
                    
                # Extract columns by position rather than by name
                time = data[:, 0]  # First time column
                vin = data[:, 2]   # v(in_inv)
                vout = data[:, 3]  # v(out_inv)
                idrain = data[:, 4]  # i(Vdd_inv)
                
                self.logger.logger.info("Switching response data read successfully")
                return time, vin, vout, idrain
            except Exception as e:
                self.logger.logger.error(f"Error parsing switching response data: {e}")
                return None, None, None, None
            
        except Exception as e:
            self.logger.logger.error(f"Error reading switching response data: {e}")
            return None, None, None, None
            
    def read_switching_power_data(self):
        """Read switching power data from file.
        
        Returns:
            tuple: (time, power) arrays of switching power data
        """
        try:
            # First check in data directory
            file_path = os.path.join(self.output_dir, 'data', 'tran_switching_power.txt')
            if not os.path.exists(file_path):
                # If not there, check in main output directory
                file_path = os.path.join(self.output_dir, 'tran_switching_power.txt')
                if not os.path.exists(file_path):
                    # As a last resort, try in netlists directory
                    file_path = os.path.join('netlists', 'tran_switching_power.txt')
                    if not os.path.exists(file_path):
                        self.logger.logger.warning(f"Switching power data file not found in any location")
                        return None, None
                    else:
                        self.logger.logger.info(f"Found switching power data in netlists directory")
                
            # Read data directly with numpy
            try:
                data = np.loadtxt(file_path, skiprows=2)
                if len(data) == 0:
                    self.logger.logger.warning("No switching power data found in file")
                    return None, None
                    
                # Extract columns by position rather than by name
                time = data[:, 0]  # First time column
                power = data[:, 2]  # Power column
                
                self.logger.logger.info("Switching power data read successfully")
                return time, power
            except Exception as e:
                self.logger.logger.error(f"Error parsing switching power data: {e}")
                return None, None
            
        except Exception as e:
            self.logger.logger.error(f"Error reading switching power data: {e}")
            return None, None

    def read_delay_effect_data(self):
        """Read delay effect data from file.
        
        Returns:
            tuple: (time, vin, v_mid1, v_mid2, vout) arrays of delay effect data
        """
        try:
            # First check in data directory
            file_path = os.path.join(self.output_dir, 'data', 'tran_delay.txt')
            if not os.path.exists(file_path):
                # If not there, check in main output directory
                file_path = os.path.join(self.output_dir, 'tran_delay.txt')
                if not os.path.exists(file_path):
                    # As a last resort, try in netlists directory
                    file_path = os.path.join('netlists', 'tran_delay.txt')
                    if not os.path.exists(file_path):
                        self.logger.logger.warning(f"Delay effect data file not found in any location")
                        return None, None, None, None, None
                    else:
                        self.logger.logger.info(f"Found delay effect data in netlists directory")
                
            # Read data directly with numpy
            try:
                data = np.loadtxt(file_path, skiprows=2)
                if len(data) == 0:
                    self.logger.logger.warning("No delay effect data found in file")
                    return None, None, None, None, None
                    
                # Extract columns by position rather than by name
                time = data[:, 0]  # First time column
                vin = data[:, 2]   # v(in_delay)
                v_mid1 = data[:, 3]  # v(mid1_delay)
                v_mid2 = data[:, 4]  # v(mid2_delay)
                vout = data[:, 5]  # v(out_delay)
                
                self.logger.logger.info("Delay effect data read successfully")
                return time, vin, v_mid1, v_mid2, vout
            except Exception as e:
                self.logger.logger.error(f"Error parsing delay effect data: {e}")
                return None, None, None, None, None
            
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
            # First check in data directory
            file_path = os.path.join(self.output_dir, 'data', f'tran_power_{temperature}C.txt')
            if not os.path.exists(file_path):
                # If not there, check in main output directory
                file_path = os.path.join(self.output_dir, f'tran_power_{temperature}C.txt')
                if not os.path.exists(file_path):
                    # As a last resort, try in netlists directory
                    file_path = os.path.join('netlists', f'tran_power_{temperature}C.txt')
                    if not os.path.exists(file_path):
                        self.logger.logger.warning(f"Power dissipation data file at {temperature}°C not found in any location")
                        return None, None
                    else:
                        self.logger.logger.info(f"Found power dissipation data for {temperature}°C in netlists directory")
                
            # Read data directly with numpy
            try:
                data = np.loadtxt(file_path, skiprows=2)
                if len(data) == 0:
                    self.logger.logger.warning(f"No power dissipation data at {temperature}°C found in file")
                    return None, None
                    
                # Extract columns by position rather than by name
                time = data[:, 0]  # First time column
                power = data[:, 4]  # Power column (4th column, 0-indexed)
                
                self.logger.logger.info(f"Power dissipation data for {temperature}°C read successfully")
                return time, power
            except Exception as e:
                self.logger.logger.error(f"Error parsing power dissipation data at {temperature}°C: {e}")
                return None, None
            
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
            # First check in data directory
            file_path = os.path.join(self.output_dir, 'data', f'tran_power_{temperature}C.txt')
            if not os.path.exists(file_path):
                # If not there, check in main output directory
                file_path = os.path.join(self.output_dir, f'tran_power_{temperature}C.txt')
                if not os.path.exists(file_path):
                    # As a last resort, try in netlists directory
                    file_path = os.path.join('netlists', f'tran_power_{temperature}C.txt')
                    if not os.path.exists(file_path):
                        self.logger.logger.warning(f"Energy consumption data file at {temperature}°C not found in any location")
                        return None, None
                    else:
                        self.logger.logger.info(f"Found energy consumption data for {temperature}°C in netlists directory")
                
            # Read data directly with numpy
            try:
                data = np.loadtxt(file_path, skiprows=2)
                if len(data) == 0:
                    self.logger.logger.warning(f"No energy consumption data at {temperature}°C found in file")
                    return None, None
                    
                # Extract columns by position rather than by name
                time = data[:, 0]  # First time column
                energy = data[:, 5]  # Energy column (5th column, 0-indexed)
                
                self.logger.logger.info(f"Energy consumption data for {temperature}°C read successfully")
                return time, energy
            except Exception as e:
                self.logger.logger.error(f"Error parsing energy consumption data at {temperature}°C: {e}")
                return None, None
            
        except Exception as e:
            self.logger.logger.error(f"Error reading energy consumption data at {temperature}°C: {e}")
            return None, None
    
    def read_quasi_static_data(self):
        """Read quasi-static analysis data from file.
        
        Returns:
            tuple: (time, vgate, vdrain, idrain) arrays of quasi-static data
        """
        try:
            # First check in data directory
            file_path = os.path.join(self.output_dir, 'data', 'tran_quasi_static.txt')
            if not os.path.exists(file_path):
                # If not there, check in main output directory
                file_path = os.path.join(self.output_dir, 'tran_quasi_static.txt')
                if not os.path.exists(file_path):
                    # As a last resort, try in netlists directory
                    file_path = os.path.join('netlists', 'tran_quasi_static.txt')
                    if not os.path.exists(file_path):
                        self.logger.logger.warning(f"Quasi-static data file not found in any location")
                        return None, None, None, None
                    else:
                        self.logger.logger.info(f"Found quasi-static data in netlists directory")
                
            # Read data directly with numpy
            try:
                data = np.loadtxt(file_path, skiprows=2)
                if len(data) == 0:
                    self.logger.logger.warning("No quasi-static data found in file")
                    return None, None, None, None
                    
                # Extract columns by position rather than by name
                time = data[:, 0]  # First time column
                vgate = data[:, 2]  # v(gate_qs)
                vdrain = data[:, 3]  # v(drain_qs)
                idrain = data[:, 4]  # id_qs
                
                self.logger.logger.info("Quasi-static data read successfully")
                return time, vgate, vdrain, idrain
            except Exception as e:
                self.logger.logger.error(f"Error parsing quasi-static data: {e}")
                return None, None, None, None
            
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
                        import shutil
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
    
    # Helper method to read NGSpice raw files
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

    # Helper method to read noise data files with robust parsing to handle text headers and complex formats
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
            # First try reading from .txt file in data directory
            txt_file_path = os.path.join(self.output_dir, 'data', f'thermal_noise_vgs{vgs:.1f}_vds{vds:.1f}.txt')
            if os.path.exists(txt_file_path):
                # Use custom parser instead of np.loadtxt
                freq, noise = self._read_noise_data_file(txt_file_path)
                if freq is not None and noise is not None:
                    self.logger.logger.info(f"Thermal noise data for Vgs={vgs}V, Vds={vds}V read successfully from txt file")
                    # Default temperature is 27°C unless specified otherwise
                    temp = 27
                    # Return a list of temperatures used (usually just the default in this case)
                    temps = np.array([temp])
                    return freq, noise, temp, temps
            
            # If txt file doesn't exist or couldn't be read, try raw file
            raw_file_path = os.path.join(self.output_dir, 'data', f'thermal_noise_vgs{vgs:.1f}_vds{vds:.1f}.raw')
            if not os.path.exists(raw_file_path):
                # Try in netlists directory as fallback
                raw_file_path = os.path.join('netlists', f'thermal_noise_vgs{vgs:.1f}_vds{vds:.1f}.raw')
                if not os.path.exists(raw_file_path):
                    self.logger.logger.warning(f"Thermal noise data file not found: {raw_file_path}")
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
            # First try reading from .txt file in data directory
            txt_file_path = os.path.join(self.output_dir, 'data', 'flicker_noise.txt')
            if os.path.exists(txt_file_path):
                # Use custom parser instead of np.loadtxt
                freq, noise = self._read_noise_data_file(txt_file_path)
                if freq is not None and noise is not None:
                    self.logger.logger.info("Flicker noise data read successfully from txt file")
                    return freq, noise
            
            # If txt file doesn't exist or couldn't be read, try raw file
            raw_file_path = os.path.join(self.output_dir, 'data', 'flicker_noise.raw')
            if not os.path.exists(raw_file_path):
                # Try in netlists directory as fallback
                raw_file_path = os.path.join('netlists', 'flicker_noise.raw')
                if not os.path.exists(raw_file_path):
                    self.logger.logger.warning(f"Flicker noise data file not found: {raw_file_path}")
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
            # First try reading from .txt file in data directory
            txt_file_path = os.path.join(self.output_dir, 'data', 'shot_noise.txt')
            if os.path.exists(txt_file_path):
                # Use custom parser instead of np.loadtxt
                freq, noise = self._read_noise_data_file(txt_file_path)
                if freq is not None and noise is not None:
                    self.logger.logger.info("Shot noise data read successfully from txt file")
                    return freq, noise
            
            # If txt file doesn't exist or couldn't be read, try raw file
            raw_file_path = os.path.join(self.output_dir, 'data', 'shot_noise.raw')
            if not os.path.exists(raw_file_path):
                # Try in netlists directory as fallback
                raw_file_path = os.path.join('netlists', 'shot_noise.raw')
                if not os.path.exists(raw_file_path):
                    self.logger.logger.warning(f"Shot noise data file not found: {raw_file_path}")
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
            file_path = os.path.join(self.output_dir, 'data', 'sparams_data.txt')
            if not os.path.exists(file_path):
                # If not there, check in main output directory as fallback
                file_path = os.path.join(self.output_dir, 'sparams_data.txt')
                if not os.path.exists(file_path):
                    self.logger.logger.warning(f"S-parameter data file not found: {file_path}")
                    return None, None, None, None, None
            
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
                return None, None, None, None, None
            
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
            return freq, s11_mag, s21_mag, s12_mag, s22_mag
            
        except Exception as e:
            self.logger.logger.error(f"Error reading S-parameter data: {e}")
            import traceback
            traceback.print_exc()
            return None, None, None, None, None
    
    def read_nqs_effects_data(self):
        """Read non-quasi-static effects data from output file.
        
        Returns:
            tuple: (freq, vg_phase, id_phase, phase_diff) arrays of NQS effect data
        """
        try:
            # First check in data directory
            file_path = os.path.join(self.output_dir, 'data', 'nqs_effects.txt')
            if not os.path.exists(file_path):
                # If not there, check in main output directory as fallback
                file_path = os.path.join(self.output_dir, 'nqs_effects.txt')
                if not os.path.exists(file_path):
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
            import traceback
            traceback.print_exc()
            return None, None, None, None 