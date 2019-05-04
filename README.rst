pybrowscap
==========

pybrowscap is a python port of PHP function `get_browser()`. It tells what the user
browser is capable of. It detects browsers capabilities and features like css, java,
javascript etc. It works on top of browscap data file.


Important notice
----------------

Version 2.0 and higher of pybrowscap supports csv browscap file version 5000 and higher. If you want to use
older version of csv browscap file, use pybrowscap version lower than 2.0.


Requirements
------------

- python 2.6+ or pythone 3+
- browscap.csv (browscap data file in csv format)


Instalation
-----------

Install via pypi or copy this module into your project or into your PYTHON_PATH.
Download latest version of browscap.csv file from http://browscap.org/stream?q=BrowsCapCSV


Example
-------

::

 from pybrowscap.loader.csv import load_file
 browscap = load_file(path_to_browscap_csv)
 browser  = browscap.search(user_agent_string)
 browser.is_crawler()


Automatic updates
-----------------

::

 from pybrowscap.loader import Downloader
 from pybrowscap.loader.csv import URL
 Downloader(URL).get(save_to_filepath)


Tests
-----

**Tested on evnironment**

- Ubuntu Linux 16.04 LTS precise 64-bit
- python 2.7.3 and python3.5
- python unitest
- browscap_14_05_2012.csv from Mon, 14 May 2012 22:20:20 -0000
- browscap.21_05_2012.csv from Mon, 21 May 2012 15:48:39 -0000
- browscap.29_11_2018.csv from Thr, 29 Nov 2018 08:50:14 +0000

**Running tests**

To run the test run command: ::

 $ python test.py
 $ python setup.py test


Author
------

| char0n (Vladimír Gorej, CodeScale s.r.o.) 
| email: gorej@codescale.net
| web: http://www.codescale.net

Credits
-------

Special thanks to these projects for inspiration:

- http://code.google.com/p/python-browscap/
- http://djangosnippets.org/snippets/267/


References
----------

- http://github.com/CodeScaleInc/pybrowscap
- http://browsers.garykeith.com/
- http://php.net/get_browser
- http://www.codescale.net/en/community#pybrowscap
