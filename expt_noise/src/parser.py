import os
import re
import numpy as np
import pandas as pd

class SpiceResultParser:
    """
    Parser for SPICE simulation result files with methods for different analysis types
    """
    def __init__(self, logger):
        """
        Initialize the parser
        
        Args:
            logger: Logger instance for logging messages
        """
        self.logger = logger
        self.logger.info("SpiceResultParser initialized")
        
    def read_spice_raw_file(self, filename):
        """
        Read a SPICE raw format file with triplet data format
        
        Args:
            filename: Path to the SPICE raw data file
            
        Returns:
            pandas.DataFrame: DataFrame containing the frequency and noise data
        """
        try:
            freq_data = []
            noise_data = []
            
            with open(filename, 'r') as f:
                lines = f.readlines()
                
                # Skip header until "Values:" section
                values_idx = 0
                for i, line in enumerate(lines):
                    if "Values:" in line:
                        values_idx = i + 1
                        break
                
                # Process the data in triplets
                i = values_idx
                while i < len(lines):
                    # Each triplet consists of: index, frequency, value
                    # Skip the index line
                    i += 1
                    if i >= len(lines):
                        break
                        
                    # Read frequency
                    if i < len(lines) and lines[i].strip():
                        try:
                            freq = float(lines[i].strip())
                            freq_data.append(freq)
                            i += 1
                        except:
                            i += 1
                            continue
                    
                    # Read noise value
                    if i < len(lines) and lines[i].strip():
                        try:
                            noise = float(lines[i].strip())
                            noise_data.append(noise)
                            i += 1
                        except:
                            i += 1
                            continue
                    
                    # Skip any empty lines
                    while i < len(lines) and not lines[i].strip():
                        i += 1
            
            # Create DataFrame
            if len(freq_data) == len(noise_data) and len(freq_data) > 0:
                return pd.DataFrame({
                    'frequency': freq_data,
                    'noise': noise_data
                })
            else:
                self.logger.error(f"Mismatched data lengths: freq={len(freq_data)}, noise={len(noise_data)}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error parsing SPICE raw file {filename}: {str(e)}")
            return None
        
    def read_noise_data(self, filename):
        """
        Read noise data from SPICE output file
        
        Args:
            filename: Path to the noise data file
            
        Returns:
            pandas.DataFrame: DataFrame containing the parsed noise data
        """
        if not os.path.exists(filename):
            self.logger.error(f"File not found: {filename}")
            return None
            
        try:
            # Check file format based on header
            with open(filename, 'r') as f:
                # Read first few lines to determine file format
                first_lines = []
                for i in range(10):
                    try:
                        line = next(f)
                        first_lines.append(line)
                    except StopIteration:
                        break
                        
                has_title = any("Title:" in line for line in first_lines)
                has_header = any("Variables:" in line for line in first_lines)
                has_plain_header = any(line.strip().startswith("frequency") for line in first_lines)
            
            if has_title or has_header:
                # This is a SPICE raw format file with formal header
                self.logger.info(f"Successfully parsed noise data from {filename}")
                return self.read_spice_raw_file(filename)
            elif has_plain_header:
                # This might be tab-separated output with column names
                try:
                    data = pd.read_csv(filename, sep=r'\s+', comment='*')
                    if not data.empty:
                        self.logger.info(f"Successfully parsed noise data from {filename}")
                        return data
                except Exception as e:
                    self.logger.error(f"Error parsing tabular data from {filename}: {str(e)}")
                    return None
            else:
                # Try to parse as space-separated data without header
                try:
                    data = pd.read_csv(filename, sep=r'\s+', header=None, comment='*')
                    if not data.empty:
                        # Assign default column names
                        data.columns = [f"Column{i}" for i in range(len(data.columns))]
                        self.logger.info(f"Successfully parsed noise data from {filename}")
                        return data
                except Exception as e:
                    self.logger.error(f"Error parsing headerless data from {filename}: {str(e)}")
                    return None
                
        except Exception as e:
            self.logger.error(f"Error reading noise data from {filename}: {str(e)}")
            return None
            
    def analyze_thermal_noise(self, data):
        """
        Analyze thermal noise data
        
        Args:
            data: DataFrame containing thermal noise data
            
        Returns:
            dict: Dictionary containing analysis results
        """
        try:
            if data is None or data.empty:
                return {"status": "error", "message": "No data available"}
                
            # Calculate noise statistics
            freq = data.iloc[:, 0].values  # Frequency column
            noise = data.iloc[:, 1].values  # Noise column
            
            # Basic statistics
            max_noise = np.max(noise)
            min_noise = np.min(noise)
            avg_noise = np.mean(noise)
            
            # Find noise floor (average of highest frequency noise values)
            high_freq_indices = freq > freq.max() * 0.8
            noise_floor = np.mean(noise[high_freq_indices]) if any(high_freq_indices) else np.min(noise)
            
            # Calculate noise spectral density
            noise_density = noise / np.sqrt(freq)
            avg_noise_density = np.mean(noise_density)
            
            # Find frequency where noise is 3dB above the floor
            noise_3db = noise_floor * np.sqrt(2)
            corner_freq_indices = noise > noise_3db
            corner_freq = np.min(freq[corner_freq_indices]) if any(corner_freq_indices) else None
            
            results = {
                "status": "success",
                "max_noise": max_noise,
                "min_noise": min_noise,
                "avg_noise": avg_noise,
                "noise_floor": noise_floor,
                "avg_noise_density": avg_noise_density,
                "corner_frequency": corner_freq
            }
            
            return results
        except Exception as e:
            self.logger.error(f"Error analyzing thermal noise: {str(e)}")
            return {"status": "error", "message": str(e)}
            
    def analyze_flicker_noise(self, data):
        """
        Analyze flicker (1/f) noise data
        
        Args:
            data: DataFrame containing flicker noise data
            
        Returns:
            dict: Dictionary containing analysis results
        """
        try:
            if data is None or data.empty:
                return {"status": "error", "message": "No data available"}
                
            # Extract frequency and noise data
            freq = data.iloc[:, 0].values  # Frequency column
            noise = data.iloc[:, 1].values  # Noise column
            
            # For 1/f noise, the product of noise * frequency should be approximately constant
            # Calculate normalized noise (noise * frequency)
            normalized_noise = noise * freq
            
            # Calculate flicker noise coefficient (K)
            # For true 1/f noise, K should be consistent across frequencies
            K_values = normalized_noise
            K_avg = np.mean(K_values)
            K_std = np.std(K_values)
            
            # Calculate flicker noise exponent (gamma)
            # For pure 1/f noise, gamma should be close to 1
            # Use linear regression on log-log scale
            log_freq = np.log10(freq)
            log_noise = np.log10(noise)
            
            # Simple linear regression to find slope (gamma)
            if len(log_freq) > 1:
                slope, intercept = np.polyfit(log_freq, log_noise, 1)
                gamma = -slope  # Negative because 1/f^gamma
            else:
                gamma = None
                
            # Calculate corner frequency (where thermal noise equals flicker noise)
            # This is approximated as the frequency where the slope changes significantly
            if len(freq) > 10:
                # Approximate by finding where slope changes
                slopes = np.diff(log_noise) / np.diff(log_freq)
                corner_idx = np.argmax(np.abs(np.diff(slopes))) + 1
                corner_freq = freq[corner_idx]
            else:
                corner_freq = None
                
            results = {
                "status": "success",
                "flicker_noise_coefficient": K_avg,
                "flicker_noise_coefficient_std": K_std,
                "flicker_noise_exponent": gamma,
                "corner_frequency": corner_freq
            }
            
            return results
        except Exception as e:
            self.logger.error(f"Error analyzing flicker noise: {str(e)}")
            return {"status": "error", "message": str(e)}
            
    def analyze_shot_noise(self, data):
        """
        Analyze shot noise data
        
        Args:
            data: DataFrame containing shot noise data
            
        Returns:
            dict: Dictionary containing analysis results
        """
        try:
            if data is None or data.empty:
                return {"status": "error", "message": "No data available"}
                
            # Extract frequency and noise data
            freq = data.iloc[:, 0].values  # Frequency column
            noise = data.iloc[:, 1].values  # Noise column
            
            # For shot noise, the noise should be frequency independent
            # Calculate basic statistics
            noise_mean = np.mean(noise)
            noise_std = np.std(noise)
            noise_variation = noise_std / noise_mean if noise_mean > 0 else 0
            
            # Check for frequency dependence (should be minimal for shot noise)
            # Calculate correlation coefficient between noise and frequency
            corr_coef = np.corrcoef(freq, noise)[0, 1] if len(freq) > 1 else 0
            
            # For true shot noise, the power spectral density should be proportional to the current
            # Since we don't have current measurements here, we can only report the noise level
            
            results = {
                "status": "success",
                "shot_noise_level": noise_mean,
                "noise_std": noise_std,
                "noise_variation": noise_variation,
                "frequency_correlation": corr_coef
            }
            
            return results
        except Exception as e:
            self.logger.error(f"Error analyzing shot noise: {str(e)}")
            return {"status": "error", "message": str(e)}
            
    def extract_noise_vs_parameter(self, file_pattern, parameter_extractor):
        """
        Extract noise values versus a parameter from multiple files
        
        Args:
            file_pattern: Glob pattern for the files to analyze
            parameter_extractor: Function to extract parameter value from filename
            
        Returns:
            tuple: (parameters, noise_values) arrays
        """
        import glob
        
        try:
            files = glob.glob(file_pattern)
            if not files:
                self.logger.warning(f"No files found matching pattern: {file_pattern}")
                return None, None
                
            parameters = []
            noise_values = []
            
            for file in sorted(files):
                param_value = parameter_extractor(file)
                if param_value is None:
                    self.logger.warning(f"Could not extract parameter from {file}")
                    continue
                    
                data = self.read_noise_data(file)
                
                if data is not None and not data.empty:
                    # Extract noise at a specific frequency (e.g., 1 kHz)
                    freq_col = data.columns[0]
                    noise_col = data.columns[1]
                    
                    # Find noise at approximately 1 kHz
                    target_freq = 1000  # 1 kHz
                    
                    # Use a safer way to find the closest frequency to 1 kHz
                    min_diff = float('inf')
                    freq_1khz_idx = 0
                    for i, freq in enumerate(data[freq_col]):
                        diff = abs(freq - target_freq)
                        if diff < min_diff:
                            min_diff = diff
                            freq_1khz_idx = i
                            
                    noise_at_1khz = data.iloc[freq_1khz_idx][noise_col]
                    
                    parameters.append(param_value)
                    noise_values.append(noise_at_1khz)
            
            # Sort data by parameter value
            if parameters and noise_values:
                param_noise = sorted(zip(parameters, noise_values))
                parameters = [p for p, n in param_noise]
                noise_values = [n for p, n in param_noise]
            
            return np.array(parameters), np.array(noise_values)
        except Exception as e:
            self.logger.error(f"Error extracting noise vs parameter: {str(e)}")
            return None, None 