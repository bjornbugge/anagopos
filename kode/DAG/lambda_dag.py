"""
"""

from collections import deque

class Node(object):
	"""
	A node in a graph...
	"""
	def __new__(cls, *args, **kw):
		instance = object.__new__(cls, *args, **kw)
		return instance

	# @classmethod
	# def get(self, id):
	# 	"""
	# 	Returns a node by its _id attribute.
	# 	"""
	# 	return cls._instances[id]
	
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
	children = []
	def assignvar(self, *variablenode):
		self.variables.extend(variablenode)
	
	def __repr__(self):
		# return "Abstraction(" + [c.__repr__() for c in self.children] + ")"
		return "Abstraction"


class Application(Node):
	"""
	Lambda application.
	"""
	children = []
	def __repr__(self):
		# return "Application(" + [c.__repr__() for c in self.children] + ")"
		return "Application"
		


class Variable(Node):
	"""
	A variable. Can be either bound or free.
	"""
	children = []
	bound = False
	def bind():
		bound = True
	
	def __repr__(self):
		# return "Variable(" + [c.__repr__() for c in self.children] + ")"
		return "Variable"



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
	
	x = Variable()
	y = Variable()
	z = Variable()
	
	root_node.add([lX, appl])
	appl.add([lY, z])
	lX.add([x])
	lX.assignvar(x)
	lY.add([y])
	lY.assignvar(y)
	
	def cb(node):
		print node
		return node.__repr__()
	
	string = traverse(root_node, cb)
	for s in string:
		print s