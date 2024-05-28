import re
import argparse
import json
import hashlib

class LogSanitizer:
    def __init__(self, input_file, output_file, mapping_file, mode):
        self.input_file = input_file
        self.output_file = output_file
        self.mapping_file = mapping_file
        self.mode = mode
        self.ip_pattern = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
        self.hostname_pattern = re.compile(r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}\b')
        self.mapping = {}

    def hash_placeholder(self, data):
        """Generate a unique placeholder for sensitive data."""
        return hashlib.sha1(data.encode()).hexdigest()[:20]

    def load_mapping(self):
        """Load the mapping file if it exists."""
        try:
            with open(self.mapping_file, 'r') as mapfile:
                self.mapping = json.load(mapfile)
        except FileNotFoundError:
            self.mapping = {}

    def save_mapping(self):
        """Save the mapping to a file."""
        with open(self.mapping_file, 'w') as mapfile:
            json.dump(self.mapping, mapfile)

    def sanitize(self):
        """Sanitize the log file."""
        with open(self.input_file, 'r') as infile, open(self.output_file, 'w') as outfile:
            for line in infile:
                for match in self.hostname_pattern.findall(line):
                    if match not in self.mapping:
                        self.mapping[match] = ' ' + self.hash_placeholder(match)
                    line = line.replace(match, self.mapping[match])

                for match in self.ip_pattern.findall(line):
                    if match not in self.mapping:
                        self.mapping[match] = '' + self.hash_placeholder(match)
                    line = line.replace(match, self.mapping[match])

                outfile.write(line)
        self.save_mapping()

    def desanitize(self):
        """Desanitize the log file."""
        self.load_mapping()
        reverse_mapping = {v: k for k, v in self.mapping.items()}
        with open(self.input_file, 'r') as infile, open(self.output_file, 'w') as outfile:
            for line in infile:
                for sanitized, original in reverse_mapping.items():
                    line = line.replace(sanitized, original)
                outfile.write(line)

    def process(self):
        """Process the log file based on the mode."""
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
