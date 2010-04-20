from operations import *
from lambda_dag import *
from copy import deepcopy

def test():
	term = Abstraction()
	term.varname = 'B1'
	t1 = Application()
	term.add(t1)
	t2 = Abstraction()
	t2.varname = 'B2'
	t1.add(t2)
	v1 = Variable('B1')
	# v2 = Variable('B2')
	v2 = Application()
	v2.add(Variable('B2'))
	v2.add(Variable('B2'))
	t1.add(v1)
	t2.add(v2)
	t3 = Application()
	t3.add(term)
	v3 = Variable('B3')
	t3.add(v3)
	assignvariables(t3)
	g = reductiongraph(t3)
	
	return g

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
	# lX.assignvar(x)
	lX.varname = 'x'
	lY.add(y)
	# lY.assignvar(y)
	lY.varname = 'y'
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
	
	assignvariables(rn)
	print str(rn)
	print str(g0)