import pika


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print(" [x] Received {0}".format(body))

channel.basic_consume(callback, queue='hello', no_ack=True)

print(" [*] Waiting for messages. To exit, press CTRL+c.")
channel.start_consuming()
