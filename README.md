![Tests](https://github.com/AlteredCoder/pyclamav/actions/workflows/pytest.yml/badge.svg)
![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/AlteredCoder/88ae1c5c4c732ba28346b3fac87b44a3/raw/covbadge.json)

# pyclamav

`pyclamav` is a Python utility script that uses the `pyclamd` library to run ClamAV scans on specified folders and files that have been modified within a specified duration. This tool is configurable via a JSON configuration file and command-line arguments.

## Features

- Scan specified folders for viruses using ClamAV.
- Scan files modified within a specified duration (or all files if not specified).
- Configurable via a JSON configuration file.
- Command-line arguments for flexibility.

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

## Configuration

Create a JSON configuration file (e.g., `config.json`) with the following structure:

```json
{
    "folders": ["/path/to/folder1", "/path/to/folder2"],
    "log_file": "pyclamav.log",
    "modified_file_since": "24h",
    "verbose": false
}
```

- `folders`: List of folders to monitor.
- `log_file`: Path to the log file.
- `modified_file_since`: Duration for which files will be scanned (e.g., `24h` for 24 hours). If this value is not specified, all the files will be scanned
- `verbose`: Verbose mode (true or false).

## Usage

Run the `pyclamav` script with the following command:

```bash
pyclamav --config config.json [--modified-since DURATION] [--verbose]
```

### Arguments

- `--config`: Path to the JSON configuration file. Default is `config.json`.
- `--modified-since`: Duration for which files will be scanned (e.g., `24h` for 24 hours, `48h` for 48 hours). Default is `24h`.
- `--verbose`: Enable verbose mode. Default is `False`.

### Examples

A test data file is available in `./tests/data/`.

You can use the following `config.json` file to test:

```json
{
    "folders" : ["./tests/data"],
    "log_folder": "./logs/",
}
```

1. **Scan folders specified in the configuration file**:

```bash
pyclamav --config config.json
```

2. **Scan folders and files modified in the last 7 days**:

```bash
pyclamav --config config.json --modified-since 7d
```

3. **Scan folders and files modified in the last 1 hour with verbose mode**:

```bash
pyclamav --config config.json --modified-since 1h --verbose
```

## Cron

Add the following cronjob configuration to run it everyday

```
0 0 * * * /path/to/venv/bin/python3.11 /path/to/pyclamav/pyclamav.py -c /path/to/pyclamav/config.json
```

## Logging

Logs are written to the user's home directory under the `logs` folder. The log file is named `pyclamav.log`.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please open an issue on the GitHub repository.