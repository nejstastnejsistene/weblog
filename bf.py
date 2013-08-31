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


def tostring_v3(s, f, n=32, k=256):
    '''Precompose an array, and start from the cell with the closest value
       when printing a byte.
    '''
    m = k / n;
    f.write('+'*m)
    f.write('[')
    for i in range(1, n):
        f.write('>')
        f.write('+'*i)
    f.write('<'*(n-1))
    f.write('-]')

    foo = [i for i in range(0, k, k/n)]
    ptr = 0
    for b in map(ord, s):
        i = min(int(float(b) / m + 0.5), n-1)
        if ptr < i:
            f.write('>'*(i-ptr))
        elif ptr > i:
            f.write('<'*(ptr-i))
        if foo[i] < b:
            f.write('+'*(b-foo[i]))
        elif foo[i] > b:
            f.write('-'*(foo[i]-b))
        f.write('.')
        ptr = i
        foo[ptr] = b


def tostring(s, func=tostring_v3, linewidth=80):
    f = StringIO.StringIO()
    func(s, f)
    bf = f.getvalue()
    # Split into evenly sized lines.
    if linewidth <= 0:
        return bf
    return '\n'.join(bf[i:i+linewidth] for i in range(0, len(bf), linewidth))

if __name__ == '__main__':
    with open('boingboing.html') as f:
        text = f.read()
    print len(tostring(text, tostring_v1, 0))
    print len(tostring(text, tostring_v2, 0))
    print len(tostring(text, tostring_v3, 0))
