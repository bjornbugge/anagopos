from lambda_dag import *

from string import *
import re
from yappsrt import *

class LambdaScanner(Scanner):
    patterns = [
        ('"\\\\)"', re.compile('\\)')),
        ('"\\\\("', re.compile('\\(')),
        ('""', re.compile('')),
        ('[ \r\t\n]+', re.compile('[ \r\t\n]+')),
        ('END', re.compile('$')),
        ('LAM', re.compile('#')),
        ('DOT', re.compile('.')),
        ('VAR', re.compile('[a-zA-Z_]+')),
        ('ID', re.compile('[a-zA-Z_]+')),
    ]
    def __init__(self, str):
        Scanner.__init__(self,None,['[ \r\t\n]+'],str)

class Lambda(Parser):
    def EXP(self):
        _token_ = self._peek('LAM', '""', 'VAR', '"\\\\("')
        if _token_ not in ['LAM', '""']:
            EXP2 = self.EXP2()
            EXP = self.EXP()
            print "EXP2 EXP;"
            child1 = EXP2
            child2 = EXP
            if not child2 is None: A = Application()
            if not child2 is None: A.add(child1)
            if not child2 is None: A.add(child2)
            if not child2 is None: return A
            else: return EXP2
        elif _token_ == 'LAM':
            LAM = self._scan('LAM')
            VAR = self._scan('VAR')
            DOT = self._scan('DOT')
            EXP = self.EXP()
            print "ABS;"
            A = Abstraction()
            child = EXP
            A.add(child)
            A.varname = VAR
            return A
        else:# == '""'
            self._scan('""')
            print "EMPTY;"

    def EXP2(self):
        _token_ = self._peek('VAR', '"\\\\("')
        if _token_ == 'VAR':
            VAR = self._scan('VAR')
            print "VAR = ", VAR
            x = Variable(VAR)
            return x
        else:# == '"\\\\("'
            self._scan('"\\\\("')
            EXP = self.EXP()
            self._scan('"\\\\)"')
            print "PAR"
            return EXP


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
