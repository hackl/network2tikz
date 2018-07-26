#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# =============================================================================
# File      : test_network2tikz.py
# Creation  : 21 May 2018
# Time-stamp: <Don 2018-07-26 16:39 juergen>
#
# Copyright (c) 2018 Jürgen Hackl <hackl@ibi.baug.ethz.ch>
#               http://www.ibi.ethz.ch
# $Id$
#
# Description : Test functions for converting networks to tikz-networks
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

import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
#from cnet import Node, Edge, Network
from network2tikz.canvas import Canvas
from network2tikz.units import UnitConverter


def test_canvas():
    canvas = Canvas()

    assert canvas.width == 6
    assert canvas.height == 6

    canvas.width = 10
    canvas.height = 8

    assert canvas.width == 10
    assert canvas.height == 8

    canvas = Canvas(4, 3)

    assert canvas.width == 4
    assert canvas.height == 3

    canvas = Canvas()

    assert isinstance(canvas.margins(), dict)
    assert canvas.margins()['top'] == 0.35

    assert canvas.margins(1)['top'] == 1

    margins = canvas.margins({'top': 2, 'left': 1, 'bottom': 2, 'right': .5})
    assert margins['top'] == 2 and margins['left'] == 1 and \
        margins['bottom'] == 2 and margins['right'] == .5

    with pytest.raises(Exception):
        canvas.margins(3)

    canvas = Canvas(6, 4, margins=0)
    layout = {'a': (-1, -1), 'b': (1, -1), 'c': (1, 1), 'd': (-1, 1)}

    l = canvas.fit(layout)
    assert l['a'] == (1, 0)
    assert l['b'] == (5, 0)
    assert l['c'] == (5, 4)
    assert l['d'] == (1, 4)

    l = canvas.fit(layout, keep_aspect_ratio=False)
    assert l['a'] == (0, 0)
    assert l['b'] == (6, 0)
    assert l['c'] == (6, 4)
    assert l['d'] == (0, 4)


def test_unit_converter():
    mm2cm = UnitConverter('mm', 'cm')

    assert mm2cm(10) == 1
    assert mm2cm.convert(10) == 1

    with pytest.raises(Exception):
        mm2m = UnitConverter('mm', 'm')
        mm2m(100)

# =============================================================================
# eof
#
# Local Variables:
# mode: python
# mode: linum
# mode: auto-fill
# fill-column: 80
# End:
