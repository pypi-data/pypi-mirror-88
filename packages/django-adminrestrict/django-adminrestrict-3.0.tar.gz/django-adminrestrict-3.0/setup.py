#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

# The directory containing this file
HERE = os.path.realpath(os.path.join(__file__, '..'))

# The text of the README file
README = open(os.path.join(HERE,"README.md")).read()

VERSION = '3.0'

setup(
    name='django-adminrestrict',
    version=VERSION,
    description="Restrict admin pages using simple IP address rules",
    long_description=README,
    long_description_content_type="text/markdown", 
    keywords='authentication, django, security',
    author='Robert Romano',
    author_email='rromano@example.com',
    url='https://github.com/robromano/django-adminrestrict',
    license='MIT',
    package_dir={'adminrestrict': 'adminrestrict'},
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: Log Analysis',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
        'Topic :: Security',
        'Topic :: System :: Logging',
    ],
    zip_safe=False,
)
