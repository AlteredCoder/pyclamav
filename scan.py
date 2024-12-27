import os
import multiprocessing
import pyclamd
import utils
from datetime import datetime

class Scan:
    """
    A class to scan files using ClamAV with multiprocessing.

    """

    def __init__(self, nb_process, last_modiciation, logger):
        """
        Initialize the Scan class.

        Args:
            nb_process (int): The number of processes to use for scanning.
            logger (logging.Logger): The logger to use for logging scan results.

        Raises:
            ValueError: If unable to connect to the ClamAV daemon.
        """
        self.nb_process = nb_process
        self.logger = logger
        self.last_modification = last_modiciation
        try:
            self.cd = pyclamd.ClamdUnixSocket()
            self.cd.ping()
        except pyclamd.ConnectionError:
            try:
                self.cd = pyclamd.ClamdNetworkSocket()
                self.cd.ping()
            except pyclamd.ConnectionError:
                raise ValueError("could not connect to clamd server either by unix or network socket")

    def scan_file(self, file, result_queue):
        """
        Scan a file and put the result in the queue.

        Args:
            filepath (pathlib.PosixPath): The file.
            result_queue (Queue): The queue to put the scan result.
        """
        filepath = str(file)
        self.logger.debug("Scanning file", extra={"file": filepath})
        if not os.access(filepath, os.F_OK):
            self.logger.debug("Permission denied", extra={"filepath" : filepath})
            return

        last_modification_dt = datetime.fromtimestamp(file.stat().st_mtime)
        if last_modification_dt < self.last_modification:
            self.logger.debug(f"Ignoring file because last modification was '{last_modification_dt}'", extra={"filepath": filepath})
            return
        
        f = open(filepath, "rb")
        result = self.cd.scan_stream(f)
        if not result:
            return

        if "stream" not in result:
            return

        result, message = result["stream"] 
        if result == "ERROR":
            if "permission denied" in message.lower():
                message = "Permission denied"
            self.logger.debug(message, extra={"filepath" : filepath})
        elif result == "FOUND":
            self.logger.info(f"File match", extra={"file": filepath, "signature": message})
            result_queue.put((filepath, message))
        else:
            self.logger.info(result, message)

    def worker(self, file_queue, result_queue, task_counter):
        """
        Worker function to process files from the queue.

        Args:
            file_queue (Queue): The queue containing file paths to scan.
            result_queue (Queue): The queue to put the scan results.
            task_counter (Value): A counter to track the number of completed tasks.
        """
        while True:
            filepath = file_queue.get()
            if filepath is None:
                break
            self.scan_file(filepath, result_queue)
            with task_counter.get_lock():
                task_counter.value += 1

    def scan_folder(self, folder):
        """
        Scan all files in a directory recursively using multiprocessing.

        Args:
            folder (str): The path to the directory.

        Returns:
            list: A list of scan results.
        """
        file_queue = multiprocessing.Queue()
        result_queue = multiprocessing.Queue()
        task_counter = multiprocessing.Value('i', 0)


        processes = []
        for _ in range(self.nb_process):
            p = multiprocessing.Process(target=self.worker, args=(file_queue, result_queue, task_counter))
            p.start()
            processes.append(p)

        for filepath in utils.iterate_folder(folder):
            file_queue.put(filepath)

        for _ in range(self.nb_process):
            file_queue.put(None)

        total_tasks = len(list(utils.iterate_folder(folder)))
        while task_counter.value < total_tasks:
            pass

        results = []
        while not result_queue.empty():
            results.append(result_queue.get())

        for p in processes:
            p.join()

        return results