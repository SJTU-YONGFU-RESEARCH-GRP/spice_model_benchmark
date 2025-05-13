import logging
from pathlib import Path
from datetime import datetime
import sys
import traceback
from typing import Optional, Any, Union

class Logger:
    """Handles logging configuration and operations with enhanced debugging capabilities.
    
    This class provides a wrapper around Python's built-in logging module with
    additional features such as:
    - Automatic log file creation with timestamps
    - Separate handlers for console and file output
    - Support for debug mode with additional logging
    - Helper methods for different log levels with support for data inspection
    
    Attributes:
        logger: The underlying Python logger instance
        debug_mode: Whether debug mode is enabled for additional logging
    """
    
    def __init__(self, log_level: int = logging.INFO, debug_mode: bool = False) -> None:
        """Initialize the logger with specified log level and debug mode.
        
        Args:
            log_level: Minimum logging level (default: logging.INFO)
            debug_mode: Whether to enable additional debug logging (default: False)
        """
        self.debug_mode = debug_mode
        self.logger = self._setup_logger(log_level)
        
    def _setup_logger(self, log_level: int) -> logging.Logger:
        """Set up logging configuration with enhanced formatting.
        
        Creates log directory, configures file and console handlers with
        appropriate formatters, and sets up debug mode if enabled.
        
        Args:
            log_level: Minimum logging level to record
            
        Returns:
            Configured logger instance
        """
        # Create log directory
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        # Create log filenames with timestamps
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f'spice_simulation_{timestamp}.log'
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - [%(levelname)s] - [%(filename)s:%(lineno)d] - %(message)s'
        )
        simple_formatter = logging.Formatter(
            '[%(levelname)s]: %(message)s'
        )
        
        # Create and configure file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(detailed_formatter)
        
        # Create and configure console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(simple_formatter)
        
        # Configure root logger
        logger = logging.getLogger(__name__)
        logger.setLevel(log_level)
        
        # Remove any existing handlers (in case logger already exists)
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # Add the handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        # Add debug mode handler if enabled
        if self.debug_mode:
            debug_file = log_dir / f'debug_{timestamp}.log'
            debug_handler = logging.FileHandler(debug_file)
            debug_handler.setLevel(logging.DEBUG)
            debug_handler.setFormatter(detailed_formatter)
            logger.addHandler(debug_handler)
            
        return logger
    
    def debug(self, message: str, data: Any = None) -> None:
        """Log debug message with optional data.
        
        Args:
            message: The log message
            data: Optional data to include in the log
        """
        if data is not None:
            self.logger.debug(f"{message}\nData: {data}")
        else:
            self.logger.debug(message)
    
    def info(self, message: str, data: Any = None) -> None:
        """Log info message with optional data.
        
        Args:
            message: The log message
            data: Optional data to include in the log
        """
        if data is not None:
            self.logger.info(f"{message}\nData: {data}")
        else:
            self.logger.info(message)
    
    def warning(self, message: str, data: Any = None) -> None:
        """Log warning message with optional data.
        
        Args:
            message: The log message
            data: Optional data to include in the log
        """
        if data is not None:
            self.logger.warning(f"{message}\nData: {data}")
        else:
            self.logger.warning(message)
    
    def error(self, message: str, exc_info: Optional[Union[bool, Exception]] = None) -> None:
        """Log error message with optional exception info.
        
        Args:
            message: The error message
            exc_info: Exception object or True to include traceback
        """
        if exc_info:
            self.logger.error(message, exc_info=exc_info)
        else:
            self.logger.error(message)
    
    def critical(self, message: str, exc_info: Optional[Union[bool, Exception]] = None) -> None:
        """Log critical message with optional exception info.
        
        Args:
            message: The critical error message
            exc_info: Exception object or True to include traceback
        """
        if exc_info:
            self.logger.critical(message, exc_info=exc_info)
        else:
            self.logger.critical(message)
    
    def set_level(self, level: int) -> None:
        """Dynamically change the logging level.
        
        Args:
            level: New logging level (e.g., logging.DEBUG, logging.INFO)
        """
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            handler.setLevel(level) 