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
import socket

libdir = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..'))
sys.path.insert(0, libdir)

# Own modules
from pb_logging.syslog_handler import PbSysLogHandler

if sys.version_info[0] > 2:
    print("This is Python 3.X")
    msg_utf8 = "Test UTF-8 with wide characters: 'äöüÄÖÜß»«¢„“”µ·…@ł€¶ŧ←↓→øþ¨æſðđŋħłĸ˝^'".encode('utf-8')
    msg_uni = "Test Unicode with wide characters: 'äöüÄÖÜß»«¢„“”µ·…@ł€¶ŧ←↓→øþ¨æſðđŋħłĸ˝^'"
else:
    print("This is Python 2.X")
    msg_utf8 = "Test UTF-8 with wide characters: 'äöüÄÖÜß»«¢„“”µ·…@ł€¶ŧ←↓→øþ¨æſðđŋħłĸ˝^'"
    msg_uni = "Test Unicode with wide characters: 'äöüÄÖÜß»«¢„“”µ·…@ł€¶ŧ←↓→øþ¨æſðđŋħłĸ˝^'".decode('utf-8')

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
lh_syslog.setFormatter(formatter_syslog)

lh_console = logging.StreamHandler(sys.stderr)
lh_console.setFormatter(formatter_console)

logger.addHandler(lh_syslog)
logger.addHandler(lh_console)

logger.info(msg_utf8)
logger.info(msg_uni)

#==============================================================================

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 nu
