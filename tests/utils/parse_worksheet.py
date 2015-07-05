import unittest
from utils import parse_worksheet
from gspread import Spreadsheet


class TestParseWorksheet(unittest.TestCase):
    def test_open_worksheet_function_is_defined(self):
        if not hasattr(parse_worksheet, '__open_worksheet'):
           self.fail('__open_sheet should be defined.')

    def test_get_data_function_is_defined(self):
        if not hasattr(parse_worksheet, '__get_data'):
           self.fail('__get_data should be defined.')

    def test_write_data_function_is_defined(self):
        if not hasattr(parse_worksheet, '__write_data'):
           self.fail('__write_data should be defined.')

    def test_parse_worksheet_function_is_defined(self):
        if not hasattr(parse_worksheet, '__parse_worksheet'):
           self.fail('__parse_worksheet should be defined.')


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestParseWorksheet)
    unittest.TextTestRunner(verbosity=2).run(suite)
