Bien sûr ! Voici le contenu complet du fichier README en markdown que vous pouvez copier et coller directement :

```markdown
# pyclamav

`pyclamav` is a Python utility script that uses the `pyclamd` library to run ClamAV scans on specified folders and files that have been modified within a specified duration. This tool is configurable via a JSON configuration file and command-line arguments.

## Features

- Scan specified folders for viruses using ClamAV.
- Scan files modified within a specified duration.
- Configurable via a JSON configuration file.
- Command-line arguments for flexibility.
- Multiprocessing support for improved performance.

## Installation

1. **Install ClamAV**: Ensure that ClamAV is installed and running on your system.

- On Ubuntu/Debian

```
sudo apt install clamav clamav-daemon
sudo systemctl start clamav-daemon
sudo systemctl enable clamav-daemon
```

- CentOS/RHEL

```
sudo yum install clamav clamav-daemon
sudo systemctl start clamav-daemon
sudo systemctl enable clamav-daemon
```

You can add the following cronjob configuration:
```
0 2 * * * /usr/bin/freshclam
```

2. **Install the requirements**

```bash
pip install -r requirements.txt
```

3. **Install pyclamav**: Clone the repository and install the script.

```bash
git clone https://github.com/yourusername/pyclamav.git
cd pyclamav
pip install .
```

## Configuration

Create a JSON configuration file (e.g., `config.json`) with the following structure:

```json
{
    "folders": ["/path/to/folder1", "/path/to/folder2"],
    "log_file": "pyclamav.log",
    "modified_file_duration": "24h",
    "nb_process": 5,
    "verbose": false
}
```

- `folders`: List of folders to monitor.
- `log_file`: Path to the log file.
- `modified_file_duration`: Duration for which files will be scanned (e.g., `24h` for 24 hours).
- `nb_process`: Number of processes to use for scanning.
- `verbose`: Verbose mode (true or false).

## Usage

Run the `pyclamav` script with the following command:

```bash
pyclamav --config config.json [--modified-duration DURATION] [--verbose] [--process NB_PROCESS]
```

### Arguments

- `--config`: Path to the JSON configuration file. Default is `config.json`.
- `--modified-duration`: Duration for which files will be scanned (e.g., `24h` for 24 hours, `48h` for 48 hours). Default is `24h`.
- `--verbose`: Enable verbose mode. Default is `False`.
- `--process`: Number of processes to use for scanning. Default is `5`.

### Examples

1. **Scan folders specified in the configuration file**:

```bash
pyclamav --config config.json
```

2. **Scan folders and files modified in the last 7 days**:

```bash
pyclamav --config config.json --modified-duration 7d
```

3. **Scan folders and files modified in the last 1 hour with verbose mode**:

```bash
pyclamav --config config.json --modified-duration 1h --verbose
```

4. **Scan folders using 10 processes**:

```bash
pyclamav --config config.json --process 10
```

## Logging

Logs are written to the user's home directory under the `logs` folder. The log file is named `pyclamav.log`.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please open an issue on the GitHub repository.
```