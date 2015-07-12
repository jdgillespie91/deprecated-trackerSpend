import unittest
from utils import export_worksheet

class ExportWorksheetUnitTests(unittest.TestCase):
    def test_export_worksheet_is_callable(self):
        self.assertTrue(callable(export_worksheet))


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ExportWorksheetUnitTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
