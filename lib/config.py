import os
import json
import datetime
import argparse
import dateparser
from typing import List
from pydantic import BaseModel, Field, model_validator

from pathlib import Path

DEFAULT_CONFIG_FILE = "config.json"
DEFAULT_MODIFIED_FILE_SINCE = "24h"


def parse_arg():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments.

    Example:
        >>> args = parse_arg()
        >>> args.config
        'path/to/config.json'
        >>> args.modified_since
        '24h'
        >>> args.verbose
        False
    """
    parser = argparse.ArgumentParser(
        prog="pyclamav",
        description="Python utility that uses ClamAV to scan files",
    )

    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default=os.path.join(DEFAULT_CONFIG_FILE),
        help="Path to configuration file",
    )
    parser.add_argument(
        "--modified-since",
        type=str,
        help="Scanning files modified within the last specified duration (e.g., 24h, 48h)",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", default=False, help="Verbose mode"
    )

    return parser.parse_args()


class Config(BaseModel):
    """
    Configuration model for pyclamav.
    Example:
        >>> config = Config(folders=["/path/to/folder"], log_folder="/var/log/pyclamav/", modified_file_since="24h", verbose=True)
        >>> config.modified_file_datetime
        datetime.datetime(2023, 10, 1, 0, 0)
    """

    folders: List[str] = Field(list(), description="Folders to monitor")
    log_folder: str = Field(str, description="Log folder")
    modified_file_since: str | None = Field(
        DEFAULT_MODIFIED_FILE_SINCE, description="File modified within the duration"
    )
    modified_file_datetime: datetime.datetime | None = Field(
        None, description="File modified within the datetime"
    )
    verbose: bool = Field(False, description="Verbose mode")

    @model_validator(mode="after")
    def set_modified_file_datetime(self):
        """
        Set the modified_file_datetime based on modified_file_since.

        Example:
            >>> config = Config(modified_file_since="24h")
            >>> config.modified_file_datetime
            datetime.datetime(2023, 10, 1, 0, 0)
        """
        self.modified_file_datetime = dateparser.parse(self.modified_file_since)
        return self


def load_config():
    """
    Load the configuration file as JSON.

    Returns:
        Config: The loaded configuration.

    Example:
        >>> config = load_config()
        >>> config.folders
        ['/path/to/folder1', '/path/to/folder2']
        >>> config.log_folder
        '/var/log/pyclamav/'
        >>> config.modified_file_since
        '24h'
        >>> config.verbose
        False
    """
    args = parse_arg()
    with open(args.config, "r") as file:
        loaded_config = json.load(file)

    if "log_folder" not in loaded_config:
        loaded_config["log_folder"] = os.path.join(Path.home(), ".pyclamav", "log")

    if args.modified_since:
        loaded_config["modified_file_since"] = args.modified_since

    if args.verbose:
        loaded_config["verbose"] = args.verbose

    return Config(**loaded_config)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
