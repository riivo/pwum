# -*- coding: utf_8 -*-

import uuid
from collections import defaultdict

from pwum import config


class LogParser:
    
    sessions = {}
    ip_blacklist = []
    pages = defaultdict(lambda :0) # keep count of each url occurance
    count = 0
    
    has_parsed = False
    
    def __init__(self, apache_log_file):
        self.apache_log_file = apache_log_file

    def format_url(self,line):
        """ format all url into same convention: no querystrin, no trailing slashes """

        q = line.url.find("?")
        if q != -1:
            line.url = line.url[0:q]
        
        if len(line.url) > 0 and line.url[-1] == "/":
            line.url = line.url[0:(len(line.url)-1)]
        
        if len(line.url) > 0 and line.url[0] == "/":
            line.url = line.url[1:]
        
        if len(line.url) == 0:
            line.url = config.HOME_PAGE
        
        return line
    
    #XXX make configurable
    def filter(self, line):
        """
        return True or False indicating if this line should be filtered or not"
        """
        result = False
        #if ip is in blacklist
        if self.ip_blacklist.count(line.ip) > 0:
            return True
        
        """following rules are not bulletproof, but work. shoudl check also if they are at the end of url"""
        find_predicates = [".png", ".gif", ".jpg", ".pjpeg", ".png", ".x-png", ".js", ".css", ".ico"]
        
        for predicate in find_predicates:
            if line.url.find(predicate) != -1:
                return True
            
        result = result or line.http_method.find("OPTIONS") != -1
        result = result or line.url.find("/~") != -1
    
        return result
    
    def parse(self):
        """
        runs of over log lines and extracts sessions and eliminates noise
        """
        if self.has_parsed: #ultimate 
            return
        
        last_session_url = {} #storing the last url for every session
        last_ip = {} #tuples (time, unique id) for IPs
        last_session_http_code = {} #storing the last http_response_code for every session
    
        for line in self.apache_log_file:
            # we consider all access to robots.txt as bots
            if line.url.find("robots.txt") != -1:
                self.ip_blacklist.append(line.ip)
    
            #whether the line should be discarded or not
            if self.filter(line):
                continue
        
            self.format_url(line)
    
            self.pages[line.url] +=1
            
            last_ip.setdefault(line.ip, (line.date, uuid.uuid4().hex))
            
            (last_time_for_ip, last_session_for_ip) = last_ip[line.ip]
            
            delta =  line.date - last_time_for_ip
            if delta.seconds  > config.SESSION_TIMEOUT:
                sess_key =  uuid.uuid4().hex
            else:
                sess_key =  last_session_for_ip

            #if last request in this session was met with http code 302, then
            #this line is probably a redirect and should be discarded
            code = last_session_http_code.get(sess_key, 0)
            if int(code) == 302 and  int(line.http_response_code) == 200 and delta.seconds < 2:
                continue        

            last_session_url.setdefault(sess_key, line.url)
            last_ip[line.ip] = (line.date, sess_key)
            # add last session http code
            last_session_http_code.setdefault(sess_key, line.http_response_code)
    
            #add line to sessions dictionary
            #if session doesn't exist in sessions, then initialize it
            self.sessions.setdefault(sess_key, Session(sess_key)).add_line(line)
    
            self.count +=1
            
            self.has_parsed = True
    
    def get_data_encoding(self, page_min_occurance=config.PAGE_MIN_OCCURANCE):
        """
        derives encoding for pages=>numbers so that sessions can be represented
        as feature vectors
        """
        #encode all pages into numebrs, easier to use in vector representation
        code_book = {}
        index = 0
        for page, count in self.pages.items():
            if count >= page_min_occurance:
                code_book[page]  = index
                index+=1
        
        return code_book
            
    def get_simple_sessions(self):
        """
        returns simple representation of session: list of urls visited
        """
        simple_sessions = []
        
        for s in self.sessions.values():
            simple_sessions.append(s.to_simple())
        
        return simple_sessions


class Session:
    
    def __init__(self,sess_key):
        self.sess_key = sess_key
        self.lines = []
    
    def add_line(self, line):
        self.lines.append(line)
        
    def to_simple(self):
        pages = [line.url for line in self.lines]
        return pages
    
        
            
