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

from computegraph.lambda_dag import *

_position  = None
_string_in = None
_symbol    = None

class LambdaParseException(Exception):
    pass

def get__symbol():
    global _position, _symbol

    while _position != len(_string_in) \
            and (_string_in[_position] == ' ' \
                     or _string_in[_position] == '\t' \
                     or _string_in[_position] == '\n' \
                     or _string_in[_position] == '\r'):
        _position += 1

    if _position == len(_string_in):
       _symbol = '\0'
       return

    _symbol = _string_in[_position]
    _position += 1

def variable():
    if not (_symbol >= 'a' and _symbol <= 'z') \
            and not (_symbol >= 'A' and _symbol <= 'Z'):
        raise LambdaParseException("Invalid _symbol on input: " + _symbol)

    string = _symbol[:]
    get__symbol() # consumes letter

    while (_symbol >= '0' and _symbol <= '9'):
        string += _symbol
        get__symbol() # consumes number

    var = Variable(string)
    return var

def abstraction():
    if not (_symbol == '\\'):
        raise LambdaParseException("Invalid _symbol on input: " + _symbol)

    get__symbol() # consumes abstraction _symbol
    var = variable()
    top = Abstraction()
    top.varname = var.name
    bottom = top
    while _symbol != '.':
        var = variable()
        ab  = Abstraction()
        ab.varname = var.name
        bottom.add(ab)
        bottom = ab

    get__symbol() # consumes dot
    subterm = term()
    bottom.add(subterm)
    return top

def term():
    if _symbol != '(' \
            and not (_symbol >= 'a' and _symbol <= 'z') \
            and not (_symbol >= 'A' and _symbol <= 'Z') \
            and not (_symbol == '\\'):
        raise LambdaParseException("Invalid _symbol on input: " + _symbol)

    first = True

    while _symbol == '(' \
            or (_symbol >= 'a' and _symbol <= 'z') \
            or (_symbol >= 'A' and _symbol <= 'Z') \
            or (_symbol == '\\'):
        if _symbol == '(':
            get__symbol() # consumes open parenthesis
            subterm = term()

            if _symbol != ')':
                raise LambdaParseException("Invalid _symbol on in: " + _symbol)

            get__symbol() # consumes closing parenthesis
        elif (_symbol >= 'a' and _symbol <= 'z') \
                or (_symbol >= 'A' and _symbol <= 'Z'):
            subterm = variable()
        elif _symbol == '\\':
            subterm = abstraction()

        if first:
            top = subterm
            first = False
        else:
            old_t = top
            top = Application()
            top.add(old_t)
            top.add(subterm)

    return top

def parse(string):
    global _string_in, _position

    _string_in = string
    _position = 0
    get__symbol()
    whole_term = term()

    if _symbol != '\0':
        raise Exception("Symbols left on input: " + _string_in[_position:])

    return whole_term

def test():
    test_term = "(\\x.x)((\\y.(\\w.w)x)z)"
    t = parse(test_term)
    t.makestr()
    print(t)
