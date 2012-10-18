#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@summary: additional logging formatter for colored output via console
"""

# Standard modules
import logging
#import os.path
#import sys
import copy

# Third party modules

# Own modules

#import pb_provisioning.common

#from pb_provisioning.common import to_unicode_or_bust, to_utf8_or_bust

__version__ = '0.1.1'

#==============================================================================
# Color coding module variables and helper functions

COLOR_CODE = {
    'ENDC':              0,  # RESET COLOR
    'BOLD':              1,
    'UNDERLINE':         4,
    'BLINK':             5,
    'INVERT':            7,
    'CONCEALD':          8,
    'STRIKE':            9,
    'GREY30':           90,
    'GREY40':            2,
    'GREY65':           37,
    'GREY70':           97,
    'GREY20_BG':        40,
    'GREY33_BG':       100,
    'GREY80_BG':        47,
    'GREY93_BG':       107,
    'DARK_RED':         31,
    'RED':              91,
    'RED_BG':           41,
    'LIGHT_RED_BG':    101,
    'DARK_YELLOW':      33,
    'YELLOW':           93,
    'YELLOW_BG':        43,
    'LIGHT_YELLOW_BG': 103,
    'DARK_BLUE':        34,
    'BLUE':             94,
    'BLUE_BG':          44,
    'LIGHT_BLUE_BG':   104,
    'DARK_MAGENTA':     35,
    'PURPLE':           95,
    'MAGENTA_BG':       45,
    'LIGHT_PURPLE_BG': 105,
    'DARK_CYAN':        36,
    'AUQA':             96,
    'CYAN_BG':          46,
    'LIGHT_AUQA_BG':   106,
    'DARK_GREEN':       32,
    'GREEN':            92,
    'GREEN_BG':         42,
    'LIGHT_GREEN_BG':  102,
    'BLACK':            30,
}

#------------------------------------------------------------------------------
def termcode(num):

    return '\033[%sm' % (num)

#------------------------------------------------------------------------------
def colorstr(message, color):
    """
    Wrapper function to colorize the message.

    @param message: The message to colorize
    @type message: str
    @param color: The color to use, must be one of the keys of COLOR_CODE
    @type color: str

    @return: the colorized message
    @rtype: str

    """

    tcode = ''
    if isinstance(color, (list, tuple)):
        for c in color:
            tcode += termcode(COLOR_CODE[c])
    else:
        tcode = termcode(COLOR_CODE[color])

    return tcode + message + termcode(COLOR_CODE['ENDC'])

logger = logging.getLogger(__name__)

#==============================================================================

class ColoredFormatter(logging.Formatter):
    # A variant of code found at:
    #  http://stackoverflow.com/questions/384076/how-can-i-make-the-python-logging-output-to-be-colored

    LEVEL_COLOR = {
        'DEBUG':    None,
        'INFO':     'GREEN',
        'WARNING':  'YELLOW',
        'ERROR':    ('BOLD', 'RED'),
        'CRITICAL': 'RED_BG',
    }

    #--------------------------------------------------------------------------
    def __init__(self, msg):

        logging.Formatter.__init__(self, msg)

    #------------------------------------------------------------
    @apply
    def color_debug():
        doc = "The color used to output debug messages."
        def fget(self):
            return self.LEVEL_COLOR['DEBUG']
        def fset(self, value):
            self.LEVEL_COLOR['DEBUG'] = value
        def fdel(self):
            pass
        return property(**locals())

    #------------------------------------------------------------
    @apply
    def color_info():
        doc = "The color used to output info messages."
        def fget(self):
            return self.LEVEL_COLOR['INFO']
        def fset(self, value):
            self.LEVEL_COLOR['INFO'] = value
        def fdel(self):
            pass
        return property(**locals())

    #------------------------------------------------------------
    @apply
    def color_warning():
        doc = "The color used to output warning messages."
        def fget(self):
            return self.LEVEL_COLOR['WARNING']
        def fset(self, value):
            self.LEVEL_COLOR['WARNING'] = value
        def fdel(self):
            pass
        return property(**locals())

    #------------------------------------------------------------
    @apply
    def color_error():
        doc = "The color used to output error messages."
        def fget(self):
            return self.LEVEL_COLOR['ERROR']
        def fset(self, value):
            self.LEVEL_COLOR['ERROR'] = value
        def fdel(self):
            pass
        return property(**locals())

    #------------------------------------------------------------
    @apply
    def color_critical():
        doc = "The color used to output critical messages."
        def fget(self):
            return self.LEVEL_COLOR['CRITICAL']
        def fset(self, value):
            self.LEVEL_COLOR['CRITICAL'] = value
        def fdel(self):
            pass
        return property(**locals())

    #--------------------------------------------------------------------------
    def format(self, record):

        record = copy.copy(record)
        levelname = record.levelname

        if levelname in self.LEVEL_COLOR:

            record.name = colorstr(record.name, 'BOLD')
            record.filename = colorstr(record.filename, 'BOLD')
            record.module = colorstr(record.module, 'BOLD')
            record.funcName = colorstr(record.funcName, 'BOLD')
            record.pathname = colorstr(record.pathname, 'BOLD')
            record.processName = colorstr(record.processName, 'BOLD')
            record.threadName = colorstr(record.threadName, 'BOLD')

            if self.LEVEL_COLOR[levelname] is not None:
                record.levelname = colorstr(levelname, self.LEVEL_COLOR[levelname])
                record.msg = colorstr(record.msg, self.LEVEL_COLOR[levelname])

        return logging.Formatter.format(self, record)


#==============================================================================

if __name__ == "__main__":

    msg = 'Hallo Ballo!'

    for key in sorted(COLOR_CODE.keys()):
        print '%s: %s' % (key, colorstr(msg, key))

    print ""
    print(colorstr('Bold Red', ('BOLD', 'RED')))
    print(colorstr('Normal Red', 'RED'))

    print ""

    logger.setLevel(logging.DEBUG)
    console = logging.StreamHandler()
    console.setFormatter(
        ColoredFormatter('%(name)s: %(message)s (%(filename)s:%(lineno)d)'))
    logger.addHandler(console)

    fh = logging.FileHandler('/tmp/test.log', 'w')
    fh.setFormatter(logging.Formatter('%(name)s: %(message)s'))
    logger.addHandler(fh)

    logger.debug('debug')
    logger.info('info')
    logger.warning('Warning')
    logger.error('ERROR')
    logger.critical('CRITICAL!!!')


#==============================================================================

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 nu
