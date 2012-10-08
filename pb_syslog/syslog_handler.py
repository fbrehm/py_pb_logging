#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Frank Brehm
@contact: frank.brehm@profitbricks.com
@organization: Profitbricks GmbH
@copyright: (c) 2010-2012 by Profitbricks GmbH
@license: GPL3
@summary: wrapping logging handler for logging.handlers.SysLogHandler
          to avoid BOM errors in syslog messages
'''

# Standard modules
import logging
import logging.handlers
import socket

from logging.handlers import SysLogHandler

# Third party modules

# Own modules

__author__ = 'Frank Brehm <frank.brehm@profitbricks.com>'
__copyright__ = '(C) 2010-2012 by profitbricks.com'
__contact__ = 'frank.brehm@profitbricks.com'
__version__ = '0.1.0'
__license__ = 'GPL3'

#==============================================================================

class PbSysLogHandler(SysLogHandler):
    """
    A wrapper  logging handler for logging.handlers.SysLogHandler
    to avoid BOM errors in syslog messages.
    """

   def __init__(self,
            address = ('localhost', SYSLOG_UDP_PORT),
            facility = LOG_USER,
            socktype = socket.SOCK_DGRAM,
            encoding = "utf-8",
            ):
        """  
        Initialize the PbSysLogHandler.

        To log to a local syslogd, "PbSysLogHandler(address = "/dev/log")"
        can be used.

        If facility is not specified, LOG_USER is used.

        @param address: either the network socket of the syslog daemon (if given
                        as tuple) or the filename of the UNIX socket of
                        the syslog daemon (if given as str).
        @type address: tuple or str
        @param facility: syslog facility to use
        @type facility: int
        @param socktype: the socket type (socket.SOCK_DGRAM or
                         socket.SOCK_STREAM) to use
        @type socktype: int
        @param encoding: the character set to use to encode unicode messages
        @type encoding: str

        """

        # Initialisation of the parent object
        super(PbSysLogHandler, self).__init__(address, facility, socktype)

        self.encoding = encoding
        """ 
        @ivar: the character set to use to encode unicode messages
        @type: str
        """

    #--------------------------------------------------------------------------
    def emit(self, record):
        """
        Wrapper method for SysLogHandler.emit() to encode an unicode message
        to UTF-8 (or whatever).
        """

        msg = record.msg
        if isinstance(msg, unicode):
            msg = msg.encode(self.encoding)
            record.msg = msg

        super(PbSysLogHandler, self).emit(record)

#==============================================================================

if __name__ == "__main__":

    pass

#==============================================================================

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 nu
