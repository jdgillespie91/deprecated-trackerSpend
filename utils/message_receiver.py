import amqp
from time import sleep


def callback(message):
    print(" [x] Received '{0}'. Sleeping...".format(message.body))
    sleep(10)


connection = amqp.Connection()
channel = connection.channel()
channel.queue_declare(queue='hello')

channel.basic_consume(queue='hello', no_ack=True, callback=callback)
print(' [x] Waiting for messages. To exit, press CTRL+c.')
while True:
    channel.wait()
