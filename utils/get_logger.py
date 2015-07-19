import logging
import sys


def get_logger(name):
    """ Retrieves the application Logger object.

    According to my best practice, all packages and modules should have logging implemented by default. The Logger object used for this will be called towards the start of the module, just after the import statements, be immediately followed by a "START" message and then finas follows:

    According to my best practice, all packages and modules should have logging implemented by default. For specifics on this, please see the best practice guide.The Logger object should be defined immediately after the import statements and a "START" and "END" message should wrap the main body of the 

    import logging


    logger = logging.getLogger(__name__)
    logger.info('START {0}.'.format(__name__))
    ...
    logger.info('END {0}.'.format(__name__))

    

    The logger object has five levels of logging available to it; DEBUG, INFO, WARNING, ERROR and CRITICAL. In all instances, the logger objects logs to stdout. The format of the log is shown below.

    Usage::
    >>> from utils import logger
    >>> logger.info('Hello, world!')
    2015-07-13 22:54:48 - INFO - __main__ - Hello, world!

    """

    # get Logger
    # create Handler
    # set level of Handler
    # create Formatter
    # add Formatter to Handler
    # add Handler to Logger
    # return Logger

    # This is good because I can have a stdout handler that logs in a certain way, a file handler that logs in another, etc. It can all be done in here and then the application level logging changes. Experiment with this by adding a stdout logger, writing an app that uses it, then adding a file handler and seeing if the logging goes straight to that without any other mods.

    # Some interesting things to test: 
    # Is it possible to add multiple Formatter instances to a Handler (I assume not).
    # 



