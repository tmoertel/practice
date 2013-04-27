#!/usr/bin/python
#
# Tom Moertel <tom@moertel.com>
# 2013-04-26


"""Solution to "Manage Your Energy" Code Jam problem
http://code.google.com/codejam/contest/2418487/dashboard#s=p1

"""

import fileinput
import functools


def memoize(fn):
    cache = dict()
    @functools.wraps(fn)
    def memoized_fn(*args):
        if args in cache:
            return cache[args]
        return cache.setdefault(args, fn(*args))
    return memoized_fn

def trace(fn):
    @functools.wraps(fn)
    def traced_fn(*args):
        try:
            res = fn(*args)
        except Exception as e:
            res = e
        print '%s%r => %r' % (fn.__name__, args, res)
        return res
    return traced_fn


def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print 'Case #%r: %r' % (i, s)

def solve(problem):
    E, R, N, vs = problem
    @memoize
    def max_gain(e, i):
        if i == N:
            return 0
        v = vs[i]
        return max(v * e_in + max_gain(min(E, e - e_in + R), i + 1)
                   for e_in in xrange(0, e + 1))
    return max_gain(E, 0)

def read_problems(lines):
    T = int(lines.next())
    for _ in xrange(T):
        yield read_problem(lines)

def read_problem(lines):
    E, R, N = read_ints(lines)
    vs = read_ints(lines)
    return E, R, N, vs

def read_ints(lines):
    return [int(s) for s in lines.next().split()]

if __name__ == '__main__':
    main()
