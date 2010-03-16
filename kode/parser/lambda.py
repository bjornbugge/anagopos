from string import *
import re
from yappsrt import *

class LambdaScanner(Scanner):
    patterns = [
        ('"\\\\)"', re.compile('\\)')),
        ('"\\\\("', re.compile('\\(')),
        ('"/"', re.compile('/')),
        ('END', re.compile('$')),
        ('LAM', re.compile('[\xc2\xa3\xe2\x80\x9d]+')),
        ('VAR', re.compile('[a-zA-Z_]+')),
    ]
    def __init__(self, str):
        Scanner.__init__(self,None,[],str)

class Lambda(Parser):
    def goal(self):
        expr = self.expr()
        END = self._scan('END')
        return expr

    def expr(self):
        term = self.term()
        v = term
        while self._peek('"/"', 'END', '"\\\\)"') == '"/"':
            self._scan('"/"')
            term = self.term()
            v = v/term
        return v

    def term(self):
        self._scan('"\\\\("')
        expr = self.expr()
        self._scan('"\\\\)"')
        return expr


def parse(rule, text):
    P = Lambda(LambdaScanner(text))
    return wrap_error_reporter(P, rule)

if __name__ == '__main__':
    from sys import argv, stdin
    if len(argv) >= 2:
        if len(argv) >= 3:
            f = open(argv[2],'r')
        else:
            f = stdin
        print parse(argv[1], f.read())
    else: print 'Args:  <rule> [<filename>]'
