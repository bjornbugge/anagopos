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
			G.add_node(str(node.name))#,pos="300,200")
		
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
		
		# Default to neato
		# drawG = G.layout()
		G.layout(prog='twopi')
		# G.draw(fname,prog='sfdp')
		
		G.write("img/fdfsdfsdf2.dot")
		
		print "4 - " + str(time.time())
		
		# G.write('img/testtest.dot')
		# Disse virker:
		#	circo	-	tegner i en cirkel								- Bezier
		#	dot		-	tegner i niveauer								+ Bezier
		#	neato	-	(fejl) tegner anne knuder i samme punkt			- Bezier
		#	fdp		-	tegner paent, men virker lidt random			- Bezier
		#	sfdp	-	virker ikke!
		#	twopi	-	tegner i flere cirkler							- Bezier
		# twopi, gvcolor, wc, ccomps, tred, sccmap, fdp, circo, neato, acyclic, nop, gvpr, dot
		
		#k = 0
		#for node in self.graph.nodes:
		#	nodePos = G.nodes()[k].attr["pos"]
		#	newNodePos = string.split(nodePos,',')
		#	posX = newNodePos[0]
		#	posY = newNodePos[1]
		#	node.x = float(posX)
		#	node.y = float(posY)
		#	# print "Node: " + str(node)
		#	# print "X: " + str(posX)
		#	# print "Y: " + str(posY)
		#	k = k + 1
		
		print "5 - " + str(time.time())
		
		k = 0
		ll = 0

		#for n in G.edges():
		E = G.edges()
		for node in self.graph.nodes:
			ll = ll + 1
			for edge in node.children:
				edgePos = E[k].attr["pos"]
				newEdgePos = string.split(edgePos,' ')
				node1 = newEdgePos[1]
				node2 = newEdgePos[len(newEdgePos)-1]
				edge.ipoints = [[0 for col in range(2)] for row in range(len(newEdgePos))]
				yy = 0
				for y in range(len(newEdgePos)):
					edge.ipoints[yy][0] = float(string.split(str(newEdgePos[y]),',')[0])
					edge.ipoints[yy][1] = float(string.split(str(newEdgePos[y]),',')[1])
					yy = yy + 1
				
				node.x = float(string.split(node1,',')[0])
				node.y = float(string.split(node1,',')[1])
				edge.get_far(node).x = float(string.split(node2,',')[0])
				edge.get_far(node).y = float(string.split(node2,',')[1])
				
				#print "Edge: " + str(G.edges()[k][0]) + "  ----->  " + str(G.edges()[k][1]) + " - POS1: " + str(node1) + " - POS2: " + str(node2)
				k=k+1
		
		
		
	#   h = 0
	#   j = 0
	#   for node in self.graph.nodes:
	#   	#print "     " + str(h)
	#   	for edge in node.children:
	#   		
	#   		edgePos = G.edges()[j].attr["pos"]
	#   		newEdgePos = string.split(edgePos,' ')
	#   		node1 = newEdgePos[1]
	#   		node2 = newEdgePos[len(newEdgePos)-1]
	#   		#print str(j) + " - Node 1: " +  str(node1)
	#   		#print str(j) + " - Node 2: " + str(node2)
	#   		
	#   		node.x = float(string.split(node1,',')[0])
	#   		node.y = float(string.split(node1,',')[1])
	#   		
	#   		edge.get_far(node).x = float(string.split(node2,',')[0])
	#   		edge.get_far(node).y = float(string.split(node2,',')[1])
	#   		
	#   		j = j + 1
	#   		
	#   	h = h + 1
				# far_node = edge.get_far(node)
				# if node == far_node:
				# 	print "Circular edge."
				# 	continue
                # 
				# G.add_edge(str(node.name),str(far_node.name),color='pink',arrowhead='normal')
		
		
		# Write previously positioned graph to PNG file
		# G.draw('img/test.dot')
		# G.draw('testfile.ps',prog='circo')
		
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
		self.viz()
		return self.graph