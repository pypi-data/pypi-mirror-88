import requests
import json
import logging

class Request_Class():
    def __init__(self, url_address):
        self.url_address = url_address

    def set_request(self):
        req_data = requests.get(self.url_address)

        r_dict = req_data.json()
        logging.debug('---------------------------')
        logging.debug(type(r_dict))
        logging.debug("---------------------------")

        return r_dict

    def parse_json(self, dict):
        logging.debug('--------test2--------')
        logging.debug(type(dict))
        


