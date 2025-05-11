import numpy as np
from pathlib import Path
import os

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
            cv_file = os.path.join(self.output_dir, 'cv_data.txt')
            if not os.path.exists(cv_file):
                self.logger.logger.warning(f"CV data file not found: {cv_file}")
                return None, None, None, None, None
                
            # Read data with column names
            with open(cv_file, 'r') as f:
                header = f.readline().strip().split()
                data = np.loadtxt(cv_file, skiprows=2)  # Skip header and column names
            
            if len(data) == 0:
                self.logger.logger.warning("No CV data found in file")
                return None, None, None, None, None
                
            # Map columns based on header names
            col_map = {name: i for i, name in enumerate(header)}
            vg = data[:, col_map['v(gate_cv)']]
            cgg = data[:, col_map['cgg']]
            ig = data[:, col_map['ig_cv']]
            is_ = data[:, col_map['is_cv']]
            ib = data[:, col_map['ib_cv']]
            
            self.logger.logger.info("CV characteristics data read successfully")
            return vg, ig, is_, ib, cgg
            
        except Exception as e:
            self.logger.logger.error(f"Error reading CV data: {e}")
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
            for filename in os.listdir(self.output_dir):
                if filename.startswith('bias_point_data_'):
                    bias_file = os.path.join(self.output_dir, filename)
                    break
            
            if bias_file is None:
                self.logger.logger.warning("No bias point data file found")
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
            # Try in output_dir first, then in netlists directory
            file_path = os.path.join(self.output_dir, 'tran_large_signal.txt')
            if not os.path.exists(file_path):
                file_path = os.path.join('netlists', 'tran_large_signal.txt')
                if not os.path.exists(file_path):
                    self.logger.logger.warning(f"Large signal transient data file not found in either {self.output_dir} or netlists directory")
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
            # Try in output_dir first, then in netlists directory
            file_path = os.path.join(self.output_dir, 'tran_switching.txt')
            if not os.path.exists(file_path):
                file_path = os.path.join('netlists', 'tran_switching.txt')
                if not os.path.exists(file_path):
                    self.logger.logger.warning(f"Switching response data file not found in either {self.output_dir} or netlists directory")
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
            # Try in output_dir first, then in netlists directory
            file_path = os.path.join(self.output_dir, 'tran_switching_power.txt')
            if not os.path.exists(file_path):
                file_path = os.path.join('netlists', 'tran_switching_power.txt')
                if not os.path.exists(file_path):
                    self.logger.logger.warning(f"Switching power data file not found in either {self.output_dir} or netlists directory")
                    return None, None
                else:
                    self.logger.logger.info(f"Found switching power data in netlists directory")
                
            # Read data directly with numpy
            try:
                data = np.loadtxt(file_path, skiprows=2)
                if len(data) == 0:
                    self.logger.logger.warning("No switching power data found in file")
                    return None, None
                    
                # Extract columns by position - this file only has time and power
                time = data[:, 0]  # First time column
                power = data[:, 2]  # Power column (power_switching)
                
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
            tuple: (time, vin, v1, v2, vout) arrays of delay chain data
        """
        try:
            # Try in output_dir first, then in netlists directory
            file_path = os.path.join(self.output_dir, 'tran_delay.txt')
            if not os.path.exists(file_path):
                file_path = os.path.join('netlists', 'tran_delay.txt')
                if not os.path.exists(file_path):
                    self.logger.logger.warning(f"Delay effect data file not found in either {self.output_dir} or netlists directory")
                    return None, None, None, None, None
                else:
                    self.logger.logger.info(f"Found delay effect data in netlists directory")
                
            # Read data directly with numpy
            try:
                data = np.loadtxt(file_path, skiprows=2)
                if len(data) == 0:
                    self.logger.logger.warning("No delay effect data found in file")
                    return None, None, None, None, None
                    
                # Extract columns by position - based on actual file structure
                time = data[:, 0]          # First time column
                vin = data[:, 2]           # v(in_delay)
                v_mid1 = data[:, 3]        # v(mid1_delay)
                v_mid2 = data[:, 4]        # v(mid2_delay)
                vout = data[:, 5]          # v(out_delay)
                
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
            temperature: Temperature in Celsius (27 or 100)
            
        Returns:
            tuple: (time, power) arrays of power dissipation data
        """
        try:
            if temperature == 27:
                file_name = 'tran_power_27C.txt'
            elif temperature == 100:
                file_name = 'tran_power_100C.txt'
            else:
                self.logger.logger.warning(f"Invalid temperature: {temperature}. Using 27°C")
                file_name = 'tran_power_27C.txt'
            
            # Try in output_dir first, then in netlists directory
            file_path = os.path.join(self.output_dir, file_name)
            if not os.path.exists(file_path):
                file_path = os.path.join('netlists', file_name)
                if not os.path.exists(file_path):
                    self.logger.logger.warning(f"Power dissipation data file not found in either {self.output_dir} or netlists directory")
                    return None, None
                else:
                    self.logger.logger.info(f"Found power dissipation data in netlists directory")
                
            # Read data directly with numpy
            try:
                data = np.loadtxt(file_path, skiprows=2)
                if len(data) == 0:
                    self.logger.logger.warning("No power dissipation data found in file")
                    return None, None
                    
                # Extract columns by position
                time = data[:, 0]  # First time column
                power = data[:, 4]  # Power column (power_diss)
                
                self.logger.logger.info(f"Power dissipation data at {temperature}°C read successfully")
                return time, power
            except Exception as e:
                self.logger.logger.error(f"Error parsing power dissipation data: {e}")
                return None, None
            
        except Exception as e:
            self.logger.logger.error(f"Error reading power dissipation data: {e}")
            return None, None
            
    def read_quasi_static_data(self):
        """Read quasi-static analysis data from file.
        
        Returns:
            tuple: (time, vgate, vdrain, idrain) arrays of quasi-static data
        """
        try:
            # Try in output_dir first, then in netlists directory
            file_path = os.path.join(self.output_dir, 'tran_quasi_static.txt')
            if not os.path.exists(file_path):
                file_path = os.path.join('netlists', 'tran_quasi_static.txt')
                if not os.path.exists(file_path):
                    self.logger.logger.warning(f"Quasi-static data file not found in either {self.output_dir} or netlists directory")
                    return None, None, None, None
                else:
                    self.logger.logger.info(f"Found quasi-static data in netlists directory")
                
            # Read data directly with numpy
            try:
                data = np.loadtxt(file_path, skiprows=2)
                if len(data) == 0:
                    self.logger.logger.warning("No quasi-static data found in file")
                    return None, None, None, None
                    
                # Extract columns by position
                time = data[:, 0]   # First time column
                vgate = data[:, 2]  # Gate voltage
                vdrain = data[:, 3] # Drain voltage
                idrain = data[:, 4] # Drain current
                
                self.logger.logger.info("Quasi-static data read successfully")
                return time, vgate, vdrain, idrain
            except Exception as e:
                self.logger.logger.error(f"Error parsing quasi-static data: {e}")
                return None, None, None, None
            
        except Exception as e:
            self.logger.logger.error(f"Error reading quasi-static data: {e}")
            return None, None, None, None
            
    def read_charge_conservation_data(self):
        """Read charge conservation analysis data from file.
        
        Returns:
            tuple: (time, vgate, vdrain, id, ig, is, ib) arrays of charge conservation data
        """
        try:
            # Try in output_dir first, then in netlists directory
            file_path = os.path.join(self.output_dir, 'tran_charge.txt')
            if not os.path.exists(file_path):
                file_path = os.path.join('netlists', 'tran_charge.txt')
                if not os.path.exists(file_path):
                    self.logger.logger.warning(f"Charge conservation data file not found in either {self.output_dir} or netlists directory")
                    return None, None, None, None, None, None, None
                else:
                    self.logger.logger.info(f"Found charge conservation data in netlists directory")
                
            # Read data directly with numpy
            try:
                data = np.loadtxt(file_path, skiprows=2)
                if len(data) == 0:
                    self.logger.logger.warning("No charge conservation data found in file")
                    return None, None, None, None, None, None, None
                    
                # Extract columns by position
                time = data[:, 0]   # First time column
                vgate = data[:, 2]  # Gate voltage
                vdrain = data[:, 3] # Drain voltage
                id = data[:, 4]     # Drain current
                ig = data[:, 5]     # Gate current
                is_ = data[:, 6]    # Source current
                ib = data[:, 7]     # Bulk current
                
                self.logger.logger.info("Charge conservation data read successfully")
                return time, vgate, vdrain, id, ig, is_, ib
            except Exception as e:
                self.logger.logger.error(f"Error parsing charge conservation data: {e}")
                return None, None, None, None, None, None, None
            
        except Exception as e:
            self.logger.logger.error(f"Error reading charge conservation data: {e}")
            return None, None, None, None, None, None, None 