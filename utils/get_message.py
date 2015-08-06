import amqp
from contextlib import closing


def get_message(queue=''):
    """ Get the first message from a queue.

    The first message from a queue is retrieved. If there is no such message, the function exits quietly. 

    :param queue (optional): The name of the queue from which to get the message. If blank, the default queue is used.

    Usage::

    >>> from utils import get_message
    >>> message = get_message('queue')

    """
    with closing(amqp.Connection()) as connection:
        channel = connection.channel()
        return channel.basic_get(queue=queue)
