import operations
from copy import deepcopy 

class Graph(object):
	def __init__(self):
		# nodesdict and nodes contain the same nodes, we just use the dictionary
		# to perform fast lookups. The list is needed in the kamada-kawai algorithm.
		self.nodesdict = {}
		self.nodes = []
		self.nodenametable = {}
		self.newest = None
	
	def __repr__(self):
		o = ''
		for (s, n) in self.nodesdict.iteritems():
			if len(n.children) == 0:
				continue
			for c in n.children:
				o = o + "\t" + str(c.source.name) + " -" + str(c.weight) + "-> " + str(c.destination.name) + "\n"
		
		return o
	
	def tostring(self):
		o = ''
		for (s, n) in self.nodesdict.iteritems():
			if len(n.children) == 0:
				continue
			for c in n.children:
				o = o + "\t" + str(c.source.term) + " -" + str(c.weight) + "-> " + str(c.destination.term) + "\n"
		
		print o
	
	def addnode(self, term, name = None):
		'''
		Adds a node made from the given term to the graph and returns it.
		If the node is already present in the graph, the method just returns it.
		Nodes are compared modulo alpha-equivalence.
		'''
		operations.sanitize(term)
		try:
			node = self.nodesdict[str(term)]
		except KeyError:
			name = 'N'+str(len(self.nodesdict))
			node = Node(term, name)
			self.nodenametable[name] = node
			if name == None:
				name = 'N'+str(len(self.nodesdict))
			node = Node(term, name)
			self.nodesdict[str(term)] = node
			self.nodes.append(node) # Append to list if we made a new node.
		
		return node
	
	def getnewest(self):
		if self.newest is None:
			cur = 0
			newest = None
			for n in self.nodes:
				if n.term.generation > cur:
					newest = n
			self.newest = newest
		return self.newest
	

class Edge(object):
	def __init__(self, source, destination):
		self.weight = 1
		self.source = source
		self.destination = destination
		self.ipoints = None

	def get_far(self, node):
		if self.source == node:
			return self.destination
		else:
			return self.source


class Node(object):
	def __init__(self, term, name):
		self.children = []
		self.parents = []
		self.term = term
		self.name = name
		self.new = False
	
	def __repr__(self):
		return "NODE " + str(self.term)
		
	def addchild(self, child):
		e = Edge(self, child)
		
		for c in self.children:
			if e.source == c.source and e.destination == c.destination:
				c.weight = c.weight + 1
				return
		
		self.children.append(e)
		child.parents.append(e)
