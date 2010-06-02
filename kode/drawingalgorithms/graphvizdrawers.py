import random
import time
import pygraphviz as pgv
import string
import pdb
import computegraph.reductiongraph as RG
from drawingalgorithm import DrawingAlgorithm

def graphvizdrawer(drawer):
	'''
	Decorator function for creating PygraphViz-algorithms that
	satisfy the specifications in drawingalgorithm.DrawingAlgorithm.
	'''
	def _reset(self, f = 0):
		for node in self.nodes:
			node.x = random.randint(1, 100)
			node.y = random.randint(1, 100)
	
	def _initwith(self, othergraph): self.reset()
	
	def _update_layout(self):
		# Layout the graph.
		self.G.layout(prog = self.algorithm)
		
		E = self.G.edges()
		N = self.G.nodes()
		
		# Assigns new positions in the GraphViz graph to the "correct" graph
		for Anode in N:
			graphnode = self.nodenametable[Anode.name]
			graphnode.x, graphnode.y = map(float, Anode.attr["pos"].split(','))
			for edge in graphnode.children:
				Aedge = self.G.get_edge(graphnode.name, edge.get_far(graphnode).name)
				newEdgePos = Aedge.attr["pos"].split(' ')
				
				if not hasattr(self, 'bezier') or not self.bezier:
					continue
				
				edge.ipoints = [[0, 0] for row in range(len(newEdgePos))]
				# pdb.set_trace()
				for i, pos in enumerate(newEdgePos):
					edge.ipoints[i] = map(float, pos.split(','))
	
	def _update_layout_animated(self, f):
		self.update_layout()
		f(self)
			
	def _init(self, graph):
		for name, value in vars(graph).iteritems():
			setattr(self, name, value)
		
		# Make a GraphViz graph and add all nodes.
		self.G = pgv.AGraph()
		for name in (n.name for n in self.nodes):
			self.G.add_node(name, width = "0.00", heigth = "0.00", fixedsize = "0", 
							margin = "0.00")#, label = " ", shape = "none"), fontsize = "8")
		
		# Adds edges in the graph to the GraphViz graph
		for node in self.nodes:
			for edge in node.children:
				far_node = edge.get_far(node)
				if node == far_node:
					continue
				self.G.add_edge(str(node.name), str(far_node.name))
		
		self.reset()
	
	def _scale(self, width, height):
		Xs = [node.x for node in self.nodes]
		Ys = [node.y for node in self.nodes]
		scaling = [max(Xs) / (width - 50), max(Ys) / (height - 50)]
		
		for node in self.nodes:
			node.x = float(node.x) / scaling[0]
			node.y = float(node.y) / scaling[1]
			
			if not hasattr(self, 'bezier') or not self.bezier:
				continue
			
			for edge in node.children:
				for i, point in enumerate(edge.ipoints):
					edge.ipoints[i] = map(lambda x:float(x[0]) / x[1], zip(point, scaling))
	
	methods = {	'__init__' 				: _init,
				'reset'					: _reset,
				'initwith'				: _initwith,
				'update_layout' 		: _update_layout,
				'update_layout_animated': _update_layout_animated,
				'scale' 				: _scale}
	
	for name, method in methods.iteritems():
		setattr(drawer, name, method)
	return drawer

@graphvizdrawer
class CircoGraph():
	algorithm = 'circo'

@graphvizdrawer
class DotGraph():
	algorithm = 'dot'
	bezier = True

@graphvizdrawer
class NeatoGraph():
	algorithm = 'neato'

@graphvizdrawer
class FdpGraph():
	algorithm = 'fdp'

@graphvizdrawer
class TwopiGraph():
	algorithm = 'twopi'