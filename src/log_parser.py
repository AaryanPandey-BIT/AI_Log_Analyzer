import re
from datetime import datetime
from typing import Dict, Optional, Generator
import sys

class LogParser:
    """
    Parses raw SSH authentication logs into structured data.
    """
    
    # Regex patterns for common SSH log formats
    # Relaxed timestamp matching and flexible whitespace (\s+)
    _LOG_PATTERN = re.compile(
        r'(?P<timestamp>^.*?\d{2}:\d{2}:\d{2})\s+'           # Flexible timestamp at start
        r'(?P<hostname>\S+)\s+'                               # Hostname
        r'sshd\[\d+\]:\s+'                                    # Process
        r'(?P<message>.*)'                                    # The rest of the message
    )

    # Specific patterns to identify event types
    # Flexible whitespace (\s+) instead of literal spaces
    _FAILED_PATTERN = re.compile(r'Failed\s+password\s+for\s+(invalid\s+user\s+)?(?P<user>\S+)\s+from\s+(?P<ip>\d{1,3}(?:\.\d{1,3}){3})')
    _ACCEPTED_PATTERN = re.compile(r'Accepted\s+password\s+for\s+(?P<user>\S+)\s+from\s+(?P<ip>\d{1,3}(?:\.\d{1,3}){3})')

    def parse_line(self, line: str) -> Optional[Dict]:
        """
        Parses a single log line into a dictionary.
        Returns None if the line doesn't match the SSH format or isn't relevant.
        """
        try:
            line = line.strip()
            if not line:
                return None

            match = self._LOG_PATTERN.match(line)
            if not match:
                return None

            data = match.groupdict()
            message = data['message']

            # Determine event type
            if 'Failed password' in message:
                fail_match = self._FAILED_PATTERN.search(message)
                if fail_match:
                    return {
                        'timestamp': data['timestamp'],
                        'ip': fail_match.group('ip'),
                        'user': fail_match.group('user'),
                        'status': 'failed'
                    }
            
            elif 'Accepted password' in message:
                success_match = self._ACCEPTED_PATTERN.search(message)
                if success_match:
                    return {
                        'timestamp': data['timestamp'],
                        'ip': success_match.group('ip'),
                        'user': success_match.group('user'),
                        'status': 'success'
                    }
        except Exception as e:
            # Senior Engineering: Log the error safely and continue (do not crash)
            print(f"Warning: Error parsing line: {line[:30]}... - {e}", file=sys.stderr)
            return None

        return None

    def parse_file(self, filepath: str) -> Generator[Dict, None, None]:
        """
        Generator that yields parsed log events from a file.
        """
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    parsed = self.parse_line(line)
                    if parsed:
                        yield parsed
        except FileNotFoundError:
            print(f"Error: File not found - {filepath}")
        except Exception as e:
            print(f"Error reading file {filepath}: {e}")
