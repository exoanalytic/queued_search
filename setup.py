#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='queued_search',
    version='1.0.3',
    description='A queuing setup for integration with Haystack.',
    author='Daniel Lindsley',
    author_email='daniel@toastdriven.com',
    url='http://github.com/toastdriven/queued_search',
    packages=[
        'queued_search',
        'queued_search.management',
        'queued_search.management.commands',
    ],
    install_requires=['distribute', 'queues>=0.5',
        'django-haystack>=1.0', 'django'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ],
)
