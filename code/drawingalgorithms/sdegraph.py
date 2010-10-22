import random
import numpy as NP
import shortestpath as SP
from drawingalgorithm import DrawingAlgorithm

# Implementation of the algorithm from 
# "SDE: Graph Drawing Using Spectral  Distance Embedding" by Ali Civril, Malik Magdon-Ismail and Eli Bocek-Rivele

# TODO Lav den...
class SDEGraph(DrawingAlgorithm):
	def __init__(self, graph = None, width = 200, height = 200):
		super(reductiongraph.Graph, self).__init__()
		
		self.drawingfunction = None
		self.nodesdict = graph.nodesdict
		self.nodes = graph.nodes
		self.width = width
		self.height = height
		random.seed()
		
		if not graph is None:
			for (key, node) in graph.nodesdict.iteritems():
				node.x = random.randint(1, width)
				node.y = random.randint(1, height)
		
	
	def update_layout(self):
		(D, A) = SP.seidel(self)
		L = NP.power(D, 2)
		Y = self._poweriteration(-0.5 * gamma * Y * gamma, epsilon)
		return Y
	
	def update_layout_animated(self, f):
		self.drawingfunction = f
		self.update_layout()
	
	def _poweriteration(M, epsilon):
		# TODO
		pass
	
	def iter_done(self):
		'''
		Placeholder function for calling a screen update
		'''
		if not self.drawingfunction is None:
			self.drawingfunction(self)
