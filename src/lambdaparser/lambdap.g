# Reduction Visualizer. A tool for visualization of reduction graphs.
# Copyright (C) 2010 Niels Bjørn Bugge Grathwohl & Jens Duelund Pallesen
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from lambda_dag import *

# The parser works on strings preprocessed by preprocessor.preprocess(x).
%%

parser Lambda:
	token LAM: "#"				# The abstractor symbol.
	token DOT: "."				# A dot!
	token VAR: "[a-zA-Z_]([0-9])*"	# Variables
	
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
	Preprocessing in this context means inserting all missing parentheses,
	making the structure of the term explicit.
	'''
	out = ''
	count = 0
	for (i, ch) in enumerate(term):
		out = out + ch
		if ch == '.' and not term[i + 1] == '(':
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
	# P = Lambda(LambdaScanner(text))
	return wrap_error_reporter(P, 'Terms')