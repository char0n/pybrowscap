from decimal import Decimal
from datetime import datetime
from StringIO import StringIO
import logging
import csv
import re
from pybrowscap.loader import Browscap, TYPE_CSV
import locale

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
            if feature == 'CSSVersion' or feature == 'AolVersion' or feature == 'Version':
                try:
                    value = Decimal(value)
                except Exception:
                    value = Decimal('0.0')
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
            else:
                locale.setlocale(locale.LC_TIME, old_locale)
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
                ua_regex = line['useragent'][1:-1]
                for unsafe_char in '^$()[].-':
                    ua_regex = ua_regex.replace(unsafe_char, '\%s' % unsafe_char)
                ua_regex = ua_regex.replace('?', '.').replace('*', '.*?')
                ua_regex = '^%s$' % ua_regex
                browscap_data.update({ua_regex: line})
                regex_cache.append(re.compile(ua_regex))
        return Browscap(
            browscap_data, regex_cache, browscap_file_path, TYPE_CSV,
            version, release_date
        )
    except Exception:
        log.exception('Error while reading browscap source file')
        raise