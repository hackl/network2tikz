#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# =============================================================================
# File      : plot.py
# Creation  : 08 May 2018
# Time-stamp: <Son 2018-07-29 16:04 juergen>
#
# Copyright (c) 2018 Jürgen Hackl <hackl@ibi.baug.ethz.ch>
#               http://www.ibi.ethz.ch
# $Id$
#
# Description : Module to plot networks as tikz-network
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
import subprocess
import errno
import webbrowser

from . import logger
from .exceptions import CnetError
from .drawing import TikzNetworkDrawer

log = logger(__name__)


def plot(network, filename=None, type=None, **kwds):
    """Plots the network as a tikz-network.

    This function generates a plot of the network, thereby different output can
    be chosen, including a standalone tex file, the tikz code, a compiled pdf or
    a node and edge list which also can be used with the tikz-network library.

    The plot function supports different network types. Currently supported are:

    * 'cnet',
    * 'networkx',
    * 'igraph',
    * 'pathpy'
    * node/edge list

    The appearance of the plot can be modified by keyword arguments which will
    be explained in more detail below. The arguments follow the options
    available in the tikz-network library.

    Note
    ----
    All the options are described in more detail in the tikz-library [tn]_.

    Parameters
    ----------

    network : network object
        Network to be drawn. The network can be a 'cnet', 'networkx', 'igraph',
        'pathpy' object, or a tuple of a node list and edge list.

    filename : file, string or None, optional (default = None)
        File or filename to save. The file ending specifies the
        output. i.e. is the file ending with '.tex' a tex file will be
        created; if the file ends with '.pdf' a pdf is created; if the file
        ends with '.csv', two csv files are generated (filename_nodes.csv
        and filename_edges.csv). If the filename is a tuple of strings, the
        first entry will be used to name the node list and the second entry
        for the edge list; and if no ending and no type is defined a
        temporary pdf file is compiled and shown.

    type : str or None, optional (default = None)
        Type of the output file. If no ending is defined trough the filename,
        the type of the output file can be specified by the type
        option. Currently the following output types are supported:
        'tex', 'pdf', 'csv' and 'dat'.

    kwds : keyword arguments, optional (default= no attributes)
        Attributes used to modify the appearance of the plot.
        For details see below.


    Keyword arguments used for the plotting:

    **Nodes:**

    - ``node_size`` : size of the node. The default is 0.6 cm.

    - ``node_color`` : color of the nodes. The default is light blue. Colors can
      be specified either by common color names, or by 3-tuples of floats
      (ranging between 0 and 255 for the R, G and B components).

    - ``node_opacity`` : opacity of the nodes. The default is 1. The range of the
      number lies between 0 and 1. Where 0 represents a fully transparent fill
      and 1 a solid fill.

    - ``node_label`` : labels drawn next to the nodes.

    - ``node_label_position`` : Per default the position of the label is in the
      center of the node. Classical Tikz commands can be used to change the
      position of the label. Instead, using such command, the position can be
      determined via an angle, by entering a number between -360 and 360. The
      origin (0) is the y axis. A positive number change the position counter
      clockwise, while a negative number make changes clockwise.

    - ``node_label_distance`` : distance between the node and the label.

    - ``node_label_color`` : color of the label.

    - ``node_label_size`` : font size of the label.

    - ``node_shape`` : shape of the vertices. Possibilities are:
      'circle', 'rectangle',  'triangle', and any other Tikz shape

    - ``node_style`` : Any other Tikz style option or command can be entered via
      the option style. Most of these commands can be found in the "TikZ and
      PGF Manual". Contain the commands additional options (e.g. shading =
      ball), then the argument for the style has to be between { } brackets.

    - ``node_layer`` : the node can be assigned to a specific layer.

    - ``node_label_off`` : is Boolean option which suppress all labels.

    - ``node_label_as_id`` : is a Boolean option which assigns the node id as label.

    - ``node_math_mode`` : is a Boolean option which transforms the labels into
      mathematical expressions without using the $ $ environment.

    - ``node_pseudo`` : is a Boolean option which creates a pseudo node, where only
      the node name and the node coordinate will be provided.

    **Edges:**

    - ``edge_width`` : width of the edges. The default unit is point (pt).

    - ``edge_color`` : color of the edges. The default is gray. Colors can
      be specified either by common color names, or by 3-tuples of floats
      (ranging between 0 and 255 for the R, G and B components).

    - ``edge_opacity`` : opacity of the edges. The default is 1. The range of the
      number lies between 0 and 1. Where 0 represents a fully transparent fill
      and 1 a solid fill.

    - ``edge_curved`` : whether the edges should be curved. Positive numbers
      correspond to edges curved in a counter-clockwise direction, negative
      numbers correspond to edges curved in a clockwise direction. Zero
      represents straight edges.

    - ``edge_label`` : labels drawn next to the edges.

    - ``edge_label_position`` : Per default the label is positioned in between
      both nodes in the center of the line. Classical Tikz commands can be used to
      change the position of the label.

    - ``edge_label_distance`` : The label position between the nodes can be
      modified with the distance option. Per default the label is centered
      between both nodes. The position is expressed as the percentage of the
      length between the nodes, e.g. of distance = 0.7, the label is placed at
      70% of the edge length away of Vertex i.

    - ``edge_label_color`` : color of the label.

    - ``edge_label_size`` : font size of the label.

    - ``edge_style`` : Any other Tikz style option or command can be entered via
      the option style. Most of these commands can be found in the "TikZ and
      PGF Manual". Contain the commands additional options (e.g. shading =
      ball), then the argument for the style has to be between { } brackets.

    - ``edge_arrow_size`` : arrow size of the edges.

    - ``edge_arrow_width`` : width of the arrowhead on the edge.

    - ``edge_loop_size`` :  modifies the length of the edge. The measure value has
      to be insert together with its units. Per default the loop size is 1 cm.

    - ``edge_loop_position`` : The position of the self-loop is defined via the
      rotation angle around the node. The origin (0) is the y axis. A positive
      number change the loop position counter clockwise, while a negative
      number make changes clockwise.

    - ``edge_loop_shape`` : The shape of the self-loop is defined by the enclosing
      angle. The shape can be changed by decreasing or increasing the argument
      value of the loop shape option.

    - ``edge_directed`` : is a Boolean option which transform edges to directed
      arrows. If the network is already defined as directed network this option
      is not needed, except to turn off the direction for one or more edges.

    - ``edge_math_mode`` : is a Boolean option which transforms the labels into
      mathematical expressions without using the $ $ environment.

    - ``edge_not_in_bg`` : Per default, the edge is drawn on the background layer
      of the tikz picture. I.e. objects which are created after the edges
      appear also on top of them. To turn this off, the option edge_not_in_bg
      has to be enabled.

    **Layout:**

    NOTE: All layout arguments can be entered with or without 'layout_' at the
    beginning, e.g. 'layout_iterations' is equal to 'iterations'

    - ``layout`` : dict or string , optional (default = None)
      A dictionary with the node positions on a 2-dimensional plane. The
      key value of the dict represents the node id while the value
      represents a tuple of coordinates (e.g. n = (x,y)). The initial
      layout can be placed anywhere on the 2-dimensional plane.

      Instead of a dictionary, the algorithm used for the layout can be defined
      via a string value. Currently, supported are:

      * Random layout, where the nodes are uniformly at random placed in the
        unit square. This algorithm can be enabled with the keywords: 'Random',
        'random', 'rand', or None

      * Fruchterman-Reingold force-directed algorithm. In this algorithm, the
        nodes are represented by steel rings and the edges are springs between
        them. The attractive force is analogous to the spring force and the
        repulsive force is analogous to the electrical force. The basic idea is
        to minimize the energy of the system by moving the nodes and changing
        the forces between them. This algorithm can be enabled with the
        keywords: 'Fruchterman-Reingold', 'fruchterman_reingold', 'fr',
        'spring_layout', 'spring layout', 'FR'

        ==================== ==================================================
        Algorithms           Keywords
        ==================== ==================================================
        Random               Random, random, rand, None
        Fruchterman-Reingold Fruchterman-Reingold, fruchterman_reingold, fr
                             spring_layout, spring layout, FR
        ==================== ==================================================

    - ``force`` : float, optional (default = None)
      Optimal distance between nodes.  If None the distance is set to
      1/sqrt(n) where n is the number of nodes.  Increase this value to move
      nodes farther apart.

    - ``positions`` : dict or None  optional (default = None)
      Initial positions for nodes as a dictionary with node as keys and values
      as a coordinate list or tuple.  If None, then use random initial
      positions.

    - ``fixed`` : list or None, optional (default = None)
      Nodes to keep fixed at initial position.

    - ``iterations`` : int, optional (default = 50)
      Maximum number of iterations taken

    - ``threshold``: float, optional (default = 1e-4)
      Threshold for relative error in node position changes.  The iteration
      stops if the error is below this threshold.

    - ``weight`` : string or None, optional (default = None)
      The edge attribute that holds the numerical value used for the edge
      weight.  If None, then all edge weights are 1.

    - ``dimension`` : int, optional (default = 2)
      Dimension of layout. Currently, only plots in 2 dimension are supported.

    - ``seed`` : int or None, optional (default = None)
      Set the random state for deterministic node layouts. If int, `seed` is
      the seed used by the random number generator, if None, the a random seed
      by created by the numpy random number generator is used.

    **General Options:**

    - ``units`` : string or tuple of strings, optional (default = ('cm','pt'))
      Per default, all size values are based on cm, and all line widths are
      defined in pt units. Whit this option the input units can be
      changed. Currently supported are: Pixel 'px', Points 'pt',
      Millimeters 'mm', and Centimeters 'cm'. If a single value is entered as
      unit all inputs have to be defined using this unit. If a tuple of units
      is given, the sizes are defined with the first entry the line widths with
      the second entry.

    - ``margins`` : None, int, float or dict, optional (default = None)
      The margins define the 'empty' space from the canvas border. If no
      margins are defined, the margin will be calculated based on the maximum
      node size, to avoid clipping of the nodes. If a single int or float is
      defined all margins using this distances. To define different the margin
      sizes for all size a dictionary with in the form of
      `{'top':2,'left':1,'bottom':2,'right':.5}` has to be used.

    - ``canvas`` : None, tuple of int or floats, optional (default = (6,6))
      Canvas or figure_size defines the size of the plot. The values entered as
      a tuple of numbers where the first number is width of the figure and the
      second number is the height of the figure. If the option ``units`` is not
      used the size is specified in cm. Per default the canvas is 6cm x 6cm. 

    - ``keep_aspect_ratio`` : bool, optional (default = True)
      Defines whether to keep the aspect ratio of the current layout. If
      ``False``, the layout will be rescaled to fit exactly into the
      available area in the canvas (i.e. removed margins). If ``True``, the
      original aspect ratio of the layout will be kept and it will be
      centered within the canvas.

    - ``standalone`` : bool, optional (default = True)
      If this option is true, a standalone latex file will be created. i.e. the
      figure can be compiled from this output file. If standalone is false,
      only the tikz environment is stored in the tex file, and can be imported
      in an existing tex file.

    - ``clean`` : bool, optional (default = True)
      Whether non-pdf files created that are created during compilation should
      be removed.

    - ``clean_tex`` : bool, optional (default = True)
      Also remove the generated tex file.

    - ``compiler`` : `str` or `None`, optional (default = None)
      The name of the LaTeX compiler to use. If it is None, cnet will choose a
      fitting one on its own. Starting with ``latexmk`` and then ``pdflatex``.

    - ``compiler_args`` : `list` or `None`, optional (default = None)
      Extra arguments that should be passed to the LaTeX compiler. If this is
      None it defaults to an empty list.

    - ``silent`` : bool, optional (default = True)
      Whether to hide compiler output or not.

    In the style dictionary multiple keywords can be used to address
    attributes. These keywords will be converted to an unique key word,
    used in the remaining code. This allows to keep the keywords used in
    'igrap'.

    ========= =================================
    keys       other valid keys
    ========= =================================
    node      vertex, v, n
    edge      link, l, e
    margins   margin
    canvas    bbox, figure_size
    units     unit
    fixed     fixed_nodes, fixed_vertices,
              fixed_n, fixed_v
    positions initial_positions, node_positions
              vertex_positions, n_positions,
              v_positions
    ========= =================================

    Examples
    --------

    For illustration purpose a similar network as in the python-igrap tutorial
    is used. Instead of igraph, the cnet module is used for creating the
    network.

    Create an empty network object, and add some edges.

    >>> net = Network(name = 'my tikz test network',directed=True)
    >>> net.add_edges_from([('ab','a','b'), ('ac','a','c'), ('cd','c','d'),
    >>>                     ('de','d','e'), ('ec','e','c'), ('cf','c','f'),
    >>>                     ('fa','f','a'), ('fg','f','g'),('gg','g','g'),
    >>>                     ('gd','g','d')])

    Adding node and edge properties.

    >>> net.nodes['name'] = ['Alice', 'Bob', 'Claire', 'Dennis', 'Esther',
    >>>                      'Frank', 'George']
    >>> net.nodes['age'] = [25, 31, 18, 47, 22, 23, 50]
    >>> net.nodes['gender'] = ['f', 'm', 'f', 'm', 'f', 'm', 'm']
    >>> net.edges['is_formal'] = [False, False, True, True, True, False, True,
    >>>                           False, False, False]

    Already now the network can be plotted.

    >>> cn.plot(net)

    .. figure:: plot_01.png
       :alt: Simple plot with no visual styles
       :align: center
       :scale: 50

    Per default, the node positions are assigned uniform random. In order to
    create a layout, the layout methods of the packages can be used, or the
    position of the nodes can be directly assigned, in form of a dictionary,
    where the key is the node id and the value is a tuple of the node position
    in x and y.

    >>> layout = {'a': (4.3191, -3.5352), 'b': (0.5292, -0.5292),
    >>>           'c': (8.6559, -3.8008), 'd': (12.4117, -7.5239),
    >>>           'e': (12.7, -1.7069), 'f': (6.0022, -9.0323),
    >>>           'g': (9.7608, -12.7)}
    >>> plot(net,layout=layout)

    This should open an external pdf viewer showing a visual representation of
    the network, something like the one on the following figure:

    .. figure:: plot_02.png
       :alt: Simple plot with layout
       :align: center
       :scale: 50

    We can simply re-using the previous layout object here, but we also
    specified that we need a bigger plot (8 x 8 cm) and a larger margin around
    the graph to fit the self loop and potential labels (1 cm).

    >>> plot(net, layout=layout, canvas=(8,8), margin=1)

    .. figure:: plot_03.png
       :alt: Simple plot with layout and margins
       :align: center
       :scale: 50

    Note, instead of the command ``margins`` the command ``margin`` can be
    used. Also instead of ``canvas``, ``figure_size`` or ``bbox`` can be
    used. For more information see table above.

    In order to keep the properties of the visual representation of your network
    separate from the network itself. You can simply set up a Python dictionary
    containing the keyword arguments you would pass to :py:meth:`plot` and then
    use the double asterisk (**) operator to pass your specific styling
    attributes to :py:meth:`plot`:

    >>> color_dict = {'m': 'blue', 'f': 'red'}
    >>> visual_style = {}

    Node options

    >>> visual_style['node_size'] = .5
    >>> visual_style['node_color'] = [color_dict[g] for g in net.nodes('gender')]
    >>> visual_style['node_opacity'] = .7
    >>> visual_style['node_label'] = net.nodes['name']
    >>> visual_style['node_label_position'] = 'below'

    Edge options

    >>> visual_style['edge_width'] = [1 + 2 * int(f) for f in net.edges('is_formal')]
    >>> visual_style['edge_curved'] = 0.1

    General options

    >>> visual_style["canvas"] = (8,8)
    >>> visual_style["margin"] = 1
    >>> plot(net,**visual_style)

    .. figure:: plot_04.png
       :alt: Plot with modified style
       :align: center
       :scale: 50

    Beside showing the network, we can also generate the latex source file,
    which can be used and modified later on. This is done by adding the output
    file name with the ending '.tex'

    >>> plot(net,'network.tex',**visual_style)

    .. code-block:: latex

       \\documentclass{standalone}
       \\usepackage{tikz-network}
       \\begin{document}
       \\begin{tikzpicture}
       \\clip (0,0) rectangle (8.0,8.0);
       \\Vertex[x=2.868,y=5.518,size=0.5,color=red,opacity=0.7,label=Alice,position=below]{a}
       \\Vertex[x=1.000,y=7.000,size=0.5,color=blue,opacity=0.7,label=Bob,position=below]{b}
       \\Vertex[x=5.006,y=5.387,size=0.5,color=red,opacity=0.7,label=Claire,position=below]{c}
       \\Vertex[x=6.858,y=3.552,size=0.5,color=blue,opacity=0.7,label=Dennis,position=below]{d}
       \\Vertex[x=7.000,y=6.419,size=0.5,color=red,opacity=0.7,label=Esther,position=below]{e}
       \\Vertex[x=3.698,y=2.808,size=0.5,color=blue,opacity=0.7,label=Frank,position=below]{f}
       \\Vertex[x=5.551,y=1.000,size=0.5,color=blue,opacity=0.7,label=George,position=below]{g}
       \\Edge[,lw=1.0,bend=-8.531,Direct](a)(b)
       \\Edge[,lw=1.0,bend=-8.531,Direct](a)(c)
       \\Edge[,lw=3.0,bend=-8.531,Direct](c)(d)
       \\Edge[,lw=3.0,bend=-8.531,Direct](d)(e)
       \\Edge[,lw=3.0,bend=-8.531,Direct](e)(c)
       \\Edge[,lw=1.0,bend=-8.531,Direct](c)(f)
       \\Edge[,lw=3.0,bend=-8.531,Direct](f)(a)
       \\Edge[,lw=1.0,bend=-8.531,Direct](f)(g)
       \\Edge[,lw=1.0,bend=-8.531,Direct](g)(g)
       \\Edge[,lw=1.0,bend=-8.531,Direct](g)(d)
       \\end{tikzpicture}
       \\end{document}

    Instead of the tex file, a node and edge list can be generates, which can
    also be used with the tikz-network library.

    >>> plot(net,'network.csv',**visual_style)

    The node list `network_nodes.csv`.

    .. code-block:: text

       id,x,y,size,color,opacity,label,position
       a,2.868,5.518,0.5,red,0.7,Alice,below
       b,1.000,7.000,0.5,blue,0.7,Bob,below
       c,5.006,5.387,0.5,red,0.7,Claire,below
       d,6.858,3.552,0.5,blue,0.7,Dennis,below
       e,7.000,6.419,0.5,red,0.7,Esther,below
       f,3.698,2.808,0.5,blue,0.7,Frank,below
       g,5.551,1.000,0.5,blue,0.7,George,below

    The edge list `network_edges.csv`.

    .. code-block:: text

       u,v,lw,bend,Direct
       a,b,1.0,-8.531,true
       a,c,1.0,-8.531,true
       c,d,3.0,-8.531,true
       d,e,3.0,-8.531,true
       e,c,3.0,-8.531,true
       c,f,1.0,-8.531,true
       f,a,3.0,-8.531,true
       f,g,1.0,-8.531,true
       g,g,1.0,-8.531,true
       g,d,1.0,-8.531,true

    References
    ----------

    .. [tn] https://github.com/hackl/tikz-network

    """

    result = Plot(network, **kwds)

    # get properties for the latex compiler
    _clean = kwds.get('clean', True)
    _clean_tex = kwds.get('clean_tex', True)
    _compiler = kwds.get('compiler', None)
    _compiler_args = kwds.get('compiler_arg', None)
    _silent = kwds.get('silent', True)

    if filename is None:
        filename = 'default_network'
    if isinstance(filename, tuple) or isinstance(filename, list) or \
            filename.endswith('.csv') or type == 'csv' or \
            filename.endswith('.dat') or type == 'dat':
        # log.debug('Create csv files')
        result.save_csv(filename)
    elif filename == 'default_network' and type is None:
        # log.debug('Show the network')
        # get current directory
        current_dir = os.getcwd()
        # create temp file name
        temp_filename = os.path.join(current_dir, filename)
        # save a pdf file
        result.save_pdf(filename, clean=_clean, clean_tex=_clean_tex,
                        compiler=_compiler, compiler_args=_compiler_args,
                        silent=_silent)
        # open the file
        webbrowser.open(r'file:///'+temp_filename+'.pdf')
        # result.show(filename)
    elif filename.endswith('.tex') or type == 'tex':
        # log.debug('Create tex file')
        standalone = kwds.get('standalone', True)
        result.save_tex(filename, standalone=standalone)
    elif filename.endswith('.pdf') or type == 'pdf':
        # log.debug('Create pdf plot')
        result.save_pdf(filename, clean=_clean, clean_tex=_clean_tex,
                        compiler=_compiler, compiler_args=_compiler_args,
                        silent=_silent)
    else:
        log.warn('No valid output option was chosen!')


class Plot(object):
    """Default class to create plots.

    The :py:class:`Plot` class is used to generate a network drawer and save the
    virtual network as a 'pdf', 'tex' or 'csv' file. Also a temporary file can
    be created to show the network figure.

    Parameters
    ----------
    network : network object
        Network to be drawn. The network can be a 'cnet', 'networkx', 'igraph',
        'pathpy' object, or a tuple of a node list and edge list.

    kwds : keyword arguments, optional (default= no attributes)
        Attributes to add to the drawer as key=value pairs.
        See also :py:meth:`plot`

    See Also
    --------
    plot

    """

    def __init__(self, network, **kwds):
        """Initialize the Plot class.

        Parameters
        ----------
        network : network object
            Network to be drawn. The network can be a 'cnet', 'networkx',
            'igraph', 'pathpy' object, or a tuple of a node list and edge list.

        kwds : keyword arguments, optional (default= no attributes)
            Attributes to add to the drawer as key=value pairs.
            See also :py:meth:`plot`

        """
        self.drawer = TikzNetworkDrawer(network, **kwds)

    def save_tex(self, filename, standalone=True):
        """Save the network as a tex file.

        Parameters
        ----------
        filename : file or string
            File or filename to save. File ending such as '.tex' is not
            necessary and will be added automatically if missing.

        standalone : bool, optional (default = True)
           If this option is true, a standalone latex file will be
           created. i.e. the figure can be compiled from this output file. If
           standalone is false, only the tikz environment is stored in the tex
           file, and can be imported in an existing tex file. 

        """
        latex_header = '\\documentclass{standalone}\n' + \
            '\\usepackage{tikz-network}\n' + \
            '\\begin{document}\n'
        latex_begin_tikz = '\\begin{tikzpicture}\n'
        latex_end_tikz = '\\end{tikzpicture}\n'
        latex_footer = '\\end{document}'

        # margins = self.drawer.margins
        w = self.drawer.canvas.width
        h = self.drawer.canvas.height
        latex_canvas = '\\clip (0,0) rectangle ({},{});\n'.format(w, h)

        # latex_margins = '\\fill[orange!20] ({},{}) rectangle ({},{});\n'\
        #                 ''.format(margins['left'],margins['bottom'],
        #                           canvas[0] - margins['right'],
        #                           canvas[1] - margins['top'])

        with open(filename, 'w') as f:
            if standalone:
                f.write(latex_header)
            f.write(latex_begin_tikz)
            f.write(latex_canvas)
            # f.write(latex_margins)

            for node in self.drawer.node_drawer:
                f.write(node.draw())
            for edge in self.drawer.edge_drawer:
                f.write(edge.draw())

            f.write(latex_end_tikz)
            if standalone:
                f.write(latex_footer)

    def save_csv(self, filename):
        """Save the network as multiple csv files.

        Parameters
        ----------
        filename : file, string or tuple of files, strings.
            File or filename to save. If the filename is a string the output
            file names are a combination from the initial filename and '_nodes'
            or '_edges'. If the filename is a tuple of strings, the first string
            defines the output name for the node list and the second string
            defines the output name for the edge list.

        """
        # if file name is a string get base name
        if isinstance(filename, str):
            basename = os.path.splitext(os.path.basename(filename))[0]
            basename_n = basename + '_nodes'
            basename_e = basename + '_edges'
        # if the file name is a tuple, use the first part for the node list and
        # the second part for the edge list.
        elif isinstance(filename, tuple) or isinstance(filename, list):
            basename_n = os.path.splitext(os.path.basename(filename[0]))[0]
            basename_e = os.path.splitext(os.path.basename(filename[1]))[0]
        else:
            log.error('File name is not correct specified!')
            raise CnetError

        # write node list
        with open(basename_n+'.csv', 'w') as f:
            f.write(self.drawer.node_drawer[0].head())
            for node in self.drawer.node_drawer:
                f.write(node.draw(mode='csv'))

        # write edge list
        with open(basename_e+'.csv', 'w') as f:
            f.write(self.drawer.edge_drawer[0].head())
            for edge in self.drawer.edge_drawer:
                f.write(edge.draw(mode='csv'))

    def save_pdf(self, filename, clean=True, clean_tex=True,
                 compiler=None, compiler_args=None, silent=True):
        """Save the network as a tex file and compile the pdf.

        Note
        ----
        This code was adapted from the module `PyLaTeX`.

        Parameters
        ----------
        filename : file or string
            File or filename to save. File ending such as '.pdf' is not
            necessary and will be added automatically if missing.

        clean: bool, optional (default = True)
            Whether non-pdf files created that are created during compilation
            should be removed.

        clean_tex: bool, optional (default = True)
            Also remove the generated tex file.

        compiler: `str` or `None`, optional (default = None)
            The name of the LaTeX compiler to use. If it is None, cnet will
            choose a fitting one on its own. Starting with ``latexmk`` and then
            ``pdflatex``.

        compiler_args: `list` or `None`, optional (default = None)
            Extra arguments that should be passed to the LaTeX compiler. If
            this is None it defaults to an empty list.

        silent: bool, optional (default = True)
            Whether to hide compiler output or not.

        """
        if compiler_args is None:
            compiler_args = []

        # get directories and file name
        current_dir = os.getcwd()
        output_dir = os.path.dirname(filename)
        # check if output dir exists if not use the base dir
        if not os.path.exists(output_dir):
            output_dir = current_dir
        basename = os.path.splitext(os.path.basename(filename))[0]

        # change to output dir
        os.chdir(output_dir)

        # save the tex file
        self.save_tex(basename+'.tex', standalone=True)

        if compiler is not None:
            compilers = ((compiler, []),)
        else:
            latexmk_args = ['--pdf']

            compilers = (
                ('latexmk', latexmk_args),
                ('pdflatex', [])
            )

        main_arguments = ['--interaction=nonstopmode', basename + '.tex']

        for compiler, arguments in compilers:
            command = [compiler] + arguments + compiler_args + main_arguments

            try:
                output = subprocess.check_output(command,
                                                 stderr=subprocess.STDOUT)
            except:
                # If compiler does not exist, try next in the list
                continue
            else:
                if not silent:
                    print(output.decode())

            if clean:
                try:
                    # Try latexmk cleaning first
                    subprocess.check_output(['latexmk', '-c', basename],
                                            stderr=subprocess.STDOUT)
                except (OSError, IOError, subprocess.CalledProcessError) as e:
                    # Otherwise just remove some file extensions.
                    extensions = ['aux', 'log', 'out', 'fls',
                                  'fdb_latexmk']

                    for ext in extensions:
                        try:
                            os.remove(basename + '.' + ext)
                        except (OSError, IOError) as e:
                            if e.errno != errno.ENOENT:
                                raise
            # remove the tex file
            if clean_tex:
                os.remove(basename + '.tex')
            # Compilation has finished, so no further compilers have to be tried
            break

        else:
            # Notify user that none of the compilers worked.
            log.error('No LaTex compiler was found! Either specify a LaTex '
                      'compiler or make sure you have latexmk or pdfLaTex'
                      ' installed.')
            raise CnetError

        # change back to current dir
        os.chdir(current_dir)

    def show(self, filename):
        """Show the compiled network.

        Create a tex file and compile the pdf out of it. After this is done the
        pdf will be automatically opened.

        Parameters
        ----------
        filename : file or string
            File or filename to save.

        See Also
        --------
        save_pdf

        """
        # get current directory
        current_dir = os.getcwd()
        # create temp file name
        temp_filename = os.path.join(current_dir, filename)
        # save a pdf file
        self.save_pdf(temp_filename)
        # open the file
        webbrowser.open(r'file:///'+temp_filename+'.pdf')


# =============================================================================
# eof
#
# Local Variables:
# mode: python
# mode: linum
# mode: auto-fill
# fill-column: 80
# End:
