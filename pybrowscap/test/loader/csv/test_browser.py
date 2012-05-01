import unittest
import os

from pybrowscap.loader.csv import load_file


BROWSCAP = load_file(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'browscap_22_06_2011.csv'))


class TestBrowserFirefox(unittest.TestCase):

    user_agent = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110628 Ubuntu/10.10 (maverick) Firefox/3.6.18'

    def setUp(self):
        self.browser = BROWSCAP.search(self.user_agent)

    def tearDown(self):
        self.browser = None

    def test_items(self):
        self.assertDictEqual(self.browser.items(),
                             {'cookies': True, 'javaapplets': True, 'parent': 'Firefox 3.6',
                              'activexcontrols': False, 'backgroundsounds': False, 'win64': False,
                              'banned': False, 'javascript': True, 'syndicationreader': False,
                              'beta': False, 'sortorder': '860', 'aolversion': 0.0, 'alpha': False,
                              'frames': True, 'cssversion': 0.0, 'crawler': False,
                              'masterparent': False, 'tables': True, 'iframes': True,
                              'minorversion': 6, 'internalid': '11277', 'mobiledevice': False,
                              'vbscript': False, 'win32': False, 'platform': 'Linux', 'version': 3.6,
                              'useragent': '[Mozilla/5.0 (X11; *; *Linux*; *; rv:1.9.2*) Gecko/* Firefox/3.6*]',
                              'browser': 'Firefox', 'win16': False, 'majorversion': 3})

    def test_get(self):
        self.assertEqual(self.browser.get('platform'), 'Linux')
        self.assertEqual(self.browser.get('parent'), 'Firefox 3.6')
        self.assertIsNone(self.browser.get('codescale'))
        self.assertEqual(self.browser.get('codescale', ''), '')

    def test_name(self):
        self.assertEqual(self.browser.name(), 'Firefox')

    def test_category(self):
        self.assertEqual(self.browser.category(), 'Firefox 3.6')

    def test_platform(self):
        self.assertEqual(self.browser.platform(), 'Linux')

    def test_aol_version(self):
        self.assertIsInstance(self.browser.aol_version(), float)
        self.assertEqual(self.browser.aol_version(), 0.0)

    def test_version(self):
        self.assertIsInstance(self.browser.version(), float)
        self.assertEqual(self.browser.version(), 3.6)

    def test_version_major(self):
        self.assertIsInstance(self.browser.version_major(), int)
        self.assertEqual(self.browser.version_major(), 3)

    def test_version_minor(self):
        self.assertIsInstance(self.browser.version_minor(), int)
        self.assertEqual(self.browser.version_minor(), 6)

    def test_css_version(self):
        self.assertIsInstance(self.browser.css_version(), float)
        self.assertEqual(self.browser.css_version(), 0.0)

    def test_supports(self):
        self.assertTrue(self.browser.supports('tables'))

    def test_supports_tables(self):
        self.assertTrue(self.browser.supports_tables())

    def test_supports_frames(self):
        self.assertTrue(self.browser.supports_frames())

    def test_supports_iframes(self):
        self.assertTrue(self.browser.supports_iframes())

    def test_supports_java(self):
        self.assertTrue(self.browser.supports_java())

    def test_supports_javascript(self):
        self.assertTrue(self.browser.supports_javascript())

    def test_supports_vbscript(self):
        self.assertFalse(self.browser.supports_vbscript())

    def test_supports_activex(self):
        self.assertFalse(self.browser.supports_activex())

    def test_supports_cookies(self):
        self.assertTrue(self.browser.supports_cookies())

    def test_supports_css(self):
        self.assertFalse(self.browser.supports_css())

    def test_is_crawler(self):
        self.assertFalse(self.browser.is_crawler())

    def test_is_mobile(self):
        self.assertFalse(self.browser.is_mobile())

    def test_is_syndication_reader(self):
        self.assertFalse(self.browser.is_syndication_reader())

    def test_is_banned(self):
        self.assertFalse(self.browser.is_banned())

    def test_is_alpha(self):
        self.assertFalse(self.browser.is_alpha())

    def test_is_beta(self):
        self.assertFalse(self.browser.is_beta())

    def test_features(self):
        self.assertListEqual(self.browser.features(), ['tables', 'frames', 'iframes', 'javascript', 'cookies', 'java'])



class BrowserGooglebotTest(unittest.TestCase):

    user_agent = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'

    def setUp(self):
        self.browser = BROWSCAP.search(self.user_agent)

    def tearDown(self):
        self.browser = None

    def test_items(self):
        self.assertDictEqual(self.browser.items(),
                             {'cookies': False, 'javaapplets': False, 'parent': 'Google',
                              'activexcontrols': False, 'backgroundsounds': False, 'win64': False,
                              'banned': False, 'javascript': False, 'syndicationreader': False,
                              'beta': False, 'sortorder': '100', 'aolversion': 0.0, 'alpha': False,
                              'frames': True, 'cssversion': 0.0, 'crawler': True, 'masterparent': False,
                              'tables': True, 'iframes': True, 'minorversion': 1,
                              'internalid': '4128', 'mobiledevice': False, 'vbscript': False,
                              'win32': False, 'platform': '', 'version': 2.1,
                              'useragent': '[*Googlebot/2.1*]', 'browser': 'Googlebot',
                              'win16': False, 'majorversion': 2})

    def test_get(self):
        self.assertEqual(self.browser.get('platform'), '')
        self.assertEqual(self.browser.get('parent'), 'Google')
        self.assertIsNone(self.browser.get('codescale'))
        self.assertEqual(self.browser.get('codescale', ''), '')

    def test_name(self):
        self.assertEqual(self.browser.name(), 'Googlebot')

    def test_category(self):
        self.assertEqual(self.browser.category(), 'Google')

    def test_platform(self):
        self.assertEqual(self.browser.platform(), '')

    def test_aol_version(self):
        self.assertIsInstance(self.browser.aol_version(), float)
        self.assertEqual(self.browser.aol_version(), 0)

    def test_version(self):
        self.assertIsInstance(self.browser.version(), float)
        self.assertEqual(self.browser.version(), 2.1)

    def test_version_major(self):
        self.assertIsInstance(self.browser.version_major(), int)
        self.assertEqual(self.browser.version_major(), 2)

    def test_version_minor(self):
        self.assertIsInstance(self.browser.version_minor(), int)
        self.assertEqual(self.browser.version_minor(), 1)

    def test_css_version(self):
        self.assertIsInstance(self.browser.css_version(), float)
        self.assertEqual(self.browser.css_version(), 0.0)

    def test_supports(self):
        self.assertTrue(self.browser.supports('tables'))

    def test_supports_tables(self):
        self.assertTrue(self.browser.supports_tables())

    def test_supports_frames(self):
        self.assertTrue(self.browser.supports_frames())

    def test_supports_iframes(self):
        self.assertTrue(self.browser.supports_iframes())

    def test_supports_java(self):
        self.assertFalse(self.browser.supports_java())

    def test_supports_javascript(self):
        self.assertFalse(self.browser.supports_javascript())

    def test_supports_vbscript(self):
        self.assertFalse(self.browser.supports_vbscript())

    def test_supports_activex(self):
        self.assertFalse(self.browser.supports_activex())

    def test_supports_cookies(self):
        self.assertFalse(self.browser.supports_cookies())

    def test_supports_css(self):
        self.assertFalse(self.browser.supports_css())

    def test_is_crawler(self):
        self.assertTrue(self.browser.is_crawler())

    def test_is_mobile(self):
        self.assertFalse(self.browser.is_mobile())

    def test_is_syndication_reader(self):
        self.assertFalse(self.browser.is_syndication_reader())

    def test_is_banned(self):
        self.assertFalse(self.browser.is_banned())

    def test_is_alpha(self):
        self.assertFalse(self.browser.is_alpha())

    def test_is_beta(self):
        self.assertFalse(self.browser.is_beta())

    def test_features(self):
        self.assertEqual(self.browser.features(), ['tables', 'frames', 'iframes'])

if __name__ == '__main__':
    unittest.main()