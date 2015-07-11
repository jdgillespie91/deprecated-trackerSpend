import amqp


def __get_channel(connection):
    return connection.channel()

def __declare_exchange(channel, exchange, type):
    channel.exchange_declare(exchange=exchange, type=type, durable=True, auto_delete=False)

def __publish_message_to_exchange(channel, message, exchange, routing_key):
    channel.basic_publish(message, exchange=exchange, routing_key=routing_key)

def publish_message(message, exchange, type, routing_key):
    """ Publish a message to an exchange with exchange type and routing key specified.

    TODO The message format is to be confirmed. The message is sent to an exchange of specified type with the provided routing key. The exchange is durable and is not automatically deleted when the last consumer detaches.

    :param message: The message to be sent.
    :param exchange: The name of the exchange the message should be sent to.
    :param routing_key: The routing key to be sent with the message.

    Usage::

    >>> from utils import publish_message
    >>> publish_message(message, 'exchange', 'type', 'routing_key')

    """
    with closing(amqp.Connection()) as connection:
        channel = __get_channel(connection)
        __declare_exchange(channel, exchange, type)
        __publish_message_to_exchange(channel, message, exchange, routing_key)
