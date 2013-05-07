#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-05-04


"""Solution to "Falling Diamonds" Code Jam problem
https://code.google.com/codejam/contest/2434486/dashboard#s=p1

The falling diamonds build, bit by bit, a series of ever-growing
triangles, which we will label i = 0, 1, ....  Let s[i] be the count
of diamonds in the complete triangle i, and b[i] the count of diamonds
in the triangle's base.  These then form the related series,

    i         0      1      2          3            4  ...
    b[i]      0      1      3          5            7  ...
    s[i]      0      1      6         15           28  ...

                                                    ◆
                                                   ◆ ◆
                                       ◆          ◆ ◆ ◆
                                      ◆ ◆        ◆ ◆ ◆ ◆
                             ◆       ◆ ◆ ◆      ◆ ◆ ◆ ◆ ◆
                            ◆ ◆     ◆ ◆ ◆ ◆    ◆ ◆ ◆ ◆ ◆ ◆
                     ◆     ◆ ◆ ◆   ◆ ◆ ◆ ◆ ◆  ◆ ◆ ◆ ◆ ◆ ◆ ◆

In closed form,

    b[i] = 2*i - 1   if i > 0,  and

    s[i] = i * (2*i - 1).

Now, consider the structure that results when N diamonds are dropped.
For the lucky case that N = s[i] for some i, the structure is a complete
triangle, and the occupancy of (X, Y) is completely determined.  If
(X, Y) is one of the triangle's diamonds, the probability we seek
is 1; otherwise, it's 0.

Looking at the problem more generally, when s[i] <= N < s[i+1], we
have 3 mutually exclusive cases to consider:

A.  (X, Y) is a diamond of triangle i.
B.  (X, Y) is a not diamond of triangle i but is of triangle i+1.
C.  (X, Y) is not even a diamond of triangle i+1.

Again, in cases A and C, there can be no uncertainty; they have
respective probabilities of 1 and 0.

But in case B, (X, Y) locates a diamond along the left or right edge
of the *complete* triangle i+1, but since N < s[i+1], we know the
structure in question is *not* a complete triangle.  Thus question
then becomes, what is the probability that the diamond remains after
s[i+1] - N diamonds have been removed at random from the complete
triangle i+1 to make a structure of N diamonds?

For example, for N = 8 we find the next-larger complete triangle of
s[3] = 15 diamonds.  In case B, (X, Y) must be one of the white
diamonds because it's within the complete triangle i = 3 but not
within the next-smallest complete triangle i = 2 (shown as black
diamonds).

       ◇
      ◇ ◇         N      =  8
     ◇ ◆ ◇        i      =  2
    ◇ ◆ ◆ ◇       s[i]   =  6
   ◇ ◆ ◆ ◆ ◇      s[i+1] = 15

If X = 0, the probability must be 0 because the peak diamond must be
missing from the structure since we're in case B for i = k (and not
case A for i = k+1).

For |X| > 0, the probability we seek is the probability that *fewer*
than |X| diamonds have been removed from the side of the triangle that
X is on.  (By symmetry we can ignore left-right distinctions and just
refer to "X's side.")  The peak diamond is already gone, and now we
must remove m = s[i+1] - N - 1 more diamonds, choosing at random
between X's side and the other side.  When m < b[i+1], it's not
possible to completely empty a side, and thus the underlying
probabilities have a vanilla binomial distribution.  Thus our
answer must be

    p = binom.cdf(abs(X) - 1, m, 0.5).

But when m >= b[i+1], it's easier to think about the dual problem of
having to *add* N - s[i] < b[i+1] diamonds to the sides of the smaller
triangle i.  The underlying distribution is again vanilla binomial,
since it's not possible to over-fill a side.  In this formulation, we
must add at least b[i+1] - |X| diamonds to X's side, which is the same
as *not* adding fewer than b[i+1] - |X| diamonds.  Thus our
answer must be

    p = 1.0 - binom.cdf(b[i+1] - abs(X) - 1, N - s[i], 0.5).

And that's it.

"""


import fileinput
from scipy.stats import binom

def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print 'Case #%r: %r' % (i, s)

def solve(problem):
    N, X, Y = problem
    if N == 0:
        return 0.0
    i = find_int_by_bisection(s, 1, N, N)
    if is_triangle_diamond(X, Y, i):
        return 1.0  # case A
    if not is_triangle_diamond(X, Y, i + 1):
        return 0.0  # case C
    # case B
    if X == 0:
        return 0.0
    m = s(i + 1) - N - 1
    if m < b(i + 1):
        return binom.cdf(abs(X) - 1, m, 0.5)
    return 1.0 - binom.cdf(b(i + 1) - abs(X) - 1, N - s(i), 0.5)

def is_triangle_diamond(x, y, i):
    """Test whether (x, y) locates a diamond in the complete triangle i."""
    size = b(i)
    xmax = size - y - 1
    return abs(x) <= xmax and (xmax + x) % 2 == 0

def s(i):
    """Get the size in diamonds of the complete triangle i."""
    return i * (2*i - 1)

def b(i):
    """Get the base length in diamonds of the complete triangle i."""
    if i < 1:
        return 0
    return 2 * i - 1

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
