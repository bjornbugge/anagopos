from lambda_dag import *

# The parser works on strings preprocessed by preprocessor.preprocess(x).
%%

parser Lambda:
	token LAM: "#"				# The abstractor symbol.
	token DOT: "."				# A dot!
	token VAR: "[a-zA-Z_0-9]"	# Variables have one-character names!
	
	ignore: '\s'				# Ignore whitespace characters.	
	
	rule Terms:		Term {{ T1 = Term }}
						( Term	{{ T2 = Term }}
								{{ if T2 is None: return T1 }}
								{{ A = Application() }} 
								{{ A.add(T1) }}
								{{ A.add(T2) }}
								{{ T1 = A }}
						)* {{ return T1 }}
	
	rule Term:		"\\(" Terms "\\)" 	{{ return Terms }}
					| 
					VAR 				{{ return Variable(VAR) }}
					|
					LAM VAR DOT Term	{{ child = Term }} 
										{{ A = Abstraction() }}
										{{ A.add(child) }}
										{{ A.varname = VAR }}
										{{ return A }}
					| ""

%%

def preprocess(term):
	'''
	Perform preprocessing on a string representation of a lambda term. 
	Preprocessing in this context means insert all missing parentheses,
	making the structure of the term explicit.
	'''
	out = ''
	count = 0
	for ch in term:
		out = out + ch
		if ch == '.':
			out = out + '('
			count = count + 1
		if ch == ')' and count > 0:
			out = out + ')'
			count = count - 1
	
	for i in range(count):
		out = out + ')'
	
	return out

def parse(text):
    P = Lambda(LambdaScanner(preprocess(text)))
    return wrap_error_reporter(P, 'Terms')