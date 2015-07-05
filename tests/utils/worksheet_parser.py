import unittest
from utils import parse_worksheet


class TestParseWorksheet(unittest.TestCase):
    def test_open_sheet_function_is_defined(self):
        if not hasattr(parse_worksheet, '__open_sheet'):
           self.fail('__open_sheet should be defined.') 

    def test_get_data_function_is_defined(self):
        if not hasattr(parse_worksheet, '__get_data'):
           self.fail('__get_data should be defined.') 

    def test_write_data_function_is_defined(self):
        if not hasattr(parse_worksheet, '__write_data'):
           self.fail('__write_data should be defined.') 


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestParseWorksheet)
    unittest.TextTestRunner(verbosity=2).run(suite)
