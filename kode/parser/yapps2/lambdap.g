from lambda_dag import *
%%

parser Lambda:
	ignore:    "[ \r\t\n]+"
	token END: "$"
	token LAM: "#"
	token DOT: "."
	token VAR: "[a-zA-Z_]+"
	token ID: "[a-zA-Z_]+"

	# If x is a variable, then x ∈ Λ
	# If x is a variable and M ∈ Λ, then (λx.M) ∈ Λ
	# If M, N ∈ Λ, then (M N) ∈ Λ
		
	rule EXP:			EXP2 EXP					
{{	print "EXP2 EXP;"	}}
{{	child1 = EXP2	}}
{{	child2 = EXP	}}
{{	if not child2 is None: A = Application()	}}
{{	if not child2 is None: A.add(child1)	}}
{{	if not child2 is None: A.add(child2)	}}
{{	if not child2 is None: return A	}}
{{	else: return EXP2 }}

						| LAM VAR DOT EXP
{{	print "ABS;"	}}
{{	A = Abstraction()	}}
{{	child = EXP	}}
{{	A.add(child)	}}
{{	A.varname = VAR	}}
{{	return A	}}

						| ""						{{ print "EMPTY;" }}

	rule EXP2:			VAR
{{	print "VAR = ", VAR	}}
{{	x = Variable(VAR)	}}
{{	return x	}}

						| "\\(" EXP "\\)"
{{	print "PAR"	}}
{{	return EXP	}}