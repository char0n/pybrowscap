pybrowscap 1.0b1
================

pybrowscap is a python port of PHP function `get_browser()`. It tells what the user
browser is capable of. It detects browsers capabilities and features like css, java,
javascript etc. It works on top of browscap data file.


Requirements
------------

- python 2.6+
- browscap.csv (browscap data file in csv format)


Instalation
-----------

Install via pipy or copy this module into your project or into your PYTHON_PATH.
Download latest version of browscap.csv file from http://browsers.garykeith.com/downloads.asp.


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
 Downloader().get(save_to_filepath)


Tests
-----

**Tested on evnironment**

- Ubuntu Linux 10.04
- python 2.6.6
- python unitest
- browscap.csv from Wed, 22 Jun 2011 23:26:51 -0000

**Running tests**

To run the test run command: ::

 python test.py


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

- http://github.com/char0n/pybrowscap
- http://browsers.garykeith.com/
- http://php.net/get_browser
- http://www.codescale.net/en/community#pybrowscap