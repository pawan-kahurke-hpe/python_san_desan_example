# Log File Sanitization and De-sanitization Script

## Overview
This script provides functionality to sanitize sensitive data (such as IP addresses, hostnames, and version numbers) in log files by replacing them with placeholders. It also allows for the reverse operation, where placeholders in a sanitized file are replaced back with the original sensitive data.

## Prerequisites
- Python 3.x
- Basic understanding of regular expressions

## Usage

### Command-line Arguments
- `-in`: Input log file (required)
- `-out`: Output file (required)
- `-map`: Mapping file to store or read the mappings (required)
- `-mode`: Mode of operation: "sanitize" to replace sensitive information, "desanitize" to restore original (required)

### Example Usage

#### Sanitization

```bash
python script_name.py -in logfile.txt -out sanitized_logfile.txt -map mappingfile.json -mode sanitize
```
### Desantization
```bash
python script_name.py -in sanitized_logfile.txt -out desanitized_logfile.txt -map mappingfile.json -mode desanitize
```
