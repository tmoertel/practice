#!/usr/bin/python
#
# Tom Moertel <tom@moertel.com>
# 2013-04-13


"""Solution to "Lawnmower" Code Jam problem
https://code.google.com/codejam/contest/2270488/dashboard#s=p1

"""

import fileinput

def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print 'Case #%r: %s' % (i, s)

def solve(problem):
    N, M, heights = problem
    return 'YES' if is_mowable_pattern(N, M, heights) else 'NO'

def is_mowable_pattern(N, M, heights):
    while True:
        lowest = min(min(row) for row in heights)
        for _ in xrange(2):
            heights = [row for row in heights if max(row) != lowest]
            if len(heights) == 0:
                return True
            heights = zip(*heights)  # transpose
        N1, M1 = len(heights), len(heights[0])
        if (N1, M1) == (N, M):
            return False
        N, M = N1, M1

def read_problems(lines):
    T = int(lines.next())
    for _ in xrange(T):
        yield read_problem(lines)

def read_problem(lines):
    N, M = read_ints(lines)
    heights = [read_ints(lines) for _ in xrange(N)]
    return N, M, heights

def read_ints(lines):
    return [int(s) for s in lines.next().split()]

if __name__ == '__main__':
    main()
