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
import syslog
import os.path
import sys
#import copy

# Third party modules

# Own modules
#import pb_provisioning.common

#from pb_provisioning.common import to_unicode_or_bust, to_utf8_or_bust

__author__ = 'Frank Brehm <frank.brehm@profitbricks.com>'
__copyright__ = '(C) 2010-2012 by profitbricks.com'
__contact__ = 'frank.brehm@profitbricks.com'
__version__ = '0.1.0'
__license__ = 'GPL3'

#==============================================================================

class UnixSyslogHandler(logging.Handler):
    '''
    A handler class which sends formatted logging records over
    the C API.
    '''

    # from <linux/sys/syslog.h>:
    # ======================================================================
    # priorities/facilities are encoded into a single 32-bit quantity, where
    # the bottom 3 bits are the priority (0-7) and the top 28 bits are the
    # facility (0-big number). Both the priorities and the facilities map
    # roughly one-to-one to strings in the syslogd(8) source code.  This
    # mapping is included in this file.
    #
    # priorities (these are ordered)

    LOG_EMERG     = syslog.LOG_EMERG        #  system is unusable
    LOG_ALERT     = syslog.LOG_ALERT        #  action must be taken immediately
    LOG_CRIT      = syslog.LOG_CRIT         #  critical conditions
    LOG_ERR       = syslog.LOG_ERR          #  error conditions
    LOG_WARNING   = syslog.LOG_WARNING      #  warning conditions
    LOG_NOTICE    = syslog.LOG_NOTICE       #  normal but significant condition
    LOG_INFO      = syslog.LOG_INFO         #  informational
    LOG_DEBUG     = syslog.LOG_DEBUG        #  debug-level messages

    #  facility codes
    LOG_KERN      = syslog.LOG_KERN         #  kernel messages
    LOG_USER      = syslog.LOG_USER         #  random user-level messages
    LOG_MAIL      = syslog.LOG_MAIL         #  mail system
    LOG_DAEMON    = syslog.LOG_DAEMON       #  system daemons
    LOG_AUTH      = syslog.LOG_AUTH         #  security/authorization messages
    LOG_LPR       = syslog.LOG_LPR          #  line printer subsystem
    LOG_NEWS      = syslog.LOG_NEWS         #  network news subsystem
    LOG_UUCP      = syslog.LOG_UUCP         #  UUCP subsystem
    LOG_CRON      = syslog.LOG_CRON         #  clock daemon

    #  other codes through 15 reserved for system use
    LOG_LOCAL0    = syslog.LOG_LOCAL0       #  reserved for local use
    LOG_LOCAL1    = syslog.LOG_LOCAL1       #  reserved for local use
    LOG_LOCAL2    = syslog.LOG_LOCAL2       #  reserved for local use
    LOG_LOCAL3    = syslog.LOG_LOCAL3       #  reserved for local use
    LOG_LOCAL4    = syslog.LOG_LOCAL4       #  reserved for local use
    LOG_LOCAL5    = syslog.LOG_LOCAL5       #  reserved for local use
    LOG_LOCAL6    = syslog.LOG_LOCAL6       #  reserved for local use
    LOG_LOCAL7    = syslog.LOG_LOCAL7       #  reserved for local use

    # options for syslog.openlog()
    # LOG_PID, LOG_CONS, LOG_NDELAY, LOG_NOWAIT
    LOG_PID       = syslog.LOG_PID          # log the pid with each message
    LOG_CONS      = syslog.LOG_CONS         # log on the console if errors in sending
    LOG_NDELAY    = syslog.LOG_NDELAY       # don't delay open
    LOG_NOWAIT    = syslog.LOG_NOWAIT       # if forking to log on console, don't wait()

    priority_names = {
        "alert":    LOG_ALERT,
        "crit":     LOG_CRIT,
        "critical": LOG_CRIT,
        "debug":    LOG_DEBUG,
        "emerg":    LOG_EMERG,
        "err":      LOG_ERR,
        "error":    LOG_ERR,        #  DEPRECATED
        "info":     LOG_INFO,
        "notice":   LOG_NOTICE,
        "panic":    LOG_EMERG,      #  DEPRECATED
        "warn":     LOG_WARNING,    #  DEPRECATED
        "warning":  LOG_WARNING,
    }

    facility_names = {
        "auth":     LOG_AUTH,
        "cron":     LOG_CRON,
        "daemon":   LOG_DAEMON,
        "kern":     LOG_KERN,
        "lpr":      LOG_LPR,
        "mail":     LOG_MAIL,
        "news":     LOG_NEWS,
        "security": LOG_AUTH,       #  DEPRECATED
        "user":     LOG_USER,
        "uucp":     LOG_UUCP,
        "local0":   LOG_LOCAL0,
        "local1":   LOG_LOCAL1,
        "local2":   LOG_LOCAL2,
        "local3":   LOG_LOCAL3,
        "local4":   LOG_LOCAL4,
        "local5":   LOG_LOCAL5,
        "local6":   LOG_LOCAL6,
        "local7":   LOG_LOCAL7,
    }

    priority_map = {
        "DEBUG": "debug",
        "INFO": "info",
        "WARNING": "warning",
        "ERROR": "error",
        "CRITICAL": "critical"
    }

    #--------------------------------------------------------------------------
    def __init__(self, ident = None, logopt = LOG_PID, facility = LOG_USER):
        """
        Initialize a handler.

        @param ident: Identifier of the syslog message, uses basename
                      or current running program, if not given
        @type ident: str
        @param logopt: options for syslog.openlog(), see there for possible
                       values (linked with a binary or). Uses LOG_PID,
                       if not given.
        @type logopt: int
        @param facility: syslog facility to use.
        @type facility: int

        """

        logging.Handler.__init__(self)

        if ident is not None:
            ident = ident.strip()
            if ident == '':
                ident = None
        if ident is None:
            ident = os.path.basename(sys.argv[0])

        self.ident = ident
        """
        @ivar: Identifier of the syslog message.
        @type: str
        """

        self.logopt = logopt
        """
        @ivar: options for syslog.openlog()
        @type: int
        """

        self.facility = facility
        """
        @ivar: syslog facility to use
        @type: int
        """

        self.formatter = None

        syslog.openlog(self.ident, self.logopt, self.facility)

    #--------------------------------------------------------------------------
    def close (self):
        """
        Closes the handler.
        """

        syslog.closelog()
        logging.Handler.close(self)

    #--------------------------------------------------------------------------
    def map_priority(self, level_name):
        """
        Map a logging level name to a key in the priority_names map.
        This is useful in two scenarios: when custom levels are being
        used, and in the case where you can't do a straightforward
        mapping by lowercasing the logging level name because of locale-
        specific issues (see SF #1524081).

        If no valid level name was given, "warning" is assumed.

        @param level_name: the level name, which should be mapped
        @type level_name: str

        @return: the numeric logging level code
        @rtype: int

        """

        prio = self.priority_map.get(level_name, "warning")
        return self.priority_names.get(prio, self.LOG_WARNING)

    #--------------------------------------------------------------------------
    def emit(self, record):
        """
        Emit a record.

        The record is formatted, and then sent to the syslog server. If
        exception information is present, it is NOT sent to the server.
        """

        msg = self.format(record)
        if isinstance(msg, basestring):
            if isinstance(msg, unicode):
                msg = msg.encode('utf-8')

        level = self.map_priority(record.levelname)

        try:
            syslog.syslog(level, msg)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

#==============================================================================

if __name__ == "__main__":

    pass

#==============================================================================

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 nu
