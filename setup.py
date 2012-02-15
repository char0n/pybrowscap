# -*- coding: utf-8 -*-
import os
from setuptools import setup

import pybrowscap

def read(fname):
    """Utility function to read the README file.

    Used for the long_description. It's nice, because now 1) we have a top level
    README file and 2) it's easier to type in the README file than to put a raw
    string in below ...

    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='pybrowscap',
    version=pybrowscap.__version__,
    description='detects browsers capabilities and features like css, java, javascript etc.',
    long_description=read('README.rst'),
    author=u'Vladimír Gorej',
    author_email='gorej@codescale.net',
    url='http://www.codescale.net/en/community#pybrowscap',
    download_url='http://github.com/char0n/pybrowscap/tarball/master',
    license='BSD',
    keywords = 'browser browscap detection user agent',
    packages=['pybrowscap', 'pybrowscap.loader', 'pybrowscap.loader.csv'],
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Browsers'
    ],
    test_suite='pybrowscap.test',
)