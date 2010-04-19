from lambda_dag import *
from operations import *
from copy import deepcopy
from random import uniform, randint

def generatereductiongraph():
	'''
	Generate a random beta-reduction graph.
	'''
	term = randomdag()
	assignvariables(term)
	print term
	print "----"
	reductiongraph(term)

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
			_lp['variable'] = _lp['variable'] + 0.07
			_lp['abstraction'] = _lp['abstraction'] - 0.06
			_lp['application'] = _lp['application'] - 0.01

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