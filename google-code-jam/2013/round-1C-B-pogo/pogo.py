#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-05-12

"""Solution to "Pogo" Code Jam problem
https://code.google.com/codejam/contest/2437488/dashboard#s=p1

"""

import collections
import fileinput

def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print 'Case #%r: %s' % (i, s)

def solve(problem):
    X, Y = problem
    # breadth-first search
    visited = set()
    frontier = collections.deque([(0, 0, 1, None)])
    def schedule(x, y, step, path):
        if (x, y, step) not in visited:
            visited.add((x, y, step))
            frontier.append((x, y, step, path))
    schedule(0, 0, 1, None)
    while frontier:
        x, y, step, path = frontier.popleft()
        if (x, y) == (X, Y):
            break  # found solution
        path = ((x, y), path)
        for x1, y1 in ((x, y-step), (x, y+step), (x-step, y), (x+step, y)):
            schedule(x1, y1, step+1, path)
    # backtrack along the solution path to get the directions
    def unwind(path):
        px, py = X, Y
        while path is not None:
            (x, y), path = path
            if x < px:
                d = 'E'
            elif x > px:
                d = 'W'
            elif y < py:
                d = 'N'
            else:
                d = 'S'
            yield d
            px, py = x, y
    return ''.join(reversed(list(unwind(path))))

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
