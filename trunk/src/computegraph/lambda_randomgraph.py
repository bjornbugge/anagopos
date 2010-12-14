'''
Generate a random DAG for a lambda term.
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

import computegraph.operations as operations
import computegraph.lambda_dag as lambda_dag
import copy
import random
import parser.lambdaparser as parser


# ((#B1.(B1) #B2.((#B3.((#B4.((#B5.(B4) #B6.(#B7.(#B8.(#B9.(B6)))))) #B10.(#B11.(#B12.(B12))))) #B13.(#B14.(#B15.(#B16.(B14))))))) #B17.(#B18.((#B19.(#B20.(#B21.(B17))) B17))))
# (#B1.((#B2.(#B3.(#B4.((#B5.(B3) B1)))) (#B6.(#B7.(#B8.(#B9.(B9)))) B1))) ((((#B10.(#B11.(B10)) #B12.((#B13.(#B14.(B12)) B12))) #B15.(#B16.(((B16 #B17.(#B18.(B18))) #B19.(#B20.(#B21.(#B22.(#B23.(B19))))))))) #B24.(#B25.(B25))) #B26.(#B27.(#B28.(#B29.((B28 #B30.(B28))))))))
# #B1.(#B2.(#B3.(((#B4.((#B5.(#B6.(#B7.(B4))) #B8.(B3))) B3) (#B9.((#B10.(#B11.(B3)) B3)) (#B12.(#B13.(#B14.(#B15.(#B16.(B13))))) B1))))))
# #B1.(((#B2.(#B3.(B3)) #B4.(#B5.(#B6.((#B7.(B6) #B8.(#B9.(#B10.(B5)))))))) (#B11.(#B12.(B11)) #B13.((F1 #B14.(#B15.(B14)))))))
def generatereductiongraph():
    '''
    Generate a random beta-reduction graph.
    '''
    term = randomterm()
    operations.assignvariables(term)
    term.makestr()
    print term
    print "----"
    g1 = operations.reductiongraph(term)
    return g1

def getgraph(termstr):
    term = parser.parse(termstr)
    operations.assignvariables(term)
    g = operations.reductiongraph(term)
    return g

def generateterms():
    term1 = randomterm()
    operations.assignvariables(term1)
    print term1
    term2 = parser.parse(str(term1))
    operations.assignvariables(term2)
    print term2
    print term1==term2
    return (term1, term2)

def randomterm():
    '''
    Generate a pseude-random DAG-representation of a lambda term.
    '''
    global freevars
    global boundvars
    freevars = 0
    boundvars = 0
    
    def _node(p, boundlist):
        global freevars
        global boundvars
        
        r = random.uniform(0,1)
        
        if r < p['abstraction']:
            _lp = p
            _lp['variable'] = _lp['variable'] + 0.09
            _lp['abstraction'] = _lp['abstraction'] - 0.07
            _lp['application'] = _lp['application'] - 0.02

            node = lambda_dag.Abstraction()
            boundvars = boundvars + 1
            b = 'B' + str(boundvars)
            node.varname = b
            node.add(_node(_lp, boundlist + [b]))
            
        elif r < p['abstraction'] + p['application']:
            _lp = copy.deepcopy(p)
            _lp['abstraction'] = _lp['abstraction'] + 0.04
            _lp['application'] = _lp['application'] - 0.06
            _lp['variable'] = _lp['variable'] + 0.02
            _rp = copy.deepcopy(p)
            _rp['abstraction'] = _rp['abstraction'] + 0.02
            _rp['application'] = _rp['application'] - 0.02
            _rp['variable'] = _rp['variable']
            
            node = lambda_dag.Application()
            node.add(_node(_lp, boundlist))
            node.add(_node(_rp, boundlist))
            
        else:
            if random.uniform(0,1) < p['boundvar'] and not len(boundlist) == 0:
                name = boundlist[random.randint(0, len(boundlist) - 1)]
            else:
                freevars = freevars + 1
                name = 'F' + str(freevars)
            node = lambda_dag.Variable(name)
        return node
    
    p = {'abstraction'  : 0.6,
         'application'  : 0.4,
         'variable'     : 0.0,
        
         'boundvar'     : 0.95}

    start = _node(p, [])
    operations.assignvariables(start)
    start.makestr()
    return start