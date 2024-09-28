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
                            ◆        ◆ ◆ ◆      ◆ ◆ ◆ ◆ ◆
                           ◆ ◆      ◆ ◆ ◆ ◆    ◆ ◆ ◆ ◆ ◆ ◆
                     ◆    ◆ ◆ ◆    ◆ ◆ ◆ ◆ ◆  ◆ ◆ ◆ ◆ ◆ ◆ ◆

In closed form,

    b[i] = 2*i - 1   if i > 0,  and

    s[i] = i * (2*i - 1).

Now, consider the structure that results when N diamonds are dropped.
For the lucky case that N = s[i] for some i, the structure is a complete
triangle, and the occupancy of (X, Y) is completely determined.  If
(X, Y) is one of the triangle's diamonds, the probability we seek
is 1; otherwise, it's 0.

Looking at the problem more generally, when we find the largest i for
which s[i] <= N, we know that s[i] <= N < s[i+1].  That is, any legal
structure of N diamonds must at least contain the complete triangle i
but cannot contain the complete triangle i+1.  Thus we have 3 mutually
exclusive cases to consider:

A.  (X, Y) is a diamond of triangle i, which the structure contains,
    and therefore *must* be in the structure.

B.  (X, Y) is a not diamond of triangle i but is of triangle i+1,
    which contains the structure, and therefore *may* be in the
    structure.

C.  (X, Y) is not even a diamond of triangle i+1, and therefore
    *cannot* be in the structure.

Again, in cases A and C, there can be no uncertainty; they have
respective probabilities of 1 and 0.

But in case B, (X, Y) locates a diamond within the complete triangle
i+1 but not within the complete triangle i.  Thus (X, Y) must be
within the difference between triangles i+1 and i, that is, along one
of triangle i+1's sides.

For example, when N = 8, (X, Y) must locate one of the white diamonds
in the diagram below if it falls into Case B:

       ◇
      ◇ ◇         N      =  8
     ◇ ◆ ◇        i      =  2
    ◇ ◆ ◆ ◇       s[i]   =  6
   ◇ ◆ ◆ ◆ ◇      s[i+1] = 15

But since N < s[i+1], we know that some of the white diamonds are
missing from the structure.  At minimum the peak diamond is missing.
Thus the question becomes, What is the probability that the white
diamond at (X, Y) remains after s[i+1] - N white diamonds have been
removed?

If X = 0, the probability must be 0 because X = 0 can only locate a
peak diamond, which we know our structure lacks.

For |X| > 0, the probability we seek is the probability that, from X's
side, the number of diamonds removed, let it be k, is less than |X|.
(By symmetry we can ignore left-right distinctions.)  That is, k is a
random variable, and we seek Pr(k < |X|).

What is the distribution of k?  The peak is already gone, and now we
must remove m = s[i+1] - N - 1 more diamonds, choosing at random
between X's side and the other side.  When m < b[i+1], it's not
possible to completely empty a side, and thus k has a vanilla binomial
distribution.  Therefore,

    Pr(k < |X|)) = Pr(k <= |X| - 1)
                 = binom.cdf(abs(X) - 1, m, 0.5).

But when m >= b[i+1], we can empty a side, and it's easier to think
about the dual problem of having to *add* N - s[i] diamonds to the
sides of the smaller triangle i.  Since N - s[i] < b[i+1] in this
case, it's not possible to over-fill a side, and the distribution of
the number of diamonds added to X's side, let it be j, is vanilla
binomial.  In this formulation, we must add at least b[i+1] - |X|
diamonds to X's side, which is the same as *not* adding fewer than
b[i+1] - |X| diamonds.  Thus our answer must be

    Pr(k < |X|) = Pr(j >= b[i+1] - |X|)
                = 1.0 - Pr(j < b[i+1] - |X|)
                = 1.0 - Pr(j <= b[i+1] - |X| - 1])
                = 1.0 - binom.cdf(b[i+1] - abs(X) - 1, N - s[i], 0.5).

And that's it.  For cases A and C, we know the answer immediately.
For case B, we know the answer after spliting it into one of 3
subcases:

    (1) X = 0
    (2) X != 0 and m < b[i+1]
    (3) X != 0 and m >= b[i+1]

"""


import fileinput
from scipy.stats import binom

def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print('Case #%r: %r' % (i, s))

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
        return 0.0  # B(1)
    m = s(i + 1) - N - 1
    if m < b(i + 1):
        return binom.cdf(abs(X) - 1, m, 0.5)  # B(2)
    return 1.0 - binom.cdf(b(i + 1) - abs(X) - 1, N - s(i), 0.5)  # B(3)

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
    T = int(next(lines))
    for _ in range(T):
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
