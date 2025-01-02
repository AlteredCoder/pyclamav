import os
import logging
from datetime import datetime
from pythonjsonlogger import jsonlogger
from . import utils

LOG_FILENAME = "pyclamav.log"

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record["time"] = datetime.utcnow().isoformat() + "Z"

def get_logger(log_folder, verbose):
    """
    Create and configure a logger that writes to a file and optionally to stdout.

    Args:
        log_folder (str): The path to the log file.
        verbose (bool): Whether to enable verbose logging.

    Returns:
        logging.Logger: The configured logger.

    Example:
        >>> logger = get_logger('path/to/log/file.log', verbose=True)
        >>> logger.info('This is an info message.')
        >>> logger.debug('This is a debug message.')
    """
    
    log_file = os.path.join(log_folder, LOG_FILENAME)
    utils.create_file_folder(log_file)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    logFileHandler = logging.FileHandler(log_file)
    stdoutHandler = logging.StreamHandler()

    if verbose:
        logger.setLevel(logging.DEBUG)
        stdoutHandler.setLevel(logging.DEBUG)
        logFileHandler.setLevel(logging.DEBUG)

    # Use the custom JSON formatter
    formatter = CustomJsonFormatter()
    logFileHandler.setFormatter(formatter)
    stdoutHandler.setFormatter(formatter)
    logger.addHandler(logFileHandler)
    logger.addHandler(stdoutHandler)

    return logger

if __name__ == "__main__":
    import doctest
    doctest.testmod()