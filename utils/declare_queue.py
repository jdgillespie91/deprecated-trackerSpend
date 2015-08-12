import amqp
from contextlib import closing


def declare_queue(queue):
    """ Declare a queue.

    A queue is declared. If a queue with the same name is already declared, the properties of the queue are checked. If the declared queue has the same properties, the function exits quietly. If the declared queue has different properties, an exception is raised.

    :param queue: The name of the queue to be declared.

    Usage::

    >>> from utils import declare_queue
    >>> message = declare_queue('queue')

    """
    with closing(amqp.Connection()) as connection:
        channel = connection.channel()
        channel.queue_declare(queue=queue)
