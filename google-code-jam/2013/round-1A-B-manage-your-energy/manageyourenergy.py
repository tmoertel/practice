#!/usr/bin/python
#
# Tom Moertel <tom@moertel.com>
# 2013-04-26


"""Solution to "Manage Your Energy" Code Jam problem
http://code.google.com/codejam/contest/2418487/dashboard#s=p1

Claim: If for problem size k - 1 we know (1) the maximum gain g_{k-1},
(2) how much energy e is available afterward (including recharge), and
also (3) how much input slack s_i remains in each previous activity i
< k, we can extend the solution to size k by filling in k's input
slack to the maximum extent possible with energy obtained by spending
less on the least-valuable activities i < k with v_i < v_k and
transferring that energy to activity k through the input slack in the
activities between, reducing their slack by the amount transferred.

"""

import fileinput
import heapq


def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print 'Case #%r: %r' % (i, s)

def solve(problem):
    E, R, _N, vs = problem
    trades = []
    slacks = []
    gain = 0
    e = E
    for i, v in enumerate(vs):
        slacks.append(E - e)
        while e < E and trades and trades[0][0] <= v:
            v1, i1, e1 = heapq.heappop(trades)
            slack = min(slacks[i1 + 1:])
            if not slack:
                continue  # remove trade since it's unusable
            e_transferred = min(E - e, e1, slack)
            e += e_transferred
            gain -= v1 * e_transferred
            for j in xrange(i1 + 1, i + 1):
                slacks[j] -= e_transferred
            if e_transferred < e1:
                heapq.heappush(trades, (v1, i1, e1 - e_transferred))
        gain += v * e
        heapq.heappush(trades, (v, i, e))
        e = R
    return gain

def read_problems(lines):
    T = int(lines.next())
    for _ in xrange(T):
        yield read_problem(lines)

def read_problem(lines):
    E, R, N = read_ints(lines)
    vs = read_ints(lines)
    return E, R, N, vs

def read_ints(lines):
    return [int(s) for s in lines.next().split()]

if __name__ == '__main__':
    main()
