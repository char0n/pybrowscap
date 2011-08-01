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

    regex_cache = {}
    cache = {}

    def __init__(self, data_dict, regex_cache):
        self.data        = data_dict
        self.regex_cache = regex_cache

    def search(self, user_agent_string):
        user_agent_string = '[%s]' % user_agent_string

        if user_agent_string in self.cache:
            return Browser(self.cache[user_agent_string])

        ua_regex_string = ''
        for ua_pattern in self.regex_cache:
            if ua_pattern.match(user_agent_string) and len(ua_pattern.pattern) > len(ua_regex_string):
                ua_regex_string = ua_pattern.pattern
        if ua_regex_string == '':
            return None
        else:
            self.cache[user_agent_string] = self.data[ua_regex_string]
            return Browser(self.data[ua_regex_string])

def load_file(browscap_file_path):
    def replace_defaults(line, defaults):
        new_line = {}
        for feature, value in line.iteritems():
            if value == 'default':
                value = defaults[feature]
            if value == 'true':
                value = True
            if value == 'false':
                value = False
            if feature == 'MajorVersion' or feature == 'MinorVersion':
                try:
                    value = int(value)
                except Exception:
                    value = 0
            if feature == 'CSSVersion' or feature == 'AolVersion':
                try:
                    value = float(value)
                except Exception:
                    value = 0.0
            new_line[feature.lower()] = value
        return new_line
    
    with open(browscap_file_path, 'rb') as csvfile:
        log.info('Reading browscap source file')
        dialect = csv.Sniffer().sniff(csvfile.read(4096))
        csvfile.seek(0)
        log.info('Removing fileinfo section')
        csvfile.readline()
        csvfile.readline()
        reader        = csv.DictReader(csvfile, dialect=dialect)
        defaults      = {}
        browscap_data = {}
        regex_cache   = []
        for line in reader:
            if line['Parent'] == 'DefaultProperties':
                continue
            if '[%s]' % line['Parent'] == line['UserAgent']:
                defaults = line
                continue
            line = replace_defaults(line, defaults)
            ua_regex = line['useragent']
            for unsafe_char in '^$()[].-':
                ua_regex = ua_regex.replace(unsafe_char, '\%s' % unsafe_char)
            ua_regex = ua_regex.replace('?', '.').replace('*', '.*?')
            ua_regex = '^%s$' % ua_regex
            browscap_data.update({ua_regex: line})
            regex_cache.append(re.compile(ua_regex))
    return Browscap(browscap_data, regex_cache)