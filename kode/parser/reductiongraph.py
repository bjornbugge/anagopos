
class Graph(object):
	def __init__(self):
		self.nodes = []
	
	def __repr__(self):
		o = ''
		for n in self.nodes:
			if len(n.children) == 0:
				continue
			for c in n.children:
				o = o + "\t" + str(c.source.term) + " -" + str(c.weight) + "-> " + str(c.destination.term) + "\n"
		
		return o

class Edge(object):
	def __init__(self, source, destination):
		self.weight = 1
		self.source = source
		self.destination = destination
		
	def get_other_end(self, node):
		if node == self.source:
			return self.destination
		elif node == self.destination:
			return self.source
		else:
			raise Exception()


class Node(object):
	def __init__(self, term):
		self.children = []
		self.parents = []
		self.term = term
	
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
