import logging
import sys


def get_logger(name):
    """ Defines a logger object.

    The logger object has five levels of logging available to it; DEBUG, INFO, WARNING, ERROR and CRITICAL. In all instances, the logger objects logs to stdout. The format of the log is shown below.

    Usage::
    >>> from utils import logger
    >>> logger.info('Hello, world!')
    2015-07-13 22:54:48 - INFO - __main__ - Hello, world!

    """
    format = '{asctime} - {levelname} - {name} - {message}'
    style = '{'
    datefmt = '%Y-%m-%d %H:%M:%S'
    level = logging.DEBUG
    stream = sys.stdout

    logging.basicConfig(format=format, style=style, datefmt=datefmt, level=level, stream=stream)
    return logging.getLogger(name)

    # get Logger
    # create Handler
    # set level of Handler
    # create Formatter
    # add Formatter to Handler
    # add Handler to Logger
    # return Logger

    # This is good because I can have a stdout handler that logs in a certain way, a file handler that logs in another, etc. It can all be done in here and then the application level logging changes. Experiment with this by adding a stdout logger, writing an app that uses it, then adding a file handler and seeing if the logging goes straight to that without any other mods.
