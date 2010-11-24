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

__doc__ = \
'''
Choose the reduction "mode". Currently there are two choices: the lambda
calculus or a first-order term reduction system. The proxy functions here takes
care of selecting the correct reduction mechanisms and the correct parser.
'''

import pdb

# May be one of 'lambda' or 'trs'.
if '__mode__' not in locals():
    __mode__ = ''

def setmode(mode):
    pdb.set_trace()
    global OPS, PARSER, __mode__
    if mode == 'lambda':
        import computegraph.lambda_operations as OPS
        import parser.lambdaparser.lambdaparser as PARSER
    elif mode == 'trs':
        import computegraph.trs_operations as OPS
        import parser.trsparser.trs_parser as PARSER
    else:
        raise Exception("Unsupported mode: " + mode)
    
    __mode__ = mode


def parse(string):
    pdb.set_trace()   
    return PARSER.parse(string)

def assignvariables(root):
    if __mode__ == '':
        return
    OPS.assignvariables(root)

def defaultRuleSet():
    '''Temporary dummy method, needed for testing.'''
    return PARSER.defaultRuleSet()

def reductiongraphiter(root, start, end, ruleSet = None):
    if __mode__ == 'lambda':
        return OPS.reductiongraphiter(root, start, end)
    elif __mode__ == 'trs':
        return OPS.reductiongraphiter(root, start, end, ruleSet)
    else:
        raise Exception("Unsupported mode: " + __mode__)
