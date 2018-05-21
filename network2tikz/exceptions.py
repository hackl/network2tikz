#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# =============================================================================
# File      : exceptions.py 
# Creation  : 30 Apr 2018
# Time-stamp: <Fre 2018-05-04 10:14 juergen>
#
# Copyright (c) 2018 Jürgen Hackl <hackl@ibi.baug.ethz.ch>
#               http://www.ibi.ethz.ch
# $Id$ 
#
# Description : Module with the base exceptions
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


class CnetException(Exception):
    """Base class for all cnet specific exceptions."""

class CnetError(CnetException):
    """Exception for a serious error in cnet"""

class CnetNotImplemented(CnetException):
    """Exception for procedure not implemented in cnet."""


    
# =============================================================================
# eof
#
# Local Variables: 
# mode: python
# mode: linum
# mode: auto-fill
# fill-column: 80
# End:  
