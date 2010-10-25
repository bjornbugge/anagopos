# Reduction Visualizer. A tool for visualization of reduction graphs.
# Copyright (C) 2010 Niels Bjoern Bugge Grathwohl and Jens Duelund Pallesen
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

from computegraph.lambda_dag import *

# The parser works on strings preprocessed by preprocessor.preprocess(x).

from string import *
import re
from yappsrt import *

class LambdaScanner(Scanner):
    patterns = [
        ('""', re.compile('')),
        ('"\\\\)"', re.compile('\\)')),
        ('"\\\\("', re.compile('\\(')),
        ('LAM', re.compile('#')),
        ('DOT', re.compile('.')),
		('VAR', re.compile('[a-zA-Z_]([0-9])*')),
        ('\\s', re.compile('\\s')),
    ]
    def __init__(self, str):
        Scanner.__init__(self,None,['\\s'],str)

class Lambda(Parser):
	def Terms(self):
		Term = self.Term()
		T1 = Term
		while self._peek('"\\\\("', 'VAR', 'LAM', '""', '"\\\\)"') != '"\\\\)"':
			Term = self.Term()
			T2 = Term
			if T2 is None: return T1
			A = Application()
			A.add(T1)
			A.add(T2)
			T1 = A
		return T1

	def Term(self):
		_token_ = self._peek('"\\\\("', 'VAR', 'LAM', '""')
		if _token_ == '"\\\\("':
			self._scan('"\\\\("')
			Terms = self.Terms()
			self._scan('"\\\\)"')
			return Terms
		elif _token_ == 'VAR':
			VAR = self._scan('VAR')
			return Variable(VAR)
		elif _token_ == 'LAM':
			LAM = self._scan('LAM')
			VAR = self._scan('VAR')
			DOT = self._scan('DOT')
			Term = self.Term()
			child = Term
			A = Abstraction()
			A.add(child)
			A.varname = VAR
			return A
		else:# == '""'
			self._scan('""')


def parse(rule, text):
    P = Lambda(LambdaScanner(text))
    return wrap_error_reporter(P, rule)

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
	return wrap_error_reporter(P, 'Terms')