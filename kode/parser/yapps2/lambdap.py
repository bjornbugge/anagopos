from string import *
import re
from yappsrt import *

class LambdaScanner(Scanner):
    patterns = [
        ('"\\\\)"', re.compile('\\)')),
        ('"\\\\("', re.compile('\\(')),
        ('""', re.compile('')),
        ('END', re.compile('$')),
        ('LAM', re.compile('#')),
        ('DOT', re.compile('.')),
        ('VAR', re.compile('[a-zA-Z_]+')),
        ('ID', re.compile('[a-zA-Z_]+')),
    ]
    def __init__(self, str):
        Scanner.__init__(self,None,[],str)

class Lambda(Parser):
    def goal(self):
        EXP = self.EXP()
        END = self._scan('END')
        print "end;"

    def x(self):
        VAR = self._scan('VAR')
        print "var"

    def EXP(self):
        _token_ = self._peek('""', 'VAR', 'LAM', '"\\\\("')
        if _token_ != '""':
            EXP2 = self.EXP2()
            EXP = self.EXP()
            print "EXP;"
        else:# == '""'
            self._scan('""')

    def EXP2(self):
        _token_ = self._peek('VAR', 'LAM', '"\\\\("')
        if _token_ == 'VAR':
            VAR = self._scan('VAR')
            print "VAR;"
        elif _token_ == 'LAM':
            LAM = self._scan('LAM')
            VAR = self._scan('VAR')
            DOT = self._scan('DOT')
            EXP = self.EXP()
            print "ABS;"
        else:# == '"\\\\("'
            self._scan('"\\\\("')
            EXP = self.EXP()
            self._scan('"\\\\)"')
            print "PAR;"


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
