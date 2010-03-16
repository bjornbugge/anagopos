"""
DAG-representation of lambda terms.
"""

class Node(object):
	"""
	A node in a graph...
	"""
	def __init__(self):
		self.children = []
		
	def add(self, nodes):
		self.children.extend(nodes)
	
	def remove(self, nodes):
		for n in nodes:
			self.children.remove(n)
	
	def clone(self):
		return NotImplementedError('')

class LambdaNode(Node):
	def alphaconvert(self, convertfrom, convertto):
		for c in self.children:
			c.alphaconvert(convertfrom, convertto)
	
	def leftchild(self):
		return self.children[0]

	def rightchild(self):
		return self.children[1]
	

class Abstraction(LambdaNode):
	"""
	A lambda abstraction. Knows which descending nodes it binds.
	"""
	def assignvar(self, variablenode):
		self.variables.extend(variablenode)
	
	def __init__(self):
		self.children = []
		self.variables = []
	
	def alphaconvert(self, convertfrom, convertto):
		for v in self.variables:
			if v.name == convertfrom:
				v.name = convertto
		for c in self.children:
			if c not in self.variables:
				c.alphaconvert(convertfrom, convertto)
	
	def reduce(self, term):
		for c in self.children:
			if c in self.variables:
				self.children.insert(self.children.index(c), term)
				self.children.remove(c)
			else:
				c.reduce()
	
	def clone(self):
		n = Abstraction()
		n.add([c.clone() for c in self.children])
		n.assignvar([v.clone() for v in self.variables])
		return n
	
	def __repr__(self):
		return "$"+self.variables[0].name+".("+ [c.__repr__() for c in self.children].__repr__() +")"


class Application(LambdaNode):
	"""
	Lambda application.
	"""
	def clone(self):
		n = Application()
		n.add([c.clone() for c in self.children])
		return n
	
	def __repr__(self):
		return "(" + self.leftchild().__repr__() + " " + self.rightchild().__repr__() + ")"

class Variable(LambdaNode):
	"""
	A variable. Can be either bound or free.
	"""	
	def __init__(self, n):
		self.bound = False
		self.children = [] # A variable can't have children
		self.name = n
	
	def clone(self):
		n = Variable(self.name)
		n.bound = self.bound
		return n
	
	def __repr__(self):
		return self.name
