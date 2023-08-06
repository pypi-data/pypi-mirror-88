#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__version__ = '0.11.9'

packages = [
    'lassie',
    'lassie.filters',
    'lassie.filters.oembed'
]

setup(
    name='lassie',
    version=__version__,
    install_requires=open("requirements.txt").read().split("\n"),
    author='Mike Helmick',
    author_email='me@michaelhelmick.com',
    license=open('LICENSE').read(),
    url='https://github.com/michaelhelmick/lassie/tree/master',
    keywords='lassie open graph web content scrape scraper',
    description='Lassie is a Python library for retrieving basic content from websites',
    long_description='',
    include_package_data=True,
    packages=packages,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ]
)
