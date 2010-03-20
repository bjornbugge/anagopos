from lambda_dag import *
from math import floor, log
from copy import deepcopy

def findredexes(root):
	'''
	Returns a list of positions of all the redexes in the lambda-graph.
	A "position" in the DAG is a binary string where "0" means left child
	and "1" means right child. The root node has position 1.
	'''
	def _find(node, bitstrings, pos):
		if type(node) is Application:
			if type(node.leftchild) is Abstraction:
				bitstrings.append(pos) # It is a redex!
		
		if not node.leftchild is None:
			_find(node.leftchild, bitstrings, pos << 1)
			if not node.rightchild is None:
				_find(node.rightchild, bitstrings, (pos << 1) + 1)
	
	# The position of the root is "1"
	bitstrings = []
	_find(root, bitstrings, 1)
	return bitstrings

def getnode(root, position):
	'''
	Returns the node at the given position. The position must be positive.
	'''
	def _getnode(node, p):
		ex = int(floor(log(position, 2))) - p
		if ex < 0:
			return node
		if position & (2 ** ex) == 0: # Bit was 0; go left
			if ex == 0:
				return node.leftchild # Stop recursion
			
			return _getnode(node.leftchild, p + 1)
		else: # Bit was 1; go right
			if ex == 0:
				return node.rightchild
			
			return _getnode(node.rightchild, p + 1)
	
	return _getnode(root, 1)

def betareduce(term, redexpos):
	'''
	Performs a one-step beta reduction on the given position in the term.
	The position denotes an Application node with an active subterm as 
	left child, as returned from the function findredexes(x)
	'''
	# The copy that are transformed into a contractum.
	contractum = deepcopy(term)
	appl = getnode(contractum, redexpos)
	
	# The active subterm that we'll reduce.
	c = appl.leftchild
	for v in c.variables:
		v.parent.swap(v, deepcopy(appl.rightchild))
	
	# Remove the argument.
	appl.remove(appl.rightchild)
	# Remove the abstractor.
	c.parent.swap(c, c.leftchild)
	
	if redexpos == 1: # The top node has been reduced
		contractum = c.leftchild
	else:
		appl.parent.swap(appl, c.leftchild)
	
	return (term, contractum)

def alphaconvert(term, newname):
	'''
	Performs an alpha conversion on the given term. The term must be an 
	Abstraction-node.
	'''
	for v in term.variables:
		v.name = newname
	
def sanitize(term):
	'''
	Gives the bound variables in the abstractors unique names. The variables
	are named vX with X unique for each abstraction.
	'''
	def _getabstractors(node, abstractors):
		if type(node) is Abstraction:
			abstractors.append(node)
		if not node.leftchild is None:
			_getabstractors(node.leftchild, abstractors)
			if not node.rightchild is None:
				_getabstractors(node.rightchild, abstractors)
	
	abstractors = []
	_getabstractors(term, abstractors)
	c = 0
	for abstraction in abstractors:
		alphaconvert(abstraction, 'v' + str(c))
		c = c + 1

def standardstrategy(root, redexes):
	'''
	Given a lambda term and a list of redex positions, this function returns 
	a permutation of the redex list, representing a particular reduction 
	strategy (i.e. the order that reductions should be performed in).
	'''
	# redexes.reverse()
	return redexes # Very basic strategy!


def reductiongraph(root, strategy = standardstrategy):
	'''
	Computes the reduction graph and returns it as a set of 
	(redex, contractum)-pairs.
	'''
	work = [root]
	graph = set()
	guard = 0
	while len(work) > 0 and guard < 20:
		term = work[0]
		positions = strategy(term, findredexes(term))
		for pos in positions:
			pair = betareduce(term, pos)
			graph.add(pair)
			if not pair[1] in work:
				work.append(pair[1])
		del work[0]
		guard = guard + 1
	
	# return graph
	
	for (k,v) in graph:
		sanitize(k)
		sanitize(v)
		print str(k) + "\t\t---->\t\t" + str(v)
	
if __name__ == "__main__":
#          @
#         / \
#        Lx  ---@
#        |     / \
#        x    Ly  z
#             |
#             y
	rn = Application()
	appl = Application()
	# appl2 = Application()
	# appl3 = Application()
	
	lX = Abstraction()
	# lA = Abstraction()
	lY = Abstraction()
	
	x = Variable('x')
	y = Variable('y')
	z = Variable('z')
	# a = Variable('a')
	# b = Variable('b')
	
	rn.add(lX)
	rn.add(appl)
	appl.add(lY)
	appl.add(z)
	lX.add(x)
	lX.assignvar(x)
	lY.add(y)
	lY.assignvar(y)
	# appl2.add(lA)
	# 	appl2.add(b)
	# 	lA.add(appl3)
	# 	appl3.add(x)
	# 	appl3.add(a)
	# 	lA.assignvar(a)
	# 	lX.add(appl2)
	# 	lX.assignvar(x)
	
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
	a2 = deepcopy(a1)
	a3 = deepcopy(a2)
	g1 = Application()
	g1.add(a1)
	g1.add(a2)
	g2 = Application()
	g2.add(g1)
	g2.add(a3)
	w31.add(g2)
	w31.assignvar(a1)
	w31.assignvar(a2)
	w31.assignvar(a3)
	
	w32 = Abstraction()
	b1 = Variable('b')
	b2 = deepcopy(b1)
	b3 = deepcopy(b2)
	g3 = Application()
	g3.add(b1)
	g3.add(b2)
	g4 = Application()
	g4.add(g3)
	g4.add(b3)
	w32.add(g4)
	w32.assignvar(b1)
	w32.assignvar(b2)
	w32.assignvar(b3)
	
	g0 = Application()
	g0.add(w31)
	g0.add(w32)
	
	print str(rn)
	print str(g0)