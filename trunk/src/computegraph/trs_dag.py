'''
Contains classes representing the nodes in a DAG for a term.
'''

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

class TRSNode(object):
    def __init__(self):
        # A term can have several children.
        self.children = []
        self.parent = None
        
        # Indicates whether the term can be sanitized.
        self.dirty = True 
        
        # Cache a terms string representation in strrepr. Do this so that 
        # each call to __repr__() doesn't calculate the representation again.
        self.strrepr = ''
        
        # [(position, rule)] where rule is (termA, termB)
        self.redexpositions = []
        
    
    def __eq__(self, other):
        return str(self) == str(other)
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def add(self, node):
        raise NotImplementedError()
    
    def remove(self, node):
        raise NotImplementedError()
    
    def swap(self, old, new):
        raise NotImplementedError()
    
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


class FunctionSymbol(TRSNode):
    '''
    An n-ary function symbol.
    '''
    def __init__(self, name, arity):
        super(FunctionSymbol, self).__init__()
        self.arity = arity
        self.name = name
    
    def copy(self):
        f = FunctionSymbol(self.name, self.arity)
        f.dirty = self.dirty
        f.strrepr = self.strrepr
        for c in self.children:
            cc = c.copy()
            f.add(cc)
        f.redexpositions.extend(self.redexpositions)
        return f
    
    def add(self, node):
        '''
        Add a child node.
        '''
        if node:
            self.children.append(node)
            node.parent = self
    
    def remove(self, node):
        '''
        Remove the node if it is a child.
        '''
        try:
            self.children.remove(node)
            node.parent = None
        except ValueError:
            pass # Ignore it
            
    def swap(self, old, new):
        '''
        Swap the old node with the new node -- if the old node is a child.
        '''
        # if new in self.children:
        #     raise Exception("Cannot swap the new node into this term, it is already present.")
        
        if old in self.children:
            i = self.children.index(old)
            self.children[i] = new
            new.parent = self
            old.parent = None

    def makestr(self):
        n = []
        for c in self.children:
            c.makestr()
            n.append(c.__repr__())
        self.strrepr = self.name
        if len(n) > 0:
            self.strrepr += "(" + reduce(lambda a, b:a + ", " + b, n) + ")"
    
    def __repr__(self):
        self.makestr()
        return self.strrepr


class Variable(TRSNode):
    def __init__(self, n):
        super(Variable, self).__init__()
        self.name = n

    def copy(self):
        v = Variable(self.name)
        v.dirty = self.dirty
        v.strrepr = self.strrepr
        v.redexpositions.extend(self.redexpositions)
        return v
        
    def makestr(self):
        self.strrepr = self.name
        
    def __repr__(self):
        self.makestr()
        return self.strrepr

class RewriteRuleSet(object):
    '''
    A set of rewrite rules is basically a list of (LHS, RHS)-terms and a name.
    '''
    def __init__(self, name):
        self.rules = []
        self.name = name
    
    def __repr__(self):
        return self.name + " : " + str(self.rules)
    
    def addRule(self, termA, termB):
        self.rules.append((termA, termB))
