import amqp
import logging
from contextlib import closing


def get_message(queue):
    """ Get the first message from a queue.

    The first message from a queue is retrieved. If the queue does not exist, an amqp.exception.NotFound error is raised. If the queue exists and there is no message, a None object is returned. If the queue exists and there is a message, it is returned as an amqp.Message object.

    :param queue: The name of the queue from which to get the message.

    Usage::

    >>> from utils import get_message
    >>> message = get_message('queue')

    """
    logger = logging.getLogger(__name__)
    logger.info('START {0}.'.format(__name__))

    with closing(amqp.Connection()) as connection:
        channel = connection.channel()
        return channel.basic_get(queue=queue)

    logger.info('END {0}.'.format(__name__))
