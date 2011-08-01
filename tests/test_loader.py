import unittest
from pybrowscap.loader import load_file, Browscap
import os

class LoaderTest(unittest.TestCase):

    browscap_file = os.path.dirname(__file__)+os.sep+'data'+os.sep+'browscap.csv'

    def test_load_browscap(self):
        browscap = load_file(self.browscap_file)
        self.assertTrue(isinstance(browscap, Browscap))

    def test_load_browscap_no_file(self):
        self.assertRaises(Exception, load_file, ('www.codescale.net'))

if __name__ == '__main__':
    unittest.main()
  