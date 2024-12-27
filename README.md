# pyclamav

`pyclamav` is a Python utility script that uses the [Alexandre Norman `pyclamd` library](https://xael.org/pages/pyclamd.html) to run ClamAV scans on specified folders and files that have been created within a specified duration. This tool is configurable via a JSON configuration file and command-line arguments.

## Features

- Scan specified folders for viruses using ClamAV.
- Scan files created within a specified duration (ex: file created during the last 24 hours).
- Configurable via a JSON configuration file.
- Command-line arguments for flexibility.

## Installation

1. **Install ClamAV**: Ensure that ClamAV is installed and running on your system.
2. **Install requirements**: Install the requirements library using pip.

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
    "folders_to_scan": [
        "/path/to/folder1",
        "/path/to/folder2"
    ],
    "created_duration": "1d"  // Optional: Specify the duration in days (e.g., 1d for 1 day)
}
```

## Usage

Run the `pyclamav` script with the following command:

```bash
pyclamav --config config.json [--created-duration DURATION]
```

### Arguments

- `--config`: Path to the JSON configuration file.
- `--created-duration`: Duration for which files will be scanned (e.g., `7d` for 7 days, `1h` for 1 hour). This argument overrides the `created_duration` specified in the configuration file.

### Examples

1. **Scan folders specified in the configuration file**:

```bash
pyclamav --config config.json
```

2. **Scan folders and files created in the last 7 days**:

```bash
pyclamav --config config.json --created-duration 7d
```

3. **Scan folders and files created in the last 1 hour**:

```bash
pyclamav --config config.json --created-duration 1h
```

## Logging

Logs are written to the user's home directory under the `logs` folder. The log file is named `pyclamav.log`.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please open an issue on the GitHub repository or contact the maintainer.
