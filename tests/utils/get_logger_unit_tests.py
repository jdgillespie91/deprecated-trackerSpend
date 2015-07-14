import sys
import unittest
from contextlib import redirect_stdout
from io import StringIO
from logging import Logger
from utils import get_logger


class Capturing(list):  # http://stackoverflow.com/questions/16571150/how-to-capture-stdout-output-from-a-python-function-call
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        sys.stdout = self._stdout


class GetLoggerUnitTests(unittest.TestCase):
    def setUp(self):
        self.logger = get_logger('test')

    def test_get_logger_is_callable(self):
        self.assertTrue(callable(get_logger))

    def test_get_logger_returns_logger_object(self):
        self.assertIsInstance(self.logger, Logger)

    def test_logger_message_prints_to_stdout(self):
        with Capturing() as output:
            self.logger.debug('test')
        # Need to test that output contains the logger message (it doesn't at the moment but it should!).
        self.assertTrue(False)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(GetLoggerUnitTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
