import logging
from pathlib import Path
from datetime import datetime
import sys
import traceback

class Logger:
    """Handles logging configuration and operations with enhanced debugging capabilities."""
    def __init__(self, log_level=logging.INFO, debug_mode=False):
        self.debug_mode = debug_mode
        self.logger = self._setup_logger(log_level)
        
    def _setup_logger(self, log_level):
        """Set up logging configuration with enhanced formatting."""
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f'spice_simulation_{timestamp}.log'
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - [%(levelname)s] - [%(filename)s:%(lineno)d] - %(message)s'
        )
        simple_formatter = logging.Formatter(
            '[%(levelname)s]: %(message)s'
        )
        
        # Create handlers
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(detailed_formatter)
        
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(simple_formatter)
        
        # Configure root logger
        logging.basicConfig(
            level=log_level,
            handlers=[file_handler, console_handler]
        )
        
        logger = logging.getLogger(__name__)
        
        # Add debug mode handlers if enabled
        if self.debug_mode:
            debug_file = log_dir / f'debug_{timestamp}.log'
            debug_handler = logging.FileHandler(debug_file)
            debug_handler.setLevel(logging.DEBUG)
            debug_handler.setFormatter(detailed_formatter)
            logger.addHandler(debug_handler)
            
        return logger
    
    def debug(self, message, data=None):
        """Log debug message with optional data."""
        if self.debug_mode:
            if data is not None:
                self.logger.debug(f"{message}\nData: {data}")
            else:
                self.logger.debug(message)
    
    def info(self, message, data=None):
        """Log info message with optional data."""
        if data is not None:
            self.logger.info(f"{message}\nData: {data}")
        else:
            self.logger.info(message)
    
    def warning(self, message, data=None):
        """Log warning message with optional data."""
        if data is not None:
            self.logger.warning(f"{message}\nData: {data}")
        else:
            self.logger.warning(message)
    
    def error(self, message, exc_info=None):
        """Log error message with optional exception info."""
        if exc_info:
            self.logger.error(f"{message}\nException: {exc_info}\nTraceback: {traceback.format_exc()}")
        else:
            self.logger.error(message)
    
    def critical(self, message, exc_info=None):
        """Log critical message with optional exception info."""
        if exc_info:
            self.logger.critical(f"{message}\nException: {exc_info}\nTraceback: {traceback.format_exc()}")
        else:
            self.logger.critical(message) 