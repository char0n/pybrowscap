__version__ = '1.0b1'

class Browser(object):

    def __init__(self, defaults, user_agent):
        self.user_agent = {}
        for feature, value in user_agent.iteritems():
            if value == 'default':
                value = defaults[feature]
            if value == 'true':
                value = True
            if value == 'false':
                value = False
            if feature.lower() == 'majorversion' or feature.lower() == 'minorversion':
                try:
                    value = int(value)
                except Exception:
                    value = 0
            if feature.lower() == 'cssversion':
                value = float(value)
            self.user_agent[feature.lower()] = value

    def name(self):
        return self.user_agent.get('browser')

    def category(self):
        return self.user_agent.get('parent')

    def version(self):
        return self.user_agent.get('version')

    def version_major(self):
        return int(self.user_agent.get('majorversion', 0))

    def version_minor(self):
        return int(self.user_agent.get('minorversion', 0))

    def css_version(self):
        return int(self.user_agent.get('cssversion', 0))

    def supports(self, feature):
        return self.user_agent.get(feature, False)

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
        return self.supports('mobiledevice')

    def is_syndication_reader(self):
        return self.supports('syndicationreader')

    def is_banned(self):
        return self.supports('banned')

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