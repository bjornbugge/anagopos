import computegraph.operations as operations
from computegraph.lambda_dag import *
from copy import deepcopy
from random import uniform, randint


# (#B1.(#B2.#B3.#B4.B1 #B5.#B6.#B7.((#B8.#B9.#B10.B6 (#B11.B1 (B7 #B12.#B13.B5))) #B14.B5)) #B15.F1)
# #B1.(#B2.#B3.B2 #B4.(B4 (((#B5.#B6.(#B7.B5 B5) #B8.#B9.B9) #B10.#B11.B1) ((F1 (#B12.B12 B1)) B1))))

def generatereductiongraph():
	'''
	Generate a random beta-reduction graph.
	'''
	term = randomdag()
	operations.assignvariables(term)
	print term
	print "----"
	return operations.reductiongraph(term)

def randomdag():
	'''
	Generate a pseude-random DAG-representation of a lambda term.
	'''
	global freevars
	global boundvars
	freevars = 0
	boundvars = 0
	
	def _node(p, boundlist):
		global freevars
		global boundvars
		
		r = uniform(0,1)
		
		if r < p['abstraction']:
			_lp = p
			_lp['variable'] = _lp['variable'] + 0.09
			_lp['abstraction'] = _lp['abstraction'] - 0.07
			_lp['application'] = _lp['application'] - 0.02

			node = Abstraction()
			boundvars = boundvars + 1
			b = 'B' + str(boundvars)
			node.varname = b
			node.add(_node(_lp, boundlist + [b]))
			
		elif r < p['abstraction'] + p['application']:
			_lp = deepcopy(p)
			_lp['abstraction'] = _lp['abstraction'] + 0.04
			_lp['application'] = _lp['application'] - 0.04
			_lp['variable'] = _lp['variable'] + 0.02
			
			node = Application()
			node.add(_node(_lp, boundlist))
			node.add(_node(p, boundlist))
			
		else:
			if uniform(0,1) < p['boundvar'] and not len(boundlist) == 0:
				name = boundlist[randint(0, len(boundlist) - 1)]
			else:
				freevars = freevars + 1
				name = 'F' + str(freevars)
			node = Variable(name)
		
		return node
	
	p = {'abstraction' 	: 0.6,
		 'application' 	: 0.4,
		 'variable'		: 0.0,
		
		 'boundvar'		: 0.95}

	start = _node(p, [])
	
	return start