import StringIO


def tostring_v1(s, f):
    '''A naive algorithm that just prints +'s and -'s within a single cell.'''
    n = 0
    for b in map(ord, s):
        if n < b:
            f.write('+'*(b-n))
        elif n > b:
            f.write('-'*(n-b))
        f.write('.')
        n = b

def findfactors(n):
    '''Yields [a, b, c] triplets where a * b + c == n'''
    for m in range(n, int(n**0.5), -1):
        for k in range(int(m**0.5), m):
            if m % k == 0:
                assert k * (m / k) + n - m == n
                yield [k, m / k, n - m]

def factor(n):
    '''Find the smallest set of factors.'''
    return min(findfactors(n), key=sum)


def tostring_v2(s, f):
    '''A slightly smarter algorithm that uses loops to optimize long strings
       of +'s or -'s. The second cell is used as an accumulator.
    '''
    n = 0
    for b in map(ord, s):
        ch = '+' if n < b else '-'
        diff = abs(b - n)
        if diff < 8:
            # If the difference is small, just write the +/-s.
            f.write(ch*diff)
        else:
            # Otherwise factor the number and write a loop.
            x, y, z = factor(abs(b - n))
            f.write('>')
            f.write('+'*x)
            f.write('[<')
            f.write(ch*y)
            f.write('>-]<')
            f.write(ch*z)
        f.write('.')
        n = b


def tostring(s, func=tostring_v2, linewidth=80):
    f = StringIO.StringIO()
    func(s, f)
    bf = f.getvalue()
    # Split into evenly sized lines.
    return '\n'.join(bf[i:i+linewidth] for i in range(0, len(bf), linewidth))
