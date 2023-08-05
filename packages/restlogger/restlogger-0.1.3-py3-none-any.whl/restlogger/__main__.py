import sys
import unittest
import logging
from .classmodule import My_Class
from .funcmodule import my_function
from .class_requests import Request_Class
from .class_logger import Logger_Class
from .test_requests import Requests_Test

logging.basicConfig(filename='test.csv', level=logging.DEBUG, format='%(asctime)s;%(levelname)s;%(message)s')

def main():
    logging.debug('====================================')
    logging.debug('in main')
    args = sys.argv[1:]
    logging.debug('count of args :: {}'.format(len(args)))

    my_function('hello world')

    my_object = My_Class('Lukas')
    my_object.say_name()

    my_object2 = Request_Class('http://api.openweathermap.org/data/2.5/weather?q=Zurich,CHZH&appid=3836093dde650898eb014e6f27304646')


    my_dict = my_object2.set_request()
    my_object2.parse_json(my_dict)
    
    logging.debug(my_dict['name'])
    

if __name__ == '__main__':
    unittest.main()
