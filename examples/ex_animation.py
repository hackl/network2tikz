#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# =============================================================================
# File      : ex_animation.py
# Creation  : 24 November 2018
# Time-stamp: <Sam 2018-11-24 08:46 juergen>
#
# Copyright (c) 2018 Jürgen Hackl <hackl@ibi.baug.ethz.ch>
#               http://www.ibi.ethz.ch
# $Id$
#
# Description : Example for converting a node/edge list to tikz-networks
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
import numpy as np

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from network2tikz import plot


def main():
    # Network
    # -------
    nodes = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    edges = [('a', 'b'), ('a', 'c'), ('b', 'c'), ('b', 'd'), ('d', 'e'), ('d', 'f'),
             ('d', 'g'), ('e', 'f'), ('f', 'g')]
    net = (nodes, edges)

    # Network attributes
    # ------------------
    layout = {'a': (0, 0), 'b': (1, 1), 'c': (0, 2), 'd': (2, 1), 'e': (3, 2),
              'f': (4, 1), 'g': (3, 0)}

    # Network transition matrix
    # -------------------------
    T = np.array([[0, 1/2, 1/2, 0, 0, 0, 0],
                  [1/3, 0, 1/3, 1/3, 0, 0, 0],
                  [1/2, 1/2, 0, 0, 0, 0, 0],
                  [0, 1/4, 0, 0, 1/4, 1/4, 1/4],
                  [0, 0, 0, 1/2, 0, 1/2, 0],
                  [0, 0, 0, 1/3, 1/3, 0, 1/3],
                  [0, 0, 0, 1/2, 0, 1/2, 0]])

    # Starting vector
    x = np.array([1, 0, 0, 0, 0, 0, 0])

    # Visual style dict
    # -----------------
    visual_style = {}

    # node styles
    # -----------
    visual_style['node_size'] = .8
    visual_style['node_color'] = 'red'

    # edge styles
    # -----------
    visual_style['edge_width'] = 2
    visual_style['edge_curved'] = 0.1

    # general options
    # ---------------
    visual_style['layout'] = layout
    visual_style["canvas"] = (10, 7)

    # create images
    # -------------
    for step in range(10):
        # create file name for step n
        filename = '{num:02d}_network.pdf'.format(num=step)

        # get distribution for step n
        values = np.linalg.matrix_power(T, step).transpose().dot(x)

        # change node label
        visual_style['node_label'] = [str(n) for n in np.round(values, 3)]

        # change node oppacity
        visual_style['node_opacity'] = list(values)
        # Create a latex file

        plot(net, filename, **visual_style)


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
