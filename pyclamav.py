import os

from lib.config import load_config
from lib.log import get_logger

from lib.scan import Scan


def main():
    config = load_config()
    logger = get_logger(config.log_folder, config.verbose)
    scanner = Scan(config.modified_file_datetime, logger)

    logger.info(f"Scanning {len(config.folders)} folders with files changed during the last {config.modified_file_since}")
    for folder in config.folders:
        logger.info(
            f"Scanning folder",
            extra={"folder": folder},
        )
        r = scanner.scan_folder(folder)


if __name__ == "__main__":
    main()
