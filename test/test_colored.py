#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Frank Brehm
@contact: frank.brehm@profitbricks.com
@organization: Profitbricks GmbH
@copyright: © 2010 - 2015 by Profitbricks GmbH
@license: GPL3
@summary: additional logging formatter for colored output via console
'''

import os
import sys
import logging

try:
    import unittest2 as unittest
except ImportError:
    import unittest

libdir = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..'))
sys.path.insert(0, libdir)

import general
from general import PbLoggingTestcase, get_arg_verbose, init_root_logger

log = logging.getLogger('test_colored')


#==============================================================================
class TestColoredFormatter(PbLoggingTestcase):

    #--------------------------------------------------------------------------
    def setUp(self):
        pass

    #--------------------------------------------------------------------------
    def test_import_modules(self):

        log.info("Test importing all appropriate modules ...")

        log.debug("Importing ColoredFormatter from pb_logging.colored ...")
        from pb_logging.colored import ColoredFormatter

    #--------------------------------------------------------------------------
    def test_colorcode(self):

        log.info("Testing colored output ...")

        from pb_logging.colored import COLOR_CODE
        from pb_logging.colored import colorstr

        msg = "Colored output"

        print('')
        for key in sorted(COLOR_CODE.keys()):

            try:
                print('%s: %s' % (key, colorstr(msg, key)))
            except Exception as e:
                self.fail("Failed to generate colored string %r with %s: %s" % (
                        key, e.__class__.__name__, str(e)))

    #--------------------------------------------------------------------------
    def test_object(self):

        log.info("Testing init of a ColoredFormatter object ...")

        from pb_logging.colored import ColoredFormatter

        try:
            formatter = ColoredFormatter(
                    '%(name)s: %(message)s (%(filename)s:%(lineno)d)')
        except Exception as e:
            self.fail("Could not instatiate ColoredFormatter object with %s: %s" % (
                    e.__class__.__name__, str(e)))

#==============================================================================

if __name__ == '__main__':

    verbose = get_arg_verbose()
    if verbose is None:
        verbose = 0
    init_root_logger(verbose)

    log.info("Starting tests ...")

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTest(TestColoredFormatter('test_import_modules', verbose))
    suite.addTest(TestColoredFormatter('test_colorcode', verbose))
    suite.addTest(TestColoredFormatter('test_object', verbose))

    runner = unittest.TextTestRunner(verbosity = verbose)

    result = runner.run(suite)

#==============================================================================

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
