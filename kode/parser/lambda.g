parser Lambda:
    token END: "$"
	token LAM: "[£”]+"
	token VAR: "[a-zA-Z_]+"

    rule goal:           expr END         {{ return expr }}



	# t ::=		#terms
	# x			#variable
	# (λx.t)	#abstraction
	# (t t)		#application
	# rule application:           "\\(" expr "\\)" {{ return expr }}



    # An expression is the sum and difference of factors
    # rule expr:           factor           {{ v = factor }}
    #                    ( "[+]" factor       {{ v = v+factor }}
    #                    |  "-"  factor       {{ v = v-factor }}
    #                    )*                 {{ return v }}

    # A factor is the product and division of terms
    # rule factor:         term             {{ v = term }}
    #                       ( "[*]" term         {{ v = v*term }}
    #                       |  "/"  term         {{ v = v/term }}
    #                       )*                 {{ return v }}


	# An expression is the sum and difference of factors
    rule expr:         term             {{ v = term }}
                       ( "/"  term         {{ v = v/term }}
                       )*                 {{ return v }}


	# If x is a variable, then x ∈ Λ


	# If x is a variable and M ∈ Λ, then (λx.M) ∈ Λ


	# If M, N ∈ Λ, then (M N) ∈ Λ


    # A term is either a number or an expression surrounded by parentheses
    rule term:           "\\(" expr "\\)" {{ return expr }}
