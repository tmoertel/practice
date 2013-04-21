#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-04-09


"""Solution to "Numbers" Code Jam problem
http://code.google.com/codejam/contest/32016/dashboard#s=p2


We want C_n = (3 + √5)^n mod 1000, but when n is large, the √5 term is
going to be unwieldy.  Further, it would be nice to get rid of the
radical altogether so we could use integral arithmetic operations
exclusively.

So let's consider D = (3 - √5), the conjugate to C = (3 + √5).  Since
0 < D < 1, we know that 0 < D^n < 1.  Letting D_n = D^n and

    X_n = C_n + D_n,

we therefore have

    (1)    X_n - 1  <  C_n  <  X_n  <  C_n + 1

So now let's consider the binomial expansions of C_n and D_n in X_n,
hoping that the square-root terms cancel out:

    X_n = C_n + D_n

        = sum(binomial(n, i) * 3^(n-i) * ( √5)^i, i, 0, n) +
          sum(binomial(n, i) * 3^(n-i) * (-√5)^i, i, 0, n)

        = sum(binomial(n, i) * 3^(n-i) * ((√5)^i + (-√5)^i), i, 0, n)

As hoped, the conjugate trick eliminated the radicals.  All the terms
for [i odd] cancel out, and all the √5 factors in the terms for [i
even] are raised to an even power.  Thus we know that X_n is integral
and, by (1), that C_n is between the integers X_n - 1 and X_n.

Therefore, the integer part of C_n must be X_n - 1 and, finally,
we have

    C_n = X_n - 1   (mod 1000).

So now let's turn to efficiently computing X_n using integer
operations.  Right now, we have a closed-form formula for X_n.  We'd
like a corresponding recurrence relation.  More typically, we have a
recurrence relation and want to find its closed form, but this time we
want to go the other way around because the closed form contains that
pesky √5 and we're hoping the recurrence relation can be solved with
integers only.

So let's try to create a second-order characteristic polynomial
since we probably need squared terms to eliminate the radicals.
We imagine a solution of the form

    X_{n+2} = a * X_{n+1} + b * X_n

and solve for a and b at n=1 and n=2 (since we have two unknowns)
using Maxima:

    (%i1) X[n] := (3 + sqrt(5))^n + (3 - sqrt(5))^n$
    (%i2) eq: X[n+2] = a * X[n+1] + b * X[n]$
    (%i3) solve([ev(eq, n=1), ev(eq, n=2)], [a, b]);
    (%o3)   [[a = 6, b = - 4]]

So we have

    X_{n+2} = 6 X_{n+1} - 4 X_n.

We can rewrite the equation into matrix form as follows:

    X_{n+2} = 6 X_{n+1} - 4 X_n
    X_{n+1} = 1 X_{n+1} + 0 X_n

which is equivalent to

    [ X_{n+2} ] = [ 6  -4 ] [ X_{n+1} ]
    [ X_{n+1} ] = [ 1   0 ] [ X_{n+0} ]

which is in turn equivalent to

    [ X_{n+1} ] = [ 6  -4 ]^^n [ X_1 ]
    [ X_n     ] = [ 1   0 ]    [ X_0 ]

Finally, we just need the initial values to compete our formula:

    (%i4) [X[1], X[0]];
    (%o4)   [6, 2]

Now all that's left is to compute X_n via fast exponentiation and
return C_n = X_n - 1 (mod 1000).

"""

import fileinput

def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print 'Case #%r: %s' % (i, s)

def solve(n):
    return '%03d' % ((X(n) + 999) % 1000, )

def X(n):
    A = [[6, -4], [1, 0]]
    B = [[6], [2]]
    if n < 2:
        return B[1 - n][0]
    mult = lambda A, B: mmul(A, B, 1000)
    Y = mult(gpow(A, n, mult), B)
    return Y[1][0]

def read_problems(lines):
    T = int(lines.next())
    for _ in xrange(T):
        yield read_problem(lines)

def read_problem(lines):
    return int(lines.next())

def gpow(x, n, mult):
    def go(x, n):
        if n == 1:
            return x
        if n % 2 == 1:
            return mult(x, go(x, n - 1))
        return go(mult(x, x), n >> 1)
    return go(x, n)

def test_gpow():
    for x in xrange(10):
        for n in xrange(1, 10):
            assert x**n == gpow(x, n, type(x).__mul__)

def mmul(A, B, modulus):
    assert len(A[0]) == len(B)
    Bt = zip(*B)  # transpose B to get column order
    return [[sum(a * b for a, b in zip(row, col)) % modulus
             for col in Bt] for row in A]

if __name__ == '__main__':
    main()
