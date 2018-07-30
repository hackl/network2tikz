#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# =============================================================================
# File      : test_overlay.py -- Test environment for overlaying networks
# Author    : Juergen Hackl <hackl@ibi.baug.ethz.ch>
# Creation  : 2018-07-30
# Time-stamp: <Mon 2018-07-30 16:08 juergen>
#
# Copyright (c) 2018 Juergen Hackl <hackl@ibi.baug.ethz.ch>
# =============================================================================

import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

#from network2tikz import plot
from network2tikz.layout import Layout, layout
from network2tikz import plot
import cnet as cn


@pytest.fixture
def net_1():
    net = cn.Network(name='my tikz test network number 1', directed=True)
    net.add_edges_from([('ab', 'a', 'b'), ('bc', 'b', 'c')])
    return net


@pytest.fixture
def net_2():
    net = cn.Network(name='my tikz test network number 2', directed=True)
    net.add_edges_from([('uv', 'u', 'v'), ('vw', 'v', 'w')])
    return net


def test_overlay(net_1, net_2):

    visual_style_1 = {}
    visual_style_1['layout'] = {'a': (0, 0), 'b': (1, 0), 'c': (2, 0)}
    visual_style_1['node_color'] = 'green'
    visual_style_1["canvas"] = (10, 10)
    visual_style_1['yshift'] = -1
    # plot(net_1, **visual_style_1)

    visual_style_2 = {}
    visual_style_2['layout'] = {'u': (0, 1), 'v': (1, 1), 'w': (2, 1)}
    visual_style_2['node_color'] = 'red'
    visual_style_2["canvas"] = (10, 10)
    visual_style_2['yshift'] = 1
    # plot(net_2, **visual_style_2)

    plot.add(net_1, **visual_style_1)
    plot.add(net_2, **visual_style_2)
    plot.show()
    # plot.save('test.tex')


# =============================================================================
# eof
#
# Local Variables:
# mode: python
# mode: linum
# mode: auto-fill
# fill-column: 80
# End:
