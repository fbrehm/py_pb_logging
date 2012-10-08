==================================
Python ProfitBricks syslog modules
==================================

These are Python modules to extend the logging mechanism in Python.

Author: Frank Brehm (<frank.brehm@profitbricks.com>)


Module pb_syslog.colored.ColoredFormatter
=========================================

Synopsis:
---------

An additional logging formatter for colored output via console.

Usage:
------

import logging
from pb_syslog.colored import ColoredFormatter

logger = logging.getLogger(__name__)

format_str = '%(name)s: %(message)s (%(filename)s:%(lineno)d)'
formatter = ColoredFormatter(format_str)

console = logging.StreamHandler()
console.setFormatter(formatter)
logger.addHandler(console)

logger.debug('Debug')
logger.info('Info')
logger.warning('Warning!')
logger.error('ERROR!')
logger.critical('CRITICAL!!!')


Module pb_syslog.syslog_handler.PbSysLogHandler
===============================================

Synopsis:
---------

A wrapping logging handler for logging.handlers.SysLogHandler
to avoid BOM errors in syslog messages.

Usage:
------

import logging
from pb_syslog.syslog_handler import PbSysLogHandler

logger = logging.getLogger(__name__)

appname = os.path.basename(sys.argv[0])
format_str = appname + ': %(name)s(%(lineno)d) %(funcName)s() ' + '%(levelname)s - %(message)s')
formatter = logging.Formatter(format_str)

lh_syslog = PbSysLogHandler(
        address = '/dev/log',
        facility = logging.handlers.SysLogHandler.LOG_USER,
)
lh_syslog.setFormatter(formatter)
logger.addHandler(lh_syslog)

logger.debug(u'Unicode message.')


Module pb_syslog.unix_handler.UnixSyslogHandler
===============================================

Synopsis:
---------

An additional logging handler for the common logging framework
to combine it with syslog.

Usage:
------

import logging
from pb_syslog.unix_handler import UnixSyslogHandler

logger = logging.getLogger(__name__)

appname = os.path.basename(sys.argv[0])
format_str = appname + ': %(name)s(%(lineno)d) %(funcName)s() ' + '%(levelname)s - %(message)s')
formatter = logging.Formatter(format_str)

lh_syslog = UnixSyslogHandler(
        ident = appname,
        facility = logging.handlers.SysLogHandler.LOG_USER,
)
lh_syslog.setFormatter(formatter)
logger.addHandler(lh_syslog)

logger.debug('Bli bla blub.')

