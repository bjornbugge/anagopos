import operations

'''
DAG-representation of lambda terms.
'''

class LambdaNode(object):
	def __init__(self):
		self.leftchild = None
		self.rightchild = None
		self.parent = None
		self.dirty = True # Indicates whether the term can be sanitized.
		
	def add(self, node):
		'''
		Add a child node. If this node already has two children, nothing happens.
		'''
		if self.leftchild is None:
			self.leftchild = node
			node.parent = self
	 	elif self.rightchild is None:
			self.rightchild = node
			node.parent = self
	
	def remove(self, node):
		'''
		Remove the node if it is a child.
		'''
		if self.leftchild == node:
			self.leftchild = None
			node.parent = None
		elif self.rightchild == node:
			self.rightchild = None
			node.parent = None
	
	def swap(self, old, new):
		'''
		Swap the old node with the new node -- if the old node is a child.
		'''
		if self.leftchild == old:
			self.leftchild = new
			new.parent = self
			old.parent = None
		elif self.rightchild == old:
			self.rightchild = new
			new.parent = self
			old.parent = None
	
	def __eq__(self, other):
		'''
		Equality of two DAGs is defined as the string equality of their 
		normalized string representations.
		'''
		if other is None:
			return False
		operations.sanitize(self)
		operations.sanitize(other)
		return str(self) == str(other)
	
	def __ne__(self, other):
		return not self.__eq__(self, other)

class Abstraction(LambdaNode):
	"""
	A lambda abstraction. Knows which descending nodes it binds.
	"""
	def __init__(self):
		super(Abstraction, self).__init__()
		self.variables = []
		self.varname = ''
	
	def assignvar(self, variablenode):
		'''
		Register the node as a variable bound by this abstractor.
		'''
		self.variables.append(variablenode)
		if self.varname == '':
			self.varname = variablenode.name
	
	def __repr__(self):
		return "#" + self.varname + ".(" + str(self.leftchild) + ")"

class Application(LambdaNode):
	"""
	Lambda application.
	"""
	def __repr__(self):
		return "(" + str(self.leftchild) + " " + str(self.rightchild) + ")"

class Variable(LambdaNode):
	"""
	A variable. Can be either bound or free.
	"""
	def __init__(self, n):
		super(Variable, self).__init__()
		self.name = n
	
	def add(self, node):
		pass # A variable can't have children
	
	def remove(self, node):
		pass
		
	def __repr__(self):
		return self.name
