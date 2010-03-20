from string import *
import re
from yappsrt import *

class LambdaScanner(Scanner):
    patterns = [
        ('"\\\\)"', re.compile('\\)')),
        ('"\\\\("', re.compile('\\(')),
        ('END', re.compile('$')),
        ('LAM', re.compile('#')),
        ('DOT', re.compile('.')),
        ('VAR', re.compile('[a-zA-Z_]+')),
    ]
    def __init__(self, str):
        Scanner.__init__(self,None,[],str)

class Lambda(Parser):
    def goal(self):
        term = self.term()
        END = self._scan('END')
        print "term end;"

    def x(self):
        VAR = self._scan('VAR')
        print "VAR"

    def term(self):
        _token_ = self._peek('VAR', 'LAM', '"\\\\("')
        if _token_ == 'VAR':
            x = self.x()
            print "rule -> "
        elif _token_ == 'LAM':
            abstraction = self.abstraction()
            print "rule -> "
        else:# == '"\\\\("'
            parentheses = self.parentheses()
            print "rule -> "

    def abstraction(self):
        LAM = self._scan('LAM')
        x = self.x()
        DOT = self._scan('DOT')
        term = self.term()
        print "abstraction; "

    def parentheses(self):
        self._scan('"\\\\("')
        term = self.term()
        self._scan('"\\\\)"')
        print "parentheses; "


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
