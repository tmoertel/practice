#!/usr/bin/python
#
# Tom Moertel <tom@moertel.com>
# 2013-03-31
#
# Solution to "Reverse Words" problem:
# http://code.google.com/codejam/contest/351101/dashboard#s=p1

import fileinput


def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print 'Case #%r: %s' % (i, s)


def solve(problem):
    words = problem
    return ' '.join(reversed(words))


def read_problems(lines):
    N = int(lines.next())
    for _ in xrange(N):
        yield read_problem(lines)


def read_problem(lines):
    spec = lines.next()
    return spec.split()


if __name__ == '__main__':
    main()
