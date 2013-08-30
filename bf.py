import StringIO

def tostring_naive(s):
    f = StringIO.StringIO()
    n = 0
    for b in map(ord, s):
        if n < b:
            f.write('+'*(b-n))
        elif n > b:
            f.write('-'*(n-b))
        f.write('.')
        n = b
    return f.getvalue()

def tostring(s, func=tostring_naive):
    bf = func(s)
    return '\n'.join(bf[i:i+80] for i in range(0, len(bf), 80))
