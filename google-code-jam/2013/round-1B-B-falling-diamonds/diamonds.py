#!/usr/bin/python
#
# Tom Moertel <tom@moertel.com>
# 2013-05-04


"""Solution to "Falling Diamonds" Code Jam problem
https://code.google.com/codejam/contest/2434486/dashboard#s=p1

The falling diamonds build, in succession, a series of ever growing
triangles.  The number of diamonds in the complete triangles forms the
series s[i] and the size of the base of those triangles the series
b[i]

    i      0   1   2   3   4   5 ...
    s[i]   0   1   6  15  28  45 ...
    b[i]   0   1   3   5   7   9

In closed form,

    s[i] = i * (2 * i - 1)  and

    b[i] = 0          if i = 0
           1          if i = 1
           2 * i - 1  if i > 1



"""

import fileinput
import functools
import sys

def memoize(f):
    """Make a memoized version of f that returns cached results."""
    cache = {}
    @functools.wraps(f)
    def g(*args):
        ret = cache.get(args, cache)
        if ret is cache:
            ret = cache[args] = f(*args)
        return ret
    return g

def main():
    sys.setrecursionlimit(int(1e6 + 1))
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print 'Case #%r: %r' % (i, s)

def solve(problem):
    N, X, Y = problem
    if N == 0 or (X % 2) != (Y % 2):
        return 0.0
    i = inner_triangle_series_index(N)
    base_size = b(i)
    if in_bounds(X, Y, base_size):
        return 1.0
    if not in_bounds(X, Y, base_size + 2):
        return 0.0
    in_play = N - s(i)
    side_len = (s(i + 1) - s(i)) // 2
    need = xbounds(0, base_size + 2) - abs(X) + 1
    if need > side_len:
        return 0.0
    p_need = prob(in_play, need)
    if in_play > side_len:
        q = prob(in_play, side_len)
        return ( (q)  * 0.5 * (1 + (in_play - side_len >= need)) +
                (1-q) * p_need)
    return p_need

@memoize
def prob(n, i):
    if i == 0:
        return 1.0
    if n == 0:
        return 0.0
    return 0.5 * (prob(n - 1, i - 1) + prob(n - 1, i))


def in_bounds(x, y, base_size):
    x = abs(x)
    xmax = xbounds(y, base_size)
    return x <= xmax and (xmax - x) % 2 == 0

@memoize
def xbounds(y, base_size):
    if base_size < 0:
        return -1
    if y > 0:
        return xbounds(y - 1, base_size - 1)
    return base_size - 1

def s(i):
    return i * (2 * i - 1)

def b(i):
    if i < 2:
        return i
    return 2 * i - 1

def inner_triangle_series_index(n):
    """Find series index i of the largest complete triangle of size <= n."""
    return find_int_by_bisection(s, 0, n, n)

def read_problems(lines):
    T = int(lines.next())
    for _ in xrange(T):
        yield read_problem(lines)

def read_problem(lines):
    N, X, Y = read_ints(lines)
    return N, X, Y

def read_ints(lines):
    return [int(s) for s in lines.next().split()]

def find_int_by_bisection(f, lo, hi, y):
    """Find maximal int x in [lo, hi] such that f(x) <= y.

    Note: f must be monotonic within the range [lo, hi].

    """
    _check_bisection_bounds(f, lo, hi, y)
    while lo < hi:
        mid = lo + ((hi - lo) >> 1)
        if f(mid) <= y:
            lo = mid + 1
        else:
            hi = mid - 1
    return lo if f(lo) <= y else lo - 1

def _check_bisection_bounds(f, lo, hi, y):
    if lo > hi:
        raise ValueError('lower bound is above upper bound')
    if y < f(lo):
        raise ValueError('solution is below lower bound')
    if y > f(hi):
        raise ValueError('solution is above upper bound')

if __name__ == '__main__':
    main()
