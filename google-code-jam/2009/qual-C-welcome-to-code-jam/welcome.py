#!/usr/bin/python
#
# Tom Moertel <tom@moertel.com>
# 2013-04-02


"""Solution to "Welcome to Code Jam" problem
http://code.google.com/codejam/contest/90101/dashboard#s=p2

"""

import fileinput
import functools
import sys


TARGET = "welcome to code jam"


def main():
    sys.setrecursionlimit(30 * 500)
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        n = solve(TARGET, p)
        print("Case #%r: %s" % (i, ("%04d" % n)[-4:]))


def solve(t, s, i=0, j=0):
    """Count sub-sequences of t[i:] in s[j:]."""
    I = len(t)
    J = len(s)

    @memoize
    def go(i, j):
        if i == I:
            return 1
        if j == J:
            return 0
        return go(i, j + 1) + (go(i + 1, j + 1) if t[i] == s[j] else 0)

    return go(i, j)


def memoize(f):
    cache = {}

    @functools.wraps(f)
    def g(*args):
        try:
            return cache[args]
        except KeyError:
            r = f(*args)
            cache[args] = r
            return r

    return g


def read_problems(lines):
    N = int(next(lines))
    for _ in range(N):
        yield read_problem(lines)


def read_problem(lines):
    return lines.next().strip()


if __name__ == "__main__":
    main()
