# network2tikz

This is `network2tikz`, a Python tool for converting network visualizations into [TikZ](https://www.ctan.org/pkg/pgf)([tikz-network](https://github.com/hackl/tikz-network)) figures, for native inclusion into your LaTeX documents.

`network2tikz` works with Python 3 and supports (currently) the following Python network modules:

- [cnet](https://github.com/hackl/cnet)
- [python-igraph](http://igraph.org/python/)
- [networkx](https://networkx.github.io/)
- [pathpy](https://github.com/IngoScholtes/pathpy)
- default node/edge lists

The output of `network2tikz` is in [tikz-network](https://github.com/hackl/tikz-network), a LaTeX library that sits on top of [TikZ](https://www.ctan.org/pkg/pgf), which allows to visualize and modify the network plot for your specific needs and publications.

Because you are not only getting an image of your network, but also the LaTeX source file, you can easily post-process the figures (e.g. adding drawings, texts, equations,...).

Because you are not only getting an image of your network, but also the LaTeX source file, you can easily post-process the figures (e.g. adding drawings, texts, equations,...).

Since *a picture is worth a thousand words* a small example:

```python,test
nodes = ['a','b','c','d']
edges = [('a','b'), ('a','c'), ('c','d'),('d','b')]
gender = ['f', 'm', 'f', 'm']
colors = {'m': 'blue', 'f': 'red'}

style = {}
style['node_label'] = ['Alice', 'Bob', 'Claire', 'Dennis']
style['node_color'] = [colors[g] for g in gender]
style['node_opacity'] = .5
style['edge_curved'] = .1

from network2tikz import plot
plot((nodes,edges),'network.tex',**style)
```
(see above) gives
```latex
\documentclass{standalone}
\usepackage{tikz-network}
\begin{document}
\begin{tikzpicture}
\clip (0,0) rectangle (6,6);
\Vertex[x=0.785,y=2.375,color=red,opacity=0.5,label=Alice]{a}
\Vertex[x=5.215,y=5.650,color=blue,opacity=0.5,label=Bob]{b}
\Vertex[x=3.819,y=0.350,color=red,opacity=0.5,label=Claire]{c}
\Vertex[x=4.654,y=2.051,color=blue,opacity=0.5,label=Dennis]{d}
\Edge[,bend=-8.531](a)(c)
\Edge[,bend=-8.531](c)(d)
\Edge[,bend=-8.531](d)(b)
\Edge[,bend=-8.531](a)(b)
\end{tikzpicture}
\end{document}
```
and looks like

![](https://hackl.github.io/network2tikz/example_01.png)

Tweaking the plot is straightforward and can be done as part of your LaTeX workflow.
[The tikz-network manual](https://github.com/hackl/tikz-network/blob/master/manual.pdf)
contains multiple examples of how to make your plot look even better.

## Installation

`network2tikz` is [available from the Python Package Index](https://pypi.org/project/network2tikz/), so simply type
```
pip install -U network2tikz
```
to install/update.

## Usage

1. Generate, manipulation, and study of the structure, dynamics, and functions of your complex networks as usual, with your preferred python module.

2. Instead of the default plot functions (e.g. `igraph.plot()` or `networkx.draw()`) invoke `network2tikz` by
   ```python
   plot(G,'mytikz.tex')
   ```
   to store your network visualisation as the TikZ file `mytikz.tex`. Load the module with:
   ```python
   from network2tikz import plot
   ```
   **Advanced usage**:
   Of course, you always can improve your plot by manipulating the generated LaTeX file, but why not do it directly in Python? To do so, all visualization options available in [tikz-network](https://github.com/hackl/tikz-network) are also implemented in `network2tikz`. The appearance of the plot can be modified by keyword arguments (for a detailed explanation, please see below).
   ```python
   my_style = {}
   plot(G,'mytikz.tex',**my_style)
   ```
    The arguments follow the options available in the [tikz-network](https://github.com/hackl/tikz-network) library and are also explained in the [tikz-network manual](https://github.com/hackl/tikz-network/blob/master/manual.pdf). 

   Additionally, if you are more interested in the final output and not only the `.tex` file, used
   ```python
   plot(G,'mypdf.pdf')
   ```
   to save your plot as a pdf, or
   ```python
   plot(G)
   ```
   to create a temporal plot and directly show the result, i.e. similar to the matplotlib function `show()`. Finally, you can also create a node and edge list, which can be read and easily modified (in a post-processing step) with [tikz-network](https://github.com/hackl/tikz-network):
   ```python
   plot(G,'mycsv.csv')
   ```
   <aside class="notice">
   Currently, the direct compilation and the show functionality are only tested on a Linux OS. I'm certainly sure, that this will not work out-of-the-box for Windows OS, probably you have to define where your LaTeX compiler is stored (see below). As soon as I have access to a Windows computer I'll find a solution to make this work (a little bit) easier for you.
   </aside>
3. <aside class="notice">
   In order to compile the plot, make sure you have installed [tikz-network](https://github.com/hackl/tikz-network)!
   </aside>
4. Compile the figure or add the contents of `mytikz.tex` into your LaTeX source code. With the option `standalone=false` only the TikZ figure will be saved, which can then be easily included in your LaTeX document via `\input{/path/to/mytikz.tex}`.

## Simple example

For illustration purpose, a similar network as in the [python-igrap tutorial](http://igraph.org/python/doc/tutorial/tutorial.html) is used. If you are using another Python network module, and like to follow this example, please have a look at the [provided examples](https://github.com/hackl/network2tikz/tree/master/examples).

Create network object and add some edges.

```python
import igraph
from network2tikz import plot

net = igraph.Graph([(0,1), (0,2), (2,3), (3,4), (4,2), (2,5), (5,0), (6,3),
                   (5,6), (6,6)],directed=True)
```

Adding node and edge properties.

```python
net.vs["name"] = ["Alice", "Bob", "Claire", "Dennis", "Esther", "Frank", "George"]
net.vs["age"] = [25, 31, 18, 47, 22, 23, 50]
net.vs["gender"] = ["f", "m", "f", "m", "f", "m", "m"]
net.es["is_formal"] = [False, False, True, True, True, False, True, False,
                       False, False]
```

Already now the network can be plotted.

```python
plot(net)
```

![](https://hackl.github.io/network2tikz/plot_01.png)

Per default, the node positions are assigned uniform random. In order to create a layout, the layout methods of the network packages can be used. Or the position of the nodes can be directly assigned, in form of a dictionary, where the key is the node id and the value is a tuple of the node position in x and y.

```python
layout = {0: (4.3191, -3.5352), 1: (0.5292, -0.5292),
          2: (8.6559, -3.8008), 3: (12.4117, -7.5239),
          4: (12.7, -1.7069), 5: (6.0022, -9.0323),
          6: (9.7608, -12.7)}
plot(net,layout=layout)
```

This should open an external pdf viewer showing a visual representation of the network, something like the one on the following figure:

![](https://hackl.github.io/network2tikz/plot_02.png)

We can simply re-using the previous layout object here, but we also specified that we need a bigger plot (8 x 8 cm) and a larger margin around the graph to fit the self loop and potential labels (1 cm).

<aside class="notice">
Per default, all size values are based on `cm`, and all line widths are defined in `pt` units. With the general option `units` this can be changed, see below.
</aside>

```python
plot(net, layout=layout, canvas=(8,8), margin=1)
```

![](https://hackl.github.io/network2tikz/plot_03.png)

<aside class="notice">
Note, instead of the command `margins` the command `margin` can be used. Also instead of `canvas`, `figure_size` or `bbox` can be used. For more information see table below.
</aside>

In to keep the properties of the visual representation of your network separate from the network itself. You can simply set up a Python dictionary containing the keyword arguments you would pass to `plot` and then use the double asterisk (`**`) operator to pass your specific styling attributes to `plot`:

```python
color_dict = {'m': 'blue', 'f': 'red'}
visual_style = {}
```

Node options

```python
visual_style['node_size'] = .5
visual_style['node_color'] = [color_dict[g] for g in net.nodes('gender')]
visual_style['node_opacity'] = .7
visual_style['node_label'] = net.nodes['name']
visual_style['node_label_position'] = 'below'
```

Edge options

```python
visual_style['edge_width'] = [1 + 2 * int(f) for f in net.edges('is_formal')]
visual_style['edge_curved'] = 0.1
```
General options and plot command.

```python
visual_style["canvas"] = (8,8)
visual_style["margin"] = 1

plot(net,**visual_style)
```

![](https://hackl.github.io/network2tikz/plot_04.png)

Beside showing the network, we can also generate the latex source file, which can be used and modified later on. This is done by adding the output file name with the ending `'.tex'`

```python
plot(net,'network.tex',**visual_style)
```
```latex
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
```
Instead of the tex file, a node and edge list can be generates, which can also be used with the tikz-network library.

```python
plot(net,'network.csv',**visual_style)
```
The node list `network_nodes.csv`.
```text
id,x,y,size,color,opacity,label,position
a,2.868,5.518,0.5,red,0.7,Alice,below
b,1.000,7.000,0.5,blue,0.7,Bob,below
c,5.006,5.387,0.5,red,0.7,Claire,below
d,6.858,3.552,0.5,blue,0.7,Dennis,below
e,7.000,6.419,0.5,red,0.7,Esther,below
f,3.698,2.808,0.5,blue,0.7,Frank,below
g,5.551,1.000,0.5,blue,0.7,George,below
```
The edge list `network_edges.csv`.

```text
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
```

Just for fun, the same plot generated above with the builtin plot function of `igraph`.

```python
igraph.plot(net,'network.png',**visual_style)
```

![](https://hackl.github.io/network2tikz/plot_04.png)

## The plot function in detail

## TODO

- [ ] Find Windows computer to test the pdf and show functionality of `network2tikz`, and probably fix the compiler location problem.

## Changelog
