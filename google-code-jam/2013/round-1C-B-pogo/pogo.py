#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-05-12

"""Solution to "Pogo" Code Jam problem
https://code.google.com/codejam/contest/2437488/dashboard#s=p1

For this problem, I found that the key insight was that any path of N
steps that doesn't backtrack is an optimal solution for its end point
and ends S(N) = N * (N + 1) / 2 units from the origin.  Perhaps
surprisingly (see proof below), we can *construct* a non-backtracking
path to any (X, Y) where X + Y = S(N) for any integer N >= 0.

So we can visualize the problem space as a grid in which the origin is
surrounded by diamond-shaped bands of points satisfying X + Y = S(N)
for various N and to which we can construct non-backtracking and hence
optimal paths.  For any point (X, Y) on one of these bands, we know we
can get to it in N steps.  For any other point, we know we must
backtrack, which will require additional steps.

A forward-only path of length N must end on the band for N.  So if we
reverse its step i, we move its end 2*i units in the opposite
direction.  So if (X, Y) is just shy of band N by D < N units, and if
D is even, we can construct an optimal path of length N to (X + D, Y)
or (X, Y + D) on the band for N and then reverse its step D/2 to end
it exactly at (X, Y).  This path to (X, Y) will be optimal as well,
since we can't possibly get to (X, Y) with only N - 1 steps, and N,
which we've just made work, is the next best possibility.

But if D is odd, no combination of reversals will suffice to move any
point on the band for N to (X, Y) because each reversal moves it
closer by an even amount.  Thus there can be no solution of N steps.
But if we advance to the next band (N + 1), it will be N + 1 units
farther out than the band for N and thus D + N + 1 units from (X, Y).
If N + 1 is odd, D + N + 1 will be even, and thus reversals can find
us a solution of length N + 1.  But if N + 1 is odd, we must go one
more step to N + 2 steps in total.  Then D + N + 1 + N + 2 will be
even, and we can construct via reversals an optimal solution of
length N + 2.

And that's the shell of the solution: Find the tightest band N that
contains and is an even distance from (X, Y).  Then construct a
non-backtracking path to the band and reverse one or more of its steps
to move its end to (X, Y).

The more rigorous analysis follows.

Let us define a "path" of length N to be a series of N-S-E-W steps
starting at the origin and increasing in size as i = 1, 2, ... N.

We shall say that a path is "forward only" if it never backtracks.

We shall measure all distances as Manhattan distances.

By symmetry, any path that moves to (X, Y) is equivalent to one that
moves to (Y, X).  Also by symmetry, it is equivalent to one in which
X's or Y's or both's signs have been negated.  Therefore, any desired
destination (X1, Y1) can be reached by finding an equivalent path to a
normalized destination (X, Y), 0 <= Y <= X where Y = min(|X1|, |Y1|)
and X = max(|X1|, |Y1|).

Claim 1.  A forward-only path ends farther from the origin than any
same-length or shorter-length path that backtracks.  Proof: Follows
trivially from definition of backtrack.

Claim 2.  A forward-only path of length N ends exactly S(N) units from
the origin, where S(N) = N * (N + 1) / 2.  Proof: Since a forward-only
path does not backtrack, it moves farther from the origin with every
step, and in the exact amount of each step size.  Thus its terminal
distance from the origin is the sum of its step sizes

    S(N) = sum(i for i in 1..N) = N * (N + 1) / 2

Claim 3.  If a forward-only path to (X, Y) exists, it is an optimal
solution.  Proof: We proceed by contradiction.  Let there be a
forward-only path P of length N to (X, Y).  Since (X, Y) is X + Y
units from the origin, S(N) must equal X + Y.  Now assume that there
exists a path P1 to (X, Y) of shorter length N1 < N.  P1 is either
forward only or it backtracks.  If it is forward only, we must have
S(N1) = X + Y, but that equation cannot hold since S(N) = X + Y and
S(N1) < S(N) for N1 < N.  If P1 backtracks, its end must be closer to
the origin than P's end (by Claim 1) but, by assumption, P and P1
both end at the same point (X, Y).  In both cases, we have a
contradiction, completing the proof.

Claim 4.  A forward-only path can be constructed to any (X, Y) where
X + Y = S(N) for some integer N >= 0.  Proof: By induction.  Without
loss of generality, assume 0 <= Y <= X.  The base case N = 0 is
trivial.  Now assume that our claim holds for N - 1.  We can extend
it to N by noting that if (X, Y) is such that X + Y = S(N),
then (X - N, Y) is N units closer to the origin and therefore
(X - N) + Y = S(N) - N = S(N - 1).  By our induction hypothesis, then,
we can build a forward-only path to (X - N, Y).  And then, by adding a
forward horizontal step of size N, we can extend it to (X, Y), creating
a forward-only path of length N, completing the proof.


"""

import fileinput
from string import maketrans

def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print 'Case #%r: %s' % (i, s)

def solve(problem):
    X, Y = problem
    if X == Y == 0:
        return ''
    X, Y, denormalize = normalize(X, Y)
    xy_dist = X + Y
    N = find_int_by_bisection(S, 0, xy_dist, xy_dist)
    # are we exactly on the band for N?
    if xy_dist == S(N):
        return denormalize(forward_path_with_optional_reversal(X, N))
    # advance to next outer band until it's an even distance from (X, Y)
    while True:
        N += 1
        diff = S(N) - xy_dist
        if diff % 2 == 0:
            break
    # make a forward path to the band and reverse a step to reach (X, Y)
    path = forward_path_with_optional_reversal(X + diff, N, diff // 2)
    return denormalize(path)

def forward_path_with_optional_reversal(x, n, reversal_size=0):
    # since x + y = S(n), y is determined by x and n
    x_steps = set()
    reversals = set()
    if reversal_size:
        assert reversal_size <= x
        for i in xrange(n, 0, -1):
            if i <= reversal_size:
                reversals.add(i)
                x -= i
                reversal_size -= i
    for i in xrange(n, 0, -1):
        if i <= x and i not in reversals:
            x_steps.add(i)
            x -= i
    assert x == 0
    def step(i):
        if i in reversals:
            return 'W'
        return 'E' if i in x_steps else 'N'
    return ''.join(step(i) for i in xrange(1, n + 1))

def normalize(x, y):
    denormalizers = []
    if x < 0:
        x = -x
        denormalizers.append(maketrans('EW', 'WE'))
    if y < 0:
        y = -y
        denormalizers.append(maketrans('NS', 'SN'))
    if x < y:
        x, y = y, x
        denormalizers.append(maketrans('NSEW', 'EWNS'))
    def denormalize(path):
        for transform in reversed(denormalizers):
            path = path.translate(transform)
        return path
    return x, y, denormalize

def S(n):
    """Compute the sum 1, 2, ... n."""
    return n * (n + 1) // 2  # Gauss's formula

def read_problems(lines):
    T = int(lines.next())
    for _ in xrange(T):
        yield read_problem(lines)

def read_problem(lines):
    X, Y = read_ints(lines)
    return X, Y

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
