#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-05-12

"""Solution to "Consonants" Code Jam problem
https://code.google.com/codejam/contest/2437488/dashboard

"""

import fileinput

def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print 'Case #%r: %r' % (i, s)

def solve(problem):
    name, n = problem
    soln = None  # compute n-value
    return soln

def read_problems(lines):
    T = int(lines.next())
    for _ in xrange(T):
        yield read_problem(lines)

def read_problem(lines):
    name, strn = lines.next().split()
    n = int(strn)
    return name, n

def read_ints(lines):
    return [int(s) for s in lines.next().split()]

if __name__ == '__main__':
    main()
