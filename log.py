import logging

from pythonjsonlogger import jsonlogger

import utils

def get_logger(log_file, verbose):
    """
    Create and configure a logger that writes to a file and optionally to stdout.

    Args:
        log_file (str): The path to the log file.
        verbose (bool): Whether to enable verbose logging.

    Returns:
        logging.Logger: The configured logger.

    Example:
        >>> logger = get_logger('path/to/log/file.log', verbose=True)
        >>> logger.info('This is an info message.')
        >>> logger.debug('This is a debug message.')
    """
    
    utils.create_file_folder(log_file)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    logFileHandler = logging.FileHandler(log_file)
    stdoutHandler = logging.StreamHandler()

    if verbose:
        logger.setLevel(logging.DEBUG)
        stdoutHandler.setLevel(logging.DEBUG)
        logFileHandler.setLevel(logging.DEBUG)

    formatter = jsonlogger.JsonFormatter()
    logFileHandler.setFormatter(formatter)
    stdoutHandler.setFormatter(formatter)
    logger.addHandler(logFileHandler)
    logger.addHandler(stdoutHandler)

    return logger

if __name__ == "__main__":
    import doctest
    doctest.testmod()
