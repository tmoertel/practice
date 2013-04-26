#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-04-09


"""Solution to "Numbers" Code Jam problem
http://code.google.com/codejam/contest/32016/dashboard#s=p2

We want C_n = (3 + √5)^n mod 1000, but when n is large, the √5 term is
going to expensive to maintain with necessary precision.  Further, it
would be nice to get rid of that term altogether so we could use
integer operations exclusively.

So let's consider D = (3 - √5), the conjugate to C = (3 + √5).  Since
0 < D < 1, we know that 0 < D^n < 1.  Letting D_n = D^n and

    X_n = C_n + D_n,

we therefore have

    (1)    X_n - 1  <  C_n  <  X_n  <  C_n + 1

So now let's consider the binomial expansions of C_n and D_n, which
together give X_n, hoping that the square-root terms do indeed cancel
out:

    X_n = C_n + D_n

        = sum(binomial(n, i) * 3^(n-i) * ( √5)^i, i, 0, n) +
          sum(binomial(n, i) * 3^(n-i) * (-√5)^i, i, 0, n)

        = sum(binomial(n, i) * 3^(n-i) * ((√5)^i + (-√5)^i), i, 0, n)

As hoped, the conjugate trick eliminated the radicals.  All the terms
for [i odd] cancel out, and all the √5 factors in the terms for [i
even] are raised to an even power and thus become integer powers of 5.
Thus we know that X_n is an integer and, by (1), that C_n is between
the integers X_n - 1 and X_n.

Therefore, the integer part of C_n must be X_n - 1 and, finally,
we have

    C_n = X_n - 1   (mod 1000).

So now let's turn to efficiently computing X_n using integer
operations.  Right now, we have a closed-form formula for X_n.  We'd
like a corresponding linear recurrence relation.  More typically, we
have a recurrence relation and want to find its closed form, but this
time we want to go the other way around because the closed form
contains that pesky √5 and we're hoping the recurrence relation can be
solved with integers only.

So let's try to create a characteristic polynomial.  We'll aim for one
of the second degree since we probably need squared terms to eliminate
the radicals.  We imagine a solution of the form

    X[n+2] = a * X[n+1] + b * X[n] + c

and solve for a, b, and c at n = 1, 2, 3 (since we have three
unknowns) using Maxima:

    (%i1) X[n] := (3 + sqrt(5))^n + (3 - sqrt(5))^n$
    (%i2) eq: X[n+2] = a * X[n+1] + b * X[n] + c$
    (%i3) solve(makelist(''eq, n, 3), [a, b, c]);
    (%o3)   [[a = 6, b = - 4, c = 0]]

So we have

    X[n+2] = 6 X[n+1] - 4 X[n].

We can rewrite the equation into matrix form as follows:

    X[n+2] = 6 X[n+1] - 4 X[n]
    X[n+1] = 1 X[n+1] + 0 X[n]

which is equivalent to

    [ X[n+2] ]   [ 6  -4 ] [ X[n+1] ]
    [        ] = [       ] [        ]
    [ X[n+1] ]   [ 1   0 ] [ X[n+0] ]

which is equivalent to

    [ X[n+1] ]   [ 6  -4 ]^^0 [ X[n+1] ]
    [        ] = [       ]    [        ]
    [ X[n]   ]   [ 1   0 ]    [ X[n]   ]

which is in turn equivalent to

    [ X[n+1] ] = [ 6  -4 ]^^n [ X[1] ]
    [        ] = [       ]    [      ]
    [ X[n]   ]   [ 1   0 ]    [ X[0] ]

Finally, we just need the initial values to complete our formula:

    (%i4) [X[1], X[0]];
    (%o4)   [6, 2]

Now all that's left is to compute X_n via fast exponentiation and
return C_n = X_n - 1 (mod 1000).

---

Here is a more-general method for using Maxima to find recurrence
relations for closed-form series formulas and convert them into
matrix-formula solutions.

(%i3) load("eigen")$

First, we state the closed-form formula for the series:

(%i4) X[n] := expand( (3 + sqrt(5))^n + (3 - sqrt(5))^n )$

Then, we build an n-by-m matrix whose each row i represents a
shifted sample [X[i], X[i+1], ... [X+m-1]] of the series.

(%i5) Y[i, j] := X[i + j - 2]$

To find the rank of the recurrence, we construct a shifted-sample
matrix of larger size (here we guess 5 is large enough) and measure
its rank:

(%i6) rank(genmatrix(Y, 5, 5));
(%o6) 2

We now know that the rank of this recurrence is 2; that is, that there
are two unknowns, which we'll call a and b.  To solve for them, we
need two equations:

(%i7) Y: genmatrix(Y, 2, 3);

      [ 2  6   28  ]
(%o7) [            ]
      [ 6  28  144 ]

(%i8) Y . [b, a, -1];

      [ 2 b +  6 a - 28  ]
(%o8) [                  ]
      [ 6 b + 28 a - 144 ]

(%i9) solve(flatten(args(%)), [a, b]);
(%o9) [[a = 6, b = -4]]

(%i10) A: matrix(ev([a, b], %), [1, 0]);

       [ 6  -4 ]
(%o10) [       ]
       [ 1   0 ]

(%i11) b: columnvector([X[1], X[0]]);

       [ 6 ]
(%o11) [   ]
       [ 2 ]

(%i12) X2[n] := (A^^n . b)[2][1]$

(%i13) makelist(X2[i], i, 0, 5);
(%o13) [2, 6, 28, 144, 752, 3936]


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
