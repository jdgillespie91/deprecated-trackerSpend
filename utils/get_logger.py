import logging
from sys import stdout


def get_logger(id):
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
    stream = stdout

    logging.basicConfig(format=format, style=style, datefmt=datefmt, level=level, stream=stream)
    return logging.getLogger(id)
