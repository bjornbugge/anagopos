
# May be one of 'lambda' or 'trs'.
__mode__ = ''

def setmode(mode):
    if mode == 'lambda':
        import computegraph.lambda_operations as OPS
    else if mode == 'trs':
        import computegraph.trs_operations as OPS
    else:
        raise Exception("Unsupported mode: " + mode)
    
    __mode__ = mode
        

def assignvariables(root):
    OPS.assignvariables(root)

def reductiongraphiter(root, start, end, ruleSet = None):
    if __mode__ == 'lambda':
        return OPS.reductiongraphiter(root, start, end)
    else if __mode__ == 'trs':
        return OPS.reductiongraphiter(root, start, end, ruleSet)
    else:
        raise Exception("Unsupported mode: " + __mode__)
