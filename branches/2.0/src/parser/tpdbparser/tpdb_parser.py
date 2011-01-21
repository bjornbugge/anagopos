'''
Parser for (a subset of) the XML-format specified at 
http://www.termination-portal.org/wiki/TPDB used for defining TRS-systems.
The parser looks only at the rule definitions, like:
<rules>
    <rule>
        <lhs>
            <funapp>
                <name>F</name>
                <arg><var>x</var><var>y</var></arg>
            </funapp>
        </lhs>
        <rhs>
            <var>x</var>
        </rhs>
    </rule>
</rules>
Everything else in the format is simply ignored.
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


import xml.parsers.expat
import pdb

from computegraph.trs_dag import FunctionSymbol, Variable, RewriteRuleSet
from computegraph.trs_operations import findredexes
from parser.trsparser import trs_parser as TRS

class TPDBParseException(Exception):
    pass

class TPDBParser(object):
    '''
    Parser class. After a succesfull parse, an instance of this class
    contains the rules specified in the TPDP-XML-file in the instance
    variable rule_set.
    '''
    
    initial_mode = -1
    push_function_mode = 0
    add_variable_mode = 1
    
    # XML tag names
    tags = {'FUNCTION_NAME'         : 'name',
            'RULE_SET_DEFINITION'   : 'rules',
            'VARIABLE_NAME'         : 'var',
            'FUNCTION_APPLICATION'  : 'funapp',
            'RULE_DEFINITION'       : 'rule',
            'LAMBDA_DEFINITION'     : 'lambda',
            'APPL_DEFINITION'       : 'application'}
    
    def __init__(self):
        self.clear()
    
    def clear(self):
        '''
        Reset the parser.
        '''
        self.mode = TPDBParser.initial_mode
        self.function_table = {}
        self.function_stack = []
        self.stack = []
        self.rule_set = None
    
    def add_rule(self):
        '''
        Adds a new rule to the active rule set.
        '''
        # pdb.set_trace()
        term_b = self.stack.pop()
        term_a = self.stack.pop()
        if isinstance(term_a, Variable):
            raise Exception("LHS of a rule cannot be a variable!")
        self.rule_set.addRule(term_a, term_b)
    
    def add_rule_set(self):
        '''
        Adds a new rule set.
        '''
        self.rule_set = RewriteRuleSet("TPDP_ruleset")
        self.function_table.clear()
    
    def add_variable(self, name):
        '''
        Append a variable to the currently active function.
        '''
        v = Variable(name)
        if len(self.function_stack) > 0:
            peek = self.function_stack[-1]
            peek.add(v)
        else:
            self.stack.append(v)
    
    def push_function(self, name):
        '''
        Pushes a function definition on the stack. Makes it a child of 
        any previous function on the top of the stack.
        '''
        if name not in self.function_table:
            self.function_table[name] = -1

        f = FunctionSymbol(name, self.function_table[name])

        if len(self.function_stack) > 0:
            peek = self.function_stack[-1]
            peek.add(f)
        else:
            self.stack.append(f)
        
        self.function_stack.append(f)
    
    def pop_function(self):
        '''
        Pops a function off the stack. Called when seeing the close tag for a
        function definition. Checks that the arity of the function is consistent.
        '''
        f = self.function_stack.pop()
        f.arity = len(f.children)
        if self.function_table[f.name] == -1:
            self.function_table[f.name] = f.arity
        if not self.function_table[f.name] == f.arity:
            raise Exception("Arity of \"" + f.name + "\" is " + \
                    str(self.function_table[f.name]) + ", not " +\
                    str(f.arity) + ".")
    
    def start_element(self, name, attrs = None):
        '''
        Handler for the start elements. Performs the appropriate actions
        for the different supported tags.
        '''
        # pdb.set_trace()
        if name == TPDBParser.tags['RULE_SET_DEFINITION']:
            self.add_rule_set()
        elif name == TPDBParser.tags['FUNCTION_NAME']:
            self.mode = TPDBParser.push_function_mode
        elif name == TPDBParser.tags['VARIABLE_NAME']:
            self.mode = TPDBParser.add_variable_mode
        elif name == TPDBParser.tags['LAMBDA_DEFINITION'] or name == TPDBParser.tags['APPL_DEFINITION']:
            raise TPDBParseException("Higher-order rewrite systems unsupported")
        else:
            pass # Ignore everything else
    
    def end_element(self, name):
        '''
        Handler for the end elements. 
        '''
        # pdb.set_trace()
        if name == TPDBParser.tags['FUNCTION_APPLICATION']:
            self.pop_function()
        elif name == TPDBParser.tags['RULE_DEFINITION']:
            self.add_rule()
        
        self.mode = TPDBParser.initial_mode
    
    def character_data(self, data):
        '''
        Manages character data. Responsible for naming the functions and variables.
        '''
        if self.mode == TPDBParser.push_function_mode:
            self.push_function(data)
        elif self.mode == TPDBParser.add_variable_mode:
            self.add_variable(data)
    
    def parse_rule_set(self, string):
        '''
        Entry-point for the parser. 
        '''
        parser = xml.parsers.expat.ParserCreate()
        parser.StartElementHandler = self.start_element
        parser.EndElementHandler = self.end_element
        parser.CharacterDataHandler = self.character_data
        parser.Parse(string)

parser_instance = TPDBParser()

def parse_rule_set(string):
    '''
    Entry point to the parser. Used by the proxy-style-interface in 
    computegraph/operations.py.
    '''
    parser_instance.clear()
    parser_instance.parse_rule_set(string)
    return parser_instance.rule_set


if __name__ == '__main__':
    pa = TPDBParser()
    
    def parsefile(file_name = 'parser/tpdbparser/ex2.xml'):
        with open(file_name, 'r') as f:
            string = f.read()
        parse(string)
    
    def parse(string):    
        pa.parse_rule_set(string)
    
    parsefile()
    
    trs_pa = TRS.TRSParser()
    term = trs_pa.parseTerm("A(S(0), S(S(A(M(S(0), S(S(0))), 0))))")
    term.redexpositions = findredexes(term, pa.rule_set)
    
    
    t = """<?xml version="1.0" encoding="UTF-8"?>
    <!--
    F(x) -> F(G(x))

    (F/1, G/1)
    -->
    <problem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" type="termination" xsi:noNamespaceSchemaLocation="http://dev.aspsimon.org/xtc.xsd">
      <trs>
        <rules>
          <rule>
            <lhs>
              <funapp>
                <name>f</name>
                <arg>
                  <var>x</var>
                </arg>
              </funapp>
            </lhs>
            <rhs>
              <funapp>
                <name>f</name>
                <arg>
                  <funapp>
                    <name>g</name>
                    <arg>
                      <var>x</var>
                    </arg>
                  </funapp>
                </arg>
              </funapp>
            </rhs>
          </rule>
        </rules>
        <signature>
          <funcsym>
            <name>f</name>
            <arity>1</arity>
          </funcsym>
          <funcsym>
            <name>g</name>
            <arity>1</arity>
          </funcsym>
        </signature>
      </trs>
      <strategy>FULL</strategy>
      <metainformation>
        <originalfilename>./TRS/HM/n006.trs</originalfilename>
      </metainformation>
    </problem>
"""