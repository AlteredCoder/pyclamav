import os
from datetime import datetime
from . import pyclamd
from . import utils


class Scan:
    """
    A class to scan files using ClamAV.
    """

    def __init__(self, modified_since, logger):
        """
        Initialize the Scan class.

        Args:
            modified_since (datetime): The file to scan that have been modified since.
            logger (logging.Logger): The logger to use for logging scan results.

        Raises:
            ValueError: If unable to connect to the ClamAV daemon.
        """
        self.logger = logger
        self.modified_since = modified_since
        try:
            self.cd = pyclamd.ClamdUnixSocket()
            self.cd.ping()
        except pyclamd.ConnectionError:
            try:
                self.cd = pyclamd.ClamdNetworkSocket()
                self.cd.ping()
            except pyclamd.ConnectionError:
                raise ValueError(
                    "could not connect to clamd server either by unix or network socket"
                )

    def scan_file(self, file):
        """
        Scan a file.

        Args:
            file (pathlib.PosixPath): The file.

        Returns:
            bool: True if the file is infected, False otherwise.
        """
        filepath = str(file)
        self.logger.debug("Scanning file", extra={"file": filepath})
        if not os.access(filepath, os.F_OK):
            self.logger.debug("Permission denied", extra={"filepath": filepath})
            return False

        last_modification_dt = datetime.fromtimestamp(file.stat().st_mtime)
        if self.modified_since and last_modification_dt < self.modified_since:
            self.logger.debug(
                f"Ignoring file because last modification was '{last_modification_dt}'",
                extra={"filepath": filepath},
            )
            return False

        with open(filepath, "rb") as f:
            result = self.cd.scan_stream(f)

        if not result:
            return False

        if "stream" not in result:
            return False

        result, message = result["stream"]
        if result == "ERROR":
            if "permission denied" in message.lower():
                message = "Permission denied"
            self.logger.debug(message, extra={"filepath": filepath})
        elif result == "FOUND":
            self.logger.info(
                f"File match", extra={"file": filepath, "signature": message}
            )
            return True
        else:
            self.logger.info(result, message)

        return False

    def scan_folder(self, folder):
        """
        Scan all files in a directory recursively.

        Args:
            folder (str): The path to the directory.

        Returns:
            list: A list of scan results.
        """
        results = []
        for filepath in utils.iterate_folder(folder):
            if self.scan_file(filepath):
                results.append(filepath)
        return results
