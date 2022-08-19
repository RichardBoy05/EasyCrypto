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
    critical = exceptions that prevent further execution of the program

    """

    def __init__(self, module: str):
        self.module = module
        self.separator = '\n----------------------------------------------------------------------------------\n\n'

        self.setup_formatter = '[%(asctime)s][EasyCrypto][%(name)s] -> %(levelname)s: %(message)s'
        self.def_formatter = f'{self.separator}[%(asctime)s][EasyCrypto][%(name)s] -> %(levelname)s: %(message)s'

        logging.basicConfig(level=logging.DEBUG, format=self.setup_formatter, filemode='a')

    def setup(self) -> logging.Logger:
        """ Creates and returns a custom logger to log setup operations -> setup.log """

        logger = logging.getLogger(self.module)

        handler = logging.FileHandler(SETUP_LOG)
        formatter = logging.Formatter(self.setup_formatter)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger

    def default(self) -> logging.Logger:
        """ Creates and returns a custom logger to log important operations and exception tracebacks -> logs.log """

        if not os.path.exists(DEF_LOG):
            with open(DEF_LOG, 'w') as file:
                file.write('[EasyCrypto Logs]\n')

        logger = logging.getLogger(__name__)

        handler = logging.FileHandler(DEF_LOG)
        formatter = logging.Formatter(self.def_formatter)
        handler.setFormatter(formatter)

        if len(logger.handlers) == 0:  # avoids adding multiple handlers
            logger.addHandler(handler)

        return logger

