import numpy,random
from bokeh.plotting import *
from bokeh.objects import HoverTool, ColumnDataSource
from collections import OrderedDict
import pydot
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def drawGraphFromSM2(SM, names, outFile):
  graph = pydot.Dot(graph_type='graph')
  # THRESHOLD SM:
  numberOfTotalConnections = numpy.sum(SM)
  # T = int(numberOfTotalConnections / 1500.0)
  T = 0.5;

  for i in range(SM.shape[0]):
    for j in range(SM.shape[0]):
      if SM[i, j] <= T:
        SM[i, j] = 0.0
      else:
        SM[i, j] = 1.0

  numOfConnections = numpy.sum(SM, axis=0)
  fig = plt.figure(1)
  plot1 = plt.imshow(SM, origin='upper', cmap=cm.gray, interpolation='nearest')
  plt.show()

  numOfConnections = 9 * numOfConnections / max(numOfConnections)

  for i, f in enumerate(names):
    if numpy.sum(SM[i, :]) > 0:
      fillColorCurrent = "{0:d}".format(int(numpy.ceil(numOfConnections[i])))
      #print fillColorCurrent
      # NOTE: SEE http://www.graphviz.org/doc/info/colors.html for color schemes
      #node = pydot.Node(f, style="filled", fontsize="8", shape="egg", fillcolor=fillColorCurrent, colorscheme = "reds9")
      node = pydot.Node(f, style="filled", fontsize="8", shape="egg")
      graph.add_node(node)

  for i in range(len(names)):
    for j in range(len(names)):
      if i < j:
        if SM[i][j] > 0:
          #gr.add_edge((names[i], names[j]))
          edge = pydot.Edge(names[i], names[j])
          graph.add_edge(edge)
  #graph.write_png(outFile)
  graph.write(outFile, prog=None, format='png')

def drawGraphFromSM2_D3js(SM, names, groupName):
  numOfConnections = numpy.sum(SM, axis=0)
  numOfConnections = 9 * numOfConnections / max(numOfConnections)

  # generate data from SM and names:
  data = {'nodes': [], 'links': []}
  for i in range(SM.shape[0]):
    curNode = {'group': groupName[i], 'name': names[i]}
    # curNode = [1]
    data['nodes'].append(curNode)

  print SM
  for i in range(SM.shape[0]):
    for j in range(SM.shape[1]):
      if SM[i][j] > 0:
        curLink = {'source': i, u'target': j, u'value': SM[i][j]}
        data['links'].append(curLink)
  print data
  nodes = data['nodes']
  names = [node['name'] for node in sorted(data['nodes'], key=lambda x: x['group'])]

  N = len(nodes)
  counts = numpy.zeros((N, N))
  for link in data['links']:
    counts[link['source'], link['target']] = link['value']
    counts[link['target'], link['source']] = link['value']

  colormap = [
    "#444444", "#a6cee3", "#1f78b4", "#b2df8a", "#33a02c", "#fb9a99",
    "#e31a1c", "#fdbf6f", "#ff7f00", "#cab2d6", "#6a3d9a"
  ]

  xname = []
  yname = []
  color = []
  alpha = []
  for i, n1 in enumerate(nodes):
    for j, n2 in enumerate(nodes):
      xname.append(n1['name'])
      yname.append(n2['name'])

      a = min(counts[i, j] / 4.0, 0.9) + 0.1
      alpha.append(a)

      if n1['group'] == n2['group']:
        color.append(colormap[n1['group']])
      else:
        color.append('lightgrey')

  output_file("simatrix.html")

  source = ColumnDataSource(
    data=dict(
      xname=xname,
      yname=yname,
      colors=color,
      alphas=alpha,
      count=counts.flatten(),
    )
  )

  figure()

  rect('xname', 'yname', 0.9, 0.9, source=source,
       x_range=list(reversed(names)), y_range=names,
       color='colors', alpha='alphas', line_color=None,
       tools="resize,hover,previewsave", title="Similarity matrix",
       plot_width=800, plot_height=800)

  grid().grid_line_color = None
  axis().axis_line_color = None
  axis().major_tick_line_color = None
  axis().major_label_text_font_size = "5pt"
  axis().major_label_standoff = 0
  xaxis().location = "top"
  xaxis().major_label_orientation = numpy.pi / 3

  hover = [t for t in curplot().tools if isinstance(t, HoverTool)][0]
  hover.tooltips = OrderedDict([
    ('names', '@yname, @xname'),
    ('count', '@count'),
  ])

  show()  # show the plot

def drawMatrix(matrix,files):
  groupName=[0,1]
  for i in range(len(files)-2):
    groupName.append(random.randrange(1,10+1))
  # SM = numpy.zeros((len(names),len(names)))
  drawGraphFromSM2_D3js(matrix, files, groupName)
