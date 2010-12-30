# -*- coding: utf-8 -*-
'''
Generate a random DAG for a TRS term.
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

import random
import computegraph.trs_dag as trs_dag

def names_arities(ruleset):
    '''
    Return a duplicate-free list of the (functionname, arity) pairs that is 
    present in the rule set.
    '''
    def _names_arities(term):
        l = []
        if type(term) is trs_dag.FunctionSymbol:
            l.append((term.name, term.arity))
            for child in term.children:
                l.extend(_names_arities(child))
        return l
        
    fs = []
    for r in ruleset.rules:
        fs.extend(_names_arities(r[0]))
        fs.extend(_names_arities(r[1]))
    
    return set(fs) # Remove duplicates

def randomterm(ruleset):
    '''
    Generate a random first-order term that can be used with the given rule set.
    '''
    global varcount
    varcount = 0
    
    def _node(p):
        global varcount
        
        r = random.uniform(0,1)
        
        if r < p['functionsymbol']:
            _lp = p
            _lp['variable'] = _lp['variable'] + 0.09
            _lp['functionsymbol'] = _lp['functionsymbol'] - 0.02
            
            i = random.randint(0, len(function_names) - 1)
            a = function_arities[i]
            node = trs_dag.FunctionSymbol(function_names[i], a)
            while a > 0:
                node.add(_node(_lp))
                a -= 1
        else:
            name = 'v' + str(varcount)
            varcount += 1
            node = trs_dag.Variable(name)
        return node
    
    p = {'functionsymbol'   : 0.9,
         'variable'         : 0.1
        }
    
    na = names_arities(ruleset)
    function_names = [n[0] for n in na]
    function_arities = [n[1] for n in na]
    
    start = _node(p)
    start.makestr()
    return start