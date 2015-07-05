import unittest
from unittest.mock import patch
from utils import parse_worksheet


class TestParseWorksheet(unittest.TestCase):
    def test_open_worksheet_function_is_defined(self):
        if not hasattr(parse_worksheet, '__open_worksheet'):
           self.fail('__open_worksheet should be defined.')

    def test_get_data_function_is_defined(self):
        if not hasattr(parse_worksheet, '__get_data'):
           self.fail('__get_data should be defined.')

    def test_write_data_function_is_defined(self):
        if not hasattr(parse_worksheet, '__write_data'):
           self.fail('__write_data should be defined.')

    def test_parse_worksheet_function_is_defined(self):
        if not hasattr(parse_worksheet, 'parse_worksheet'):
           self.fail('parse_worksheet should be defined.')


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestParseWorksheet)
    unittest.TextTestRunner(verbosity=2).run(suite)
