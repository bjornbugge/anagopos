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

import operations as OP

class Graph(object):
    def __init__(self):
        self.nodesdict = {}
        self.nodes = []
        self.nodenametable = {}
        self.newest = None
    
    def __repr__(self):
        o = ''
        for (s, n) in self.nodesdict.iteritems():
            if len(n.children) == 0:
                continue
            for c in n.children:
                o = o + "\t" + str(c.source.name) + " -" + str(c.weight) + "-> " + str(c.destination.name) + "\n"
        
        return o
    
    def tostring(self):
        o = ''
        for (s, n) in self.nodesdict.iteritems():
            if len(n.children) == 0:
                continue
            for c in n.children:
                o = o + "\t" + str(c.source.term) + " -" + str(c.weight) + "-> " + str(c.destination.term) + "\n"
        
        print o
    
    def addnode(self, term, name = None):
        '''
        Adds a node made from the given term to the graph and returns it.
        If we use beta-reduction for the lambda calculus, addnode() ensures
        that nodes are compared modulo alpha-equivalence.
        '''
        OP.sanitize(term)
        try:
            node = self.nodesdict[str(term)]
        except KeyError:
            if name == None:
                name = 'N' + str(len(self.nodesdict))
            node = Node(term, name)
            self.nodesdict[str(term)] = node
            self.nodes.append(node) # Append to list if we made a new node.
            self.nodenametable[name] = node
        
        return node
    
class Edge(object):
    def __init__(self, source, destination):
        self.weight = 1
        self.source = source
        self.destination = destination
    
    def get_far(self, node):
        if self.source == node:
            return self.destination
        else:
            return self.source


class Node(object):
    def __init__(self, term, name):
        self.children = []
        self.parents = []
        self.term = term
        self.name = name
    
    def __repr__(self):
        return "NODE " + str(self.term)
        
    def addchild(self, child):
        e = Edge(self, child)
        
        for c in self.children:
            if e.source == c.source and e.destination == c.destination:
                c.weight = c.weight + 1
                return
        
        self.children.append(e)
        child.parents.append(e)
