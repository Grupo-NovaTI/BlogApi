import logging

class FileLogger:
    def __init__(self, logger_name : str = __name__, log_file: str = 'execution.log', encoding: str = 'utf-8', show_log_file: bool = True):
        """
        Initializes the FileLogger with a specified logger name, log file, encoding, and an option to show the log file.
        :param logger_name: Name of the logger, defaults to __name__.
        :param
        log_file: Path to the log file where logs will be written, defaults to 'execution.log'.
        :param encoding: Encoding for the log file, defaults to 'utf-8'.
        :param show_log_file: If True, the log file will be displayed in the console, defaults to True.
        """
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(log_file, encoding=encoding)
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        if show_log_file:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
            self.logger.debug("FileLogger initialized with log file: %s", log_file)

    def log_info(self, message: str):
        self.logger.setLevel(logging.INFO)
        self.logger.info(message)

    def log_warning(self, message: str):
        self.logger.setLevel(logging.WARNING)
        self.logger.warning(message)

    def log_error(self, message: str):
        self.logger.setLevel(logging.ERROR)
        self.logger.error(message)
        
    def log_debug(self, message: str):
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug(message)