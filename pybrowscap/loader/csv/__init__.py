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

    If something went wrong, Exception is raised

    """
    def replace_defaults(line, defaults):
        """
        Replaces 'default' values for a line with parent line value and
        converting it into native python value.

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
            log.info('Reading browscap source file')
            dialect = csv.Sniffer().sniff(csvfile.read(4096))
            csvfile.seek(0)
            log.info('Getting file version and release date')
            csvfile.readline()
            line = csv.reader(StringIO(csvfile.readline())).next()
            try:
                version = int(line[0])
                old_locale = locale.getlocale()
                locale.setlocale(locale.LC_TIME, locale.normalize('en_US.utf8'))
                release_date = datetime.strptime(line[1][:-6], '%a, %d %b %Y %H:%M:%S')
            except Exception:
                log.exception('Error while getting file version and release date')
                version = None
                release_date = None
            finally:
                try:
                    locale.setlocale(locale.LC_TIME, old_locale)
                except Exception:
                    pass
            log.info('Reading browscap user-agent data')
            reader = csv.DictReader(csvfile, dialect=dialect)
            defaults = {}
            browscap_data = {}
            regex_cache = []
            for line in reader:
                if line['Parent'] == 'DefaultProperties':
                    continue
                if '[%s]' % line['Parent'] == line['UserAgent']:
                    defaults = line
                    continue
                line = replace_defaults(line, defaults)
                ua_regex = '^%s$' % re.escape(line['useragent'][1:-1])
                ua_regex = ua_regex.replace('\\?', '.').replace('\\*', '.*?')
                browscap_data.update({ua_regex: line})
                regex_cache.append(re.compile(ua_regex))
        return Browscap(
            browscap_data, regex_cache, browscap_file_path, TYPE_CSV,
            version, release_date
        )
    except Exception:
        log.exception('Error while reading browscap source file')
        raise