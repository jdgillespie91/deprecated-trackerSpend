import ast
import configparser
import os
import pika
import smtplib
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

    def callback(self, ch, method, properties, body):
        print(' [x] Received {0}'.format(body))
        print(' [x] Sending email.')
        try:
            body = ast.literal_eval(body)
            self.send_email(body['to'], body['subject'], body['email_body'])
            print(' [x] Email sent.')
        except KeyError as e:
            print(' [e] The message is missing the following key: {'
                  '0}'.format(e.args))
        except Exception as e:
            print(' [e] An exception of type {0} occurred.'.format(type(
                e).__name__))
            print(' [e] Arguments: {0}'.format(e.args))
            print(' [e] Email not sent.')

    def send_email(self, recipient, subject, email_body):
        # Build email.
        email = MIMEMultipart()
        email['From'] = self.sender
        email['To'] = recipient
        email['Subject'] = subject
        body = email_body
        email.attach(MIMEText(body, 'plain'))

        # Send email.
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(self.username, self.password)
        server.sendmail(self.sender, recipient, email.as_string())
        server.close()

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
