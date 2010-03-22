from lambda_dag import *
import yapps2
%%

parser Lambda:
	token END: "$"
	token LAM: "#"
	token DOT: "."
	token VAR: "[a-zA-Z_]+"
	token ID: "[a-zA-Z_]+"

	# If x is a variable, then x ∈ Λ
	# If x is a variable and M ∈ Λ, then (λx.M) ∈ Λ
	# If M, N ∈ Λ, then (M N) ∈ Λ
	
	rule EXP:			EXP2 EXP					
{{	A = Application()	}}
{{	child1 = EXP2	}}
{{	child2 = EXP	}}
{{	A.add(child1)	}}
{{	A.add(child2)	}}
{{	return A	}}

						| LAM VAR DOT EXP
{{	A = Abstraction()	}}
{{	child = EXP	}}
{{	A.add(child)	}}
{{	return A	}}

						| ""						{{ print "EMPTY;" }}

	rule EXP2:			VAR
{{	x = Variable(VAR)	}}
{{	return x	}}

						| "\\(" EXP "\\)"
{{	return EXP	}}