import logging
import os
from datetime import datetime
from pathlib import Path

class ApplicationLogger:
    def __init__(
        self,
        name: str = "ApplicationLogger",
        logger_level: int = logging.DEBUG,
        log_to_console: bool = True,
        log_to_file: bool = True,
        log_dir: str = "logs"
    ) -> None:
        """
        Initialize the logger with both console and file handlers.
        
        Args:
            name (str): The name of the logger
            logger_level (int): Logging level (default is logging.DEBUG)
            log_to_console (bool): Whether to log to console (default True)
            log_to_file (bool): Whether to log to file (default True)
            log_dir (str): Directory to store log files (default "logs")
        """
        self.logger: logging.Logger = logging.getLogger(name)
        self.logger.setLevel(logger_level)
        
        # Create formatter
        self.formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Setup handlers if logger doesn't have any
        if not self.logger.hasHandlers():
            # Console handler
            if log_to_console:
                self._setup_console_handler(logger_level)
            
            # File handler
            if log_to_file:
                self._setup_file_handler(logger_level, log_dir)

    def _setup_console_handler(self, level: int) -> None:
        """Setup console handler with formatting"""
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)

    def _setup_file_handler(self, level: int, log_dir: str) -> None:
        """Setup file handler with formatting and rotation"""
        # Create logs directory if it doesn't exist
        log_path = Path(log_dir)
        log_path.mkdir(exist_ok=True)

        # Create log file with timestamp
        timestamp = datetime.now().strftime('%Y%m%d')
        log_file = log_path / f"application_{timestamp}.log"

        # Setup file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)

    def add_logger_handler(self, handler: logging.Handler) -> None:
        """Add a custom logging handler."""
        if handler not in self.logger.handlers:
            self.logger.addHandler(handler)
        else:
            self.logger.warning("Handler is already added to the logger.")

    def remove_handler(self, handler: logging.Handler) -> None:
        """Remove a specific logging handler."""
        if handler in self.logger.handlers:
            self.logger.removeHandler(handler)
        else:
            self.logger.warning("Handler not found in logger handlers.")

    def clear_handlers(self) -> None:
        """Remove all logging handlers."""
        self.logger.handlers.clear()

    def set_formatter(self, fmt: logging.Formatter) -> None:
        """Set a formatter for all handlers."""
        for handler in self.logger.handlers:
            handler.setFormatter(fmt)

    def set_level(self, level: int) -> None:
        """Set the logging level dynamically."""
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            handler.setLevel(level)

    def log_debug(self, message: str) -> None:
        """Log a debug message."""
        self.logger.debug(message)

    def log_info(self, message: str) -> None:
        """Log an info message."""
        self.logger.info(message)

    def log_warning(self, message: str) -> None:
        """Log a warning message."""
        self.logger.warning(message)

    def log_error(self, message: str) -> None:
        """Log an error message."""
        self.logger.error(message)

    def log_critical(self, message: str) -> None:
        """Log a critical message."""
        self.logger.critical(message)

    def debug(self, message: str) -> None:
        """Alias for debug logging."""
        self.logger.debug(message)
    
    def log_exception(self, exc: Exception) -> None:
        """
        Log an exception with traceback.
        
        Args:
            exc (Exception): The exception to log
        """
        self.logger.exception(f"Exception occurred: {str(exc)}")

    @classmethod
    def get_logger(
        cls,
        name: str,
        level: int = logging.DEBUG,
        log_to_console: bool = True,
        log_to_file: bool = True
    ) -> 'ApplicationLogger':
        """
        Factory method to create or get an existing logger.
        
        Args:
            name (str): Logger name
            level (int): Logging level
            log_to_console (bool): Whether to log to console
            log_to_file (bool): Whether to log to file
        
        Returns:
            ApplicationLogger: Configured logger instance
        """
        return cls(
            name=name,
            logger_level=level,
            log_to_console=log_to_console,
            log_to_file=log_to_file
        )