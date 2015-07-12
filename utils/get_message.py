import amqp
from contextlib import closing


def __get_channel(connection):
    return connection.channel()

def __declare_queue(channel, queue):
    channel.queue_declare(queue=queue, durable=True, auto_delete=False)

def __get_message_from_queue(channel, queue):
    return channel.basic_get(queue=queue)

def get_message(queue):
    """ Get the first message from a queue.

    The first message from a queue is retrieved. If there is no such message, the function exits quietly. The queue is declared if one of the same name does not already exist. If one of the same name does already exist but has different parameters, an error is raised. The queue has durable=True and auto_delete=False set as default.

    :param queue: The name of the queue from which to get the message.

    Usage::

    >>> from utils import get_message
    >>> message = get_message('queue')

    """
    with closing(amqp.Connection()) as connection:
        channel = __get_channel(connection)
        __declare_queue(channel, queue)
        return  __get_message_from_queue(channel, queue)
