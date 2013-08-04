#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@summary: wrapping logging handler for logging.handlers.SysLogHandler
          to avoid BOM errors in syslog messages
"""

# Standard modules
import logging
import logging.handlers
import socket
import sys
import os
import stat
import errno

from logging.handlers import SYSLOG_UDP_PORT
from logging.handlers import SysLogHandler

# Third party modules

# Own modules

__version__ = '0.2.0'

#==============================================================================

class PbSysLogHandler(SysLogHandler):
    """
    A wrapper  logging handler for logging.handlers.SysLogHandler
    to avoid BOM errors in syslog messages.
    """

    def __init__(self,
            address = ('localhost', SYSLOG_UDP_PORT),
            facility = SysLogHandler.LOG_USER,
            socktype = None
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
                         socket.SOCK_STREAM) to use.
                         Not used in Python2 <= 2.6 and Python3 <= 3.1.
        @type socktype: int
        @param encoding: the character set to use to encode unicode messages
        @type encoding: str

        """

        # Initialisation of the parent object
        do_socktype = False
        do_ux_socket = False

        if sys.version_info[0] > 2:
            if sys.version_info[1] > 1:
                do_socktype = True
        else:
            if sys.version_info[1] > 6:
                do_socktype = True

        if isinstance(address, basestring):
            if not os.path.exists(address):
                raise OSError(errno.ENOENT, "File doesn't exists", address)
            mode = os.stat(sddress).st_mode
            if not stat.S_ISSOCK(mode):
                raise OSError(errno.EPERM, "File is not a UNIX socket file", address)
            if not os.access(address, os.W_OK):
                raise OSError(errno.EPERM, "No write access to socket", address)

            do_ux_socket = True

        if do_socktype and not do_ux_socket:
            SysLogHandler.__init__(self, address, facility, socktype)
        else:
            SysLogHandler.__init__(self, address, facility)

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

        SysLogHandler.emit(self, record)

#==============================================================================

if __name__ == "__main__":

    pass

#==============================================================================

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 nu
