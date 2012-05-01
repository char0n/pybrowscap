import os
import unittest
import urllib2

from pybrowscap.loader import Downloader


class DownloaderTest(unittest.TestCase):

    def setUp(self):
        self.url = 'http://www.codescale.net/en/'
        self.downloader = Downloader(self.url)
        self.new_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'tmp'+'browscap_22_06_2011.csv')

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

    def test_download_no_url(self):
        with self.assertRaises(ValueError):
            self.downloader.url = ''
            self.downloader.get()

    def test_download_invalid_url(self):
        with self.assertRaises(urllib2.URLError):
            self.downloader.url = 'http://test'
            self.downloader.get()

    def test_download_invalid_proxy(self):
        with self.assertRaises(urllib2.URLError):
            self.downloader.proxy = 'http://test'
            self.downloader.get()

    def test_download_timeout_error(self):
        with self.assertRaises(urllib2.URLError):
            self.downloader.timeout = 0
            self.downloader.get()

    def test_download_http_error(self):
        with self.assertRaises(urllib2.HTTPError):
            self.downloader.url += 'a' * 4
            self.downloader.get()


if __name__ == '__main__':
    unittest.main()