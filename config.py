import os
import json
import datetime
import argparse
import dateparser
from typing import List
from pydantic import BaseModel, Field, model_validator

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
DEFAULT_CONFIG_FILE = os.path.join(CURRENT_DIR, "config.json")
DEFAULT_MODIFIED_FILE_DURATION = "24h"
DEFAULT_NB_PROCESS = 5

def parse_arg():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments.

    Example:
        >>> args = parse_arg()
        >>> args.config
        'path/to/config.json'
        >>> args.modified_duration
        '24h'
        >>> args.verbose
        False
    """
    parser = argparse.ArgumentParser(
                    prog='pyclamav',
                    description='Python utility that uses ClamAV to scan files',
                    )

    parser.add_argument("-c", "--config", type=str, default=DEFAULT_CONFIG_FILE, help="Path to configuration file")
    parser.add_argument("--modified-duration", type=str, default=DEFAULT_MODIFIED_FILE_DURATION, help="Scanning files modified within the last specified duration (e.g., 24h, 48h)")
    parser.add_argument("-v", "--verbose", action='store_true', default=False, help="Verbose mode")
    parser.add_argument("-p", "--process", type=int, default=DEFAULT_NB_PROCESS, help="Number of process")

    return parser.parse_args()

class Config(BaseModel):
    """
    Configuration model for pyclamav.
    Example:
        >>> config = Config(folders=["/path/to/folder"], log_file="pyclamav.log", modified_file_duration="24h", verbose=True)
        >>> config.modified_file_datetime
        datetime.datetime(2023, 10, 1, 0, 0)
    """
    folders: List[str] = Field(list(), description="Folders to monitor")
    log_file: str = Field(os.path.join(CURRENT_DIR, "log", "pyclamav.log"), description="Log file path")
    modified_file_duration: str = Field(DEFAULT_MODIFIED_FILE_DURATION, description="File modified within the duration")
    modified_file_datetime: datetime.datetime = Field(None, description="File modified within the datetime")
    nb_process: int = Field(DEFAULT_NB_PROCESS, description="Number of process")
    verbose: bool = Field(False, description="Verbose mode")

    @model_validator(mode="after")
    def set_modified_file_datetime(self):
        """
        Set the modified_file_datetime based on modified_file_duration.

        Example:
            >>> config = Config(modified_file_duration="24h")
            >>> config.modified_file_datetime
            datetime.datetime(2023, 10, 1, 0, 0)
        """
        self.modified_file_datetime = dateparser.parse(self.modified_file_duration)
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
        >>> config.log_file
        'path/to/log/pyclamav.log'
        >>> config.modified_file_duration
        '24h'
        >>> config.verbose
        False
    """
    args = parse_arg()
    with open(args.config, 'r') as file:
        loaded_config = json.load(file)

    if "log_file" in loaded_config:
        loaded_config["log_file"] = os.path.join(CURRENT_DIR, "log", loaded_config["log_file"])

    if args.modified_duration:
        loaded_config["modified_file_duration"] = args.modified_duration

    if args.verbose:
        loaded_config["verbose"] = args.verbose

    if args.process:
        loaded_config["nb_process"] = args.process

    return Config(**loaded_config)

if __name__ == "__main__":
    import doctest
    doctest.testmod()