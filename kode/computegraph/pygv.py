import math
import time
import computegraph.operations as operations
import lambdaparser as parser
import randomgraph
import graphicsutils
import pygraphviz as pgv
import string
import random
#from computegraph.kkgraph import KKGraph
from computegraph.reductiongraph import *
#from OpenGL.GLUT import *
#from OpenGL.GLU import *
#from OpenGL.GL import *


# Her begynder pygraphviz koden
class GraphViz(object):
	def __init__(self, alg):
		self.term = None
		self.graph = None
		self.node = None
		self.G = None
		self.alg = alg
			
	def viz( self ):
		# Start time
		inittime = time.time()
		
		# Adds nodes in graph to the GraphViz graph
		G = pgv.AGraph()
		for node in self.graph.nodes:
			G.add_node(str(node.name))
		
		# Adds edges in graph to the GraphViz graph
		for node in self.graph.nodes:
			for edge in node.children:
				far_node = edge.get_far(node)
				if node == far_node:
					continue
				G.add_edge(str(node.name),str(far_node.name))
		
		# Applies layout (algorithm) to the GraphViz graph
		#G.write("img/beforelayout.dot")
		G.layout(prog=self.alg)
		#G.write("img/afterlayout.dot")
		#G.draw("img/1111.png")
		
		k = 0
		n = 0
		ll = 0

		E = G.edges()
		N = G.nodes()
		
		# Applies new positions in the GraphViz graph back to the "corect" graph
		for node in N:
			graphnode = self.graph.nodenametable[node.name]
			nodePos = node.attr["pos"]
			graphnode.x = float(string.split(str(nodePos),',')[0])
			graphnode.y = float(string.split(str(nodePos),',')[1])
			for edge in graphnode.children:
				edgePos = E[k].attr["pos"]
				newEdgePos = string.split(edgePos,' ')
				edge.ipoints = [[0 for col in range(2)] for row in range(len(newEdgePos))]
				for y in range(len(newEdgePos)):
					edge.ipoints[y][0] = float(string.split(str(newEdgePos[y]),',')[0])
					edge.ipoints[y][1] = float(string.split(str(newEdgePos[y]),',')[1])
				k=k+1
			n = n + 1

		endtime = time.time()
		
		self.G = G
		
	def draw(self, graph):
		#print "0 - " + str(time.time())
		self.graph = graph
		self.viz()
		return self.graph