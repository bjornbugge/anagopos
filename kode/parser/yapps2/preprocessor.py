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
		if ch == ')':
			out = out + ')'
			count = count - 1
	
	for i in range(count):
		out = out + ')'
	
	return out