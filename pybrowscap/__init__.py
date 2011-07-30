__version__ = '1.0b1'

import csv

with open('../browscap.csv', 'rb') as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.read(4096))
    csvfile.seek(0)
    csvfile.readline()
    csvfile.readline()
    reader = csv.DictReader(csvfile, dialect=dialect)
    defaults = {}
    for line in reader:
        if reader.line_num == 2:
            defaults = line
            continue

        print line
