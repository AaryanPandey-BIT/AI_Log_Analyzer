import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from log_parser import LogParser

class TestLogParser:
    
    def setup_method(self):
        self.parser = LogParser()

    def test_parse_failed_login(self):
        line = "Dec 24 10:00:01 server sshd[123]: Failed password for invalid user admin from 192.168.1.100 port 22 ssh2"
        result = self.parser.parse_line(line)
        assert result is not None
        assert result['status'] == 'failed'
        assert result['user'] == 'admin'
        assert result['ip'] == '192.168.1.100'

    def test_parse_successful_login(self):
        line = "Dec 24 10:05:00 server sshd[124]: Accepted password for user1 from 192.168.1.101 port 22 ssh2"
        result = self.parser.parse_line(line)
        assert result is not None
        assert result['status'] == 'success'
        assert result['user'] == 'user1'
        assert result['ip'] == '192.168.1.101'

    def test_parse_irrelevant_line(self):
        line = "Dec 24 10:06:00 server sshd[125]: Connection closed by 192.168.1.102"
        result = self.parser.parse_line(line)
        assert result is None

    def test_parse_with_excess_whitespace(self):
        # Test with extra spaces between fields
        line = "Dec 24   10:00:01     server    sshd[123]:    Failed password for   invalid user   admin   from   192.168.1.100 port 22 ssh2"
        result = self.parser.parse_line(line)
        assert result is not None
        assert result['status'] == 'failed'
        assert result['user'] == 'admin'
        assert result['ip'] == '192.168.1.100'

    def test_malformed_line_no_crash(self):
        # Test that garbage input returns None instead of raising an exception
        line = "This is just total garbage content !!! @@@"
        result = self.parser.parse_line(line)
        assert result is None
