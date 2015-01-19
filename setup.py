#!/usr/bin/env python

import os
import sys

sys.path.insert(0, os.path.abspath('lib'))
from vmdatastore import __version__, __author__
from distutils.core import setup

setup(name='vmdatastore',
      version=__version__,
      description='vCenter datastore manager',
      long_description='This command-line tool lets you create datastore for a ESX host.',
      author=__author__,
      author_email='contact@sebbrochet.com',
      url='https://github.com/sebbrochet/vmdatastore/',
      platforms=['linux'],
      license='MIT License',
      install_requires=[
          'argparse == 1.2.2',
          'pyvmomi == 5.5.0.2014.1.1',
          'requests == 2.5.0',
          'six == 1.8.0',
          'wsgiref==0.1.2',
      ],
      package_dir={'vmdatastore': 'lib/vmdatastore'},
      packages=['vmdatastore'],
      scripts=['bin/vmdatastore'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: MIT License',
          'Operating System :: POSIX :: Linux',
          'Operating System :: Microsoft :: Windows',
          'Programming Language :: Python',
          'Topic :: System :: Systems Administration',
          ],
      )
