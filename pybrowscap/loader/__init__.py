import logging
import urllib2

log = logging.getLogger(__name__)

class Downloader(object):

    url = 'http://browsers.garykeith.com/stream.asp?BrowsCapCSV'

    def __init__(self, timeout=20, proxy=None, additional_handlers=[]):
        self.timeout             = timeout
        self.proxy               = proxy
        self.additional_handlers = additional_handlers

    def get(self, save_to_filepath=None):
        try:
            log.debug('Downloading latest version of browscap from %s' % self.url)
            opener = urllib2.build_opener()
            if self.proxy is not None:
                log.debug('Setting up proxy server %s' % self.proxy)
                opener.add_handler(urllib2.ProxyHandler({'http': self.proxy}))
                for handler in self.additional_handlers:
                    opener.add_handler(handler)
            opener.add_headers = [('User-agent', 'pybrowscap downloader')]
            response = opener.open(self.url, timeout=self.timeout)
            contents = response.read()
            response.close()
        except Exception:
            log.exception('Error while downloading latest version of browscap')

        if save_to_filepath is not None:
            try:
                log.debug('Saving latest version of browscap file to %s' % save_to_filepath)
                file = open(save_to_filepath, 'wb')
                file.write(contents)
                file.close()
            except Exception:
                log.exception('Error while saving latest version of browscap file')
        else:
            return contents


class Loader(object):
    pass