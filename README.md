# LogSanitizer

`LogSanitizer` is a Python script that sanitizes and desanitizes sensitive information (such as IP addresses and hostnames) in log files. This tool is useful for masking sensitive data before sharing logs and restoring the original data when needed.

## Features

- **Sanitize Mode**: Replaces sensitive information with hashed placeholders.
- **Desanitize Mode**: Restores the original sensitive information using a mapping file.
- **Configurable Patterns**: Easily adjust the regex patterns to target different types of sensitive data.

## Prerequisites

- Python 3.x
- Required Python packages: `re`, `argparse`, `json`, `hashlib`

## Installation

1. Ensure Python 3.x is installed on your system.
2. Save the script as `log_sanitizer.py`.

## Usage

### Command-Line Arguments

- `-in`: Path to the input log file (required).
- `-out`: Path to the output file (required).
- `-map`: Path to the mapping file (required).
- `-mode`: Mode of operation (`sanitize` or `desanitize`) (required).
# Sanitize the Log File
```python
python log_sanitizer.py -in input.log -out sanitized_output.log -map mapping.json -mode sanitize
```
# Desanitize the Log File
```python
python log_sanitizer.py -in sanitized_output.log -out desanitized_output.log -map mapping.json -mode desanitize
```
