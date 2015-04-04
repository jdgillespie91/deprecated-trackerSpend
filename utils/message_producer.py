import argparse
import pika


def send_message(queue, body=None):
    """
    Sends a message to the specified queue with specified body if applicable.

    :param queue: Name of queue.
    :type queue: str
    :param body: Content of message body in the form "{'key': 'value'}".
    :type body: str
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue=queue)

    channel.basic_publish(exchange='', routing_key=queue, body=body)
    print(" [x] Message sent.")
    print(" Queue: {0}".format(queue))
    print(" Body: {0}".format(body))

    connection.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send a message to the '
                                                 'specified queue.')
    parser.add_argument('-q', '--queue', required=True,
                        help='The destination of the message')
    parser.add_argument('-b', '--body', help='The message body, if applicable.')
    args = parser.parse_args()

    send_message(args.queue, args.body)