#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 14:18:36 2020

@author: asyntychaki
"""

from setuptools import setup

setup(name = 'distributions-asyn',
      version = '0.1',
      description = 'Gaussian and Binomial distributions',
      packages = ['distributions-asyn'],
      author = 'Anastasia Syntychaki',
      author_email = 'asyntychaki@gmail.com',
      classifiers=[
                   # How mature is this project?
                   'Development Status :: 5 - Production/Stable',
                   # Indicate who your project is intended for
                   'Topic :: Scientific/Engineering :: Mathematics',
                   # Specify the Python versions you support here. In particular, ensure
                   # that you indicate whether you support Python 2, Python 3 or both.
                   'Programming Language :: Python :: 3',
                   # OS
                   'Operating System :: MacOS',
                   'Operating System :: Microsoft',
                   'Operating System :: POSIX'
                   ],
      keywords=['gaussian', 'binomial', 'distributions'],
      zip_safe = False)
