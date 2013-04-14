#!/usr/bin/python
#
# Tom Moertel <tom@moertel.com>
# 2013-04-13


"""Solution to "Fair and Square" Code Jam problem
https://code.google.com/codejam/contest/2270488/dashboard#s=p2

"""

import fileinput

def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print 'Case #%r: %r' % (i, s)

def solve(problem):
    A, B = problem
    a, b = isqrt(A), isqrt(B, want_upper_bound=True)
    ndigits_a, ndigits_b = len(str(a)), len(str(b))
    digit1_a = int(str(a)[0])
    count = 0
    for ndigits in xrange(ndigits_a, ndigits_b + 1):
        min_leading_digit = digit1_a if ndigits == ndigits_a else 1
        for i in palindromes(ndigits, min_leading_digit):
            ii = i * i
            if ii < A:
                continue
            if ii > B:
                return count
            sii = str(ii)
            if list(sii) == list(reversed(sii)):
                count += 1

def read_problems(lines):
    T = int(lines.next())
    for _ in xrange(T):
        yield read_problem(lines)

def read_problem(lines):
    A, B = read_ints(lines)
    return A, B

def isqrt(x, want_upper_bound=False):
    lo, hi = 1, x
    while True:
        if hi - lo < 2:
            return hi if want_upper_bound else lo
        mid = lo + ((hi - lo) >> 1)
        d = cmp(mid * mid, x)
        if d < 0:
            lo = mid
        elif d > 0:
            hi = mid
        else:
            return mid

def palindromes(ndigits, min_leading_digit=1):
    if ndigits == 0:
        return [0]
    digits = range(min_leading_digit, 10)
    if ndigits == 1:
        return digits
    def pals2(ndigits):
        if ndigits == 0:
            return 1, [0]
        if ndigits == 1:
            return 10, range(10)
        mul, ps = pals2(ndigits - 2)
        def gen():
            for p in ps:
                yield 10*p
            for i in xrange(1, 10):
                for p in pals2(ndigits - 2)[1]:
                    yield 10*mul*i + 10*p + i
        return 100 * mul, gen()
    mul, ps = pals2(ndigits - 2)
    def gen():
        i = digits[0]
        for p in ps:
            yield 10*mul*i + 10*p + i
        for i in digits[1:]:
            for p in pals2(ndigits - 2)[1]:
                yield 10*mul*i + 10*p + i
    return gen()

def read_ints(lines):
    return [int(s) for s in lines.next().split()]


if __name__ == '__main__':
    main()
