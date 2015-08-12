import unittest
from utils import declare_queue


class DeclareQueueUnitTests(unittest.TestCase):
    def test_declare_queue_is_callable(self):
        self.assertTrue(callable(declare_queue))


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(DeclareQueueUnitTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
