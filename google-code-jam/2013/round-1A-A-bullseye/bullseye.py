#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-04-26


"""Solution to "Bullseye" Code Jam problem
http://code.google.com/codejam/contest/2418487/dashboard

The total amount of paint in ml consumed by n disks around
a white center of r cm is given by

    paint(r, n) := sum(2*r + 4*i - 3, i, 1, n)

which simplifies to the closed form

    paint(r, n) := n*(2*r+2*n-1).

Now, for a given r and paint volume t, we want to find the
corresponding n, and the answer we seek is floor(n).  Solving
for n in terms of r and t,

(%i99) t = ans[r, n];
(%o99) t=n*(2*r+2*n-1)
(%i100) solve(%, n);
(%o100) [n=-(sqrt(8*t+4*r^2-4*r+1)+2*r-1)/4,n=(sqrt(8*t+4*r^2-4*r+1)-2*r+1)/4]

we find one positive root

(%i101) n, %[2];
(%o101) (sqrt(8*t+4*r^2-4*r+1)-2*r+1)/4

And that's our closed-form for n.

"""

import fileinput

def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print 'Case #%r: %r' % (i, s)

def solve(problem):
    r, t = problem
    x = 8*t + 4*r*r - 4*r + 1
    n = int((isqrt(x)- 2*r + 1) / 4.0)
    while n * (2*r + 2*n - 1) <= t:
        n += 1
    return n - 1

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

def read_problems(lines):
    T = int(lines.next())
    for _ in xrange(T):
        yield read_problem(lines)

def read_problem(lines):
    r, t = read_ints(lines)
    return r, t

def read_ints(lines):
    return [int(s) for s in lines.next().split()]

if __name__ == '__main__':
    main()
