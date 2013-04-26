#!/usr/bin/python
#
# Tom Moertel <tom@moertel.com>
# 2013-04-26


"""Solution to "Password Problem" Code Jam problem
http://code.google.com/codejam/contest/1645485/dashboard

"""

import fileinput


def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print 'Case #%r: %r' % (i, s)

def solve(problem):
    A, B, ps = problem

    # compute cumulative probabilities Ps[i] = product(ps[:i])
    Ps = [1.0]
    for p in ps:
        Ps.append(Ps[-1] * p)

    # use them to compute the cost of "keep going" from position i
    def e_keep_going(i):
        return -Ps[i] * (B + 1) + 2 * B - i + 2

    # find the best strategy
    min_e_press_enter = 1 + B + 1
    min_e_backspace = min(e_keep_going(i) + A - i for i in xrange(A))
    return min(e_keep_going(A), min_e_press_enter, min_e_backspace)

def read_problems(lines):
    T = int(lines.next())
    for _ in xrange(T):
        yield read_problem(lines)

def read_problem(lines):
    A, B = read_ints(lines)
    ps = [float(s) for s in lines.next().split()]
    return A, B, ps

def read_ints(lines):
    return [int(s) for s in lines.next().split()]

if __name__ == '__main__':
    main()
