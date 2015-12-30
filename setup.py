#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Frank Brehm
@contact: frank.brehm@profitbricks.com
@license: LGPL3+
@copyright: © 2010 - 2015 ProfitBricks GmbH, Berlin
@summary: Additional loghandler and logging formater objects
"""

import os
import sys
import re
from distutils.core import setup, Command

# own modules:
cur_dir = os.getcwd()
if sys.argv[0] != '' and sys.argv[0] != '-c':
    cur_dir = os.path.dirname(sys.argv[0])

libdir = os.path.join(cur_dir)
pkg_dir = os.path.join(libdir, 'pb_logging')
init_py = os.path.join(pkg_dir, '__init__.py')

if os.path.exists(pkg_dir):
    sys.path.insert(0, os.path.abspath(libdir))

import pb_logging

packet_version = pb_logging.__version__
packet_name = 'pb_logging'
debian_pkg_name = 'pb-logging'
packet_descr = 'Additional loghandler and logging formater objects'
git_url = 'https://gitlab.pb.local/dcops/pb-logging.git'

__author__ = 'Frank Brehm'
__contact__ = 'frank@profitbricks.com'
__copyright__ = '(C) 2010 - 2015 by ProfitBricks GmbH, Berlin'
__license__ = 'LGPL3+'

#------------------------------------
def read(fname):

    content = None
    print("Reading %r ..." % (fname))
    if sys.version_info[0] > 2:
        with open(fname, 'r', encoding = 'utf-8') as fh:
            content = fh.read()
    else:
        with open(fname, 'r') as fh:
            content = fh.read()
    return content

#------------------------------------
debian_dir = os.path.join(cur_dir, 'debian')
changelog_file = os.path.join(debian_dir, 'changelog')
readme_file = os.path.join(cur_dir, 'README.txt')

#------------------------------------
def get_debian_version():
    if not os.path.isfile(changelog_file):
        return None
    changelog = read(changelog_file)
    first_row = changelog.splitlines()[0].strip()
    if not first_row:
        return None
    pattern = r'^' + re.escape(debian_pkg_name) + r'\s+\(([^\)]+)\)'
    match = re.search(pattern, first_row)
    if not match:
        return None
    return match.group(1).strip()

debian_version = get_debian_version()
if debian_version is not None and debian_version != '':
    packet_version = debian_version

#------------------------------------
setup(
    name = packet_name,
    version = packet_version,
    description = packet_descr,
    long_description = read(readme_file),
    author = __author__,
    author_email = __contact__,
    url = git_url,
    license = __license__,
    platforms = ['posix'],
    packages = ['pb_logging'],
    classifiers = [
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
            'Natural Language :: English',
            'Operating System :: POSIX',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: System :: Logging',

    ],
    provides = [packet_name],
)

#========================================================================

# vim: fileencoding=utf-8 filetype=python ts=4 expandtab

