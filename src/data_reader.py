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