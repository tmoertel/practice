#!/usr/bin/python
#
# Tom Moertel <tom@moertel.com>
# 2013-03-31
#
# Solution to "Store Credit" problem:
# http://code.google.com/codejam/contest/351101/dashboard#s=p0


import fileinput


def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        j1, j2 = solve(p)
        print 'Case #%r: %r %r' % (i, j1, j2)


def solve(problem):
    C, _, Ps = problem
    seen = {}
    for i, p in enumerate(Ps, 1):
        try:
            return seen[C - p], i
        except KeyError:
            seen[p] = i


def read_problems(lines):
    N = int(lines.next())
    for _ in xrange(N):
        yield read_problem(lines)


def read_problem(lines):
    C = int(lines.next())
    I = int(lines.next())
    Ps = map(int, lines.next().split())
    return C, I, Ps


if __name__ == '__main__':
    main()
