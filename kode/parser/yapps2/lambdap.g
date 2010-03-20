parser Lambda:
	token END: "$"
	token LAM: "#"
	token DOT: "."
	token VAR: "[a-zA-Z_]+"
	token ID: "[a-zA-Z_]+"

	# If x is a variable, then x ∈ Λ
	# If x is a variable and M ∈ Λ, then (λx.M) ∈ Λ
	# If M, N ∈ Λ, then (M N) ∈ Λ

	rule goal:			  EXP END				{{ print "end;" }}

	rule x:				  VAR					{{ print "var" }}

	# rule exp1:			  term exp2				{{ print "exp1" }}
	# 
	# rule exp2:			  term exp2				{{ print "exp2" }}
	# 
	# rule term:			  x						{{ print "rule1" }}
	# 					| abstraction			{{ print "rule2" }}
	# 					| parentheses			{{ print "rule3" }}
	# 					| exp1					{{ print "rule4" }}
	# 
	# rule abstraction:	  LAM x DOT exp1		{{ print "abstraction;" }}
	# 
	# rule parentheses:	  "\\("exp1"\\)"		{{ print "parentheses;" }}
	
	
	# rule EXP:			  VAR					{{ print "VAR;" }}
	# 						| LAM VAR DOT EXP		{{ print "ABS;" }}
	# 						| "\\(" EXP "\\)"	 	{{ print "PAR;" }}
	# 						| EXP2					{{ print "EXP2 EXP;" }}
	# 						
	# 	rule EXP2:			  EXP EXP2
	
	rule EXP:			  EXP2 EXP					{{ print "EXP;" }}
						| ""

	rule EXP2:			  VAR						{{ print "VAR;" }}
						| LAM VAR DOT EXP			{{ print "ABS;" }}
						| "\\(" EXP "\\)"			{{ print "PAR;" }}