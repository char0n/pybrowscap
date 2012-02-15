pybrowscap
==========

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
 from pybrowscap.loader.csv import URL
 Downloader(URL).get(save_to_filepath)


Tests
-----

**Tested on evnironment**

- Xubuntu Linux 11.10 oneiric 64-bit
- python 2.7.2+
- python unitest
- browscap_22_06_2011.csv from Wed, 22 Jun 2011 23:26:51 -0000
- browscap.07_10_2011.csv from Fri, 07 Oct 2011 06:46:46 -0000

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

- http://github.com/char0n/pybrowscap
- http://browsers.garykeith.com/
- http://php.net/get_browser
- http://www.codescale.net/en/community#pybrowscap
