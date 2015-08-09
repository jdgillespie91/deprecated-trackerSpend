import amqp
import unittest
from utils import publish_message


class PublishMessageIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.exchange = 'test_exchange'
        self.type = 'direct'
        self.msg_body = 'test_message'
        self.routing_key = 'test_routing_key'
        self.connection = amqp.Connection()
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange, type=self.type)

    def test_error_is_raised_if_exchange_does_not_exist(self):
        with self.assertRaises(amqp.exceptions.NotFound):
            publish_message(msg_body=self.msg_body, exchange='does_not_exist', routing_key=self.routing_key)

    def test_none_is_returned_if_exchange_exists(self):
        resp = publish_message(msg_body=self.msg_body, exchange=self.exchange, routing_key=self.routing_key)
        self.assertIs(resp, None)

    def tearDown(self):
        self.channel.exchange_delete(exchange=self.exchange)
        self.channel.close()
        self.connection.close()


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(PublishMessageIntegrationTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
