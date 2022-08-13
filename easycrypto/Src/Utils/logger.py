
# built-in modules
import os
import logging

# app modules
from easycrypto.Src.Utils.paths import SETUP_LOG, DEF_LOG


class Logger:
    """
    Defines TWO custom loggers:
        - Setup Logger -> logs setup operations to "setup.log" file
        - Default Logger -> logs important actions and exceptions to "logs.log" file

    LOGGING RULES:

    info = general information
    warnings = expected exceptions
    errors = unexpected exceptions
    critical = exceptions that prevents the program from running any further

    """

    def __init__(self, module: str):
        self.module = module
        self.formatter = '[%(asctime)s][EasyCrypto][%(name)s] -> %(levelname)s: %(message)s'
        logging.basicConfig(level=logging.DEBUG, format=self.formatter, filemode='a')

    def setup(self) -> logging.Logger:
        setuplogger = logging.getLogger(self.module)

        setup_handler = logging.FileHandler(SETUP_LOG)
        setup_formatter = logging.Formatter(self.formatter)
        setup_handler.setFormatter(setup_formatter)
        setuplogger.addHandler(setup_handler)

        return setuplogger

    def default(self) -> logging.Logger:
        if not os.path.exists(DEF_LOG):
            open(DEF_LOG, 'w')

        logger = logging.getLogger(self.module)
        formatter = _SeperatedExcFormatter(self.formatter)

        logger.propagate = False

        setup_handler = logging.FileHandler(DEF_LOG)
        setup_handler.setFormatter(formatter)

        if not logger.hasHandlers():
            logger.addHandler(setup_handler)

        return logger


class _SeperatedExcFormatter(logging.Formatter):  # source: https://stackoverflow.com/a/59092065/14554798
    def formatException(self, exc_info):
        result = super().formatException(exc_info)
        if exc_info:
            result = result + "\n\n----------------------------------------------------------------------------------\n\n"
        return result
