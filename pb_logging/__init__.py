#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author: Frank Brehm
@contact: frank.brehm@profitbricks.com
@copyright: (c) 2010 - 2012 by Frank Brehm, Berlin
@summary: All modules for python logging stuff
"""

__author__ = 'Frank Brehm <frank.brehm@profitbricks.com>'
__copyright__ = '(C) 2010-2012 by profitbricks.com'
__contact__ = 'frank.brehm@profitbricks.com'
__version__ = '0.2.6-1'
__license__ = 'GPL3'

# Standard modules
import sys
import os
import logging
import logging.handlers
import syslog

#------------------------------------------------------------------------------
# Module variables

valid_syslog_facility = {}
'''
a dictionary with all valid syslog facility names as keys and their
integer value as values.
@type: dict
'''

syslog_facility_name = {}
'''
The reverse dictionary to valid_syslog_facility with all facility values
as keys and their names as values.
'''

#==============================================================================
def use_unix_syslog_handler():
    '''
    Use UnixSyslogHandler for logging instead of SyslogHandler.

    @return: using UnixSyslogHandler
    @rtype: bool

    '''

    use_syslog = False
    un = os.uname()
    os_name = un[0].lower()
    if os_name == 'sunos':
        use_syslog = True

    return use_syslog

#==============================================================================
def _init_valid_facilities():
    '''
    Initialise the module variables valid_syslog_facility and
    syslog_facility_name.

    '''

    global valid_syslog_facility, syslog_facility_name

    if use_unix_syslog_handler():

        valid_syslog_facility = {
            'kern': syslog.LOG_KERN,
            'user': syslog.LOG_USER,
            'mail': syslog.LOG_MAIL,
            'daemon': syslog.LOG_DAEMON,
            'auth': syslog.LOG_AUTH,
            'lpr': syslog.LOG_LPR,
            'news': syslog.LOG_NEWS,
            'uucp': syslog.LOG_UUCP,
            'cron': syslog.LOG_CRON,
            'local0': syslog.LOG_LOCAL0,
            'local1': syslog.LOG_LOCAL1,
            'local2': syslog.LOG_LOCAL2,
            'local3': syslog.LOG_LOCAL3,
            'local4': syslog.LOG_LOCAL4,
            'local5': syslog.LOG_LOCAL5,
            'local6': syslog.LOG_LOCAL6,
            'local7': syslog.LOG_LOCAL7,
        }

    else:

        valid_syslog_facility = {
            'kern': logging.handlers.SysLogHandler.LOG_KERN,
            'user': logging.handlers.SysLogHandler.LOG_USER,
            'mail': logging.handlers.SysLogHandler.LOG_MAIL,
            'daemon': logging.handlers.SysLogHandler.LOG_DAEMON,
            'auth': logging.handlers.SysLogHandler.LOG_AUTH,
            'syslog': logging.handlers.SysLogHandler.LOG_SYSLOG,
            'lpr': logging.handlers.SysLogHandler.LOG_LPR,
            'news': logging.handlers.SysLogHandler.LOG_NEWS,
            'uucp': logging.handlers.SysLogHandler.LOG_UUCP,
            'cron': logging.handlers.SysLogHandler.LOG_CRON,
            'authpriv': logging.handlers.SysLogHandler.LOG_AUTHPRIV,
            'local0': logging.handlers.SysLogHandler.LOG_LOCAL0,
            'local1': logging.handlers.SysLogHandler.LOG_LOCAL1,
            'local2': logging.handlers.SysLogHandler.LOG_LOCAL2,
            'local3': logging.handlers.SysLogHandler.LOG_LOCAL3,
            'local4': logging.handlers.SysLogHandler.LOG_LOCAL4,
            'local5': logging.handlers.SysLogHandler.LOG_LOCAL5,
            'local6': logging.handlers.SysLogHandler.LOG_LOCAL6,
            'local7': logging.handlers.SysLogHandler.LOG_LOCAL7,
        }

    syslog_facility_name = {}
    for fac_name in valid_syslog_facility.keys():
        fac_nr = valid_syslog_facility[fac_name]
        syslog_facility_name[fac_nr] = fac_name

#==============================================================================
def get_syslog_facility_name(syslog_facility):
    '''
    Returns the name of the given syslog facility.
    Returns None, if not found.

    @return: syslog facility name
    @rtype: str
    '''

    global valid_syslog_facility, syslog_facility_name

    if syslog_facility in syslog_facility_name:
        return syslog_facility_name[syslog_facility]

    return None

#==============================================================================
def get_syslog_facility_of_name(facility_name):
    '''
    Returns the numeric value of the given syslog facility name.
    Returns None, if not found.

    @return: syslog facility value
    @rtype: int
    '''

    global valid_syslog_facility, syslog_facility_name

    if facility_name in syslog_facility_name:
        return facility_name

    facility_name = facility_name.lower()
    if facility_name in valid_syslog_facility:
        return valid_syslog_facility[facility_name]

    return None

#==============================================================================

_init_valid_facilities()

if __name__ == "__main__":

    import pprint
    import argparse

    arg_parser = argparse.ArgumentParser(
        prog = 'pb_logging/__init__.py',
    )
    arg_parser.add_argument("-v", "--verbosity", action = "count",
            dest = 'verbose', help = 'Increase the verbosity level')
    args = arg_parser.parse_args()

    use_unixsyslog = 'no'
    if use_unix_syslog_handler():
        use_unixsyslog = 'yes'

    print "Using UNIX syslog handler: %s" % (use_unixsyslog)
    print ""

    if args.verbose:
        pretty_printer = pprint.PrettyPrinter(indent = 4)
        print "valid_syslog_facility:\n" + pretty_printer.pformat(
                valid_syslog_facility)
        print ""
        print "syslog_facility_name:\n" + pretty_printer.pformat(
                syslog_facility_name)
        print ""


#==============================================================================
# vim: fileencoding=utf-8 filetype=python ts=4
