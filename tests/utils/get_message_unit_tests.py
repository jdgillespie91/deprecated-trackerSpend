import unittest
from utils import get_message

class GetMessageUnitTests(unittest.TestCase):
    def test_get_message_is_callable(self):
        self.assertTrue(callable(get_message))


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(GetMessageUnitTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
