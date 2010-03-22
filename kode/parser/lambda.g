parser Lambda:
	token END: "$"
	token LAM: "#"
	token DOT: "."
	token VAR: "[a-zA-Z_]+"
	token ID: "[a-zA-Z_]+"

	# If x is a variable, then x ∈ Λ
	# If x is a variable and M ∈ Λ, then (λx.M) ∈ Λ
	# If M, N ∈ Λ, then (M N) ∈ Λ

	rule goal:			  EXP END					{{ print "END;" }}

	rule x:				  VAR						{{ print "x -> VAR" }}
	
	rule EXP:			  EXP2 EXP					{{ print "EXP2 EXP;" }}
						| ""

	rule EXP2:			  VAR						{{ print "VAR = ", VAR }}
						| LAM VAR DOT EXP			{{ print "ABS;" }}
						| "\\(" EXP "\\)"			{{ print "PAR;" }}