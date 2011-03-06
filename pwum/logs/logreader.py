import re
import fileinput
from datetime import datetime

_lineRegex = re.compile(r'([^ ]*) ([^ ]*) ([^ ]*) \[([^\]]*)\] "([^"]*)" (\d+) ([^ ]*)')
class LogLineReader:
    """
    A Python class whose attributes are the fields of Apache log line.
    """
    
    def __init__(self, line):
        m = _lineRegex.match(line.strip())
 
        self.ip, self.ident, \
        self.http_user, self.time, \
        self.request_line, self.http_response_code, \
        self.http_response_size = m.groups()
        
        self.http_method, self.url, self.http_vers = self.request_line.split()
        self.time = self.time.split()[0] ##currently we discard timezone
        
        
        self.date = datetime.strptime(self.time, '%d/%b/%Y:%H:%M:%S')
        
    def __str__(self):
        """Return a simple string representation of an ApacheLogLine."""
        return ' '.join([self.ip, self.time, self.http_method, self.url, self.http_response_code, self.http_response_size])


class LogFile:
    """
    An abstraction for reading and parsing log files.
    """
    
    def __init__(self, line_parser, *filename):
        """Instantiating an ApacheLogFile opens a log file.    
        Client is responsible for closing the opened log file by calling close()"""
        
        self.line_parser = line_parser
        self.f = fileinput.input(filename)
    def close(self):
        self.f.close()

    def __iter__(self):
        """Returns parsed log line object for each iteration. """
        
        for line in self.f:
            log_line = self.line_parser(line)
            yield log_line

                    
