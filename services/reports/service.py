"""
TODO Update this docstring
This service builds a report and send a message to the reports queue.

Subscribes to queue: reports_service.
Required attributes in message body: 

For example,

"{}"
"""

import ast
import datetime
import os
import pika
import psycopg2
from configs import config
from utils import message_producer


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
            view = 'net_expenditure_category_month'  # TODO Replace this with a message attribute.
            report_path = self.__build_report_from_view(view)
            print(' [x] Report built.')
            self.__send_message(report_path)
            print(' [x] Message sent.')
        except KeyError as e:
            print(' [e] The message is missing the following key: {'
                  '0}'.format(e.args))
        except Exception as e:
            print(' [e] An exception of type {0} occurred.'.format(type(
                e).__name__))
            print(' [e] Arguments: {0}'.format(e.args))

    def __build_report_from_view(self, view):
        """ 
        TODO Make this useful.
        This is a method of Service.
        """
        pass
        # Set up directory.
        report_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'reports')
        if not os.path.isdir(report_dir):
            os.makedirs(report_dir)
        report_path = os.path.join(report_dir, 'report_{0}.csv'.format(datetime.datetime.today().strftime("%Y-%m-%d_%H:%M:%S")))

        # Get data from Postgres.
        select_query = """
            SELECT *
            FROM {0}
            ;
        """.format(view)

        report_query = """
            COPY ({0}) TO '{1}' DELIMITER ',' CSV HEADER;
        """.format(select_query, report_path)

        con = None
        database = 'postgres'
        user = 'postgres'

        con = psycopg2.connect(database=database, user=user)
        cur = con.cursor()
        cur.execute(report_query)
        con.commit()
        if con:
            con.close()

        return report_path

    def __send_message(self, report_path):
        """
        TODO Make this useful.
        This is a method of Service.
        """
        queue = 'email_service'
        body_dict = {'to': 'jdgillespie91@gmail.com', 'subject': 'Report',
                     'email_body': 'Your report will be attached.',
                     'attachment_path': report_path}
        body = str(body_dict)
        message_producer.send_message(queue, body)

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
        print(' [x] Waiting for messages. Press CTRL+C to exit.')

        channel.basic_consume(self.__callback, queue='reports_service',
                              no_ack=True)
        channel.start_consuming()


if __name__ == '__main__':
    service = Service()
    service.run()
