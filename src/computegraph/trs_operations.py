'''
This module contains functions that operate on terms in a first-order term
reduction system (TRS). The general format is, that a function takes some
term and a set of reduction rules, reduces the term and outputs the result.
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

from trs_dag import FunctionSymbol, Variable
import reductiongraph as redgraph
import pdb
from graphcopy import copygraph

def assignvariables(root):
    pass # dummy function!

def sanitize(term):
    pass # dummy function!

def termsmatch(term1, term2):
    '''
    True if the two terms "match" in a rule oriented sense, i.e. does the 
    pattern in the rule given by term2 apply to the term in term1?
    '''
    def _bind(t1, t2, varbindings):
        if isinstance(t1, Variable):
            if t1.name not in varbindings:
                varbindings[t1.name] = t2
            if not varbindings[t1.name] == t2:
                return False
        return True
        
    def _match(term1, term2, varbindings):
        if isinstance(term1, Variable) and isinstance(term2, Variable):
            # print "Don't show that true is false!"
            return False
        
        if not _bind(term1, term2, varbindings):
            return False
        if not _bind(term2, term1, varbindings):
            return False
        
        for (c1, c2) in zip(term1.children, term2.children):
            if not _match(c1, c2, varbindings):
                return False
        
        if isinstance(term1, FunctionSymbol) and isinstance(term2, FunctionSymbol):
            return term1.name == term2.name and term1.arity == term2.arity
        
        return True
    
    return _match(term1, term2, {})


def findredexes(term, ruleSet):
    '''
    Returns a list of tuples: [(position, (termA, termB))].
    Positions are defined in getnode().
    '''
    def _findredexes(t, rule, positions, posAccum):
        if isinstance(t, Variable):
            # print "A variable is in normal form (_findredexes)!"
            return
        
        if termsmatch(t, rule[0]):
            positions.append((posAccum, (rule[0].copy(), rule[1].copy())))
        
        for (i, child) in enumerate(t.children):
            _findredexes(child, rule, positions, posAccum + [i])
    
    positions = []
    for rule in ruleSet.rules:
        _findredexes(term, rule, positions, [])
    
    return positions

def getnode(root, position):
    '''
    A position is a list of integers [i0,i1,...] where i0 is the index of the
    child of the root term, i1 is the index of that terms child, etc.
    The empty list denotes the root term.'''
    cur_node = root
    i = 0
    while i < len(position):
        cur_node = cur_node.children[position[i]]
        i += 1
    return cur_node

def performreduction(redex, posRule):
    '''
    Performs the given one-step-reduction of a term. The reduction is assumed
    to be "correct", i.e. applicable to the term. It is given by a (position, rule)
    tuple, following the same design as described in getnode() and findredexes().
    '''
    bindings = {}
    def bindVars(ruleTerm, actualTerm):
        if isinstance(ruleTerm, Variable):
            if ruleTerm.name not in bindings:
                bindings[ruleTerm.name] = actualTerm
            if not bindings[ruleTerm.name] == actualTerm:
                raise Exception("Error in variable binding!")
        else:
            for (c1, c2) in zip(ruleTerm.children, actualTerm.children):
                bindVars(c1, c2)
    
    def assignVars(term):
        if term.name in bindings:
            if term.parent is None:
                return bindings[term.name]
            term.parent.swap(term, bindings[term.name])
        else:
            for c in term.children:
                assignVars(c)
    
    redexpos, rule = posRule
    contractum = redex.copy()
    
    subterm = getnode(contractum, redexpos)
    
    bindVars(rule[0], subterm)
    newSubTerm = rule[1].copy()
    r = assignVars(newSubTerm)
    if r:
        newSubTerm = r
    
    if subterm is contractum:
        contractum = newSubTerm
    else:
        subterm.parent.swap(subterm, newSubTerm)
        
    
    return (redex, contractum)

def reductiongraphiter(root, start, end, ruleset):
    work = [root]
    root.redexpositions = findredexes(root, ruleset)
    graph = redgraph.Graph()
    guard = 0
    reductions = 0
    alreadydone = []
    while len(work) > 0 and (end == 0 or guard <= end):
        term = work[0]
        positionsRules = term.redexpositions
        n1 = graph.addnode(term)
        if n1.name in alreadydone:
            del work[0]
            continue
        
        graph.newest = n1
        
        for posRule in positionsRules:
            (term, contractum) = performreduction(term, posRule)
            
            n2 = graph.addnode(contractum)
            contractum.redexpositions = findredexes(contractum, ruleset)
            n1.addchild(n2)
            
            if not contractum in work:
                work.append(contractum)
            
            reductions = reductions + 1
            print "Reduction #" + str(reductions)
        
        alreadydone.append(n1.name)
        del work[0]
        
        if guard >= start:
            yield copygraph(graph)
            # yield deepcopy(graph)
            # yield graph
        
        guard = guard + 1

    
    print "Performed " + str(reductions) + " reductions."
    if len(work) > 0:
        print "Incomplete reduction graph!"


def reductiongraph(root, start, end, ruleset):
    last = None
    for g in reductiongraphiter(root, start, end, ruleset):
        # print "GOT: " + str(g)
        last = g
    return last