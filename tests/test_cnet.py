#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# =============================================================================
# File      : test_cnet.py
# Creation  : 21 May 2018
# Time-stamp: <Mon 2018-11-05 10:38 juergen>
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

import cnet as cn
from network2tikz import plot, layout


@pytest.fixture
def net():
    net = cn.Network(name='my tikz test network', directed=True)
    net.add_edges_from([('ab', 'a', 'b'), ('ac', 'a', 'c'), ('cd', 'c', 'd'),
                        ('de', 'd', 'e'), ('ec', 'e', 'c'), ('cf', 'c', 'f'),
                        ('fa', 'f', 'a'), ('fg', 'f', 'g'), ('gd', 'g', 'd'),
                        ('gg', 'g', 'g')])

    net.nodes['name'] = ['Alice', 'Bob', 'Claire', 'Dennis', 'Esther', 'Frank',
                         'George']
    net.nodes['age'] = [25, 31, 18, 47, 22, 23, 50]
    net.nodes['gender'] = ['f', 'm', 'f', 'm', 'f', 'm', 'm']

    net.edges['is_formal'] = [False, False, True, True, True, False, True,
                              False, False, False]
    return net


@pytest.fixture
def color_dict():
    return {"m": "blue", "f": "red"}


@pytest.fixture
def shape_dict():
    return {"m": "circle", "f": "rectangle"}


@pytest.fixture
def style_dict():
    return {"m": "{shading=ball}", "f": None}


@pytest.fixture
def _layout():
    layout = {'a': (4.3191, -3.5352), 'b': (0.5292, -0.5292),
              'c': (8.6559, -3.8008), 'd': (12.4117, -7.5239),
              'e': (12.7, -1.7069), 'f': (6.0022, -9.0323),
              'g': (9.7608, -12.7)}
    return layout


def test_plot(net, _layout, color_dict):

    # plot(net) # plot_01.png

    # plot(net,layout=layout) # plot_02.png

    # plot(net, layout=layout, canvas=(8,8), margin=1) # plot_03.png

    visual_style = {}
    visual_style['layout'] = _layout
    visual_style['node_size'] = .5
    visual_style['node_color'] = [color_dict[g] for g in net.nodes('gender')]
    visual_style['node_opacity'] = .7
    visual_style['node_label'] = net.nodes['name']
    visual_style['node_label_position'] = 'below'
    visual_style['edge_width'] = [
        1 + 2 * int(f) for f in net.edges('is_formal')]
    visual_style['edge_curved'] = 0.1
    visual_style['canvas'] = (8, 8)
    visual_style['margin'] = 1

    plot(net, 'network.tex', **visual_style)

    plot(net, 'network.csv', **visual_style)

    plot(net, 'network.pdf', **visual_style)

    plot(net, **visual_style)


def test_plot_all_options(net, _layout, color_dict, shape_dict, style_dict):

    visual_style = {}
    # node styles
    # -----------
    visual_style['node_size'] = 5
    visual_style['node_color'] = [color_dict[g] for g in net.nodes('gender')]
    visual_style['node_opacity'] = .7
    visual_style['node_label'] = net.nodes['name']
    visual_style['node_label_position'] = 'below'
    visual_style['node_label_distance'] = 15
    visual_style['node_label_color'] = 'gray'
    visual_style['node_label_size'] = 3
    visual_style['node_shape'] = [shape_dict[g] for g in net.nodes('gender')]
    visual_style['node_style'] = [style_dict[g] for g in net.nodes('gender')]
    visual_style['node_label_off'] = {'e': True}
    visual_style['node_math_mode'] = [True]
    visual_style['node_label_as_id'] = {'f': True}
    visual_style['node_pseudo'] = {'d': True}

    # edge styles
    # -----------
    visual_style['edge_width'] = [.3 + .3 *
                                  int(f) for f in net.edges('is_formal')]
    visual_style['edge_color'] = 'black'
    visual_style['edge_opacity'] = .8
    visual_style['edge_curved'] = 0.1
    visual_style['edge_label'] = [e for e in net.edges]
    visual_style['edge_label_position'] = 'above'
    visual_style['edge_label_distance'] = .6
    visual_style['edge_label_color'] = 'gray'
    visual_style['edge_label_size'] = {'ac': 5}
    visual_style['edge_style'] = 'dashed'
    visual_style['edge_arrow_size'] = .2
    visual_style['edge_arrow_width'] = .2

    visual_style['edge_loop_size'] = 15
    visual_style['edge_loop_position'] = 90
    visual_style['edge_loop_shape'] = 45
    visual_style['edge_directed'] = [True, True, False, True, True, False, True,
                                     True, True, True]
    visual_style['edge_label'][1] = '\\frac{\\alpha}{\\beta}'
    visual_style['edge_math_mode'] = {'ac': True}
    visual_style['edge_not_in_bg'] = {'fa': True}

    # general options
    # ---------------
    visual_style['unit'] = 'mm'
    visual_style['layout'] = _layout
    visual_style["margin"] = {'top': 5, 'bottom': 8, 'left': 5, 'right': 5}
    visual_style["canvas"] = (100, 60)
    visual_style['keep_aspect_ratio'] = False

    plot(net, 'network.tex', **visual_style)

    plot(net, 'network.csv', **visual_style)

    plot(net, 'network.pdf', **visual_style)

    plot(net, **visual_style)


def test_layout(net):

    layout_style = {}
    layout_style['layout'] = 'fr'
    layout_style['seed'] = 1
    _layout = layout(net, **layout_style)

    plot(net, layout=_layout)


# =============================================================================
# eof
#
# Local Variables:
# mode: python
# mode: linum
# mode: auto-fill
# fill-column: 80
# End:
