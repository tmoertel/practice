#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-06-05

"""Solution to "Number Sets" Code Jam problem
https://code.google.com/codejam/contest/32017/dashboard#s=p1&a=0

The key to solving this problem is that the size of the interval is
limited to 10^6, which (by Claim 1, below) limits the largest factor
we must consider and correspondingly allows us to precompute a table
of eligible prime factors that we can reuse for all tests.  Then for
each test's P, A, B values we can take each prime p : P <= p <= B - A
and step over the multiples of p between A and B and take the union of
all sets we encounter.  A standard disjoint-set data structure makes
the unions fast.  And that's basically the algorithm.

Claim 1.  On the closed interval [A, B], no two integers i < j can
share a factor greater than B - A.  Proof: If i < j share a prime
factor p, then there must be some multiple of p between them.
Therefore, they must be separated by at least p.  Since no two points
on the interval can be separated by more than B - A, p can be no
greater.

"""

from bisect import bisect_left, bisect_right
import fileinput


def main():
    primes = prime_sieve(10**6)
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p, primes)
        print("Case #%r: %r" % (i, s))


def solve(problem, primes):
    A, B, P = problem
    union, find = mk_union_find_domain(range(A, B + 1))
    for i in range(bisect_left(primes, P), bisect_right(primes, B - A + 1)):
        p = primes[i]
        start = (A // p) * p
        if start < A:
            start += p
        for i in range(start + p, B + 1, p):
            union(i, start)
    return len(set(find(i) for i in range(A, B + 1)))


def read_problems(lines):
    T = int(next(lines))
    for _ in range(T):
        yield read_problem(lines)


def read_problem(lines):
    A, B, P = read_ints(lines)
    return A, B, P


def read_ints(lines):
    return [int(s) for s in lines.next().split()]


# number theory


def prime_sieve(n):
    """Get an increasing list of all primes <= n."""
    candidates = [True] * (n + 1)
    primes = []
    for i in range(2, n + 1):
        if candidates[i]:
            primes.append(i)
            for j in range(i + i, n + 1, i):
                candidates[j] = False
    return primes


# disjoint sets


def mk_union_find_domain(elems):
    """Make union and find methods over disjoint singleton sets from elems."""
    d = dict((e, e) for e in elems)
    r = dict((e, 1) for e in elems)

    def union(u, v):
        urep = find(u)
        vrep = find(v)
        if urep != vrep:
            rank_diff = r[urep] - r[vrep]
            if rank_diff < 0:
                d[urep] = vrep
            else:
                d[vrep] = urep
                if rank_diff == 0:
                    r[urep] += 1

    def find(u):
        urep = d[u]
        if urep != u:
            urep = d[u] = find(urep)
        return urep

    return union, find


if __name__ == "__main__":
    main()
