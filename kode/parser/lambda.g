parser Lambda:
    token END: "$"
    token LAM: "#"
    token DOT: "."
    token VAR: "[a-zA-Z_]+"

    # If x is a variable, then x ∈ Λ
    # If x is a variable and M ∈ Λ, then (λx.M) ∈ Λ
    # If M, N ∈ Λ, then (M N) ∈ Λ

     rule goal:          term END            {{ print "term end" }}

     rule x:              VAR                {{ print "VAR" }}
       
     rule term:           x                  {{ print "rule -> " }}
                        | abstraction        {{ print "rule -> " }}
                        | parentheses        {{ print "rule -> " }}
                        | term2              {{ print "rule -> " }}
          
     rule term2:          term term2         {{ print "term" }}

     rule abstraction:    LAM x DOT term     {{ print "abstraction" }}

     rule parentheses:    "\\("term"\\)"     {{ print "parentheses" }}
