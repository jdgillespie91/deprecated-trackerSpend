import amqp
import unittest
from utils import get_message


class GetMessageIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.queue = 'test_queue'
        self.msg = amqp.Message('test_message')
        self.connection = amqp.Connection()
        self.channel = self.connection.channel()
        self.channel.queue_declare(self.queue)

    def test_error_is_raised_if_queue_does_not_exist(self):
        with self.assertRaises(amqp.exceptions.NotFound):
            get_message(queue='does_not_exist')

    def test_none_is_returned_if_queue_exists_and_no_message_exists(self):
        self.assertIs(get_message(queue=self.queue), None)

    def test_message_is_returned_if_queue_exists_and_message_exists(self):
        self.channel.basic_publish(msg=self.msg, routing_key=self.queue)
        self.assertIsInstance(get_message(queue=self.queue), amqp.basic_message.Message)

    def tearDown(self):
        self.channel.queue_delete(queue=self.queue)
        self.channel.close()
        self.connection.close()


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(GetMessageIntegrationTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
