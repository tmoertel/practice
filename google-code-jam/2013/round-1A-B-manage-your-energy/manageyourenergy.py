#!/usr/bin/python
#
# Tom Moertel <tom@moertel.com>
# 2013-04-26


"""Solution to "Manage Your Energy" Code Jam problem
http://code.google.com/codejam/contest/2418487/dashboard#s=p1

Claim: If for problem size k - 1 we know (1) the maximum gain g_{k-1},
(2) how much energy e is available afterward (including recharge), and
also (3) how much input slack s_i remains in each previous activity i
< k, we can extend the solution to size k by filling k's input slack
s_k = E - e to the maximum extent possible with energy taken from the
least-valuable activities i < k for which v_i < v_k and for which all
the activities j in between have non-zero slacks to allow for energy
transfer. We call such a transfer a "trade." Each bit transferred from
i, however, reduces the available slack in activities j, until one of
the slacks s_j reaches 0, sealing off all activities < j from
participation in future trades.

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
    earliest_slack = 0
    e = E
    for i, v in enumerate(vs):
        slacks.append(E - e)
        while e < E and trades and trades[0][0] <= v:
            v1, i1, e1 = heapq.heappop(trades)
            if i1 + 1 < earliest_slack:
                continue  # no slack between i1 and i: i1 is sealed off
            slack = min(slacks[i1 + 1:])
            if not slack:
                continue  # remove trade since it's unusable
            e_transferred = min(E - e, e1, slack)
            e += e_transferred
            gain -= v1 * e_transferred
            for j in xrange(i1 + 1, i + 1):
                slacks[j] -= e_transferred
                if slacks[j] == 0:
                    earliest_slack = j + 1
            if e_transferred < e1 and i1 + 1 >= earliest_slack:
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
