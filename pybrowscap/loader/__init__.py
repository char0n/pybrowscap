from pybrowscap import Browser
import logging
import urllib2
import csv
import re

log = logging.getLogger(__name__)

class Downloader(object):

    url = 'http://browsers.garykeith.com/stream.asp?BrowsCapCSV'

    def __init__(self, timeout=20, proxy=None, additional_handlers=[]):
        self.timeout             = timeout
        self.proxy               = proxy
        self.additional_handlers = additional_handlers

    def get(self, save_to_filepath=None):
        try:
            log.info('Downloading latest version of browscap from %s' % self.url)
            opener = urllib2.build_opener()
            if self.proxy is not None:
                log.info('Setting up proxy server %s' % self.proxy)
                opener.add_handler(urllib2.ProxyHandler({'http': self.proxy}))
                for handler in self.additional_handlers:
                    opener.add_handler(handler)
            opener.add_headers = [('User-agent', 'pybrowscap downloader')]
            response = opener.open(self.url, timeout=self.timeout)
            contents = response.read()
            response.close()
        except Exception:
            log.exception('Error while downloading latest version of browscap')
            raise

        if save_to_filepath is not None:
            try:
                log.info('Saving latest version of browscap file to %s' % save_to_filepath)
                with open(save_to_filepath, 'wb') as file:
                    file.write(contents)
            except Exception:
                log.exception('Error while saving latest version of browscap file')
                raise
        else:
            return contents


class Browscap(object):

    cache = {}

    def __init__(self, defaults, data_dict):
        self.defaults = defaults
        self.data     = data_dict

    def search(self, user_agent_string):
        user_agent_string = '[%s]' % user_agent_string

        ua_regex_pattern = ''
        for ua_regex, line in self.data.iteritems():
            if ua_regex.match(user_agent_string) and len(ua_regex.pattern) > len(ua_regex_pattern):
                ua_regex_pattern = ua_regex.pattern
        if ua_regex_pattern == '':
            return None
        else:
            ua_regex = re.compile(ua_regex)
            return Browser(self.defaults, self.data[ua_regex])

def load_file(browscap_file_path):
    with open(browscap_file_path, 'rb') as csvfile:
        log.info('Reading browscap source file')
        dialect = csv.Sniffer().sniff(csvfile.read(4096))
        csvfile.seek(0)
        log.info('Removing fileinfo section')
        csvfile.readline()
        csvfile.readline()
        reader = csv.DictReader(csvfile, dialect=dialect)
        defaults = {}
        browscap_data = {}
        for line in reader:
            if reader.line_num == 2:
                defaults = line
                continue
            ua_regex = line['UserAgent']
            for unsafe_char in '^$()[].-':
                ua_regex = ua_regex.replace(unsafe_char, '\%s' % unsafe_char)
            ua_regex = ua_regex.replace('?', '.').replace('*', '.*?')
            ua_regex = '^%s$' % ua_regex
            browscap_data.update({re.compile(ua_regex): line})
    return Browscap(defaults, browscap_data)


browscap = load_file('/var/projects/python/pybrowscap/browscap.csv')
browser = browscap.search('[Mozilla/5.0 (X11; U; Linux i686; de; rv:1.8.0.5) Gecko/20060731 Ubuntu/dapper-security Firefox/1.5.0.5]')
print browser.name()