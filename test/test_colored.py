#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Frank Brehm
@contact: frank.brehm@profitbricks.com
@organization: Profitbricks GmbH
@copyright: (c) 2010-2012 by Profitbricks GmbH
@license: GPL3
@summary: additional logging formatter for colored output via console
'''



import unittest
import os
import sys

libdir = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..'))
sys.path.insert(0, libdir)

import pb_syslog.colored

from pb_syslog.colored import COLOR_CODE
from pb_syslog.colored import colorstr
from pb_syslog.colored import ColoredFormatter


class TestColoredFormatter(unittest.TestCase):

    def setUp(self):
        pass

    def test_colorcode(self):

        msg = "Colored output"

        for key in sorted(COLOR_CODE.keys()):

            try:
                print '%s: %s' % (key, colorstr(msg, key))
            except Exception, e:
                self.fail("Failed to generate colored string %r with %s: %s" % (
                        key, e.__class__.__name__, str(e)))

    def test_object(self):

        try:
            formatter = ColoredFormatter(
                    '%(name)s: %(message)s (%(filename)s:%(lineno)d)')
        except Exception, e:
            self.fail("Could not instatiate ColoredFormatter object with %s: %s" % (
                    e.__class__.__name__, str(e)))

#==============================================================================

if __name__ == '__main__':
    unittest.main()

#==============================================================================

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 nu
