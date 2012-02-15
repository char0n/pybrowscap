import logging
import urllib2
from datetime import datetime

from pybrowscap import Browser
load_csv_file = None


log = logging.getLogger(__name__)


TYPE_CSV = 1


class Downloader(object):
    """
    This class is responsible for downloading new versions of browscap file.
    It is possible to to define a timeout for connection and proxy server settings.

    """

    def __init__(self, url, timeout=20, proxy=None, additional_handlers=None):
        """Constructor

        Args:

        :param url: URL of browscap file
        :type url: string
        :param timeout: connection timeout
        :type timeout: int
        :param proxy: url of proxy server
        :type proxy: string
        :param additional_handlers: list of additional urllib2 handlers
        :type additional_handlers: list
        :returns: Downloader instance
        :rtype: Downloader

        """
        self.url = url
        self.timeout = timeout
        self.proxy = proxy
        self.additional_handlers = additional_handlers

    def get(self, save_to_file_path=None):
        """
        Getting browscap file contents and saving it to file or returning it as a string.
        Returns file contents if save_to_file_path is not None, file contents as string otherwise.

        ;param save_to_file_path: path on filesystem where browscap file will be saved
        :rtype save_to_file_path: string
        :returns: None or browscap file contents
        :rtype: string
        :raises: ValueError, urllib2.URLError, urllib2.HTTPError

        """
        try:
            log.info('Downloading latest version of browscap file from %s', self.url)
            opener = urllib2.build_opener()
            if self.proxy is not None:
                log.info('Setting up proxy server %s' % self.proxy)
                opener.add_handler(urllib2.ProxyHandler({'http': self.proxy}))
                if self.additional_handlers is not None:
                    for handler in self.additional_handlers:
                        opener.add_handler(handler)
            opener.addheaders = [('User-agent', 'pybrowscap downloader')]
            urllib2.install_opener(opener)
            response = opener.open(self.url, timeout=self.timeout)
            contents = response.read()
            response.close()
        except ValueError:
            log.exception('Url to browscap file is probably invalid')
            raise
        except urllib2.URLError:
            log.exception('Something went wrong while processing urllib2 handlers')
            raise
        except urllib2.HTTPError:
            log.exception('Something went wrong while downloading browscap file')
            raise

        if save_to_file_path is not None:
            try:
                log.info('Saving latest version of browscap file to %s', save_to_file_path)
                with open(save_to_file_path, 'wb') as file:
                    file.write(contents)
            except IOError:
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
        """Constructor

        :param data_dict: dictionary of regex:line pairs
        :type data_dict: dict
        :param regex_cache: list of compiled regex patterns
        :type regex_cache: list
        :param browscap_file_path: path to the browscap file
        :type browscap_file_path: string
        :param type: type of browscap file csv, ini...
        :type type: int
        :param version: browscap file version
        :type version: int
        :param release_date: release date of browscap file
        :type release_date: datetime.datetime
        :returns: Browscap instance
        :rtype: pybrowscap.loader.Browscap

        """

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

        :param browscap_file_path: location of new browcap file on filesystem, or use old
        :type browscap_file_path: string or None
        :returns: None
        :raises: IOError

        """
        global load_csv_file
        if load_csv_file is None:
            from pybrowscap.loader.csv import load_file as load_csv_file
        try:
            file_to_load = browscap_file_path or self.browscap_file_path
            log.info('Reloading browscap instance with file %s', file_to_load)
            if self.type == TYPE_CSV:
                reloaded_browscap = load_csv_file(file_to_load)
            self.data = reloaded_browscap.data
            self.regex_cache = reloaded_browscap.regex_cache
            self.version = reloaded_browscap.version
            self.release_date = reloaded_browscap.release_date
            self.browscap_file_path = file_to_load
            self.cache = {}
            self.reloaded_at = datetime.now()
        except IOError:
            log.exception('Error while reloading Browscap instance with file %s', file_to_load)
            raise

    def search(self, user_agent_string):
        """Searching browscap data file for longest user_agent_string that matches the regex.

        :param user_agent_string: user agent to search in browscap file
        :type user_agent_string: string
        :returns: Browser instance or None
        :rtype: pybrowscap.Browser or None

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
            log.info('No match found')
            return None
        else:
            log.info('Match found, returning Browser instance for: %s', ua_regex_string)
            self.cache[user_agent_string] = self.data[ua_regex_string]
            return Browser(self.data[ua_regex_string])