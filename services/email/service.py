import ast
import configparser
import os
import pika
import smtplib
import sys
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


class Service():
    def __init__(self):
        self.sender, self.username, self.password = self.parse_config()

    def parse_config(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), "config.ini"))

        sender = config.get("service", "sender")
        username = config.get("service", "username")
        password = config.get("service", "password")

        return sender, username, password

    def parse_message(self, body):
        body = ast.literal_eval(body)
        recipient = body['to']
        subject = body['subject']
        email_body = body['email_body']

        return recipient, subject, email_body

    def callback(self, ch, method, properties, body):
        print(' [x] Received {0}'.format(body))
        print(' [x] Sending email.')
        try:
            recipient, subject, email_body = self.parse_message(body)
            self.send_email(recipient, subject, email_body)
            print(' [x] email sent.')
        except KeyError as e:
            print(' [e] The message is missing the following key: {'
                  '0}'.format(e.args))
        except Exception as e:
            print(' [e] An exception of type {0} occurred.'.format(type(
                e).__name__))
            print(' [e] Arguments: {0}'.format(e.args))
            print(' [e] email not sent.')


    def run(self):
        print('Starting service.')

        # Establish connection with RabbitMQ server.
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            'localhost'))
        channel = connection.channel()

        # Ensure queue exists.
        channel.queue_declare(queue='email_service')

        # Wait for messages.
        print(' [*] Waiting for messages. Press CTRL+C to exit.')

        channel.basic_consume(self.callback, queue='email_service', no_ack=True)
        channel.start_consuming()

        # Message should contain:
        # Recipient, subject, message body.
        # Service should send email according to these instructions.
        # Service should then wait for new message.
        # i.e. I think we need a subscribe to queue method that, on message,
        # sends the email. Do we want to send a message out? I don't think so.

    def send_email(self, recipient, subject, email_body):
        # Build email.
        email = MIMEMultipart()
        email['From'] = self.sender
        email['To'] = recipient
        email['Subject'] = subject
        body = email_body
        email.attach(MIMEText(body, 'plain'))

        # Send email.
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.sender, recipient, email.as_string())
            server.close()
        except Exception as e:
            print('Exception: {0}'.format(e))
