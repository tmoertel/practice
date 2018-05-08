#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2018-05-07

"""Solution to "Slides!" Code Jam problem
https://code.google.com/codejam/contest/4314486/dashboard#s=p1

"""

import fileinput

def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print('Case #%r: %s' % (i, s))

def solve(problem):
    buildings, needed_paths = problem
    weight = 1 if buildings < 3 else 1 << (buildings - 3)
    taps = ['0'] * buildings
    for building in range(1, buildings):
        if weight <= needed_paths:
            taps[building] = '1'
            needed_paths -= weight
        weight = (weight + 1) >> 1
    if needed_paths > 0:
        return 'IMPOSSIBLE'
    def has_edge(i, j):
        if i == 0:
            return taps[j]
        return '1' if i < j else '0'
    adj_matrix = [[has_edge(i, j) for j in range(buildings)]
                  for i in range(buildings)]
    return 'POSSIBLE\n' + '\n'.join(''.join(row) for row in adj_matrix)

def read_problems(lines):
    T = int(lines.next())
    for _ in range(T):
        yield read_problem(lines)

def read_problem(lines):
    B, M = read_ints(lines)
    return B, M

def read_ints(lines):
    return [int(s) for s in lines.next().split()]

if __name__ == '__main__':
    main()
