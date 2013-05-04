#!/usr/bin/python
#
# Tom Moertel <tom@moertel.com>
# 2013-05-04


"""Solution to "Osmos" Code Jam problem
https://code.google.com/codejam/contest/2434486/dashboard

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
    A, N, sizes = problem
    sizes = sorted(sizes)
    @memoize
    def cost(my_size, i):
        while i < N and sizes[i] < my_size:
            my_size += sizes[i]
            i += 1
        if i >= N:
            return 0
        if my_size > 1:
            insert_cost = 1 + cost(2 * my_size - 1, i)
            if insert_cost == 1:
                return insert_cost  # strictly dominates skip option
        skip_cost = 1 + cost(my_size, i + 1)
        return skip_cost if my_size == 1 else min(skip_cost, insert_cost)
    return cost(A, 0)

def read_problems(lines):
    T = int(lines.next())
    for _ in xrange(T):
        yield read_problem(lines)

def read_problem(lines):
    A, N = read_ints(lines)
    sizes = read_ints(lines)
    return A, N, sizes

def read_ints(lines):
    return [int(s) for s in lines.next().split()]

if __name__ == '__main__':
    main()
