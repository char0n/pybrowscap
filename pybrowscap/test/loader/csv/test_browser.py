import unittest
import os

from pybrowscap.loader.csv import load_file


BROWSCAP = load_file(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'browscap_14_05_2012.csv'))


class TestBrowserFirefox(unittest.TestCase):

    user_agent = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.18) Gecko/20110628 Ubuntu/10.10 (maverick) Firefox/3.6.18'

    def setUp(self):
        self.browser = BROWSCAP.search(self.user_agent)

    def tearDown(self):
        self.browser = None

    def test_items(self):

        self.assertDictEqual(self.browser.items(),
                             {'cookies': True, 'activexcontrols': False, 'aolversion': 0.0, 'frames': True,
                              'cssversion': 0.0, 'majorver': 3, 'tables': True, 'iframes': True, 'vbscript': False,
                              'comments': 'Firefox 3.6', 'platform_version': 0.0, 'platform': 'Linux', 'version': 3.6,
                              'masterparent': False, 'renderingengine_version': 0.0, 'javaapplets': True,
                              'parent': 'Firefox 3.6', 'backgroundsounds': False, 'win64': False,
                              'propertyname': 'Mozilla/5.0 (X11; *; *Linux*; *; rv:1.9.2*) Gecko/* Firefox/3.6*',
                              'javascript': True, 'beta': False, 'alpha': False,
                              'renderingengine_description': 'For Firefox, Camino, K-Meleon, SeaMonkey, Netscape, and other Gecko-based browsers.',
                              'crawler': False, 'renderingengine_name': 'Gecko', 'device_maker': '',
                              'platform_description': '', 'minorver': 6, 'issyndicationreader': False,
                              'device_name': '', 'win32': False, 'ismobiledevice': False, 'litemode': True,
                              'agentid': '11277', 'win16': False, 'browser': 'Firefox'})

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

    def test_rendering_engine_name(self):
        self.assertEqual(self.browser.rendering_engine_name(), 'Gecko')

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
        self.assertTrue(self.browser.litemode())

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
        self.assertIsNone(self.browser.is_banned())

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
                             {'cookies': False, 'activexcontrols': False, 'aolversion': 0.0, 'frames': True,
                              'cssversion': 0.0, 'majorver': 2, 'tables': True, 'iframes': True, 'vbscript': False,
                              'comments': 'Google', 'platform_version': 0.0, 'platform': '', 'version': 2.1,
                              'masterparent': False, 'renderingengine_version': 0.0, 'javaapplets': False,
                              'parent': 'Google', 'backgroundsounds': False, 'win64': False,
                              'propertyname': '*Googlebot/2.1*', 'javascript': False, 'beta': False,
                              'alpha': False, 'renderingengine_description': '', 'crawler': True,
                              'renderingengine_name': '', 'device_maker': '', 'platform_description': '',
                              'minorver': 1, 'issyndicationreader': False, 'device_name': '', 'win32': False,
                              'ismobiledevice': False, 'litemode': True, 'agentid': '4128', 'win16': False,
                              'browser': 'Googlebot'})

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
        self.assertTrue(self.browser.litemode())

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
        self.assertIsNone(self.browser.is_banned())

    def test_is_alpha(self):
        self.assertFalse(self.browser.is_alpha())

    def test_is_beta(self):
        self.assertFalse(self.browser.is_beta())

    def test_features(self):
        self.assertEqual(self.browser.features(), ['tables', 'frames', 'iframes'])

if __name__ == '__main__':
    unittest.main()