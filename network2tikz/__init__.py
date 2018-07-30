#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# =============================================================================
# File      : __init__.py
# Creation  : 21 May 2018
# Time-stamp: <Mon 2018-07-30 15:41 juergen>
#
# Copyright (c) 2018 Jürgen Hackl <hackl@ibi.baug.ethz.ch>
#               http://www.ibi.ethz.ch
# $Id$
#
# Description : init file for the package
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# =============================================================================

from .__about__ import(
    __title__,
    __version__,
    __author__,
    __email__,
    __copyright__,
    __license__,
    __maintainer__,
    __status__,
    __credits__
)

import logging


def logger(name, level='INFO'):
    """A function to generate logger for the modules."""
    # initialize new logger
    logger = logging.getLogger(name)
    # set logger level
    logger.setLevel(logging._nameToLevel[level])
    return logger


from .plot import Plot
from .layout import layout
plot = Plot()

# =============================================================================
# eof
#
# Local Variables:
# mode: python
# mode: linum
# mode: auto-fill
# fill-column: 80
# End:
