import unittest
from pybrowscap.loader.csv import load_file
from pybrowscap.loader import Browscap, TYPE_CSV
from datetime import datetime
import os

class LoaderTest(unittest.TestCase):

    browscap_file1 = os.path.dirname(__file__)+os.sep+'data'+os.sep+'browscap_22_06_2011.csv'
    browscap_file2 = os.path.dirname(__file__)+os.sep+'data'+os.sep+'browscap_07_10_2011.csv'

    def test_load_csv_browscap(self):
        browscap = load_file(self.browscap_file1)
        self.assertTrue(isinstance(browscap, Browscap))
        self.assertEqual(browscap.browscap_file_path, self.browscap_file1)
        self.assertEqual(browscap.type, TYPE_CSV)
        self.assertGreaterEqual(datetime.now(), browscap.loaded_at)
        self.assertTrue(browscap.reloaded_at is None)
        self.assertEqual(len(browscap.data), 3814)
        self.assertEqual(len(browscap.regex_cache), 3816)

    def test_reload_original_csv_browscap_file(self):
        browscap = load_file(self.browscap_file1)
        self.assertEqual(len(browscap.data), 3814)
        self.assertEqual(len(browscap.regex_cache), 3816)
        browscap.reload()
        self.assertEqual(len(browscap.data), 3814)
        self.assertEqual(len(browscap.regex_cache), 3816)

    def test_reload_new_csv_browscap_file(self):
        browscap = load_file(self.browscap_file1)
        self.assertEqual(len(browscap.data), 3814)
        self.assertEqual(len(browscap.regex_cache), 3816)
        browscap.reload(self.browscap_file2)
        self.assertEqual(len(browscap.data), 4078)
        self.assertEqual(len(browscap.regex_cache), 4239)

    def test_load_browscap_no_file(self):
        self.assertRaises(Exception, load_file, ('www.codescale.net'))

if __name__ == '__main__':
    unittest.main()
  