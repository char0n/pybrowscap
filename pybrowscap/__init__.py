
__version__ = '2.0'

import traceback
import warnings
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO


class Error(Exception):
    """Base pybrowscap Error."""

    def __init__(self, value, e):
        s = StringIO()
        traceback.print_exc(file=s)
        self.value = (value, s.getvalue())
        s.close()

    def __str__(self):
        return repr(self.value)


class Browser(object):
    """Browser class represents one record in  browscap data file."""

    def __init__(self, user_agent):
        self.user_agent = user_agent

    def items(self):
        return self.user_agent.copy()

    def get(self, feature, default=None):
        return self.user_agent.get(feature, default)

    def name(self):
        return self.get('browser')

    def category(self):
        return self.get('parent')

    def platform(self):
        return self.get('platform')

    def aol_version(self):
        return self.get('aolversion')

    def version(self):
        return self.get('version')

    def version_major(self):
        return self.get('majorver', 0)

    def version_minor(self):
        return self.get('minorver', 0)

    def css_version(self):
        return self.get('cssversion', 0)

    def rendering_engine_name(self):
        return self.get('renderingengine_name')

    def rendering_engine_version(self):
        return self.get('renderingengine_version')

    def device_maker(self):
        return self.get('device_maker')

    def device_name(self):
        return self.get('device_name')

    def platform_description(self):
        return self.get('platform_description')

    def platform_version(self):
        return self.get('platform_version')

    def litemode(self):
        return self.get('litemode')

    def supports(self, feature):
        to_return = self.get(feature, False)
        if isinstance(to_return, bool):
            return to_return
        else:
            return False

    def supports_tables(self):
        return self.supports('tables')

    def supports_frames(self):
        return self.supports('frames')

    def supports_iframes(self):
        return self.supports('iframes')

    def supports_java(self):
        return self.supports('javaapplets')

    def supports_javascript(self):
        return self.supports('javascript')

    def supports_vbscript(self):
        return self.supports('vbscript')

    def supports_activex(self):
        return self.supports('activexcontrols')

    def supports_cookies(self):
        return self.supports('cookies')

    def supports_css(self):
        return self.css_version() > 0

    def is_crawler(self):
        return self.supports('crawler')

    def is_mobile(self):
        return self.supports('ismobiledevice')

    def is_syndication_reader(self):
        return self.supports('issyndicationreader')

    def is_banned(self):
        warnings.warn(u'This field was removed from csv browscap file', DeprecationWarning, stacklevel=2)
        return None

    def is_alpha(self):
        return self.supports('alpha')

    def is_beta(self):
        return self.supports('beta')

    def features(self):
        features = []
        for feature in ['tables', 'frames', 'iframes', 'javascript', 'vbscript', 'cookies']:
            if self.supports(feature) is True:
                features.append(feature)
        if self.supports_activex():
            features.append('activex')
        if self.supports_java():
            features.append('java')
        if self.css_version() > 0:
            features.append('css1')
        if self.css_version() > 1:
            features.append('css2')
        if self.css_version() > 2:
            features.append('css3')
        return features