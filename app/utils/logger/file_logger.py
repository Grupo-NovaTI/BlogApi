import logging
from logging.handlers import RotatingFileHandler
from typing import Optional
import os

class FileLogger:
    """A class for logging messages to a file with enhanced configuration options.
    This logger supports rotating file handlers, custom formats, and console output.
    It can be used as a context manager to ensure proper resource management.
    Example usage:
        with FileLogger(log_file='app.log', log_level=logging.INFO) as logger:
            logger.log_info("This is an info message.")
    """
    def __init__(
        self,
        logger_name: str = __name__,
        log_file: str = 'execution.log',
        encoding: str = 'utf-8',
        show_log_file: bool = True,
        log_level: int = logging.DEBUG,
        max_bytes: int = 5_242_880,  # 5MB
        backup_count: int = 3,
        custom_format: Optional[str] = None
    ):
        """
        Initializes the FileLogger with enhanced configuration options.
        
        Args:
            logger_name: Name of the logger
            log_file: Path to the log file
            encoding: File encoding
            show_log_file: Enable console output
            log_level: Initial logging level
            max_bytes: Maximum size of log file before rotation
            backup_count: Number of backup files to keep
            custom_format: Custom log format string
        """
        try:
            self.logger = logging.getLogger(logger_name)
            self.logger.setLevel(log_level)
            
            # Create log directory if it doesn't exist
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)

            # Configure rotating file handler
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding=encoding
            )
            file_handler.setLevel(log_level)

            # Configure formatter
            format_string = custom_format or '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            formatter = logging.Formatter(format_string)
            file_handler.setFormatter(formatter)
            
            # Clear existing handlers
            self.logger.handlers.clear()
            self.logger.addHandler(file_handler)

            if show_log_file:
                console_handler = logging.StreamHandler()
                console_handler.setLevel(log_level)
                console_handler.setFormatter(formatter)
                self.logger.addHandler(console_handler)

            self.logger.debug(f"FileLogger initialized with log file: {log_file}")
            
        except Exception as e:
            raise RuntimeError(f"Failed to initialize FileLogger: {str(e)}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for handler in self.logger.handlers:
            handler.close()
            self.logger.removeHandler(handler)

    def set_level(self, level: int) -> None:
        """Set the logging level for all handlers."""
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            handler.setLevel(level)

    def set_format(self, format_string: str) -> None:
        """Set a custom format for all handlers."""
        formatter = logging.Formatter(format_string)
        for handler in self.logger.handlers:
            handler.setFormatter(formatter)

    def log_info(self, message: str):
        try:
            self.logger.info(message)
        except Exception as e:
            print(f"Failed to log info message: {str(e)}")

    def log_warning(self, message: str):
        try:
            self.logger.warning(message)
        except Exception as e:
            print(f"Failed to log warning message: {str(e)}")

    def log_error(self, message: str):
        try:
            self.logger.error(message)
        except Exception as e:
            print(f"Failed to log error message: {str(e)}")
        
    def log_debug(self, message: str):
        try:
            self.logger.debug(message)
        except Exception as e:
            print(f"Failed to log debug message: {str(e)}")