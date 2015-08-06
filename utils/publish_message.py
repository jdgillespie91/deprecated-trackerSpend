import amqp
from contextlib import closing


def publish_message(message_body, exchange, type, routing_key):
    """ Publish a message to an exchange with exchange type and routing key specified.

    A message is sent to a specified exchange with the provided routing_key.

    :param message_body: The body of the message to be sent.
    :param exchange: The name of the exchange the message is sent to.
    :param routing_key: The routing key to be sent with the message.

    Usage::

    >>> from utils import publish_message
    >>> publish_message('message', 'exchange', 'routing_key')

    """
    with closing(amqp.Connection()) as connection:
        channel = connection.channel()
        msg = amqp.Message(message)
        channel.basic_publish_confirm(msg=msg, exchange=exchange, routing_key=routing_key)
