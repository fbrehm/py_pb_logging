#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Frank Brehm
@contact: frank.brehm@profitbricks.com
@organization: Profitbricks GmbH
@copyright: © 2010 - 2013 by Profitbricks GmbH
@license: GPL3
@summary: test script (and module) for unit tests on logging objects
'''

import unittest
import os
import sys
import logging
import logging.handlers

libdir = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..'))
sys.path.insert(0, libdir)

import general
from general import PbLoggingTestcase, get_arg_verbose, init_root_logger

log = logging.getLogger(__name__)

#==============================================================================

class TestSyslogTestcase(PbLoggingTestcase):

    #--------------------------------------------------------------------------
    def setUp(self):

        self.msg_utf8 = "Test UTF-8 without wide characters."
        self.msg_uni = u"Test Unicode with wide characters: 'äöüÄÖÜß»«¢„“”µ·…@ł€¶ŧ←↓→øþ¨æſðđŋħłĸ˝^'"


    #--------------------------------------------------------------------------
    def test_import_modules(self):

        log.info("Test importing all appropriate modules ...")

        log.debug("Importing ColoredFormatter from pb_logging.colored ...")
        from pb_logging.colored import ColoredFormatter

        log.debug("Importing PbSysLogHandler from pb_logging.syslog_handler ...")
        from pb_logging.syslog_handler import PbSysLogHandler

        log.debug("Importing UnixSyslogHandler from pb_logging.unix_handler ...")
        from pb_logging.unix_handler import UnixSyslogHandler

    #--------------------------------------------------------------------------
    def test_logging_syslog(self):

        log.info("Test logging with PbSysLogHandler ...")

        from pb_logging.syslog_handler import PbSysLogHandler

        log.debug("Init of a test logger instance ...")
        test_logger = logging.getLogger('test.unicode')
        test_logger.setLevel(logging.INFO)
        appname = os.path.basename(sys.argv[0])

        format_str_syslog = (appname + ': %(name)s(%(lineno)d) %(funcName)s() ' +
                '%(levelname)s - %(message)s')
        format_str_console = ('[%(asctime)s]: ' + appname +
                ': %(name)s(%(lineno)d) %(funcName)s() %(levelname)s - %(message)s')

        formatter_syslog = logging.Formatter(format_str_syslog)
        formatter_console = logging.Formatter(format_str_console)

        log.debug("Init of a PbSysLogHandler ...")
        lh_syslog = PbSysLogHandler(
                address = '/dev/log',
                facility = logging.handlers.SysLogHandler.LOG_USER,
        )

        lh_syslog.setFormatter(formatter_syslog)

        log.debug("Init of a StreamHandler ...")
        lh_console = logging.StreamHandler(sys.stderr)
        lh_console.setFormatter(formatter_console)

        log.debug("Adding log handlers to test logger instance ...")
        test_logger.addHandler(lh_syslog)
        test_logger.addHandler(lh_console)

        log.debug("Logging an UTF-8 message without wide characters ...")
        test_logger.info(self.msg_utf8)
        log.debug("Logging an unicode message with wide characters ...")
        test_logger.info(self.msg_uni)

    #--------------------------------------------------------------------------
    def test_unix_syslog(self):

        log.info("Test logging with UnixSyslogHandler ...")

        from pb_logging.unix_handler import UnixSyslogHandler

        log.debug("Init of a test logger instance ...")
        test_logger = logging.getLogger('test.unix_handler')
        test_logger.setLevel(logging.INFO)
        appname = os.path.basename(sys.argv[0])

        format_str_syslog = (appname + ': %(name)s(%(lineno)d) %(funcName)s() ' +
                '%(levelname)s - %(message)s')
        format_str_console = ('[%(asctime)s]: ' + appname +
                ': %(name)s(%(lineno)d) %(funcName)s() %(levelname)s - %(message)s')

        formatter_syslog = logging.Formatter(format_str_syslog)
        formatter_console = logging.Formatter(format_str_console)

        log.debug("Init of a UnixSyslogHandler ...")
        lh_unix_syslog = UnixSyslogHandler(
                ident = appname,
                facility = UnixSyslogHandler.LOG_INFO,
        )

        lh_unix_syslog.setFormatter(formatter_syslog)

        log.debug("Init of a StreamHandler ...")
        lh_console = logging.StreamHandler(sys.stderr)
        lh_console.setFormatter(formatter_console)

        log.debug("Adding log handlers to test logger instance ...")
        test_logger.addHandler(lh_unix_syslog)
        test_logger.addHandler(lh_console)

        log.debug("Logging an UTF-8 message without wide characters ...")
        test_logger.info(self.msg_utf8)
        log.debug("Logging an unicode message with wide characters ...")
        test_logger.info(self.msg_uni)

#==============================================================================

if __name__ == '__main__':

    verbose = get_arg_verbose()
    if verbose is None:
        verbose = 0
    init_root_logger(verbose)

    log.info("Starting tests ...")

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTest(TestSyslogTestcase('test_import_modules', verbose))
    suite.addTest(TestSyslogTestcase('test_logging_syslog', verbose))
    suite.addTest(TestSyslogTestcase('test_unix_syslog', verbose))

    runner = unittest.TextTestRunner(verbosity = verbose)

    result = runner.run(suite)


#==============================================================================

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
