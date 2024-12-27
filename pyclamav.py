import os

from lib.config import load_config
from lib.log import get_logger

from lib.scan import Scan

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

def main():
    config = load_config(CURRENT_DIR)
    logger = get_logger(config.log_file, config.verbose)
    scanner = Scan(config.nb_process, config.modified_file_datetime,logger)

    logger.info(f"Scanning with {config.nb_process} process")
    for folder in config.folders:
        logger.info(f"Scanning folder for last {config.modified_file_duration} changes", extra={"folder": folder})
        r = scanner.scan_folder(folder)


if __name__ == "__main__":
    main()
