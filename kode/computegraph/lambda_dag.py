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
		self.strrepr = ''
		self.redexepositions = []
		self.generation = -1
	
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
		# Use identity, not equality. The DAG must contain the node in order to
		# be able to delete it.
		if self.leftchild is node:
			self.leftchild = None
			node.parent = None
		elif self.rightchild is node:
			self.rightchild = None
			node.parent = None
	
	def swap(self, old, new):
		'''
		Swap the old node with the new node -- if the old node is a child.
		'''
		# Use identity, not equality. The DAG must contain the nodes in order to
		# be able to swap them.
		if self.leftchild is old:
			self.leftchild = new
			new.parent = self
			old.parent = None
		elif self.rightchild is old:
			self.rightchild = new
			new.parent = self
			old.parent = None
	
	def makestr(self):
		pass
	
	def copy(self):
		'''
		Use instead of the copy.deepcopy(), this is much much faster!
		'''
		pass
	
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
	
	def copy(self):
		a = Abstraction()
		c = self.leftchild.copy()
		a.varname = self.varname
		a.add(c)
		a.dirty = self.dirty
		a.strrepr = self.strrepr
		a.redexepositions.extend(self.redexepositions)
		a.generation = self.generation
		return a
	
	def assignvar(self, variablenode):
		'''
		Register the node as a variable bound by this abstractor.
		'''
		self.variables.append(variablenode)
		if self.varname == '':
			self.varname = variablenode.name
	
	def makestr(self):
		self.leftchild.makestr()
		self.strrepr = "#" + self.varname + ".(" + self.leftchild.strrepr + ")"
	
	def __repr__(self):
		return self.strrepr
		# return "#" + self.varname + ".(" + str(self.leftchild) + ")"

class Application(LambdaNode):
	"""
	Lambda application.
	"""
	def copy(self):
		a = Application()
		c1 = self.leftchild.copy()
		c2 = self.rightchild.copy()
		a.add(c1)
		a.add(c2)
		a.dirty = self.dirty
		a.strrepr = self.strrepr
		a.redexepositions.extend(self.redexepositions)
		a.generation = self.generation
		return a
	
	def makestr(self):
		s1 = s2 = ''
		if self.leftchild:
			self.leftchild.makestr()
			s1 = self.leftchild.strrepr
		if self.rightchild:
			self.rightchild.makestr()
			s2 = self.rightchild.strrepr
		self.strrepr = "(" + s1 + " " + s2 + ")"
	
	def __repr__(self):
		return self.strrepr

class Variable(LambdaNode):
	"""
	A variable. Can be either bound or free.
	"""
	def copy(self):
		v = Variable(self.name)
		v.dirty = self.dirty
		v.strrepr = self.strrepr
		v.redexepositions.extend(self.redexepositions)
		v.generation = self.generation
		return v
		
	def makestr(self):
		self.strrepr = self.name
		
	def __init__(self, n):
		super(Variable, self).__init__()
		self.name = n
	
	def add(self, node):
		pass # A variable can't have children
	
	def remove(self, node):
		pass
		
	def __repr__(self):
		return self.strrepr
