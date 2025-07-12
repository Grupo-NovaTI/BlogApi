"""
Logger utility for application-wide logging configuration and usage.

This module defines the ApplicationLogger class, which provides a flexible and configurable
logging utility for Python applications. It supports both console and file logging, log rotation,
custom formatting, and dynamic log level changes.
"""

import logging
from datetime import datetime
from pathlib import Path


class ApplicationLogger:
    """
    ApplicationLogger provides a flexible and configurable logging utility for Python applications.

    This class wraps Python's built-in logging module, allowing for easy setup of console and file logging,
    custom formatting, dynamic log level changes, and handler management. It supports log rotation by date,
    custom handler addition/removal, and exception logging with traceback.

    Attributes:
        logger (logging.Logger): The underlying logger instance.
        formatter (logging.Formatter): The formatter used for log messages.
    """

    def __init__(
        self,
        name: str = "ApplicationLogger",
        logger_level: int = logging.DEBUG,
        log_to_console: bool = True,
        log_to_file: bool = True,
        log_dir: str = "logs"
    ) -> None:
        """
        Initializes the ApplicationLogger instance.

        Args:
            name (str): The name of the logger. Defaults to "ApplicationLogger".
            logger_level (int): The logging level (e.g., logging.DEBUG, logging.INFO). Defaults to logging.DEBUG.
            log_to_console (bool): Whether to log messages to the console. Defaults to True.
            log_to_file (bool): Whether to log messages to a file. Defaults to True.
            log_dir (str): Directory where log files will be stored. Defaults to "logs".
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
        """
        Sets up a console (stdout) logging handler.

        Args:
            level (int): The logging level for the console handler.
        """
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)

    def _setup_file_handler(self, level: int, log_dir: str) -> None:
        """
        Sets up a file logging handler with daily log file rotation.

        Args:
            level (int): The logging level for the file handler.
            log_dir (str): Directory where log files will be stored.
        """
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
        """
        Adds a custom logging handler to the logger.

        Args:
            handler (logging.Handler): The handler to add.
        """
        if handler not in self.logger.handlers:
            self.logger.addHandler(handler)
        else:
            self.logger.warning("Handler is already added to the logger.")

    def remove_handler(self, handler: logging.Handler) -> None:
        """
        Removes a specific logging handler from the logger.

        Args:
            handler (logging.Handler): The handler to remove.
        """
        if handler in self.logger.handlers:
            self.logger.removeHandler(handler)
        else:
            self.logger.warning("Handler not found in logger handlers.")

    def clear_handlers(self) -> None:
        """
        Removes all logging handlers from the logger.
        """
        self.logger.handlers.clear()

    def set_formatter(self, fmt: logging.Formatter) -> None:
        """
        Sets the formatter for all handlers.

        Args:
            fmt (logging.Formatter): The formatter to set.
        """
        for handler in self.logger.handlers:
            handler.setFormatter(fmt)

    def set_level(self, level: int) -> None:
        """
        Dynamically sets the logging level for the logger and all handlers.

        Args:
            level (int): The logging level to set.
        """
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            handler.setLevel(level)

    def log_debug(self, message: str) -> None:
        """
        Logs a debug-level message.

        Args:
            message (str): The message to log.
        """
        self.logger.debug(message)

    def log_info(self, message: str) -> None:
        """
        Logs an info-level message.

        Args:
            message (str): The message to log.
        """
        self.logger.info(message)

    def log_warning(self, message: str) -> None:
        """
        Logs a warning-level message.

        Args:
            message (str): The message to log.
        """
        self.logger.warning(message)

    def log_error(self, message: str) -> None:
        """
        Logs an error-level message.

        Args:
            message (str): The message to log.
        """
        self.logger.error(message)

    def log_critical(self, message: str) -> None:
        """
        Logs a critical-level message.

        Args:
            message (str): The message to log.
        """
        self.logger.critical(message)

    def debug(self, message: str) -> None:
        """
        Alias for logging a debug-level message.

        Args:
            message (str): The message to log.
        """
        self.logger.debug(message)

    def log_exception(self, exc: Exception) -> None:
        """
        Logs an exception with traceback.

        Args:
            exc (Exception): The exception to log.
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
            name (str): The name of the logger.
            level (int): The logging level.
            log_to_console (bool): Whether to log to the console.
            log_to_file (bool): Whether to log to a file.

        Returns:
            ApplicationLogger: A configured logger instance.
        """
        return cls(
            name=name,
            logger_level=level,
            log_to_console=log_to_console,
            log_to_file=log_to_file
        )
