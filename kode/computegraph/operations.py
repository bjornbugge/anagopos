import lambda_dag
import reductiongraph as graphrepr # nameclash!
import math
import copy
import collections

def assignvariables(root):
	'''
	Alters the DAG such that every Abstraction node knows which descending 
	Variable nodes it binds.
	'''
	def _assignall(node, abstractorstack):
		if type(node) is lambda_dag.Variable:
			for abstractor in abstractorstack:
				if node.name == abstractor.varname:
					abstractor.assignvar(node)
					break
		elif type(node) is lambda_dag.Abstraction:
			abstractorstack.appendleft(node)
			node.variables = []
			_assignall(node.leftchild, abstractorstack)
			abstractorstack.popleft()
		else: # type(node) is Application
			_assignall(node.leftchild, abstractorstack)
			_assignall(node.rightchild, abstractorstack)
	
	_assignall(root, collections.deque([]))

def findredexes(root):
	'''
	Returns a list of positions of all the redexes in the lambda-graph.
	A "position" in the DAG is a binary string where "0" means left child
	and "1" means right child. The root node has position 1.
	'''
	def _find(node, bitstrings, pos):
		if type(node) is lambda_dag.Application:
			if type(node.leftchild) is lambda_dag.Abstraction:
				bitstrings.append(pos) # It is a redex!
		
		if not node.leftchild is None:
			_find(node.leftchild, bitstrings, pos << 1)
			if not node.rightchild is None:
				_find(node.rightchild, bitstrings, (pos << 1) + 1)
	
	# The position of the root is "1"
	bitstrings = []
	_find(root, bitstrings, 1)
	return bitstrings

def findredexesdirectly(root):
	'''
	Returns a list containing pointers to the Application nodes in the DAG
	whose left child is a redex.
	'''
	def _find(node, redexes):
		if type(node) is lambda_dag.Application:
			if type(node.leftchild) is lambda_dag.Abstraction:
				redexes.append(node)
		if not node.leftchild is None:
			_find(node.leftchild, redexes)
			if not node.rightchild is None:
				_find(node.rightchild, redexes)
	
	rs = []
	_find(root, rs)
	return rs

def getnode(root, position):
	'''
	Returns the node at the given position. The position must be positive.
	'''
	def _getnode(node, p):
		ex = int(math.floor(math.log(position, 2))) - p
		if ex < 0:
			return node
		if position & (2 ** ex) == 0: # Bit was 0; go left
			if ex == 0:
				return node.leftchild # Stop recursion
			
			return _getnode(node.leftchild, p + 1)
		else: # Bit was 1; go right
			if ex == 0:
				return node.rightchild # Stop recursion
			
			return _getnode(node.rightchild, p + 1)
	
	return _getnode(root, 1)

def betareduce(term, redexpos):
	'''
	Performs a one-step beta reduction on the given position in the term.
	The position denotes an Application node with an active subterm as 
	left child, as returned from the function findredexes(x)
	'''
	# The copy that is transformed into a contractum.
	contractum = copy.deepcopy(term)
	appl = getnode(contractum, redexpos)
	
	# The active subterm that we'll reduce.
	c = appl.leftchild
	for v in c.variables:
		v.parent.swap(v, copy.deepcopy(appl.rightchild))
	
	# Remove the argument.
	appl.remove(appl.rightchild)
	
	# Remove the abstractor.
	c.parent.swap(c, c.leftchild)
	
	if redexpos == 1: # The top node has been reduced.
		contractum = c.leftchild
	else:
		appl.parent.swap(appl, c.leftchild)
	
	# Refresh variable bindings so newly copied variables are known by abstractors.
	assignvariables(contractum)
	
	contractum.dirty = True
	return (term, contractum)

def alphaconvert(term, newname):
	'''
	Performs an alpha conversion on the given term. The term must be an 
	Abstraction-node.
	'''
	for v in term.variables:
		v.name = newname
	term.varname = newname
	
def sanitize(term):
	'''
	Gives the bound variables in the abstractors unique names. The variables
	are named vX with X unique for each abstraction.
	If the term has its dirty flag set to False, sanitize() doesn't do anything.
	'''
	if not term.dirty:
		return
	
	def _getabstractors(node, abstractors):
		if type(node) is lambda_dag.Abstraction:
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
	
	term.dirty = False

def reductiongraph(root, maximum = 20):
	'''
	Computes the reduction graph and returns it in the format specified
	in reductiongraph.py.
	'''
	work = [root]
	graph = graphrepr.Graph()
	guard = 0
	reductions = 0
	while len(work) > 0 and (maximum == 0 or guard < maximum):
		term = work[0]
		positions = findredexes(term)
		for pos in positions:
			(term, contractum) = betareduce(term, pos)
			n1 = graph.addnode(term)
			n2 = graph.addnode(contractum)
			n1.addchild(n2)
			
			if not contractum in work:
				work.append(contractum)
			
			reductions = reductions + 1
		del work[0]
		guard = guard + 1
	print "Performed " + str(reductions) + " reductions."
	if len(work) > 0:
		print "Incomplete reduction graph!"
	return graph

def reductiongraphyield(root, start, end):
	'''
	Computes the reduction graph and returns it in the format specified
	in reductiongraph.py.
	'''
	work = [root]
	graph = graphrepr.Graph()
	guard = 0
	reductions = 0
	while len(work) > 0 and (end == 0 or guard < end):
		term = work[0]
		positions = findredexes(term)
		for pos in positions:
			(term, contractum) = betareduce(term, pos)
			n1 = graph.addnode(term)
			n2 = graph.addnode(contractum)
			n1.addchild(n2)
			
			if not contractum in work:
				work.append(contractum)
			
			
			reductions = reductions + 1
		del work[0]
		if guard >= start:
			yield copy.deepcopy(graph)
		guard = guard + 1
	print "Performed " + str(reductions) + " reductions."
	if len(work) > 0:
		print "Incomplete reduction graph!"
	