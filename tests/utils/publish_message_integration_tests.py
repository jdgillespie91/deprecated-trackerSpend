import amqp
import unittest
from utils import publish_message


class PublishMessageIntegrationTests(unittest.TestCase):
    def setUp(self):
        connection = amqp.Connection()
        self.channel = connection.channel()

        self.message_body = 'test_message'
        self.message = amqp.Message(self.message_body)
        self.exchange = 'test_exchange'
        self.type = 'direct'
        self.routing_key = 'test_routing_key'
        publish_message(self.message_body, self.exchange, self.type, self.routing_key)

    def test_test_exchange_is_declared(self):
        self.channel.exchange_declare(exchange=self.exchange, type=self.type, passive=True)

    def test_random_exchange_is_not_declared(self):
        with self.assertRaises(amqp.exceptions.NotFound):
            self.channel.exchange_declare(exchange='random_exchange', type=self.type, passive=True)

    def test_declared_exchange_is_durable(self):
        with self.assertRaises(amqp.exceptions.PreconditionFailed):
            self.channel.exchange_declare(exchange=self.exchange, type=self.type, durable=False)

    def test_declared_exchange_does_not_auto_delete(self):
        with self.assertRaises(amqp.exceptions.PreconditionFailed):
            self.channel.exchange_declare(exchange=self.exchange, type=self.type, auto_delete=True)

    def test_declared_exchange_is_correct_type(self):
        with self.assertRaises(amqp.exceptions.PreconditionFailed):
            self.channel.exchange_declare(exchange=self.exchange, type='fanout')

    def test_message_is_published_to_correct_exchange(self):
        self.channel.basic_publish_confirm(msg=self.message, exchange=self.exchange, routing_key=self.routing_key)

    def test_published_message_has_correct_routing_key(self):
        queue = 'test_queue'

        try:
            self.channel.queue_declare(queue=queue)
            self.channel.queue_bind(queue=queue, exchange=self.exchange, routing_key=self.routing_key)
            publish_message(self.message_body, self.exchange, self.type, self.routing_key)
            message = self.channel.basic_get(queue=queue)
        finally:
            self.channel.queue_delete(queue=queue)

        self.assertIsNotNone(message)
        self.assertTrue(hasattr(message, 'routing_key'))
        self.assertEqual(message.routing_key, 'test_routing_key')

    def test_message_does_not_publish_if_exchange_does_not_exist(self):
        with self.assertRaises(amqp.exceptions.NotFound):
            self.channel.basic_publish_confirm(msg=self.message, exchange='random_exchange', routing_key=self.routing_key)

    def tearDown(self):
        self.channel.exchange_delete(exchange=self.exchange)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(PublishMessageIntegrationTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
