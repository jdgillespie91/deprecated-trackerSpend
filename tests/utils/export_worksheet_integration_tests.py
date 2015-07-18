import json
import os
import unittest
from utils import export_worksheet


class ExportWorksheetIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        auth_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'google_key.json')
        workbook_name = 'expenditure_responses'
        worksheet_name = 'entries'
        out_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'out_file.json')
        export_worksheet(auth_file, workbook_key, worksheet_name, out_file)

    def setUp(self):
        self.auth_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'google_key.json')
        self.workbook_name = 'expenditure_responses'
        self.worksheet_name = 'entries'
        self.out_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'out_file.json')

    def test_auth_file_exists_in_current_directory(self):
        self.assertTrue(os.path.isfile(self.auth_file))

    def test_out_file_exists_in_current_directory(self):
        self.assertTrue(os.path.isfile(self.out_file))

    def test_out_file_has_lines(self):
        with open(self.out_file) as f:
            self.assertTrue(f.readline())

    def test_out_file_is_list_when_loaded(self):
        with open(self.out_file) as f:
            self.assertTrue(isinstance(json.load(f), list))
        
    def test_out_file_is_list_of_dict_when_loaded(self):
        with open(self.out_file) as f:
            for item in json.load(f):
                self.assertTrue(isinstance(item, dict))

    @classmethod
    def tearDownClass(cls):
        out_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'out_file.json')
        os.remove(out_file)

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ExportWorksheetIntegrationTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
