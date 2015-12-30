#!/usr/bin/env python
# encoding: utf-8

"""
Add colors to Streamhandler.

Patches Streamhandler's emit method to add ANSI colors to output.
Colors for each loglevel can be specified via a dictionary.
ANSI codes are only added if stream is not redirected.

Example usage:

>>> import logging
>>> from pb_logging.colorer import Colors, add_colors_to_streamhandler
>>> colordict = {logging.ERROR: Colors.RED, logging.WARN: Colors.YELLOW}
>>> add_colors_to_streamhandler({logging.ERROR: Colors.RED})

"""

import logging
import os
import sys


# =============================================================================
class Colors:
    ENDC = 0
    BOLD = 1
    UNDERLINE = 4
    BLINK = 5
    INVERT = 7
    CONCEALD = 8
    STRIKE = 9
    GREY30 = 90
    GREY40 = 2
    GREY65 = 37
    GREY70 = 97
    GREY20_BG = 40
    GREY33_BG = 100
    GREY80_BG = 47
    GREY93_BG = 107
    DARK_RED = 31
    RED = 91
    RED_BG = 41
    LIGHT_RED_BG = 101
    DARK_YELLOW = 33
    YELLOW = 93
    YELLOW_BG = 43
    LIGHT_YELLOW_BG = 103
    DARK_BLUE = 34
    BLUE = 94
    BLUE_BG = 44
    LIGHT_BLUE_BG = 104
    DARK_MAGENTA = 35
    PURPLE = 95
    MAGENTA_BG = 45
    LIGHT_PURPLE_BG = 105
    DARK_CYAN = 36
    AUQA = 96
    CYAN_BG = 46
    LIGHT_AUQA_BG = 106
    DARK_GREEN = 32
    GREEN = 92
    GREEN_BG = 42
    LIGHT_GREEN_BG = 102
    BLACK = 30

    @staticmethod
    def colorize(text, color):
        return '\x1b[{0}m{1}\x1b[{2}m'.format(color, text, Colors.ENDC)


# =============================================================================
def stdout_is_redirected():
    """ Check if stdout is redirected """
    return os.fstat(0) != os.fstat(1)


# =============================================================================
def stderr_is_redirected():
    """ Check if stderr is redirected """
    return os.fstat(0) != os.fstat(2)


# =============================================================================
def add_colors_to_streamhandler(colordict=None):
    """
    Patches Streamhandler to log colorized output.
    :param colordict: A dictionary with loglevel:color
    :type colordict: dict
    """
    if not colordict:
        colordict = {
            logging.CRITICAL:   Colors.YELLOW,
            logging.ERROR:      Colors.RED,
            logging.WARN:       Colors.DARK_YELLOW,
        }

    def add_coloring_to_emit_ansi(fn):
        # add methods we need to the class
        def new(*args):
            # Only add color if stream is not redirected
            self = args[0]
            if (self.stream == sys.stdout and stdout_is_redirected()) \
                    or (self.stream == sys.stderr and stderr_is_redirected()):
                return fn(*args)

            levelno = args[1].levelno
            if levelno in colordict:
                color = colordict[levelno]
                args[1].msg = Colors.colorize(args[1].msg, color)

            return fn(*args)
        return new

    logging.StreamHandler.emit = \
        add_coloring_to_emit_ansi(logging.StreamHandler.emit)

# =============================================================================
if __name__ == '__main__':

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    add_colors_to_streamhandler({
        logging.ERROR: Colors.RED,
        logging.CRITICAL: Colors.RED_BG,
        logging.WARNING: Colors.YELLOW,
        logging.INFO: Colors.GREEN,
    })

    logger.debug("test blub")
    logger.info("test blub")
    logger.warn("test blub")
    logger.error("test blub")
    logger.critical("test blub")

# =============================================================================

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
