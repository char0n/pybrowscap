import unittest
import os
from datetime import datetime

from pybrowscap.loader.csv import load_file
from pybrowscap.loader import Browscap, TYPE_CSV


class LoaderTest(unittest.TestCase):

    browscap_file1 = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'browscap_22_06_2011.csv')
    browscap_file2 = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'browscap_07_10_2011.csv')

    def test_load_csv_browscap(self):
        browscap = load_file(self.browscap_file1)
        self.assertIsInstance(browscap, Browscap)
        self.assertEqual(browscap.browscap_file_path, self.browscap_file1)
        self.assertEqual(browscap.type, TYPE_CSV)
        self.assertGreaterEqual(datetime.now(), browscap.loaded_at)
        self.assertIsNone(browscap.reloaded_at)
        self.assertEqual(len(browscap.data), 2)
        self.assertEqual(len(browscap.regex_cache), 2)
        self.assertEqual(browscap.version, 4856)
        self.assertEqual(browscap.release_date, datetime.strptime('Wed, 22 Jun 2011 23:26:51', '%a, %d %b %Y %H:%M:%S'))

    def test_reload_original_csv_browscap_file(self):
        browscap = load_file(self.browscap_file1)
        self.assertEqual(len(browscap.data), 2)
        self.assertEqual(len(browscap.regex_cache), 2)
        self.assertEqual(browscap.version, 4856)
        self.assertEqual(browscap.release_date, datetime.strptime('Wed, 22 Jun 2011 23:26:51', '%a, %d %b %Y %H:%M:%S'))
        browscap.reload()
        self.assertEqual(len(browscap.data), 2)
        self.assertEqual(len(browscap.regex_cache), 2)
        self.assertEqual(browscap.version, 4856)
        self.assertEqual(browscap.release_date, datetime.strptime('Wed, 22 Jun 2011 23:26:51', '%a, %d %b %Y %H:%M:%S'))

    def test_reload_new_csv_browscap_file(self):
        browscap = load_file(self.browscap_file1)
        self.assertEqual(len(browscap.data), 2)
        self.assertEqual(len(browscap.regex_cache), 2)
        self.assertEqual(browscap.version, 4856)
        self.assertEqual(browscap.release_date, datetime.strptime('Wed, 22 Jun 2011 23:26:51', '%a, %d %b %Y %H:%M:%S'))
        browscap.reload(self.browscap_file2)
        self.assertEqual(len(browscap.data), 2)
        self.assertEqual(len(browscap.regex_cache), 2)
        self.assertEqual(browscap.version, 4862)
        self.assertEqual(browscap.release_date, datetime.strptime('Fri, 07 Oct 2011 06:46:46', '%a, %d %b %Y %H:%M:%S'))


    def test_load_browscap_no_file(self):
        self.assertRaises(Exception, load_file, ('www.codescale.net'))

if __name__ == '__main__':
    unittest.main()