#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from distutils.core import setup, Command

# own modules:
cur_dir = os.getcwd()
if sys.argv[0] != '' and sys.argv[0] != '-c':
    cur_dir = os.path.dirname(sys.argv[0])
if os.path.exists(os.path.join(cur_dir, 'pb_logging')):
    sys.path.insert(0, os.path.abspath(cur_dir))
del cur_dir

import pb_logging

packet_version = pb_logging.__version__

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'pb_logging',
    version = packet_version,
    description = 'Additional loghandler and logging formater objects',
    long_description = read('README.txt'),
    author = 'Frank Brehm',
    author_email = 'frank.brehm@profitbricks.com',
    url = 'ssh://git.profitbricks.localdomain/srv/git/python/pb-logging.git',
    license = 'LGPLv3+',
    platforms = ['posix'],
    packages = ['pb_logging'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Logging',

    ],
    provides = [
        'pb_logging',
    ],
)

#========================================================================

# vim: fileencoding=utf-8 filetype=python ts=4 expandtab

