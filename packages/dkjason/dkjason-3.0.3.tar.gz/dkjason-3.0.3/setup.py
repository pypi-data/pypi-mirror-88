#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""dkjason - Helper module to send json encoded data from Python
"""

classifiers = """\
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Topic :: Software Development :: Libraries
"""

import setuptools

version = '3.0.3'


setuptools.setup(
    name='dkjason',
    version=version,
    install_requires=[
        "Django==1.8.19",
        "ttcal",
    ],
    description=__doc__.strip(),
    classifiers=[line for line in classifiers.split('\n') if line],
    long_description=open('README.rst').read(),
    packages=setuptools.find_packages(exclude=["tests"]),
    zip_safe=False,
)
