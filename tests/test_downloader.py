import unittest
from pybrowscap.loader import Downloader
import os

class DownloaderTest(unittest.TestCase):

    original_url = None

    def setUp(self):
        self.original_url  = Downloader.url
        Downloader.url     = 'http://www.codescale.net/en/'
        self.downloader    = Downloader()
        self.new_file_path = os.getcwd()+os.sep+'browscap.csv'

    def tearDown(self):
        Downloader.url    = self.original_url
        self.original_url = None
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