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
A parser for a term reduction system (TRS).
'''

from pyparsing import OneOrMore,Optional,Literal,Word,Forward,Keyword,nums,\
    alphas,delimitedList,srange,cppStyleComment,pythonStyleComment

from computegraph.trs_dag import FunctionSymbol, Variable, RewriteRuleSet
from computegraph.trs_operations import *

class TRSParser:
    """
    Variable        := [a-z][a-zA-Z0-9_]*
    FunctionName    := [A-Z0-9][a-zA-Z0-9_]*
    TermArgs        := Term ["," TermArgs]
    Term            := Variable | FunctionName ["(" TermArgs ")"]
    Rule            := Term "->" Term
    RuleName        := [a-zA-Z0-9_]+
    RulesDefinition := RuleName "{" (Rules)* "}"
    Program         := Term
    TRS             := (RulesDefinition)+ [Program]

    C++-style comments are supported, as well as "#"-comments.
    """
    def __init__(self):
        self._parser = None
        self._functionTable = {}
        self._functionStack = []
        self._stack = []
        self.ruleSets = []
        self._makeGrammar()
    
    def parse(self, string):
        self._parser.parseString(string)

    def clear(self):
        self._functionTable = {}
        self._functionStack = []
        self._stack = []
        self.ruleSets = []

    def _addRule(self, tokens):
        termB = self._stack.pop()
        termA = self._stack.pop()
        # if type(termA) is Variable:
        if isinstance(termA, Variable):
            raise Exception("LHS of a rule cannot be a variable!")
        
        self.ruleSets[-1].addRule(termA, termB)

    def _addVariable(self, tokens):
        v = Variable(tokens[0])
        if len(self._functionStack) > 0:
            peek = self._functionStack[-1]
            peek.add(v)
        else:
            self._stack.append(v)

    def _pushFunction(self, tokens):
        if tokens[0] not in self._functionTable:
            self._functionTable[tokens[0]] = -1

        f = FunctionSymbol(tokens[0], self._functionTable[tokens[0]])

        if len(self._functionStack) > 0:
            peek = self._functionStack[-1]
            peek.add(f)
        else:
            self._stack.append(f)
        self._functionStack.append(f)

    def _popFunction(self):
        f = self._functionStack.pop()
        f.arity = len(f.children)
        if self._functionTable[f.name] == -1:
            self._functionTable[f.name] = f.arity
        if not self._functionTable[f.name] == f.arity:
            raise Exception("Arity of \"" + f.name + "\" is " + \
                    str(self._functionTable[f.name]) + ", not " +\
                    str(f.arity) + ".")

    def _addRuleSet(self, tokens):
        r = RewriteRuleSet(tokens[0])
        self.ruleSets.append(r)
        self._functionTable.clear()
    
    def _makeGrammar(self):
        lowerCaseAlphas = srange("[a-z]")
        upperCaseAlphas = lowerCaseAlphas.upper()
        
        arrow               = Literal("->").suppress()
        comma               = Literal(",").suppress()
        lpar                = Literal("(").suppress()
        rpar                = Literal(")").suppress()
        lcurl               = Literal("{").suppress()
        rcurl               = Literal("}").suppress()
        
        term1               = Forward()
        
        variable            = Word(lowerCaseAlphas, alphas + nums + "_")
        functionName        = Word(upperCaseAlphas + nums, alphas + nums + "_")
        functionCall        = functionName + Optional(lpar + term1 + rpar)
        ruleName            = Word(alphas + nums + "_")
        
        variable.setParseAction(self._addVariable)
        functionName.setParseAction(self._pushFunction)
        functionCall.setParseAction(self._popFunction)
        ruleName.setParseAction(self._addRuleSet)
        
        term                = variable | functionCall
        term1               << delimitedList(term, ",")
        
        rule                = term + arrow + term
        rule.setParseAction(self._addRule)
        
        rulesDefinition     = ruleName + lcurl + OneOrMore(rule) + rcurl
        
        program             = term # ?
        
        self._parser         = OneOrMore(rulesDefinition) + Optional(program)
        self._parser.ignore(cppStyleComment)
        self._parser.ignore(pythonStyleComment)
    

# Parse a term, quick, for testing.
def term(functionstring):
    functionStack = []
    functions = []
    var = []
    
    def push(tokens):
        f = FunctionSymbol(tokens[0], -1)
        if len(functionStack) > 0:
            functionStack[-1].add(f)
        
        functionStack.append(f)
        functions.append(f)
    
    def addVar(tokens):
        v = Variable(tokens[0])
        if len(functionStack) > 0:
            functionStack[-1].add(v)
        else:
            var.append(v)
    
    def pop():
        functionStack[-1].arity = len(functionStack[-1].children)
        functionStack.pop()
    
    lowerCaseAlphas = srange("[a-z]")
    upperCaseAlphas = lowerCaseAlphas.upper()
    lpar                = Literal("(").suppress()
    rpar                = Literal(")").suppress()
    term1               = Forward()
    variable            = Word(lowerCaseAlphas, alphas + nums + "_")
    functionName        = Word(upperCaseAlphas + nums, alphas + nums + "_")
    functionCall        = functionName + Optional(lpar + term1 + rpar)
    ruleName            = Word(alphas + nums + "_")
    term                = variable | functionCall
    term1               << delimitedList(term, ",")
    
    functionName.setParseAction(push)
    variable.setParseAction(addVar)
    functionCall.setParseAction(pop)
    
    term.parseString(functionstring)
    
    if len(functions) == 0:
        return var[0]
    return functions[0]
    


p = TRSParser()
def testFile(fileName):
    with open(fileName, 'r') as f:
        string = f.read()
    p.parse(string)
    print p.ruleSets

if __name__ == "__main__":
    print testFile("trsparser/TRS1.trs")

    s = p.ruleSets[0]

    # t1 = s.rules[0][0]
    # t2 = s.rules[2][0]
    # t3 = s.rules[1][1]
    # t4 = s.rules[4][0]
    # t5 = s.rules[5][0]
    
    # t6 = term("A(S(0), S(0))")
    t6 = term("M(any_variable, any_other_variable)")
    t7 = term("x")
    t8 = term("A(S(0), S(S(A(M(S(0), S(S(0))), 0))))")
    
    t6.redexpositions = findredexes(t6, s)
    t7.redexpositions = findredexes(t7, s)
    t8.redexpositions = findredexes(t8, s)
