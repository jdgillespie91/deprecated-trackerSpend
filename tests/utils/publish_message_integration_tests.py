import amqp
import unittest
from utils import publish_message


class PublishMessageIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.exchange = 'test_exchange'
        self.type = 'direct'
        self.message = amqp.Message('test_message')
        self.exchange = 'test_exchange'
        self.routing_key = 'test_routing_key'
        self.connection = amqp.Connection()
        self.channel = self.connection.channel()
        self.channel.exchange_declare(self.exchange, self.type)

    def test_error_if_exchange_does_not_exist(self):
        with self.assertRaises(amqp.exceptions.NotFound):
            publish_message(message=self.message, exchange='this_exchange_does_not_exist', routing_key=self.routing_key)

    def test_no_error_if_no_exchange_and_no_routing_key_are_passed(self):
         publish_message(message=self.message)

    def skip_test_published_message_has_correct_routing_key(self):
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
