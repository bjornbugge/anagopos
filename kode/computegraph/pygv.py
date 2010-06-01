import time
import pygraphviz as pgv
import string


# Her begynder pygraphviz koden
class GraphViz(object):
	def __init__(self, alg):
		self.term = None
		self.graph = None
		self.node = None
		self.G = None
		self.alg = alg
			
	def viz(self, graph):
		self.graph = graph
		
		# Start time
		inittime = time.time()
		
		# Adds nodes in graph to the GraphViz graph
		G = pgv.AGraph()
		for node in self.graph.nodes:
			G.add_node(str(node.name),width="0.00",heigth="0.00",fixedsize="0",margin="0.00",label=" ",shape="none",fontsize="8")
		
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
			#print "Node X: " + str(graphnode.x)
			for edge in graphnode.children:
				e = G.get_edge(graphnode.name, edge.get_far(graphnode).name)
				edgePos = e.attr["pos"]
				newEdgePos = string.split(edgePos,' ')
				edge.ipoints = [[0 for col in range(2)] for row in range(len(newEdgePos))]
				for y in range(len(newEdgePos)):
					edge.ipoints[y][0] = float(string.split(str(newEdgePos[y]),',')[0])
					edge.ipoints[y][1] = float(string.split(str(newEdgePos[y]),',')[1])
				k=k+1
				#print "	Node X: " + str(edge.ipoints[0][0])
			n = n + 1
			
		endtime = time.time()
		
		print "	Total time used by GraphViz: " + str(endtime - inittime) + "\n"