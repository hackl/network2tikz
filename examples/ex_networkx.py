#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# =============================================================================
# File      : ex_networkx.py 
# Creation  : 21 May 2018
# Time-stamp: <Son 2018-05-27 09:47 juergen>
#
# Copyright (c) 2018 Jürgen Hackl <hackl@ibi.baug.ethz.ch>
#               http://www.ibi.ethz.ch
# $Id$ 
#
# Description : Example for converting igraph networks to tikz-networks
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

import os
import sys

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import networkx as nx
from network2tikz import plot

def main():
    # Network and attributes
    # ----------------------
    net = nx.DiGraph()
    net.add_node('a', name='Alice', age=25, gender='f')
    net.add_node('b', name='Bob', age=31, gender='m')
    net.add_node('c', name='Claire', age=18, gender='f')
    net.add_node('d', name='Dennis', age=47, gender='m')
    net.add_node('e', name='Esther', age=22, gender='f')
    net.add_node('f', name='Frank', age=23, gender='m')
    net.add_node('g', name='George', age=50, gender='m')

    net.add_edge('a','b',is_formal=False)
    net.add_edge('a','c',is_formal=False)
    net.add_edge('c','d',is_formal=True)
    net.add_edge('d','e',is_formal=True)
    net.add_edge('e','c',is_formal=True)
    net.add_edge('c','f',is_formal=False)
    net.add_edge('f','a',is_formal=True)
    net.add_edge('f','g',is_formal=False)
    net.add_edge('g','g',is_formal=False)
    net.add_edge('g','d',is_formal=False)

    # Network dicts
    # -------------
    color_dict = {"m": "blue", "f": "red"}
    shape_dict = {"m": "circle", "f": "rectangle"}
    style_dict = {"m": "{shading=ball}", "f": None}
    layout = {'a': (4.3191, -3.5352), 'b': (0.5292, -0.5292),
              'c': (8.6559, -3.8008), 'd': (12.4117, -7.5239),
              'e': (12.7, -1.7069), 'f': (6.0022, -9.0323),
              'g': (9.7608, -12.7)}

    # Visual style dict
    # -----------------
    visual_style = {}

    # node styles
    # -----------
    visual_style['vertex_size'] = 5
    visual_style['vertex_color'] = {n:color_dict[g] for n,g in nx.get_node_attributes(net,'gender').items()}
    visual_style['vertex_opacity'] = .7
    visual_style['vertex_label'] = nx.get_node_attributes(net,'name')
    visual_style['vertex_label_position'] = 'below'
    visual_style['vertex_label_distance'] = 15
    visual_style['vertex_label_color'] = 'gray'
    visual_style['vertex_label_size'] = 3
    visual_style['vertex_shape'] = {n:shape_dict[g] for n,g in nx.get_node_attributes(net,'gender').items()}
    visual_style['vertex_style'] = {n:style_dict[g] for n,g in nx.get_node_attributes(net,'gender').items()}
    visual_style['vertex_label_off'] = {'e':True}
    visual_style['vertex_math_mode'] = {'a':True}
    visual_style['vertex_label_as_id'] = {'f':True}
    visual_style['vertex_pseudo'] = {'d':True}

    # edge styles
    # -----------
    visual_style['edge_width'] = {e:.3 + .3 * int(f) for e,f in nx.get_edge_attributes(net,'is_formal').items()}
    visual_style['edge_color'] = 'black'
    visual_style['edge_opacity'] = .8
    visual_style['edge_curved'] = 0.1
    visual_style['edge_label'] = {e:e[0]+e[1] for e in net.edges}
    visual_style['edge_label_position'] = 'above'
    visual_style['edge_label_distance'] = .6
    visual_style['edge_label_color'] = 'gray'
    visual_style['edge_label_size'] = {('a','c'):5}
    visual_style['edge_style'] = 'dashed'
    visual_style['edge_arrow_size'] = .2
    visual_style['edge_arrow_width'] = .2
    visual_style['edge_loop_size'] = 15
    visual_style['edge_loop_position'] = 90
    visual_style['edge_loop_shape'] = 45
    visual_style['edge_directed'] = {('a','b'):True, ('a','c'):True,
                                     ('c','d'):False, ('d','e'):True,
                                     ('e','c'):True, ('c','f'):False,
                                     ('f','a'):True, ('f','g'):True,
                                     ('g','g'):True}
    visual_style['edge_label'][('a','c')] = '\\frac{\\alpha}{\\beta}'
    visual_style['edge_math_mode'] = {('a','c'):True}
    visual_style['edge_not_in_bg'] = {('f','a'):True}

    # general options
    # ---------------
    visual_style['unit'] = 'mm'
    visual_style['layout'] = layout
    visual_style["margin"] = {'top':5,'bottom':8,'left':5,'right':5}
    visual_style["canvas"] = (100,60)
    visual_style['keep_aspect_ratio'] = False

    # Create a latex file
    plot(net,'network.tex',**visual_style)

    # Create a node and edge list used by tikz-network

    # plot(net,'network.csv',**visual_style)

    # Create pdf figure of the network
    # ONLY POSSIBLE IF tikz-network IS INSTALLED
    # AND (for Widows OS) COMPLETER HAS TO BE SET RIGHT

    # plot(net,'network.pdf',**visual_style)

    # Create temp pdf and show the output
    # ONLY POSSIBLE IF tikz-network IS INSTALLED
    # AND (for Widows OS) COMPLETER HAS TO BE SET RIGHT

    # plot(net,**visual_style)


if __name__ == '__main__':
    main()

# =============================================================================
# eof
#
# Local Variables: 
# mode: python
# mode: linum
# mode: auto-fill
# fill-column: 80
# End:  
