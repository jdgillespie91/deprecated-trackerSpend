import amqp
import unittest
from utils import get_message


class GetMessageIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.queue = 'test_queue'
        self.connection = amqp.Connection()
        self.channel = self.connection.channel()
        self.channel.queue_declare(self.queue)

    def test_error_if_queue_does_not_exist(self):
        with self.assertRaises(amqp.exceptions.NotFound):
            get_message(queue='this_queue_does_not_exist')

    def test_error_if_no_queue_is_passed(self):
        with self.assertRaises(amqp.exceptions.NotFound):
            get_message()

    def test_returns_none_if_queue_exists_and_no_message_in_queue(self):
        self.assertIs(get_message(queue=self.queue), None)

    def test_returns_message_if_queue_exists_and_message_in_queue(self):
        self.channel.basic_publish(msg=amqp.Message('test_message'), routing_key=self.queue)
        self.assertIsInstance(get_message(queue=self.queue), amqp.basic_message.Message)

    def test_returned_message_has_correct_attributes(self):
        self.channel.basic_publish(msg=amqp.Message('test_message'), routing_key=self.queue)
        message = get_message(queue=self.queue)
        self.assertTrue(hasattr(message, 'body'))
        self.assertEqual(message.body, 'test_message')

    def skip_test_message_is_removed_from_queue_after_getting(self):
        pass

    def tearDown(self):
        self.channel.queue_delete(queue=self.queue)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(GetMessageIntegrationTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
