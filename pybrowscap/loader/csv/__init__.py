import sre_constants
import logging
import locale
import csv
import re
from StringIO import StringIO
from datetime import datetime

from pybrowscap.loader import Browscap, TYPE_CSV


log = logging.getLogger(__name__)


# Url where latest version of csv browscap data file is located
URL = 'http://browsers.garykeith.com/stream.asp?BrowsCapCSV'


def load_file(browscap_file_path):
    """
    Loading browscap csv data file, parsing in into accessible python
    form and returning a new Browscap class instance with all appropriate data.

    :param browscap_file_path: location of browcap file on filesystem
    :type browscap_file_path: string
    :returns: Browscap instance filled with data
    :rtype: pybrowscap.loader.Browscap

    """
    def replace_defaults(line, defaults):
        """Replaces 'default' values for a line with parent line value and converting it into native python value.

        :param line: original line from browscap file
        :type line: dict
        :param defaults: default values for current line
        :type defaults: dict
        :returns: dictionary with replaced default values
        :rtype: dict
        :raises: IOError

        """
        new_line = {}
        for feature, value in line.iteritems():
            if value == 'default' or value == '':
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
            if feature == 'CSSVersion' or feature == 'AolVersion' or feature == 'Version':
                try:
                    value = float(value)
                except Exception:
                    value = float(0)
            new_line[feature.lower()] = value
        return new_line
    try:
        with open(browscap_file_path, 'rb') as csvfile:
            log.info('Reading browscap source file %s', browscap_file_path)
            dialect = csv.Sniffer().sniff(csvfile.read(4096))
            csvfile.seek(0)
            log.info('Getting file version and release date')
            csvfile.readline()
            line = csv.reader(StringIO(csvfile.readline())).next()
            log.info('Getting browcap file version')
            try:
                version = int(line[0])
            except ValueError:
                log.exception('Error while getting browscap file version')
                version = None
            log.info('Getting browscap file release date')
            try:
                old_locale = locale.getlocale()
                locale.setlocale(locale.LC_TIME, locale.normalize('en_US.utf8'))
                release_date = datetime.strptime(line[1][:-6], '%a, %d %b %Y %H:%M:%S')
            except (ValueError, locale.Error):
                log.exception('Error while getting browscap file release date')
                release_date = None
            finally:
                locale.setlocale(locale.LC_TIME, old_locale)

            log.info('Reading browscap user-agent data')
            reader = csv.DictReader(csvfile, dialect=dialect)
            defaults = {}
            browscap_data = {}
            regex_cache = []
            for line in reader:
                if line['Parent'] == 'DefaultProperties':
                    continue
                if '[{0}]'.format(line['Parent']) == line['UserAgent']:
                    defaults = line
                    continue
                line = replace_defaults(line, defaults)
                try:
                    ua_regex = '^{0}$'.format(re.escape(line['useragent'][1:-1]))
                    ua_regex = ua_regex.replace('\\?', '.').replace('\\*', '.*?')
                    browscap_data[ua_regex] = line
                    log.debug('Compiling user agent regex: %s', ua_regex)
                    regex_cache.append(re.compile(ua_regex))
                except sre_constants.error:
                    continue
        return Browscap(browscap_data, regex_cache, browscap_file_path, TYPE_CSV,
                        version, release_date)
    except IOError:
        log.exception('Error while reading browscap source file %s', browscap_file_path)
        raise