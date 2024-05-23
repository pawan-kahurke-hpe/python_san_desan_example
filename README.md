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

# Importing Required Modules
```python
import re
import argparse
import json
```
- `re`: Provides support for regular expressions to identify and replace patterns in text.
- `argparse`: Facilitates easy parsing of command-line arguments.
- `json`: Enables reading from and writing to JSON files.
  
# Defining the sanitize_log Function
```python
def sanitize_log(input_file, output_file, mapping_file, mode):
```
- `sanitize_log`: This function handles the sanitization and de-sanitization of log files based on the provided mode.

# Defining Patterns for Sensitive Information
```python
    hostname_pattern = re.compile(r'(hostname\s*=\s*)(\S+)')
    ip_pattern = re.compile(r'(\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b)')
    version_pattern = re.compile(r'(version\s*=\s*)(\S+)')
```
- `hostname_pattern`: Matches patterns like hostname = somehost.
- `ip_pattern`: Matches IP addresses in the form xxx.xxx.xxx.xxx.
- `version_pattern`: Matches patterns like version = 1.2.3.
# Initializing the Mapping Dictionary
```python
    mapping = {
        "server.example.com": "#########",
        "192.168.1.10": "*.*.*.*",
        "v5.4.2": "x.y.z"
    }
```
 # To store the mapping of original to sanitized values
- `mapping`: A dictionary that maps original sensitive values to their sanitized placeholders.
  
# Handling the Sanitization Mode
```python
    if mode == 'sanitize':
```
- `mode == 'sanitize'`: Checks if the mode is 'sanitize'.

# Reading the Input File and Writing the Sanitized Output File
```python
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
```
- `with open`: Opens the input file for reading and the output file for writing.
```python
                line = hostname_pattern.sub(r'\1#########', line)
                line = ip_pattern.sub(r'*.*.*.*', line)
                line = version_pattern.sub(r'\1x.y.z', line)
                outfile.write(line)
```
- `line = ...sub`: Replaces sensitive information in each line with placeholders and writes the sanitized line to the output file.
  
# Generating the Mapping
```python
                for match in hostname_pattern.finditer(line):
                    mapping[match.group(2)] = '#########'
                for match in ip_pattern.finditer(line):
                    mapping[match.group()] = '*.*.*.*'
                for match in version_pattern.finditer(line):
                    mapping[match.group(2)] = 'x.y.z'
```
- `for match in ...finditer`: Finds all matches of the patterns in the line and updates the mapping dictionary.

# Writing the Mapping to a File
```python
        with open(mapping_file, 'w') as mapfile:
            json.dump(mapping, mapfile)
```
- `with open(mapping_file, 'w')`: Opens the mapping file for writing.
- `json.dump(mapping, mapfile)`: Writes the mapping dictionary to the mapping file in JSON format.
- 
# Handling the De-sanitization Mode
```python
    elif mode == 'desanitize':
        with open(mapping_file, 'r') as mapfile:
            mapping = json.load(mapfile)
```
- `mode == 'desanitize'`: Checks if the mode is 'desanitize'.
- `json.load(mapfile)`: Loads the mapping dictionary from the mapping file.
Reading the Input File and Writing the De-sanitized Output File
```python
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
```
- `with open`: Opens the input file for reading and the output file for writing.

```python
                for original, sanitized in mapping.items():
                    line = line.replace(sanitized, original)
                outfile.write(line)
```
- `for original, sanitized in mapping.items()`: Iterates over the mapping dictionary and replaces placeholders with the original sensitive information.

# Main Script Execution
```python
if __name__ == "__main__":
```
- `if name == "main"`: Ensures the following code block runs only when the script is executed directly, not when imported as a module.

# Setting Up Argument Parsing
```python
    parser = argparse.ArgumentParser(description='Sanitize or desanitize log files')
    parser.add_argument('-in', dest='input_file', required=True, help='Input log file')
    parser.add_argument('-out', dest='output_file', required=True, help='Output file')
    parser.add_argument('-map', dest='mapping_file', required=True, help='Mapping file')
    parser.add_argument('-mode', dest='mode', choices=['sanitize', 'desanitize'], required=True,
                        help='Mode: "sanitize" to replace sensitive information, "desanitize" to restore original')
    args = parser.parse_args()
```
- `argparse.ArgumentParser`: Creates a parser object for handling command-line arguments.
- `add_argument`: Defines the command-line arguments and their properties.
  
# Calling the sanitize_log Function
```python
    sanitize_log(args.input_file, args.output_file, args.mapping_file, args.mode)
```
- `sanitize_log(args.input_file, args.output_file, args.mapping_file, args.mode)`: Calls the sanitize_log function with the parsed command-line arguments.

  # vaibhav
  ```python
  print("hello world")
```
- `project1:` This is project1
