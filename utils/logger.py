import logging
from sys import stdout


def get_logger():
    """ Returns a logger object.

    get_logger returns a logger object that has five levels of logging available to it; DEBUG, INFO, WARNING, ERROR and CRITICAL. In all instances, the logger object logs to stdout. The format of the log is shown below.

    Usage::
    >>> from utils import logger
    >>> logger.info('Hello, world!')
    2015-07-01 12:34:56 - INFO - Hello, world!

    """
    logging.basicConfig(format='{asctime} - {levelname} - {name} - {message}', style='{', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG, stream=stdout)
    return logging.getLogger()


logger = get_logger()
