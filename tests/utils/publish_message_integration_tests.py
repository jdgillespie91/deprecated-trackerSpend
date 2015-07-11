import unittest
from utils import publish_message


class PublishMessageIntegrationTests(unittest.TestCase):
    def test_tests(self):
        self.assertTrue(True)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(PublishMessageIntegrationTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
