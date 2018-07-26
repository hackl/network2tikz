#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# =============================================================================
# File      : layout.py -- Module to layout the network
# Author    : Juergen Hackl <hackl@ibi.baug.ethz.ch>
# Creation  : 2018-07-26
# Time-stamp: <Don 2018-07-26 18:36 juergen>
#
# Copyright (c) 2018 Juergen Hackl <hackl@ibi.baug.ethz.ch>
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
import numpy as np
from . import logger
from .exceptions import CnetError

log = logger(__name__)


class Layout(object):
    """Documentation for Layout

    """

    def __init__(self, network, **kwds):
        self.network = network
        # self.layout

    def fruchterman_reingold(self, network,
                             k=None,
                             layout=None,
                             fixed=None,
                             iterations=50,
                             threshold=1e-4,
                             weight=None,
                             dimension=2,
                             seed=None):
        """Position nodes using Fruchterman-Reingold force-directed algorithm.

        Parameters
        ----------
        network : NetworkX graph or list of nodes
            A position will be assigned to every node in G.

        k : float (default=None)
            Optimal distance between nodes.  If None the distance is set to
            1/sqrt(n) where n is the number of nodes.  Increase this value
            to move nodes farther apart.

        layout : dict or None  optional (default=None)
            Initial positions for nodes as a dictionary with node as keys
            and values as a coordinate list or tuple.  If None, then use
            random initial positions.

        fixed : list or None  optional (default=None)
            Nodes to keep fixed at initial position.

        iterations : int  optional (default=50)
            Maximum number of iterations taken

        threshold: float optional (default = 1e-4)
            Threshold for relative error in node position changes.
            The iteration stops if the error is below this threshold.

        weight : string or None   optional (default='weight')
            The edge attribute that holds the numerical value used for
            the edge weight.  If None, then all edge weights are 1.

        dimension : int
            Dimension of layout.

        seed : int, RandomState instance or None  optional (default=None)
            Set the random state for deterministic node layouts.
            If int, `seed` is the seed used by the random number generator,
            if numpy.random.RandomState instance, `seed` is the random
            number generator,
            if None, the random number generator is the RandomState instance used
            by numpy.random.

        Returns
        -------
        layout : dict
            A dictionary of positions keyed by node

        Examples
        --------
        >>> G = nx.path_graph(4)
        >>> pos = nx.spring_layout(G)

        # The same using longer but equivalent function name
        >>> pos = nx.fruchterman_reingold_layout(G)
        """

        if fixed is not None:
            fixed = np.asarray([network.nodes.index(v) for v in fixed])

        if layout is not None:
            # Determine size of existing domain to adjust initial positions
            _size = max(coord for t in layout.values() for coord in t)
            if _size == 0:
                _size = 1
            _layout = np.random.rand(
                network.number_of_nodes(), dimension) * _size

            for i, n in enumerate(network.nodes):
                if n in layout:
                    _layout[i] = np.asarray(layout[n])
        else:
            _layout = None

        if k is None and fixed is not None:
            # We must adjust k by domain size for layouts not near 1x1
            k = _size / np.sqrt(network.number_of_nodes())

        try:
            # Sparse matrix
            if network.number_of_nodes() < 500:  # sparse solver for large graphs
                raise ValueError
            A = network.adjacency_matrix(weight=weight)
            layout = self._sparse_fruchterman_reingold(A, k, _layout, fixed,
                                                       iterations, threshold,
                                                       dimension, seed)
        except:
            A = network.adjacency_matrix(weight=weight).todense()
            layout = self._fruchterman_reingold(A, k, _layout, fixed, iterations,
                                                threshold, dimension, seed)

        layout = dict(zip(network.nodes, layout))

        return layout

    def _fruchterman_reingold(self, A, k=None, layout=None, fixed=None, iterations=50,
                              threshold=1e-4, dimension=2, seed=None):
        """Fruchterman-Reingold algorithm.

        This algorithm is based on the Fruchterman-Reingold algorithm provided
        by networkx.
        """
        try:
            _n, _ = A.shape
        except AttributeError:
            log.error('Fruchterman-Reingold algorithm needs an adjacency '
                      'matrix as input')
            raise CnetError

        # make sure we have an array instead of a matrix
        A = np.asarray(A)

        if layout is None:
            # random initial positions
            layout = np.asarray(np.random.rand(_n, dimension), dtype=A.dtype)
        else:
            # make sure positions are of same type as matrix
            layout = layout.astype(A.dtype)

        # optimal distance between nodes
        if k is None:
            k = np.sqrt(1.0 / _n)
        # the initial "temperature"  is about .1 of domain area (=1x1)
        # this is the largest step allowed in the dynamics.
        # We need to calculate this in case our fixed positions force our domain
        # to be much bigger than 1x1
        t = max(max(layout.T[0]) - min(layout.T[0]),
                max(layout.T[1]) - min(layout.T[1])) * 0.1
        # simple cooling scheme.
        # linearly step down by dt on each iteration so last iteration is size dt.
        dt = t / float(iterations + 1)
        delta = np.zeros(
            (layout.shape[0], layout.shape[0], layout.shape[1]), dtype=A.dtype)
        # the inscrutable (but fast) version
        # this is still O(V^2)
        # could use multilevel methods to speed this up significantly
        for iteration in range(iterations):
            # matrix of difference between points
            delta = layout[:, np.newaxis, :] - layout[np.newaxis, :, :]
            # distance between points
            distance = np.linalg.norm(delta, axis=-1)
            # enforce minimum distance of 0.01
            np.clip(distance, 0.01, None, out=distance)
            # displacement "force"
            displacement = np.einsum('ijk,ij->ik',
                                     delta,
                                     (k * k / distance**2 - A * distance / k))
            # update layoutitions
            length = np.linalg.norm(displacement, axis=-1)
            length = np.where(length < 0.01, 0.1, length)
            delta_layout = np.einsum('ij,i->ij', displacement, t / length)
            if fixed is not None:
                # don't change positions of fixed nodes
                delta_layout[fixed] = 0.0
            layout += delta_layout
            # cool temperature
            t -= dt
            error = np.linalg.norm(delta_layout) / _n
            if error < threshold:
                break
        return layout

    def _sparse_fruchterman_reingold(self, A, k=None, layout=None, fixed=None,
                                     iterations=50, threshold=1e-4, dimension=2,
                                     seed=None):
        pass
# =============================================================================
# eof
#
# Local Variables:
# mode: python
# mode: linum
# mode: auto-fill
# fill-column: 80
# End:
