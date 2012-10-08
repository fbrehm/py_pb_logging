#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Frank Brehm
@contact: frank.brehm@profitbricks.com
@organization: Profitbricks GmbH
@copyright: (c) 2010-2012 by Profitbricks GmbH
@license: GPL3
@summary: additional logging handler for the common logging framework
          to combine it with syslog
'''

# Standard modules
import logging
import logging.handlers
import syslog
import sys
import os

libdir = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..'))
sys.path.insert(0, libdir)

# Own modules
from pb_syslog.syslog_handler import PbSysLogHandler

msg_utf8 = "Test UTF-8"
msg_uni = u"Test Unicode"

logger = logging.getLogger('test.unicode')

logger.setLevel(logging.INFO)

appname = os.path.basename(sys.argv[0])

format_str_syslog = (appname + ': %(name)s(%(lineno)d) %(funcName)s() ' +
        '%(levelname)s - %(message)s')
format_str_console = ('[%(asctime)s]: ' + appname +
        ': %(name)s(%(lineno)d) %(funcName)s() %(levelname)s - %(message)s')

formatter_syslog = logging.Formatter(format_str_syslog)
formatter_console = logging.Formatter(format_str_console)

lh_syslog = PbSysLogHandler(
        address = '/dev/log',
        facility = logging.handlers.SysLogHandler.LOG_USER,
)
lh_console = logging.StreamHandler(sys.stderr)

logger.addHandler(lh_syslog)
logger.addHandler(lh_console)

logger.info(msg_utf8)
logger.info(msg_uni)

#==============================================================================

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 nu