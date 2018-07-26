#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# =============================================================================
# File      : test_layout.py
# Creation  : 17 July 2018
# Time-stamp: <Don 2018-07-26 16:39 juergen>
#
# Copyright (c) 2018 Jürgen Hackl <hackl@ibi.baug.ethz.ch>
#               http://www.ibi.ethz.ch
# $Id$
#
# Description : Test functions for converting cnet networks to tikz-networks
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

from network2tikz import plot


@pytest.fixture
def net():
    nodes = ['a', 'b', 'c']
    edges = [('a', 'b'), ('b', 'c')]
    return nodes, edges


def test_layout(net):

    visual_style = {}
    visual_style['layout'] = {'a': (0, 0), 'b': (0, 0), 'c': (0, 0)}
    visual_style['keep_aspect_ratio'] = False
    plot(net, **visual_style)

    visual_style = {}
    visual_style['layout'] = {'a': (0, 0), 'b': (0, 0), 'c': (1, 0)}
    visual_style['keep_aspect_ratio'] = False
    plot(net, **visual_style)

    visual_style = {}
    visual_style['layout'] = {'a': (0, 0), 'b': (0, 0), 'c': (0, 1)}
    visual_style['keep_aspect_ratio'] = False
    plot(net, **visual_style)


# test_layout(net())

# =============================================================================
# eof
#
# Local Variables:
# mode: python
# mode: linum
# mode: auto-fill
# fill-column: 80
# End:
