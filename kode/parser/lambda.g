parser Lambda:
    token END: "$"
	token LAM: "[£”]+"
	token VAR: "[a-zA-Z_]+"

    rule goal:           expr END         {{ return expr }}

    # An expression is the sum and difference of factors
    rule expr:           factor           {{ v = factor }}
                       ( "[+]" factor       {{ v = v+factor }}
                       |  "-"  factor       {{ v = v-factor }}
                       )*                 {{ return v }}

    # A factor is the product and division of terms
    rule factor:         term             {{ v = term }}
                       ( "[*]" term         {{ v = v*term }}
                       |  "/"  term         {{ v = v/term }}
                       )*                 {{ return v }}

    # A term is either a number or an expression surrounded by parentheses
    rule term:           "\\(" expr "\\)" {{ return expr }}
