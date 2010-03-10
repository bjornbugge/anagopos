"""
"""

from collections import deque

class Node(object):
	"""
	A node in a graph...
	"""
	v_count = 0
	def __init__(self):
		self.children = []
	
	def alphaconvert(self):
		raise NotImplementedError("")
	
	def add(self, nodes):
		self.children.extend(nodes)
	
	def remove(self, nodes):
		for n in nodes:
			self.children.remove(n)

class Abstraction(Node):
	"""
	A lambda abstraction. Knows which descending nodes it binds.
	"""
	variables = []
	def assignvar(self, *variablenode):
		self.variables.extend(variablenode)
	
	def alphaconvert(self):
		
	
	def __repr__(self):
		return "Abstraction(" + [c.__repr__() for c in self.children].__repr__() + ")"


class Application(Node):
	"""
	Lambda application.
	"""
	def __repr__(self):
		return "Application(" + [c.__repr__() for c in self.children].__repr__() + ")"
		


class Variable(Node):
	"""
	A variable. Can be either bound or free.
	"""
	bound = False
	def bind():
		bound = True
	
	def __init__(self, opt_name):
		self.children = []
		self.given_name = opt_name
	
	def __repr__(self):
		return "Variable_" + self.given_name + "(" + [c.__repr__() for c in self.children].__repr__() + ")"


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
	lX.assignvar(x)
	lY.add([y])
	lY.assignvar(y)
	
	def cb(node):
		print node.__repr__()
	
	traverse(root_node, cb)