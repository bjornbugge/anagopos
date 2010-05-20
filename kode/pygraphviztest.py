import math
import time
import computegraph.operations as operations
import lambdaparser as parser
import randomgraph
import graphicsutils
import gldraw2
import pygraphviz as pgv
import string
import random
from computegraph.kkgraph import KKGraph
from computegraph.reductiongraph import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *


# Her begynder pygraphviz koden
class GraphViz(object):
	def __init__(self):
		self.term = None
		self.graph = None
		self.node = None
		self.G = None
			
	def viz( self ):
		
		# Graph
		print "1 - " + str(time.time())
		inittime = time.time()
		
		G = pgv.AGraph()
		
		for node in self.graph.nodes:
			G.add_node(str(node.name))
		
		for node in self.graph.nodes:
			for edge in node.children:
				far_node = edge.get_far(node)
				if node == far_node:
					print "Circular edge."
					continue
				
				G.add_edge(str(node.name),str(far_node.name))
		
		print "2 - " + str(time.time())
		
		G.write("img/fdfsdfsdf.dot")
		
		print "3 - " + str(time.time())
		
		G.layout(prog='dot')
		G.draw("img/1111.png")
		
		print "4 - " + str(time.time())
		
		#G.write("img/fdfsdfsdf2.dot")
		#G.draw("img/fdfsdfsdf2.png")
		
		print "5 - " + str(time.time())
		
		k = 0
		n = 0
		ll = 0

		#for n in G.edges():
		E = G.edges()
		N = G.nodes()
		
		for node in N:
			graphnode = self.graph.nodenametable[node.name]
			nodePos = node.attr["pos"]
			graphnode.x = float(string.split(str(nodePos),',')[0])
			graphnode.y = float(string.split(str(nodePos),',')[1])
			for edge in graphnode.children:
				edgePos = E[k].attr["pos"]
				newEdgePos = string.split(edgePos,' ')
				#node1 = newEdgePos[1]
				#node2 = newEdgePos[len(newEdgePos)-1]
				edge.ipoints = [[0 for col in range(2)] for row in range(len(newEdgePos))]
				yy = 0
				for y in range(len(newEdgePos)):
					edge.ipoints[yy][0] = float(string.split(str(newEdgePos[y]),',')[0])
					edge.ipoints[yy][1] = float(string.split(str(newEdgePos[y]),',')[1])
					yy = yy + 1
				
				#node.x = float(string.split(node1,',')[0])
				#node.y = float(string.split(node1,',')[1])
				#edge.get_far(node).x = float(string.split(node2,',')[0])
				#edge.get_far(node).y = float(string.split(node2,',')[1])
				
				#print "Edge: " + str(G.edges()[k][0]) + "  ----->  " + str(G.edges()[k][1]) + " - POS1: " + str(node1) + " - POS2: " + str(node2)
				k=k+1
			#edge.ipoints[0][0] = node.x
			#edge.ipoints[0][1] = node.y
			n = n + 1
			#print "Graph Node: " + str(graphnode.name) + " - X: " + str(graphnode.x)
		
		graphnodeN1 = self.graph.nodenametable["N1"]
		#print "N1 Child: " + str(graphnodeN1.children[0].ipoints)
		
		#for node in self.graph.nodes:
		#	nodePos = N[n].attr["pos"]
		#	node.x = float(string.split(str(nodePos),',')[0])
		#	node.y = float(string.split(str(nodePos),',')[1])
		#	ll = ll + 1
		#	for edge in node.children:
		#		edgePos = E[k].attr["pos"]
		#		newEdgePos = string.split(edgePos,' ')
		#		#node1 = newEdgePos[1]
		#		#node2 = newEdgePos[len(newEdgePos)-1]
		#		edge.ipoints = [[0 for col in range(2)] for row in range(len(newEdgePos))]
		#		yy = 0
		#		for y in range(len(newEdgePos)):
		#			edge.ipoints[yy][0] = float(string.split(str(newEdgePos[y]),',')[0])
		#			edge.ipoints[yy][1] = float(string.split(str(newEdgePos[y]),',')[1])
		#			yy = yy + 1
		#		
		#		#node.x = float(string.split(node1,',')[0])
		#		#node.y = float(string.split(node1,',')[1])
		#		#edge.get_far(node).x = float(string.split(node2,',')[0])
		#		#edge.get_far(node).y = float(string.split(node2,',')[1])
		#		
		#		#print "Edge: " + str(G.edges()[k][0]) + "  ----->  " + str(G.edges()[k][1]) + " - POS1: " + str(node1) + " - POS2: " + str(node2)
		#		k=k+1
		#	#edge.ipoints[0][0] = node.x
		#	#edge.ipoints[0][1] = node.y
		#	n = n + 1
		
		print "6 - " + str(time.time())
		endtime = time.time()
		
		print "Total time: " + str(endtime - inittime)
		print "Number of nodes: " + str(ll)
		print "Number of edges: " + str(k)
		
		self.G = G
		
	def draw(self, kkgraph):
		print "0 - " + str(time.time())
		self.graph = kkgraph
		self.viz()
		g = gldraw2.GlDraw()
		g.draw(self.graph)
	
	def update(self, kkgraph):
		self.graph = kkgraph
		#print "random knuder"
		for node in self.graph.nodes:
			node.x = random.randint(1, 1000)
			node.y = random.randint(1, 700)
			for edge in node.children:
				for y in range(len(edge.ipoints)):
					edge.ipoints[y][0] = random.randint(1, 10)
					edge.ipoints[y][1] = random.randint(1, 10)
				#print "Points: " + str(edge.ipoints)
		self.viz()
		return self.graph