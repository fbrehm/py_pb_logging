#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Frank Brehm
@contact: frank.brehm@profitbricks.com
@license: GPL3
@copyright: (c) 2010-2012 by Profitbricks GmbH
@summary: Additional loghandler and logging formater objects
          to use with the logging framework.
"""

from setuptools import setup
import os
import sys
import os.path

# own modules:
cur_dir = os.getcwd()
if sys.argv[0] != '' and sys.argv[0] != '-c':
    cur_dir = os.path.dirname(sys.argv[0])
if os.path.exists(os.path.join(cur_dir, 'pb_logging')):
    sys.path.insert(0, os.path.abspath(cur_dir))
del cur_dir

import pb_logging

packet_version = pb_logging.__version__


setup(
    name = 'pb_logging',
    version = packet_version,
    description = 'Additional loghandler and logging formater objects',
    author = 'Frank Brehm',
    author_email = 'frank.brehm@profitbricks.com',
    url = 'ssh://git.profitbricks.localdomain/srv/git/python/pb_logging.git',
    packages = ['pb_logging'],
)

#========================================================================

# vim: fileencoding=utf-8 filetype=python ts=4 expandtab

