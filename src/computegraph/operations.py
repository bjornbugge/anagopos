'''
Choose the reduction "mode". Currently there are two choices: the lambda
calculus or a first-order term reduction system. The proxy functions here takes
care of selecting the correct reduction mechanisms and the correct parser.
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

import computegraph.lambda_operations as lambda_operations
import computegraph.trs_operations as trs_operations

import parser.lambdaparser.lambdaparser as lambda_parser
import parser.trsparser.trs_parser as trs_parser
import parser.tpdbparser.tpdb_parser as tpdb_parser


# May be one of 'lambda' or 'trs'.
if '_mode' not in locals():
    _mode = ''

def setmode(mode):
    '''
    Set the mode, i.e. choose which parser and associated operations to use:
    'trs' or 'lambda'.
    '''
    global OPS, PARSER, TPDBPARSER, _mode
    if mode == 'lambda':
        OPS = lambda_operations
        PARSER = lambda_parser
    elif mode == 'trs':
        OPS = trs_operations
        PARSER = trs_parser
        TPDBPARSER = tpdb_parser
    else:
        raise Exception("Unsupported mode: " + mode)
    
    _mode = mode

def current_mode():
	return _mode

def parse_rule_set(file_type, string):
    '''
    Parse rule set definitions and return a set of rules. Can parse the 
    XML specifcation used by TPDB and our own .trs-format.
    '''
    if not _mode == 'trs':
        raise Exception("Lambda calculus has no rule set files.")
    
    ruleparser = None
    
    if file_type == 'xml': # The TPDB format
        ruleparser = TPDBPARSER
    elif file_type == 'trs': # The home-made (better!) format
        ruleparser = PARSER
    
    return ruleparser.parse_rule_set(string)

def parse(string):
    '''
    Parse either a lambda calculus term or a TRS-term.
    '''
    return PARSER.parse(string)

def assignvariables(root):
    '''
    Assign bound variables. No-op on TRS-systems.
    '''
    if _mode == '':
        return
    OPS.assignvariables(root)


def sanitize(term):
    '''
    Call the system-specific sanitizzing operation. On TRS-systems this is a 
    no-op.
    '''
    if _mode == '':
        return
    OPS.sanitize(term)

def defaultRuleSet():
    '''Temporary dummy method, needed for testing.'''
    return PARSER.defaultRuleSet()

def reductiongraphiter(root, start, end, ruleSet = None):
    '''
    Returns an iterator over the reduction graph, evovlving the graph in each
    iteration step.
    '''
    if _mode == 'lambda':
        return OPS.reductiongraphiter(root, start, end)
    elif _mode == 'trs':
        return OPS.reductiongraphiter(root, start, end, ruleSet)
    else:
        raise Exception("Unsupported mode: " + _mode)
