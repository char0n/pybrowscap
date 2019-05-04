import sre_constants
import logging
import locale
import csv
import re
from datetime import datetime
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

from pybrowscap.loader import Browscap, TYPE_CSV


log = logging.getLogger(__name__)


# Url where latest version of csv browscap data file is located
URL = 'http://browscap.org/stream?q=BrowsCapCSV'


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
        try:
            items = line.iteritems()
        except AttributeError:
            items = line.items()
        for feature, value in items:
            feature = feature.lower()
            if value == 'default' or value == '':
                value = defaults.get(feature, value)
            if value == 'true':
                value = True
            if value == 'false':
                value = False
            if feature == 'minorver' and value == '0':
                value = defaults.get(feature, value)
            if feature == 'majorver' or feature == 'minorver':
                try:
                    value = int(value)
                except (ValueError, OverflowError):
                    value = 0
            if (feature == 'version' or feature == 'renderingengine_version') and value == '0':
                value = defaults.get(feature, value)
            if (feature == 'cssversion' or feature == 'aolversion' or feature == 'version' or
                feature == 'renderingengine_version' or feature == 'platform_version'):
                try:
                    value = float(value)
                except (ValueError, OverflowError):
                    value = float(0)
            new_line[feature.lower()] = value
        return new_line

    try:
        with open(browscap_file_path, 'r') as csvfile:
            # in py3 
            # mode='rb', read return bytes
            # mode='r' , read return str
            log.info('Reading browscap source file %s', browscap_file_path)
            dialect = csv.Sniffer().sniff(csvfile.read(4096))
            csvfile.seek(0)
            log.info('Getting file version and release date')
            csvfile.readline()
            reader = csv.reader(StringIO(csvfile.readline()))
            for line in reader:     # read version and date to line
                break
            log.info('Getting browcap file version')
            try:
                version = int(line[0])
            except ValueError:
                log.exception('Error while getting browscap file version')
                version = None
            log.info("Browscap Version: {}".format(version))
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
            log.info("Browscap Release Date: {}".format(release_date))

            log.info('Reading browscap user-agent data')
            reader = csv.DictReader(csvfile, dialect=dialect)
            defaults = {}
            browscap_data = {}
            regex_cache = []

            for line in reader:
                if line['PropertyName'] == 'DefaultProperties':
                    for key in line:
                        defaults[key.lower()] = line[key]       # turn defaults key to lower
                    break
            for line in reader:
                line = replace_defaults(line, defaults)
                try:
                    ua_regex = '^{0}$'.format(re.escape(line['propertyname']))
                    ua_regex = ua_regex.replace('\\?', '.').replace('\\*', '.*?')
                    browscap_data[ua_regex] = line
                    log.debug('Compiling user agent regex: %s', ua_regex)
                    regex_cache.append(re.compile(ua_regex,re.IGNORECASE))
                except sre_constants.error:
                    continue
        return Browscap(browscap_data, regex_cache, browscap_file_path, TYPE_CSV,
                        version, release_date)
    except IOError:
        log.exception('Error while reading browscap source file %s', browscap_file_path)
        raise
