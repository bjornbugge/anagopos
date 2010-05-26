import pdb
import sys
import math
import random
import numpy
import reductiongraph
import shortestpath as SP
from copy import deepcopy
import time
import scipy.weave as weave
import pygraphviz

class DotGraph(reductiongraph.Graph):
	def __init__(self, graph):
		for name,value in vars(graph).iteritems():
			setattr(self, name, value)
		self.reset()
		#self.update_layout()
		self.virgin = True
		
	def reset(self, f = 0, clearstate = True):
		for node in self.nodes:
			node.x = random.randint(1, 100)
			node.y = random.randint(1, 100)
	
	def initwith(self, othergraph):
		self.reset()
	
	def update_layout(self):
		print "-----------------------------------------------------------------------------------------------"
		gv = pygraphviz.GraphViz("dot")
		gv.draw(self)
		
	def update_layout_animated(self, f):
		self.update_layout()
		f(self)