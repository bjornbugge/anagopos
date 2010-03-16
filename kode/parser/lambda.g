parser Lambda:
    token END: "$"
	token LAM: "#"
	token DOT: "."
	token VAR: "[a-zA-Z_]+"


	# If x is a variable, then x ∈ Λ
	# If x is a variable and M ∈ Λ, then (λx.M) ∈ Λ
	# If M, N ∈ Λ, then (M N) ∈ Λ
	
#	rule goal:           term END         {{ print "term" }}
#
#
#	# x			#variable
#	rule x:                 VAR                   {{ print "var" }}
#
#	# t ::=		#terms
#	rule term:              x                       {{  }}
#                          | abstraction             {{  }}
#                          | parentheses             {{  }}
#
#	# (λx.t)	#abstraction
#	rule abstraction:       LAM x DOT term   {{ print "abstraction" }}
#
#	# # (t t)		#parentheses
#	rule parentheses:       "\\("term term"\\)"     {{ print "parentheses" }}
#

    rule goal:  term END    {{}}
    
    rule exp:   VAR                 {{}}
                | LAM VAR DOT exp   {{}}
                | exp exp           {{}}   # LEFT RECURSION!
                | "\\(" exp "\\)"   {{}}

#
#    <Exp> ::= <ident> |
#              <constant> |
#              lambda <ident> . <Exp> |      -- function abstraction
#              <Exp> <Exp> |                 -- function application
#              ( <Exp> )
#

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
