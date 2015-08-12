import amqp
import unittest
from utils import declare_queue


class DeclareQueueIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.queue = 'test_queue'
        self.connection = amqp.Connection()
        self.channel = self.connection.channel()
        declare_queue(queue=self.queue)

    def test_queue_is_declared(self):
        self.channel.queue_declare(queue=self.queue, passive=True)

    def test_error_is_raised_if_queue_is_durable(self):
        with self.assertRaises(amqp.exceptions.PreconditionFailed):
            self.channel.queue_declare(queue=self.queue, durable=True)

    def test_error_is_raised_if_queue_is_exclusive(self):
        with self.assertRaises(amqp.exceptions.ResourceLocked):
            self.channel.queue_declare(queue=self.queue, exclusive=True)

    def test_error_is_raised_if_queue_is_not_auto_deleting(self):
        with self.assertRaises(amqp.exceptions.PreconditionFailed):
            self.channel.queue_declare(queue=self.queue, auto_delete=False)

    def test_none_is_returned_if_queue_with_same_properties_exists(self):
        self.assertIs(declare_queue(queue=self.queue), None)

    def tearDown(self):
        self.channel.queue_delete(queue=self.queue)
        self.channel.close()
        self.connection.close()


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(DeclareQueueIntegrationTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
