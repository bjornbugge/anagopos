from string import *
import re
from yappsrt import *

class LambdaScanner(Scanner):
    patterns = [
        ('"\\\\)"', re.compile('\\)')),
        ('"\\\\("', re.compile('\\(')),
        ('"\xce\xbb"', re.compile('\xce\xbb')),
        ('END', re.compile('$')),
        ('LAM', re.compile('[\xce\xbb]+')),
        ('DOT', re.compile('[.]+')),
        ('VAR', re.compile('[a-zA-Z_]+')),
    ]
    def __init__(self, str):
        Scanner.__init__(self,None,[],str)

class Lambda(Parser):
    def x(self):
        x = self.x()
        VAR = self._scan('VAR')
        return x

    def term(self):
        _token_ = self._peek('"\xce\xbb"', '"\\\\("')
        if _token_ == '"\xce\xbb"':
            abstraction = self.abstraction()
            return abstraction
        else:# == '"\\\\("'
            parentheses = self.parentheses()
            return parentheses

    def abstraction(self):
        _token_ = self._peek('"\xce\xbb"')
        self._scan('"\xce\xbb"')
        x = self.x()
        DOT = self._scan('DOT')
        abstraction = self.abstraction()
        return term

    def parentheses(self):
        self._scan('"\\\\("')
        term = self.term()
        term = self.term()
        self._scan('"\\\\)"')
        return term


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
