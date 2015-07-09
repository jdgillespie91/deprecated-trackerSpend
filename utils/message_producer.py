import amqp
from time import sleep


def callback(message):
    print(" [x] Received '{0}'. Sleeping...".format(message.body))
    sleep(10)


connection = amqp.Connection()
channel = connection.channel()
channel.queue_declare(queue='hello')

message = amqp.Message('Hello, world!')
channel.basic_publish(message, exchange='', routing_key='hello')
print(' [x] Sent: {0}'.format(message.body))

connection.close()
