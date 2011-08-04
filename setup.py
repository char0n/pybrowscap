# -*- coding: utf-8 -*-
from setuptools import setup
import pybrowscap
import os

# Utility function to read the README file.
# Used for the long_description. It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='pybrowscap',
    version=pybrowscap.__version__,
    description='detects browsers capabilities and features like css, java, javascript etc.',
    long_description=read('README.rst'),
    author='Vladimír Gorej',
    author_email='gorej@codescale.net',
    url='http://www.codescale.net/en/community#pybrowscap',
    license='BSD',
    keywords = "browser browscap detection user agent",
    packages=['pybrowscap', 'pybrowscap.loader', 'pybrowscap.loader.csv']
)

