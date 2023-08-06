import sys, getopt, io, re
import requests, logging, threading, time
import json, csv
from datetime import datetime

from .func_arg import my_argument_function
from .class_logger import My_Logger_Class
from .test_requests import Requests_Test

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s|%(levelname)s%(message)s")
file_handler = logging.FileHandler("main.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def main():
    now = datetime.now()
    now = now.strftime("%H:%M:%S")
    args = sys.argv[1:]
    logger.debug('count of args :: {}'.format(len(args)))

    for arg in args:
        logger.debug('passed argument :: {}'.format(arg))

    argu = my_argument_function(sys.argv[1:]) 

    yes_change = re.search("y", argu['change'], flags = re.I)

    my_object = My_Logger_Class(argu, now)
    my_object.clean_up()
    my_object.set_header()
    
    print("restlogger started logging at {} for every {} seconds".format(now,argu['freq']))
    print(my_object.__str__())
    for _ in range(1,10):
        my_dict = my_object.set_request()
        my_information = my_object.set_content(my_dict)
        now = datetime.now()
   
        if yes_change:
            my_object.logging_changes(my_information)
        else:
            my_object.logging_fixed(my_information)

        my_object.scroll()
        time.sleep(argu['freq'])
    
    now = datetime.now()
    now = now.strftime("%H:%M:%S")

    #help(My_Logger_Class)
    print("finished at {}".format(now))

if __name__ == '__main__':
    main()

