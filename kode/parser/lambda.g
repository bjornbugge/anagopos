parser Lambda:
    token END: "$"
	token LAM: "[λ]+"
	token DOT: "[.]+"
	token VAR: "[a-zA-Z_]+"


	# If x is a variable, then x ∈ Λ
	# If x is a variable and M ∈ Λ, then (λx.M) ∈ Λ
	# If M, N ∈ Λ, then (M N) ∈ Λ


	# x			#variable
	rule x:                 x VAR                   {{ return x }}

	# t ::=		#terms
	rule term:              x                       {{ return x }}
                          | abstraction             {{ return abstraction }}
                          | parentheses             {{ return parentheses }}

	# (λx.t)	#abstraction
	rule abstraction:       "λ" x DOT abstraction   {{ return term }}
                          | x                       {{ return x }}

	# # (t t)		#parentheses
	rule parentheses:       "\\("term term"\\)"     {{ return term }}





	# 						    rule goal:           expr END         {{ return expr }}
	
	# 						    # An expression is the sum and difference of factors
	# 						    rule expr:           factor           {{ v = factor }}
	# 						                       ( "[+]" factor       {{ v = v+factor }}
	# 						                       |  "-"  factor       {{ v = v-factor }}
	# 						                       )*                 {{ return v }}
	
	# 						    # A factor is the product and division of terms
	# 						    rule factor:         term             {{ v = term }}
	# 						                       ( "[*]" term         {{ v = v*term }}
	# 						                       |  "/"  term         {{ v = v/term }}
	# 						                       )*                 {{ return v }}
	
	# 						    # A term is either a number or an expression surrounded by parentheses
	# 						    rule term:           NUM              {{ return atoi(NUM) }}
	# 						                       | "\\(" expr "\\)" {{ return expr }}
