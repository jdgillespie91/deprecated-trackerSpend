import amqp
import logging
from contextlib import closing


def publish_message(msg_body, exchange='', routing_key=''):
    """ Publish a message to an exchange with exchange type and routing key specified.

    A message is sent to a specified exchange with the provided routing_key. If the exchange doesn't exist, an exception is raised.

    :param msg_body: A string containing the body of the message to be sent.
    :param exchange (optional): The name of the exchange the message is sent to. If blank, the default exchange is used.
    :param routing_key (optional): The routing key to be sent with the message.

    Usage::

    >>> from utils import publish_message
    >>> publish_message('msg_body', exchange='exchange', routing_key='routing_key')

    """
    logger = logging.getLogger(__name__)
    logger.info('START {0}.'.format(__name__))

    with closing(amqp.Connection()) as connection:
        channel = connection.channel()

        # Raise an exception if the exchange doesn't exist.
        channel.exchange_declare(exchange=exchange, type='direct', passive=True)

        msg = amqp.Message(msg_body)
        channel.basic_publish(msg=msg, exchange=exchange, routing_key=routing_key)

    logger.info('END {0}.'.format(__name__))
