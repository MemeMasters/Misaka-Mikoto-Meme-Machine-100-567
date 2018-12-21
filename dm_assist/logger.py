import sys
import os
from os import path
import logging

from os.path import dirname as d
log_folder = path.join(d(d(__file__)), 'logs')
if not path.isdir(log_folder):
    os.makedirs(log_folder)


root_logger = logging.getLogger()


def setLogLevel(lvl):
    root_logger.setLevel(lvl)

log_formatter = logging.Formatter(
    '[%(asctime)s: %(name)s (%(levelname)s)] %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p'  # Uses time.strftime format: https://docs.python.org/3.5/library/time.html#time.strftime
)

# Setup the file logger
file_handler = logging.FileHandler('{0}/{1}.log'.format(log_folder, 'dnd_bot'))
file_handler.setFormatter(log_formatter)
root_logger.addHandler(file_handler)

# Setup the console logger
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)
root_logger.addHandler(console_handler)

# Set the base log level
setLogLevel(logging.INFO)
