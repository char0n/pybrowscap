from pybrowscap import Browser
from datetime import datetime
import logging
import urllib2

log = logging.getLogger(__name__)


TYPE_CSV = 1


class Downloader(object):
    """
    This class is responsible for downloading new versions of
    browscap file. It is possible to to define a timeout for connection
    and proxy server settings.
    
    """

    def __init__(self, url, timeout=20, proxy=None, additional_handlers=[]):
        self.url                 = url
        self.timeout             = timeout
        self.proxy               = proxy
        self.additional_handlers = additional_handlers

    def get(self, save_to_filepath=None):
        """
        Getting browscap file contents and saving it to file or returning
        it as a string.

        Returns file contents if save_to_filepath is not None,
        file contents as string otherwise.

        """
        try:
            log.info('Downloading latest version of browscap from %s' % self.url)
            opener = urllib2.build_opener()
            if self.proxy is not None:
                log.info('Setting up proxy server %s' % self.proxy)
                opener.add_handler(urllib2.ProxyHandler({'http': self.proxy}))
                for handler in self.additional_handlers:
                    opener.add_handler(handler)
            opener.addheaders = [('User-agent', 'pybrowscap downloader')]
            urllib2.install_opener(opener)
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
    """
    Browscap class represents abstraction on top of browscap data file.
    It contains all browscap data file data in python accessible form.

    """

    cache = {}

    def __init__(self, data_dict, regex_cache, browscap_file_path, type, version, release_date):
        self.data = data_dict
        self.regex_cache = regex_cache
        self.browscap_file_path = browscap_file_path
        self.type = type
        self.version = version
        self.release_date = release_date
        self.loaded_at = datetime.now()
        self.reloaded_at = None

    def reload(self, browscap_file_path=None):
        """
        Reloads new data to this Browscap instance. This is useful
        mainly in apps that run in long living threads, like django projects.

        """
        from pybrowscap.loader.csv import load_file as load_csv_file
        try:
            file_to_load = browscap_file_path or self.browscap_file_path
            if self.type == TYPE_CSV:
                reloaded_browscap = load_csv_file(file_to_load)
            self.data = reloaded_browscap.data
            self.regex_cache = reloaded_browscap.regex_cache
            self.version = reloaded_browscap.version
            self.release_date = reloaded_browscap.release_date
            self.browscap_file_path = file_to_load
            self.cache = {}
            self.reloaded_at = datetime.now()
        except Exception:
            log.exception('Error while reloading Browscap instance')
            raise

    def search(self, user_agent_string):
        """
        Searching browscap data file for longest user_agent_string that
        matches the regex.

        Returns Browser instance if match is found, None otherwise.

        """
        log.info('Searching for user-agent: %s', user_agent_string)
        if user_agent_string in self.cache:
            log.debug('Cache-hit, searching skipped')
            return Browser(self.cache[user_agent_string])

        ua_regex_string = ''
        for ua_pattern in self.regex_cache:
            if ua_pattern.match(user_agent_string) and len(ua_pattern.pattern) > len(ua_regex_string):
                ua_regex_string = ua_pattern.pattern
        if ua_regex_string == '':
            log.debug('No match found')
            return None
        else:
            log.debug('Match found, returning Browser instance for: %s', ua_regex_string)
            self.cache[user_agent_string] = self.data[ua_regex_string]
            return Browser(self.data[ua_regex_string])