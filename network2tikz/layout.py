#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# =============================================================================
# File      : layout.py -- Module to layout the network
# Author    : Juergen Hackl <hackl@ibi.baug.ethz.ch>
# Creation  : 2018-07-26
# Time-stamp: <Fre 2018-07-27 17:55 juergen>
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


def layout(network, **kwds):
    pass


class Layout(object):
    """Documentation for Layout

    """

    def __init__(self, nodes, adjacency_matrix, **attr):
        self.nodes = nodes
        self.adjacency_matrix = adjacency_matrix

        # options for the layouts
        self.layout_type = attr.get('layout', None)
        self.k = attr.get('layout_force', None,)
        self.fixed = attr.get('layout_fixed', None)
        self.iterations = attr.get('layout_iterations', 50)
        self.threshold = attr.get('layout_threshold', 1e-4)
        self.weight = attr.get('layout_weight', None)
        self.dimension = attr.get('layout_dimension', 2)
        self.seed = attr.get('layout_seed', None)
        self.positions = attr.get('layout_positions', None)

    def generate_layout(self):
        # method names
        names_rand = ['Random', 'random', 'rand', None]
        names_fr = ['Fruchterman-Reingold', 'fruchterman_reingold', 'fr',
                    'spring_layout', 'spring layout', 'FR']
        # check which layout should be plotted
        if self.layout_type in names_rand:
            self.layout = self.random()
        elif self.layout_type in names_fr:
            self.layout = self.fruchterman_reingold()

        # print(self.layout)
        return self.layout

    def random(self):
        layout = np.random.rand(len(self.nodes), self.dimension)
        return dict(zip(self.nodes, layout))

    def fruchterman_reingold(self):
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

        if self.fixed is not None:
            self.fixed = np.asarray([self.nodes.index(v) for v in self.fixed])

        if self.positions is not None:
            # Determine size of existing domain to adjust initial positions
            _size = max(coord for t in layout.values() for coord in t)
            if _size == 0:
                _size = 1
            self.layout = np.random.rand(
                len(self.nodes), self.dimension) * _size

            for i, n in enumerate(self.nodes):
                if n in self.positions:
                    self.layout[i] = np.asarray(self.positions[n])
        else:
            self.layout = None

        if self.k is None and self.fixed is not None:
            # We must adjust k by domain size for layouts not near 1x1
            self.k = _size / np.sqrt(len(self.nodes))

        try:
            # Sparse matrix
            if len(self.nodes) < 500:  # sparse solver for large graphs
                raise ValueError
            layout = self._sparse_fruchterman_reingold()
        except:
            layout = self._fruchterman_reingold()

        layout = dict(zip(self.nodes, layout))

        return layout

    def _fruchterman_reingold(self):
        """Fruchterman-Reingold algorithm.

        This algorithm is based on the Fruchterman-Reingold algorithm provided
        by networkx.
        """
        A = self.adjacency_matrix.todense()
        k = self.k
        try:
            _n, _ = A.shape
        except AttributeError:
            log.error('Fruchterman-Reingold algorithm needs an adjacency '
                      'matrix as input')
            raise CnetError

        # make sure we have an array instead of a matrix
        A = np.asarray(A)

        if self.layout is None:
            # random initial positions
            layout = np.asarray(np.random.rand(
                _n, self.dimension), dtype=A.dtype)
        else:
            # make sure positions are of same type as matrix
            layout = self.layout.astype(A.dtype)

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
        dt = t / float(self.iterations + 1)
        delta = np.zeros(
            (layout.shape[0], layout.shape[0], layout.shape[1]), dtype=A.dtype)
        # the inscrutable (but fast) version
        # this is still O(V^2)
        # could use multilevel methods to speed this up significantly
        for iteration in range(self.iterations):
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
            if self.fixed is not None:
                # don't change positions of fixed nodes
                delta_layout[self.fixed] = 0.0
            layout += delta_layout
            # cool temperature
            t -= dt
            error = np.linalg.norm(delta_layout) / _n
            if error < self.threshold:
                break
        return layout

    def _sparse_fruchterman_reingold(self):
        """Fruchterman-Reingold algorithm.

        This algorithm is based on the Fruchterman-Reingold algorithm provided
        by networkx.
        """
        A = self.adjacency_matrix
        k = self.k
        try:
            _n, _ = A.shape
        except AttributeError:
            log.error('Fruchterman-Reingold algorithm needs an adjacency '
                      'matrix as input')
            raise CnetError
        try:
            from scipy.sparse import spdiags, coo_matrix
        except ImportError:
            log.error('The sparse Fruchterman-Reingold algorithm needs the '
                      'scipy package: http://scipy.org/')
            raise ImportError
        # make sure we have a LIst of Lists representation
        try:
            A = A.tolil()
        except:
            A = (coo_matrix(A)).tolil()

        if self.layout is None:
            # random initial positions
            layout = np.asarray(np.random.rand(
                _n, self.dimension), dtype=A.dtype)
        else:
            # make sure positions are of same type as matrix
            layout = layout.astype(A.dtype)

        # no fixed nodes
        if self.fixed is None:
            self.fixed = []

        # optimal distance between nodes
        if k is None:
            k = np.sqrt(1.0 / _n)
        # the initial "temperature"  is about .1 of domain area (=1x1)
        # this is the largest step allowed in the dynamics.
        t = max(max(layout.T[0]) - min(layout.T[0]),
                max(layout.T[1]) - min(layout.T[1])) * 0.1
        # simple cooling scheme.
        # linearly step down by dt on each iteration so last iteration is size dt.
        dt = t / float(self.iterations + 1)

        displacement = np.zeros((self.dimension, _n))
        for iteration in range(self.iterations):
            displacement *= 0
            # loop over rows
            for i in range(A.shape[0]):
                if i in self.fixed:
                    continue
                # difference between this row's node position and all others
                delta = (layout[i] - layout).T
                # distance between points
                distance = np.sqrt((delta**2).sum(axis=0))
                # enforce minimum distance of 0.01
                distance = np.where(distance < 0.01, 0.01, distance)
                # the adjacency matrix row
                Ai = np.asarray(A.getrowview(i).toarray())
                # displacement "force"
                displacement[:, i] +=\
                    (delta * (k * k / distance**2 - Ai * distance / k)).sum(axis=1)
            # update positions
            length = np.sqrt((displacement**2).sum(axis=0))
            length = np.where(length < 0.01, 0.1, length)
            delta_layout = (displacement * t / length).T
            layout += delta_layout
            # cool temperature
            t -= dt
            err = np.linalg.norm(delta_layout) / _n
            if err < self.threshold:
                break
        return layout


# =============================================================================
# eof
#
# Local Variables:
# mode: python
# mode: linum
# mode: auto-fill
# fill-column: 80
# End:
