#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-05-12

"""Solution to "The Great Wall" Code Jam problem
https://code.google.com/codejam/contest/2437488/dashboard#s=p2

"""

import fileinput

def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print 'Case #%r: %r' % (i, s)

def solve(problem):
    tribes = problem
    soln = None
    return soln

def read_problems(lines):
    T = int(lines.next())
    for _ in xrange(T):
        yield read_problem(lines)

def read_problem(lines):
    N = read_ints(lines)
    tribes = []
    for _ in xrange(N):
        tribe = d, n, w, e, s, delta_d, delta_p, delta_s = read_ints(lines)
        tribes.append(tribe)
    return tribes

def read_ints(lines):
    return [int(s) for s in lines.next().split()]

if __name__ == '__main__':
    main()
