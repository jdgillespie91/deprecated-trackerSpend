import unittest
from utils import publish_message


class PublishMessageIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        message = 'test_message'
        exchange = 'test_exchange'
        type = 'direct'
        routing_key = 'test_routing_key'
        publish_message(message, exchange, type, routing_key)

    def test_tests(self):
        self.assertTrue(True)

    def test_declared_exchange_is_durable(self):
        self.assertTrue(False)

    def test_declared_exchange_does_not_auto_delete(self):
        self.assertTrue(False)

    def test_message_is_published(self):
        self.assertTrue(False)

    def test_message_is_published_to_correct_exchange(self):
        self.assertTrue(False)

    def test_message_is_published_with_correct_routing_key(self):
        self.assertTrue(False)

    def test_connection_closes_if_exception_is_raised(self):
        self.assertTrue(False)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(PublishMessageIntegrationTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
