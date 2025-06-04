import logging
from typing import Optional

class ApplicationLogger:
    def __init__(self, name: str = "ApplicationLogger", logger_level: int = logging.DEBUG) -> None:
        """
        Initialize the logger.
        
        Args:
            name (str): The name of the logger.
            logger_level (int): Logging level (default is logging.DEBUG).
        """
        self.logger: logging.Logger = logging.getLogger(name)
        self.logger.setLevel(logger_level)

        # Default console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logger_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        if not self.logger.hasHandlers():
            self.logger.addHandler(console_handler)

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
