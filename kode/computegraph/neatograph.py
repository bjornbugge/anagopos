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
import pygv

class NeatoGraph(reductiongraph.Graph):
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
		print "Updating layout using neato"
		self.bezier = False
		gv = pygv.GraphViz("neato")
		gv.viz(self)
		
	def update_layout_animated(self, f):
		self.update_layout()
		f(self)
		
	def scale(self, width, heigth):
		#print "will scale"
		#print width
		#print heigth
		Xs = []
		Ys = []
		for node in self.nodes:
			Xs.append(node.x)
			Ys.append(node.y)
			
		maxPosX = max(Xs)
		maxPosY = max(Ys)
		scalingX = (maxPosX)/(width-50)
		scalingY = (maxPosY)/(heigth-50)
		
		for node in self.nodes:
			node.x = float(node.x)/(scalingX)
			node.y = float(node.y)/(scalingY)
			for edge in node.children:
				for point in range(len(edge.ipoints)):
					edge.ipoints[point][0] = float(edge.ipoints[point][0])/(scalingX)
					edge.ipoints[point][1] = float(edge.ipoints[point][1])/(scalingY)