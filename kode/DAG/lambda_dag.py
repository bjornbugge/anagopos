"""
"""

from collections import deque

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

class LambdaNode(Node):
	def alphaconvert(self, convertfrom, convertto):
		for c in self.children:
			c.alphaconvert(convertfrom, convertto)
	
	def betareduce(self):
		raise NotImplementedError("")
	

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
	
	def __repr__(self):
		return "Abstraction(" + [c.__repr__() for c in self.children].__repr__() + ")"


class Application(LambdaNode):
	"""
	Lambda application.
	"""
	def __repr__(self):
		return "Application(" + [c.__repr__() for c in self.children].__repr__() + ")"
	
	def betareduce(self):
		if isinstance(self.children[0], Abstraction):
			# return some kind of reduct/thingy perhaps...


class Variable(LambdaNode):
	"""
	A variable. Can be either bound or free.
	"""	
	def __init__(self, n):
		self.bound = False
		self.children = []
		self.name = n
	
	def __repr__(self):
		return "Variable_" + self.name + "(" + [c.__repr__() for c in self.children].__repr__() + ")"


def traverse(root, dispatch):
	"""
	Traverse down the tree, processing nodes from left to right, calling dispatch on each node.
	"""
	stack = deque([root])
	stack_pop = stack.popleft
	stack_extend = stack.extend
	stack_rotate = stack.rotate
	while stack:
		# print "Traversing..."
		node = stack_pop() 
		dispatch(node)
		if hasattr(node, 'children'):
			stack_extend(node.children)
			stack_rotate(len(node.children))


if __name__ == "__main__":	
	root_node = Application()
	appl = Application()
	
	lX = Abstraction()
	lY = Abstraction()
	
	x = Variable('x')
	y = Variable('y')
	z = Variable('z')
	
	root_node.add([lX, appl])
	appl.add([lY, z])
	lX.add([x])
	lX.assignvar([x])
	lY.add([y])
	lY.assignvar([y])
	
	def cb(node):
		print node
	
	traverse(root_node, cb)