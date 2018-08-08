#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# =============================================================================
# File      : ex_chicken.py -- Chicken image to network to LaTeX/TikZ
# Author    : Juergen Hackl <hackl@ibi.baug.ethz.ch>
# Creation  : 2018-08-08
# Time-stamp: <Mit 2018-08-08 11:06 juergen>
#
# The code is based on the blog post "Transforming images into networks"
# from Vedran Sekara (https://vedransekara.github.io/)
#
# =============================================================================
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import imread
from scipy.spatial import cKDTree
import random

# function to transform color image to grayscale


def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.299, 0.587, 0.114])


def rgb2hex(color):
    '''
    Matplotlib scatter is not happy with rgb tuples so we need to transform them to hex
    '''
    c = tuple([np.int(255 if c == 1.0 else c * 256.0) for c in color])
    return "#%02x%02x%02x" % c


# parameters
p = 0.003  # propability of selecting a pixel/node
k = 5  # number of connections pre per pixel/node
# remove values above this value 0 (white) - 255 (black) OR 0 (black) - 1 (white)
pix_threshold = 0.9

# load image
data = plt.imread('./data/chicken_in.png')
y, x = np.where(rgb2gray(data[:, :, :3]) < pix_threshold)
y_norm, x_norm = map(float, data[:, :, 0].shape)
colors = data[:, :, :3]

# if its a large image it might be a good idea to downsample
# y,x = np.where(rgb2gray(data[::3,::3,:3])<pix_threshold)
# y_norm, x_norm = map(float,data[::3,::3,0].shape)
# colors = data[::3,::3,:3]

# select nodes
X = np.array(random.sample(list(zip(x, y)), int(len(y)*p)))*1.0

# find k nearest neighbors using scipy.spatial.cKDTree
tree = cKDTree(X)
# construct figure
plt.figure(figsize=(x_norm/120., y_norm/120.))
ax = plt.subplot(111)

# create lists for position of links
x_ = []
y_ = []

# go through each node and construct links
for pt in X:
    # find k nearest neighbors
    # k' = k+1 because method returns points itself
    dist, ind = tree.query(pt, k=k+1)
    for kneigh in ind[1:]:
        x_.append([pt[0], X[kneigh][0]])
        y_.append([pt[1], X[kneigh][1]])

plt.plot(np.array(x_).T, np.array(y_).T,
         color='#282828', lw=0.8, alpha=0.4, zorder=2)

# unpack nodes
# y,x = zip(*X)

# plot using a single color
# plt.scatter(y,x,marker='o',c='#282828',s=0.5,alpha=1)

# or if you want to draw the network with the original colors of your image
# c = [rgb2hex(colors[int(xx),int(yy),:]) for yy,xx in X] # colors
# plt.scatter(y,x,marker='o',c=c,s=3,alpha=1,zorder=3)

plt.axis('off')
plt.ylim(y_norm, 0)
plt.xlim(0, x_norm)

plt.tight_layout()
plt.savefig('chicken_out.png', dpi=250, pad=0.0, bbox_inches='tight')
plt.close()


# transforming your network to a latex source file
from network2tikz import plot
nodes = {(u, v): 'N{}'.format(i) for i, (u, v) in enumerate(X)}
edges = [(nodes[x_[i][0], y_[i][0]], nodes[x_[i][1], y_[i][1]])
         for i in range(len(x_))]

# add some additional style to your figure
visual_style = {}
visual_style['layout'] = {v: (k[0], -k[1]) for k, v in nodes.items()}
visual_style['node_size'] = .2
visual_style['edge_opacity'] = .8
visual_style['canvas'] = (25, 25)

# create the latex file
plot((nodes.values(), edges), 'chicken.tex', ** visual_style)

# =============================================================================
# eof
#
# Local Variables:
# mode: python
# mode: linum
# mode: auto-fill
# fill-column: 80
# End:
