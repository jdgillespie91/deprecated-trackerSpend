""" Defines a logger object.

The logger object has five levels of logging available to it; DEBUG, INFO, WARNING, ERROR and CRITICAL. In all instances, the logger objects logs to stdout. The format of the log is:
    2015-01-01 12:34:56 - INFO - Hello, world!

Usage::
>>> from utils import logger
>>> logger.info('Hello, world!')
2015-01-01 12:34:56 - INFO - Hello, world!

"""
import logging
from sys import stdout


__all__ = ['logger']

logging.basicConfig(format='{asctime} - {levelname} - {name} - {message}', style='{', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG, stream=stdout)
logger = logging.getLogger()
