import os
import logging

# LOGGING RULES:

# info = general information
# warnings = expected exceptions
# errors = unexpected exceptions
# critical = exceptions that prevents the program from running any further

LOGS_PATH = os.path.join(os.path.join(os.path.join(os.getenv('APPDATA'), 'EasyCrypto'), 'logs'))
SETUP_FILEPATH = os.path.join(LOGS_PATH, 'setup.log')
DEFAULT_FILEPATH = os.path.join(LOGS_PATH, 'logs.log')
FORMATTER = '[%(asctime)s][EasyCrypto][%(name)s] -> %(levelname)s: %(message)s'

logging.basicConfig(level=logging.DEBUG, format=FORMATTER, filemode='a')


def setup_logger(module):

    setuplogger = logging.getLogger(module)

    setup_handler = logging.FileHandler(SETUP_FILEPATH)
    setup_formatter = logging.Formatter(FORMATTER)
    setup_handler.setFormatter(setup_formatter)
    setuplogger.addHandler(setup_handler)

    return setuplogger


def default_logger(module):
    if not os.path.exists(DEFAULT_FILEPATH):
        open(DEFAULT_FILEPATH, 'w')

    logger = logging.getLogger(module)
    formatter = SeperatedExcFormatter(FORMATTER)

    logger.propagate = False

    setup_handler = logging.FileHandler(DEFAULT_FILEPATH)
    setup_handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(setup_handler)

    return logger


class SeperatedExcFormatter(logging.Formatter):  # source: https://stackoverflow.com/a/59092065/14554798
    def formatException(self, exc_info):
        result = super().formatException(exc_info)
        if exc_info:
            result = result + "\n\n----------------------------------------------------------------------------------\n\n"
        return result
