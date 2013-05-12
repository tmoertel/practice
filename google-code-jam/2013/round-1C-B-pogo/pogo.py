#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-05-12

"""Solution to "Pogo" Code Jam problem
https://code.google.com/codejam/contest/2437488/dashboard#s=p1

"""

import fileinput

def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print 'Case #%r: %r' % (i, s)

def solve(problem):
    # dynamic programming for making change?
    X, Y = problem
    soln = None  # IMPORTANT! OUTPUT FOR LARGE PROBLEM IS DIFFERENT !!!
    return soln

def read_problems(lines):
    T = int(lines.next())
    for _ in xrange(T):
        yield read_problem(lines)

def read_problem(lines):
    X, Y = read_ints(lines)
    return X, Y

def read_ints(lines):
    return [int(s) for s in lines.next().split()]

if __name__ == '__main__':
    main()
