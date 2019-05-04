import unittest
import os

from pybrowscap.loader.csv import load_file


BROWSCAP = load_file(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'browscap_29_11_2018.csv'))


class TestBrowserFirefox(unittest.TestCase):

    user_agent = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110628 Ubuntu/10.10 (maverick) Firefox/3.6.18'

    def setUp(self):
        self.browser = BROWSCAP.search(self.user_agent)

    def tearDown(self):
        self.browser = None

    def test_items(self):

        self.assertDictEqual(self.browser.items(),
                             {'tables': True, 'iframes': True, 'browser_bits': '32', 'beta': False, 'issyndicationreader': False,
                             'istablet': False, 'device_name': 'Linux Desktop', 'device_maker': '',
                             'platform_maker': 'Canonical Foundation', 'parent': 'Firefox 3.6',
                             'renderingengine_description':
                             'For Firefox, Camino, K-Meleon, SeaMonkey, Netscape, and other Gecko-based browsers.',
                             'renderingengine_name': 'Gecko', 'majorver': 3, 'javascript': True, 'cookies': True,
                             'browser_maker': 'Mozilla Foundation', 'device_code_name': 'Linux Desktop', 'win64': False,
                             'javaapplets': True, 'isanonymized': False, 'platform_description': 'Ubuntu Linux', 'version': 3.6,
                             'renderingengine_version': 0.0, 'platform_version': 10.1, 'alpha': False, 'frames': True,
                             'masterparent': False, 'win16': False, 'browser': 'Firefox', 'vbscript': False, 'cssversion': 3.0,
                             'comment': 'Firefox 3.6', 'backgroundsounds': False, 'platform': 'Ubuntu', 'device_type': 'Desktop',
                             'propertyname': 'Mozilla/5.0 (*Linux i686*) Gecko*Ubuntu/10.10* Firefox/3.6*', 'browser_type': 'Browser',
                             'ismodified': False, 'isfake': False, 'aolversion': 0.0, 'ismobiledevice': False, 'minorver': 6,
                             'browser_modus': '', 'win32': False, 'litemode': False, 'device_brand_name': '',
                             'device_pointing_method': 'mouse', 'activexcontrols': False, 'platform_bits': '32',
                             'crawler': False, 'renderingengine_maker': 'Mozilla Foundation'})

    def test_get(self):
        self.assertEqual(self.browser.get('platform'), 'Ubuntu')
        self.assertEqual(self.browser.get('parent'), 'Firefox 3.6')
        self.assertIsNone(self.browser.get('codescale'))
        self.assertEqual(self.browser.get('codescale', ''), '')

    def test_name(self):
        self.assertEqual(self.browser.name(), 'Firefox')

    def test_category(self):
        self.assertEqual(self.browser.category(), 'Firefox 3.6')

    def test_platform(self):
        self.assertEqual(self.browser.platform(), 'Ubuntu')

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
        self.assertEqual(self.browser.css_version(), 3.0)

    def test_rendering_engine_name(self):
        self.assertEqual(self.browser.rendering_engine_name(), 'Gecko')

    def test_rendering_engine_version(self):
        self.assertIsInstance(self.browser.rendering_engine_version(), float)
        self.assertEqual(self.browser.rendering_engine_version(), 0.0)

    def test_device_maker(self):
        self.assertEqual(self.browser.device_maker(), '')

    def test_device_name(self):
        self.assertEqual(self.browser.device_name(), 'Linux Desktop')

    def test_platform_description(self):
        self.assertEqual(self.browser.platform_description(), 'Ubuntu Linux')

    def test_platform_version(self):
        self.assertIsInstance(self.browser.platform_version(), float)
        self.assertEqual(self.browser.platform_version(), 10.1)

    def test_litemode(self):
        self.assertFalse(self.browser.litemode())

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
        self.assertTrue(self.browser.supports_css())

    def test_is_crawler(self):
        self.assertFalse(self.browser.is_crawler())

    def test_is_mobile(self):
        self.assertFalse(self.browser.is_mobile())

    def test_is_syndication_reader(self):
        self.assertFalse(self.browser.is_syndication_reader())

    def test_is_banned(self):
        self.assertIsNone(self.browser.is_banned())

    def test_is_alpha(self):
        self.assertFalse(self.browser.is_alpha())

    def test_is_beta(self):
        self.assertFalse(self.browser.is_beta())

    def test_features(self):
        self.assertListEqual(self.browser.features(), ['tables', 'frames', 'iframes', 'javascript', 'cookies', 'java', 'css1', 'css2', 'css3'])



class BrowserGooglebotTest(unittest.TestCase):

    user_agent = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'

    def setUp(self):
        self.browser = BROWSCAP.search(self.user_agent)

    def tearDown(self):
        self.browser = None

    def test_items(self):
        self.assertDictEqual(self.browser.items(),
                             {'tables': False, 'iframes': False, 'browser_bits': '0', 'beta': False,
                             'issyndicationreader': False, 'istablet': False, 'device_name': '',
                             'device_maker': '', 'platform_maker': '', 'parent': 'Googlebot 2.1',
                             'renderingengine_description': '', 'renderingengine_name': '',
                             'majorver': 2, 'javascript': False, 'cookies': False,
                             'browser_maker': 'Google Inc', 'device_code_name': '', 'win64': False,
                             'javaapplets': False, 'isanonymized': False, 'platform_description': '',
                             'version': 2.1, 'renderingengine_version': 0.0, 'platform_version': 0.0,
                             'alpha': False, 'frames': False, 'masterparent': False, 'win16': False,
                             'browser': 'Google Bot', 'vbscript': False, 'cssversion': 0.0,
                             'comment': 'Googlebot 2.1', 'backgroundsounds': False, 'platform': '',
                             'device_type': '', 'propertyname': 'Mozilla/5.0 (compatible; Googlebot/2.1*',
                             'browser_type': 'Bot/Crawler', 'ismodified': False, 'isfake': False,
                             'aolversion': 0.0, 'ismobiledevice': False, 'minorver': 1,
                             'browser_modus': '', 'win32': False, 'litemode': False,
                             'device_brand_name': '', 'device_pointing_method': '',
                             'activexcontrols': False, 'platform_bits': '0', 'crawler': True,
                             'renderingengine_maker': ''})

    def test_get(self):
        self.assertEqual(self.browser.get('platform'), '')
        self.assertEqual(self.browser.get('parent'), 'Googlebot 2.1')
        self.assertIsNone(self.browser.get('codescale'))
        self.assertEqual(self.browser.get('codescale', ''), '')

    def test_name(self):
        self.assertEqual(self.browser.name(), 'Google Bot')

    def test_category(self):
        self.assertEqual(self.browser.category(), 'Googlebot 2.1')

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

    def test_rendering_engine_name(self):
        self.assertEqual(self.browser.rendering_engine_name(), '')

    def test_rendering_engine_version(self):
        self.assertIsInstance(self.browser.rendering_engine_version(), float)
        self.assertEqual(self.browser.rendering_engine_version(), 0.0)

    def test_device_maker(self):
        self.assertEqual(self.browser.device_maker(), '')

    def test_device_name(self):
        self.assertEqual(self.browser.device_name(), '')

    def test_platform_description(self):
        self.assertEqual(self.browser.platform_description(), '')

    def test_platform_version(self):
        self.assertIsInstance(self.browser.platform_version(), float)
        self.assertEqual(self.browser.platform_version(), 0.0)

    def test_litemode(self):
        self.assertFalse(self.browser.litemode())

    def test_supports(self):
        self.assertFalse(self.browser.supports('tables'))

    def test_supports_tables(self):
        self.assertFalse(self.browser.supports_tables())

    def test_supports_frames(self):
        self.assertFalse(self.browser.supports_frames())

    def test_supports_iframes(self):
        self.assertFalse(self.browser.supports_iframes())

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
        self.assertIsNone(self.browser.is_banned())

    def test_is_alpha(self):
        self.assertFalse(self.browser.is_alpha())

    def test_is_beta(self):
        self.assertFalse(self.browser.is_beta())

    def test_features(self):
        self.assertEqual(self.browser.features(), [])

if __name__ == '__main__':
    unittest.main()