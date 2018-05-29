#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# =============================================================================
# File      : setup.py
# Creation  : 21 May 2018
# Time-stamp: <Die 2018-05-29 07:49 juergen>
#
# Copyright (c) 2018 Jürgen Hackl <hackl@ibi.baug.ethz.ch>
#               http://www.ibi.ethz.ch
# $Id$
#
# Description : Setup script for network2tikz
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
from setuptools import setup, find_packages

about = {}
base_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(base_dir, 'network2tikz', '__about__.py'), 'rb') as f:
    exec(f.read(), about)

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='network2tikz',
    version=about['__version__'],
    packages=find_packages(),
    url='https://github.com/hackl/network2tikz',
    download_url = 'https://pypi.org/project/network2tikz',
    author=about['__author__'],
    author_email=about['__email__'],
    install_requires=['numpy'],
    description='A converter that takes a network (cnet, igraph, networkx, pathpy, ...) and creates a tikz-network for smooth integration into LaTeX.',
    long_description = readme,
    long_description_content_type='text/markdown',
    license = about['__license__'],
    classifiers=[
        about['__status__'],
        about['__license__'],
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Science/Research',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
        'Topic :: Scientific/Engineering :: Visualization',
        ]
)

# =============================================================================
# eof
#
# Local Variables:
# mode: python
# mode: linum
# mode: auto-fill
# fill-column: 80
# End:
