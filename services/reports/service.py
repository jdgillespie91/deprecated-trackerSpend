"""
TODO Update this docstring
This service builds a report and send a message to the reports queue.

Subscribes to queue: reports_service.
Required attributes in message body: 

For example,

"{}"
"""

import ast
import os
import pika
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from configs import config


class Service():
    """ 
    TODO Make this useful.
    This is the Service class. 
    """
    def __init__(self):
        """ 
        TODO Make this useful.
        This is a method of Service.
        """
        self.config = config.Config('reports_service')

    def __callback(self, ch, method, properties, body):
        """ 
        TODO Make this useful.
        This is a method of Service.
        """
        print(' [x] Received {0}'.format(body))
        print(' [x] Building report.')
        try:
            body = ast.literal_eval(body)
            self.__build_report()
            print(' [x] Report built.')
            self.__send_message()
            print(' [x] Message sent.')
        except KeyError as e:
            print(' [e] The message is missing the following key: {'
                  '0}'.format(e.args))
        except Exception as e:
            print(' [e] An exception of type {0} occurred.'.format(type(
                e).__name__))
            print(' [e] Arguments: {0}'.format(e.args))

    def __build_report(self):
        """ 
        TODO Make this useful.
        This is a method of Service.
        """
        pass

    def __send_message(self):
        """
        TODO Make this useful.
        This is a method of Service.
        """
        pass

    def run(self):
        """ 
        TODO Make this useful.
        This is a method of Service.
        """
        print('Starting service.')

        # Establish connection with RabbitMQ server.
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            'localhost'))
        channel = connection.channel()

        # Ensure queue exists.
        channel.queue_declare(queue='reports_service')

        # Wait for messages.
        print(' [*] Waiting for messages. Press CTRL+C to exit.')

        channel.basic_consume(self.__callback, queue='reports_service',
                              no_ack=True)
        channel.start_consuming()


if __name__ == '__main__':
    service = Service()
    service.run()
