import logging
import os
import sys
from datetime import datetime

class Logger:
    """
    Logger class for noise analysis tool that handles log files and console output
    """
    def __init__(self, log_level=logging.INFO, log_dir="logs"):
        """
        Initialize the logger
        
        Args:
            log_level: Logging level (default: INFO)
            log_dir: Directory to store log files (default: logs)
        """
        # Create logs directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # Set up timestamp for log filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"noise_analysis_{timestamp}.log")
        
        # Configure logging
        self.logger = logging.getLogger("noise_analysis")
        self.logger.setLevel(log_level)
        
        # Clear any existing handlers
        if self.logger.handlers:
            self.logger.handlers.clear()
            
        # Create file handler
        file_handler = logging.FileHandler(log_file)
        file_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_format)
        self.logger.addHandler(file_handler)
        
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_format = logging.Formatter("%(levelname)s: %(message)s")
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)
        
        self.logger.info(f"Logger initialized. Log file: {log_file}")
        
    def info(self, message):
        """Log an info message"""
        self.logger.info(message)
        
    def warning(self, message):
        """Log a warning message"""
        self.logger.warning(message)
        
    def error(self, message):
        """Log an error message"""
        self.logger.error(message)
        
    def debug(self, message):
        """Log a debug message"""
        self.logger.debug(message)
        
    def critical(self, message):
        """Log a critical message"""
        self.logger.critical(message) 