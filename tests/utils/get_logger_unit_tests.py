import io
import unittest
from contextlib import redirect_stdout
from logging import Logger
from utils import get_logger


class GetLoggerUnitTests(unittest.TestCase):
    def setUp(self):
        self.logger = get_logger('test')

    def test_get_logger_is_callable(self):
        self.assertTrue(callable(get_logger))

    def test_get_logger_returns_logger_object(self):
        self.assertIsInstance(self.logger, Logger)

    def test_logger_message_returns_None_type(self):
        self.assertIsNone(self.logger.debug('test'))
        self.assertIsNone(self.logger.info('test'))
        self.assertIsNone(self.logger.warning('test'))
        self.assertIsNone(self.logger.error('test'))
        self.assertIsNone(self.logger.critical('test'))

    def skip_test_logger_message_prints_to_stdout(self):
        pass


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(GetLoggerUnitTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
