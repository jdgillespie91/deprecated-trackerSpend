"""
This service sends an email from trackerspend@gmail.com.

Subscribes to queue: email_service.
Required attributes in message body: to, subject, email_body.

For example,

"{'to': 'jdgillespie91@gmail', 'subject': 'Hello, world', 'email_body': 'Hello
to you too.'}"
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
        self.config = config.Config('email_service')

    def __callback(self, ch, method, properties, body):
        """ 
        TODO Make this useful.
        This is a method of Service.
        """
        print(' [x] Received {0}'.format(body))
        print(' [x] Sending email.')
        try:
            body = ast.literal_eval(body)
            self.__send_email(body['to'], body['subject'], body['email_body'], body['attachment_path'])
            print(' [x] Email sent.')
        except KeyError as e:
            print(' [e] The message is missing the following key: {'
                  '0}'.format(e.args))
        except Exception as e:
            print(' [e] An exception of type {0} occurred.'.format(type(
                e).__name__))
            print(' [e] Arguments: {0}'.format(e.args))
            print(' [e] Email not sent.')

    def __send_email(self, recipient, subject, email_body, attachment_path):
        """ 
        TODO Make this useful.
        This is a method of Service.
        """
        # Build email.
        email = MIMEMultipart()
        email['From'] = self.config.sender
        email['To'] = recipient
        email['Subject'] = subject
        if attachment_path:
            # TODO add attachment to email.
            pass
        body = email_body
        email.attach(MIMEText(body, 'plain'))

        # Send email.
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(self.config.username, self.config.password)
        server.sendmail(self.config.sender, recipient, email.as_string())
        server.close()

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
        channel.queue_declare(queue='email_service')

        # Wait for messages.
        print(' [*] Waiting for messages. Press CTRL+C to exit.')

        channel.basic_consume(self.__callback, queue='email_service',
                              no_ack=True)
        channel.start_consuming()


if __name__ == '__main__':
    service = Service()
    service.run()
