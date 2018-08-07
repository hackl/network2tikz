#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# =============================================================================
# File      : ex_igraph_gentoo.py -- Plotting a colaboration network as tikz
# Author    : Juergen Hackl <hackl@ibi.baug.ethz.ch>
# Creation  : 2018-08-07
# Time-stamp: <Die 2018-08-07 11:27 juergen>
#
# Copyright (c) 2018 Juergen Hackl <hackl@ibi.baug.ethz.ch>
# =============================================================================
import os
import sys

import igraph as ig
import networkx as nx


# sys.path.insert(0, os.path.abspath(
#    os.path.join(os.path.dirname(__file__), '..')))

from network2tikz import plot

# Load data into a graph
# ======================
G = ig.Graph.Read_Ncol('./data/gentoo.txt', directed=False)
#G = nx.read_edgelist('./data/gentoo.txt')

# Layout setup
# ============
visual_style = {}
visual_style['node_size'] = .3
visual_style['edge_width'] = 1.1
visual_style['edge_curved'] = 0.1
visual_style["layout"] = 'FR'
visual_style['canvas'] = (20, 20)
visual_style['layout_seed'] = 3
# Plot the network as tex
# =======================
plot(G, "gentoo.pdf", **visual_style)


# =============================================================================
# eof
#
# Local Variables:
# mode: python
# mode: linum
# mode: auto-fill
# fill-column: 80
# End:
