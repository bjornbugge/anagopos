from computegraph.operations import *
from computegraph.lambda_dag import *
import lambdaparser.lambdaparser as par
from copy import deepcopy
import pdb

# problemterm = '(#v0.((#v1.(#v2.(#v3.(v0))) #v4.(v4))) #v5.(#v6.((v6 v6))))'
# problemterm = '#a.(#x.(x x) a) (#b.(b))'
problemterm = '(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((#v0.(((((v0 v0) v0) a) a)) #v1.(((((v1 v1) v1) a) a))) #v2.(((((v2 v2) v2) a) a))) a) a) #v3.(((((v3 v3) v3) a) a))) a) a) #v4.(((((v4 v4) v4) a) a))) a) a) #v5.(((((v5 v5) v5) a) a))) a) a) #v6.(((((v6 v6) v6) a) a))) a) a) #v7.(((((v7 v7) v7) a) a))) a) a) #v8.(((((v8 v8) v8) a) a))) a) a) #v9.(((((v9 v9) v9) a) a))) a) a) #v10.(((((v10 v10) v10) a) a))) a) a) #v11.(((((v11 v11) v11) a) a))) a) a) #v12.(((((v12 v12) v12) a) a))) a) a) #v13.(((((v13 v13) v13) a) a))) a) a) #v14.(((((v14 v14) v14) a) a))) a) a) #v15.(((((v15 v15) v15) a) a))) a) a) #v16.(((((v16 v16) v16) a) a))) a) a) #v17.(((((v17 v17) v17) a) a))) a) a) #v18.(((((v18 v18) v18) a) a))) a) a) #v19.(((((v19 v19) v19) a) a))) a) a) #v20.(((((v20 v20) v20) a) a))) a) a) #v21.(((((v21 v21) v21) a) a))) a) a) #v22.(((((v22 v22) v22) a) a))) a) a) #v23.(((((v23 v23) v23) a) a))) a) a) #v24.(((((v24 v24) v24) a) a))) a) a) #v25.(((((v25 v25) v25) a) a))) a) a) #v26.(((((v26 v26) v26) a) a))) a) a) #v27.(((((v27 v27) v27) a) a))) a) a) #v28.(((((v28 v28) v28) a) a))) a) a) #v29.(((((v29 v29) v29) a) a))) a) a) #v30.(((((v30 v30) v30) a) a))) a) a) #v31.(((((v31 v31) v31) a) a))) a) a) #v32.(((((v32 v32) v32) a) a))) a) a) #v33.(((((v33 v33) v33) a) a))) a) a) #v34.(((((v34 v34) v34) a) a))) a) a) #v35.(((((v35 v35) v35) a) a))) a) #v36.((((v36 v36) v36) a)))'
# problemterm = '((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((#v0.(((((v0 v0) v0) a) a)) #v1.(((((v1 v1) v1) a) a))) #v2.(((((v2 v2) v2) a) a))) a) a) #v3.(((((v3 v3) v3) a) a))) a) a) #v4.(((((v4 v4) v4) a) a))) a) a) #v5.(((((v5 v5) v5) a) a))) a) a) #v6.(((((v6 v6) v6) a) a))) a) a) #v7.(((((v7 v7) v7) a) a))) a) a) #v8.(((((v8 v8) v8) a) a))) a) a) #v9.(((((v9 v9) v9) a) a))) a) a) #v10.(((((v10 v10) v10) a) a))) a) a) #v11.(((((v11 v11) v11) a) a))) a) a) #v12.(((((v12 v12) v12) a) a))) a) a) #v13.(((((v13 v13) v13) a) a))) a) a) #v14.(((((v14 v14) v14) a) a))) a) a) #v15.(((((v15 v15) v15) a) a))) a) a) #v16.(((((v16 v16) v16) a) a))) a) a) #v17.(((((v17 v17) v17) a) a))) a) a) #v18.(((((v18 v18) v18) a) a))) a) a) #v19.(((((v19 v19) v19) a) a))) a) a) #v20.(((((v20 v20) v20) a) a))) a) a) #v21.(((((v21 v21) v21) a) a))) a) a) #v22.(((((v22 v22) v22) a) a))) a) a) #v23.(((((v23 v23) v23) a) a))) a) a) #v24.(((((v24 v24) v24) a) a))) a) a) #v25.(((((v25 v25) v25) a) a))) a) a) #v26.(((((v26 v26) v26) a) a))) a) a) #v27.(((((v27 v27) v27) a) a))) a) a) #v28.(((((v28 v28) v28) a) a))) a) a) #v29.(((((v29 v29) v29) a) a))) a) a) #v30.(((((v30 v30) v30) a) a))) a) a) #v31.(((((v31 v31) v31) a) a))) a) a) #v32.(((((v32 v32) v32) a) a))) a) a) #v33.(((((v33 v33) v33) a) a))) a) a) #v34.(((((v34 v34) v34) a) a))) a) #v35.((((v35 v35) v35) a)))'

# '#x.#y.(x y x) #x.(x x x a) #x.(x x x a a)'

def test(t = problemterm):
	term = par.parse(t)
	assignvariables(term)
	mgs = []
	pdb.set_trace()
	gs = [g for g in reductiongraphiter(term, 0, 10)]
	for g in gs:
		print g.tostring()
	return gs

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