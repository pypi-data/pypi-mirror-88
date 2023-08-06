import sys, getopt, io 
import requests, logging, threading
import json, csv
from datetime import datetime

filename = 'log_restlogger.csv'
delim = '|'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s"+delim+"%(levelname)s"+delim+"%(message)s")
file_handler = logging.FileHandler(filename)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class My_Logger_Class():
    """NAME
        My_Logger_Class - A Class for logging url requests
       Description
        


    """


    def __init__(self, argu, now):
        self.argu = argu
        self.key_name = argu['key'] 
        self.url = argu['url']
        self.change = argu['change']
        self.check = 'check'
        self.now = now
        self.filename = filename
        self.max_lines = 5

    def __str__(self):
        """Representational function for the user as a string."""
        return 'Key = {} | change only = {} | URL = {}'.format(self.key_name, self.change, self.url)
        

    def __eq__(self, other):
        """Hashable objects which compare should have the same hash value"""
        return (self.__class__ == other.__class__
                and self.key == other.key)


    def set_request(self):
        """The set_request function pulls data from the API with the requests module & saves python doct in req_datai."""

        req_data = requests.get(self.argu['url'])
        return req_data.json()

    def set_content(self, req_key):
        uberdict = self.argu['xpath']
        key = self.argu['key']

        if uberdict == '':
            requested_data = req_key[key]
        elif key == '':
            requested_data = req_key[uberdict]
            self.key_name = uberdict
        else:
            requested_data = req_key[uberdict][key]

        return requested_data

    def set_header(self):
        """This function sets the two first lines of the logging file."""
        f = open(self.filename, "a")
        f.write("# Logging in file {} beginning at {}\n".format(self.filename,self.now))
        f.write("YYYY-MM-DD hh-mm-ss,mil Level {}\n".format(self.key_name))
        f.close()

    def logging_fixed(self, requested_data):
        """This function does the easy mode where it just loggs it when called."""
        logger.debug(requested_data)

    def logging_changes(self, requested_data):
        """This function only loggs when the key has changed.
            The first time when called it logs the key and sets up the check variable."""
        if self.check == requested_data:
            pass
        else:
            logger.debug(requested_data)
        self.check = requested_data


    def clean_up(self):
        """This function cleans the log file before starting the logging."""
        open(self.filename, 'w').close()


    def scroll(self):
        """This function deletes the first log entry to not get too long."""
        f = open(self.filename)
        lines = f.readlines()
        count = len(lines)
        f.close

        if count >= self.max_lines:
            del lines[2]

            f2 = open(self.filename, "w+")
            for line in lines:
                f2.write(line)
            f2.close()


