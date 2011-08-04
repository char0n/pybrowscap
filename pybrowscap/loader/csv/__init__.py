from decimal import Decimal
import logging
import csv
import re
from pybrowscap.loader import Browscap

log = logging.getLogger(__name__)

URL = 'http://browsers.garykeith.com/stream.asp?BrowsCapCSV'

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
    except Exception:
        log.exception('Error while reading browscap source file')
        raise