import unittest
from utils import publish_message


class PublishMessageUnitTests(unittest.TestCase):
    def test_publish_message_is_callable(self):
        self.assertTrue(callable(publish_message))


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(PublishMessageUnitTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
