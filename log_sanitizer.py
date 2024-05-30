import re
import argparse
import json
import hashlib
import functools
from patterns import IP_PATTERN, HOSTNAME_PATTERN, EMAIL_PATTERN, PASSWORD_PATTERN

def log_decorator(func):
    """Decorator to log the start and end of a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Starting {func.__name__}...")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}.")
        return result
    return wrapper

def manage_mapping_decorator(func):
    """Decorator to load and save mapping automatically."""
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        self.load_mapping()
        result = func(self, *args, **kwargs)
        self.save_mapping()
        return result
    return wrapper

class LogSanitizer:
    def __init__(self, input_file, output_file, mapping_file, mode):
        self.input_file = input_file
        self.output_file = output_file
        self.mapping_file = mapping_file
        self.mode = mode
        self.ip_pattern = IP_PATTERN
        self.hostname_pattern = HOSTNAME_PATTERN
        self.email_pattern = EMAIL_PATTERN
        self.password_pattern = PASSWORD_PATTERN
        self.mapping = {}

    def hash_placeholder(self, data, data_type):
        """Generate a unique placeholder for sensitive data with a type prefix."""
        hashed_value = hashlib.sha1(data.encode()).hexdigest()[:20]
        return f"{data_type}_{hashed_value}"

    def load_mapping(self):
        try:
            with open(self.mapping_file, 'r') as mapfile:
                self.mapping = json.load(mapfile)
        except FileNotFoundError:
            self.mapping = {}

    def save_mapping(self):
        with open(self.mapping_file, 'w') as mapfile:
            json.dump(self.mapping, mapfile)

    @log_decorator
    @manage_mapping_decorator
    def sanitize(self):
        with open(self.input_file, 'r') as infile, open(self.output_file, 'w') as outfile:
            for line in infile:
                for pattern, data_type in [(self.hostname_pattern, 'HOST'), 
                                           (self.ip_pattern, 'IP'), 
                                           (self.email_pattern, 'EMAIL'), 
                                           (self.password_pattern, 'PASS')]:
                    for match in pattern.findall(line):
                        if match not in self.mapping:
                            self.mapping[match] = self.hash_placeholder(match, data_type)
                        line = line.replace(match, self.mapping[match])
                outfile.write(line)

    @log_decorator
    @manage_mapping_decorator
    def desanitize(self):
        reverse_mapping = {v: k for k, v in self.mapping.items()}
        with open(self.input_file, 'r') as infile, open(self.output_file, 'w') as outfile:
            for line in infile:
                for sanitized, original in reverse_mapping.items():
                    line = line.replace(sanitized, original)
                outfile.write(line)

    def process(self):
        if self.mode == 'sanitize':
            self.sanitize()
        elif self.mode == 'desanitize':
            self.desanitize()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sanitize or desanitize log files')
    parser.add_argument('-in', dest='input_file', required=True, help='Input log file')
    parser.add_argument('-out', dest='output_file', required=True, help='Output file')
    parser.add_argument('-map', dest='mapping_file', required=True, help='Mapping file')
    parser.add_argument('-mode', dest='mode', choices=['sanitize', 'desanitize'], required=True,
                        help='Mode: "sanitize" to replace sensitive information, "desanitize" to restore original')
    args = parser.parse_args()

    sanitizer = LogSanitizer(args.input_file, args.output_file, args.mapping_file, args.mode)
    sanitizer.process()
