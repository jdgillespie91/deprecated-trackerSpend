import amqp
import unittest
from utils import get_message


class GetMessageIntegrationTests(unittest.TestCase):
    def setUp(self):
        connection = amqp.Connection()
        self.channel = connection.channel()

        self.queue = 'test_queue'
        get_message(self.queue)

    def test_test_queue_is_declared(self):
        self.channel.queue_declare(queue=self.queue, passive=True)

    def test_random_queue_is_not_declared(self):
        with self.assertRaises(amqp.exceptions.NotFound):
            self.channel.queue_declare(queue='random_queue', passive=True)

    def test_declared_queue_is_durable(self):
        with self.assertRaises(amqp.exceptions.PreconditionFailed):
            self.channel.queue_declare(queue=self.queue, durable=False)

    def test_declared_queue_does_not_auto_delete(self):
        with self.assertRaises(amqp.exceptions.PreconditionFailed):
            self.channel.queue_declare(queue=self.queue, auto_delete=True)

    def test_message_is_retrieved_if_message_exists_in_queue(self):
        exchange = 'test_exchange'
        type = 'fanout'
        queue = 'local_test_queue'
        message = amqp.Message('test_message')

        try:
            self.channel.exchange_declare(exchange=exchange, type=type, durable=True, auto_delete=False)
            self.channel.queue_declare(queue=queue, durable=True, auto_delete=False)
            self.channel.queue_bind(queue=queue, exchange=exchange)
            self.channel.basic_publish_confirm(msg=message, exchange=exchange, routing_key='')
            message = get_message(queue)
        finally:
            self.channel.queue_delete(queue=queue)
            self.channel.exchange_delete(exchange=exchange)

        self.assertIsNotNone(message)
        self.assertTrue(hasattr(message, 'body'))
        self.assertEqual(message.body, 'test_message')

    def tearDown(self):
        self.channel.queue_delete(queue=self.queue)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(GetMessageIntegrationTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
