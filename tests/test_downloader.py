import unittest
from pybrowscap.loader import Downloader
import os

class DownloaderTest(unittest.TestCase):

    def setUp(self):
        self.downloader    = Downloader('http://www.codescale.net/en/')
        self.new_file_path = os.path.dirname(__file__)+os.sep+'data'+os.sep+'tmp'+'browscap_22_06_2011.csv'

    def tearDown(self):
        if os.path.exists(self.new_file_path):
            os.remove(self.new_file_path)

    def test_download_save_to_file(self):
        self.downloader.get(self.new_file_path)
        self.assertTrue(os.path.exists(self.new_file_path))
        self.assertTrue(os.path.isfile(self.new_file_path))

    def test_downloaded_file_content(self):
        self.downloader.get(self.new_file_path)
        with open(self.new_file_path, 'rb') as fp:
            contents = fp.read()
        self.assertNotEqual(contents.find('Software Development Done Right'), -1)

    def test_download_get_contents(self):
        contents = self.downloader.get()
        self.assertNotEqual(contents.find('Software Development Done Right'), -1)

if __name__ == '__main__':
    unittest.main()