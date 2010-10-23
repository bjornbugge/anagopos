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

import operations as OP

'''
DAG-representation of lambda terms.
'''

class LambdaNode(object):
	def __init__(self):
		self.leftchild = None
		self.rightchild = None
		self.parent = None
		
		# Indicates whether the term can be sanitized.
		self.dirty = True 
		
		# Cache a terms string representation in strrepr. Do this so that 
		# each call to __repr__() doesn't calculate the representation again.
		self.strrepr = ''
		
		# The positions of redexes in this term. The format of the positions
		# is as specified in operations.findredexes().
		self.redexpositions = []
	
	def __eq__(self, other):
		'''
		Equality of two DAGs is defined as the string equality of their 
		normalized string representations to account for alpha congruence.
		'''
		if other is None:
			return False
		s = OP.sanitize
		st = str
		s(self)
		s(other)
		return st(self) == st(other)
	
	def __ne__(self, other):
		return not self.__eq__(self, other)

	def add(self, node):
		'''
		Add a child node. If this node already has two children, nothing happens.
		'''
		if self.leftchild is None:
			self.leftchild = node
			node.parent = self
	 	elif self.rightchild is None:
			self.rightchild = node
			node.parent = self
	
	def remove(self, node):
		'''
		Remove the node if it is a child.
		'''
		# Use identity, not equality. The DAG must contain the node in order to
		# be able to delete it.
		if self.leftchild is node:
			self.leftchild = None
			node.parent = None
		elif self.rightchild is node:
			self.rightchild = None
			node.parent = None
	
	def swap(self, old, new):
		'''
		Swap the old node with the new node -- if the old node is a child.
		'''
		# Use identity, not equality. The DAG must contain the nodes in order to
		# be able to swap them.
		if self.leftchild is old:
			self.leftchild = new
			new.parent = self
			old.parent = None
		elif self.rightchild is old:
			self.rightchild = new
			new.parent = self
			old.parent = None
	
	def makestr(self):
		'''
		Make the string representation of the lambda term. After a call to
		this method, self.strrepr is set with the correct string representation,
		and calls to str() will return the value.
		'''
		raise NotImplementedError()
	
	def copy(self):
		'''
		Return a deep copy of the DAG.
		Use instead of the copy.deepcopy(), this is much much faster!
		'''
		raise NotImplementedError()


class Abstraction(LambdaNode):
	'''
	A lambda abstraction. Knows which descending nodes it binds.
	'''
	def __init__(self):
		super(Abstraction, self).__init__()
		self.variables = []
		self.varname = ''
	
	def copy(self):
		a = Abstraction()
		c = self.leftchild.copy()
		a.varname = self.varname
		a.add(c)
		a.dirty = self.dirty
		a.strrepr = self.strrepr
		a.redexpositions.extend(self.redexpositions)
		return a
	
	def assignvar(self, variablenode):
		'''
		Register the node as a variable bound by this abstractor.
		'''
		self.variables.append(variablenode)
		if self.varname == '':
			self.varname = variablenode.name
	
	def makestr(self):
		self.leftchild.makestr()
		self.strrepr = "#" + self.varname + ".(" + self.leftchild.strrepr + ")"
	
	def __repr__(self):
		return self.strrepr


class Application(LambdaNode):
	'''
	Lambda application.
	'''
	def copy(self):
		a = Application()
		c1 = self.leftchild.copy()
		c2 = self.rightchild.copy()
		a.add(c1)
		a.add(c2)
		a.dirty = self.dirty
		a.strrepr = self.strrepr
		a.redexpositions.extend(self.redexpositions)
		return a
	
	def makestr(self):
		s1 = s2 = ''
		if self.leftchild:
			self.leftchild.makestr()
			s1 = self.leftchild.strrepr
		if self.rightchild:
			self.rightchild.makestr()
			s2 = self.rightchild.strrepr
		self.strrepr = "(" + s1 + " " + s2 + ")"
	
	def __repr__(self):
		return self.strrepr


class Variable(LambdaNode):
	'''
	A variable. Can be either bound or free.
	'''
	def copy(self):
		v = Variable(self.name)
		v.dirty = self.dirty
		v.strrepr = self.strrepr
		v.redexpositions.extend(self.redexpositions)
		return v
		
	def makestr(self):
		self.strrepr = self.name
		
	def __init__(self, n):
		super(Variable, self).__init__()
		self.name = n
	
	def add(self, node):
		pass # A variable can't have children
	
	def remove(self, node):
		pass
		
	def __repr__(self):
		return self.strrepr
