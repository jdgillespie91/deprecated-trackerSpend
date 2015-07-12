import amqp
from contextlib import closing


def __get_channel(connection):
    return connection.channel()

def __bind_queue_to_exchange(channel, queue, exchange, routing_key):
    channel.queue_bind(queue=queue, exchange=exchange, routing_key=routing_key)

def bind_queue_to_exchange(queue, exchange, routing_key):
    """ Bind a queue to an exchange with specified routing_key.

    This function binds a queue to an exchange. The routing_key specifies what messages the queue should receive. Note that the routing_key is only required with particular exchange types. TODO Be specific about exchange types and implement verification.

    :param queue: The name of the queue to be bound.
    :param exchange: The name of the exchange to be bound to.
    :param routing_key: The routing key to be sent with the message.

    Usage::

    >>> from utils import bind_queue_to_exchange
    >>> bind_queue_to_exchange('queue', 'exchange', 'routing_key')

    """
    with closing(amqp.Connection()) as connection:
        channel = __get_channel(connection)
        __bind_queue_to_exchange(channel, message, exchange, routing_key)
