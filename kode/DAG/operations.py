from lambda_dag import *
from collections import deque

def traverse(root, dispatch):
	"""
	Traverse down the tree, processing nodes from left to right, calling dispatch on each node.
	"""
	stack = deque([root])
	stack_pop = stack.popleft
	stack_extend = stack.extend
	stack_rotate = stack.rotate
	while stack:
		node = stack_pop() 
		dispatch(node)
		if hasattr(node, 'children'):
			stack_extend(node.children)
			stack_rotate(len(node.children))

def reductiongraph(root):
	"""
	Returns the beta-reduction-graph.
	"""
	graph = []
	todo = [root]
	
	while todo:
		elm = onestep(todo[0])
		if not elm is None:
			redex, contractum = elm
			graph.append((redex, contractum.clone()))
			print "Contractum", str(contractum)
			todo.append(contractum)
		del todo[0]
	
	for (k,v) in graph:
		print str(k) + "\t\t---->\t\t" + str(v)
	
	return graph

def onestep(term):
	"""
	Performs a beta reduction (single step).
	"""
	if type(term) is Application:
		# Make a copy of the old node to maintain a 'history'.
		redex = term.clone()
		left = term.leftchild()
		right = term.rightchild()
		print "Before reduce;", left, right
		left.reduce(right)
		print "After reduce;", left
		contractum = left.leftchild()
		del term
		
		return (redex, contractum)
	

if __name__ == "__main__":
#          @
#         / \
#        Lx  ---@
#        |     / \
#        x    Ly  z
#             |
#             y
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

#        @
#       / \
#      La  Lb
#      |   |
#      @   ---@
#     / \    / \
#    @   a   @  b
#   / \     / \
#  a   a   b   b

	w31 = Abstraction()
	a1 = Variable('a')
	g1 = Application()
	g1.add([a1, a1])
	g2 = Application()
	g2.add([g1, a1])
	w31.add([g2])
	w31.assignvar([a1])
	
	w32 = Abstraction()
	a2 = Variable('b')
	g3 = Application()
	g3.add([a2, a2])
	g4 = Application()
	g4.add([g3, a2])
	w32.add([g4])
	w32.assignvar([a2])

	g0 = Application()
	g0.add([w31, w32])
	
	def cb(n):
		print n
	traverse(root_node, cb)