#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-09-15

"""Solution to "Many Prizes" Code Jam problem
https://code.google.com/codejam/contest/2442487/dashboard#s=p1


Discussion
==========

It is evident that the outcomes of earlier rounds dominate later
rounds in the final rankings.  In effect, a team's series of wins and
losses can be seen as a binary number having one digit for every round
in the tournament, with W=0 and L=1.  Thus a team's final (0-based)
position in the tournament rankings is given by its corresponding
win-loss number.

Seen this way, it becomes clear that a team's best ranking occurs when
it manages to get as many early wins as possible -- in effect, forcing
as many leading digits to be zero as possible.  Since a win can only
occur when there is a higher-numbered team to play against, the best
tournament ordering (for our team) is that which places our team into
early sub-tournaments with as many higher-numbered teams as possible.

That is, at every round, we want a higher-numbered team to play
against, assuring a win, and then we want to preserve as co-winners as
many of the remaining higher-numbered teams as possible, assuring wins
in the next rounds.  This we can do by pairing the remaining
higher-numbered teams off with each other to the greatest extent
possible, assuring that half of them so paired will win and join us in
the next round.  (If we paired them instead with teams having numbers
less than ours, all so paired would lose, and on the next round our
team would find fewer opponents it could win against.)

Following this strategy every round leads to a linear-time recursive
algorithm to compute a team's best possible ranking in an N-round
tournament, given w, the number of remaining teams it can win against
(i.e., those with higher team numbers):

    best_rank(0, 0) = 0
    best_rank(N, 0) = 1 * 2^(N-1) + best_rank(N-1, 0) = 2^N - 1
    best_rank(N, w) = 0 * 2^(N-1) + best_rank(N-1, (w-1)//2)

Note that this ranking is 0 based: the first-place team has a position
of 0 in the rankings.

Now let's consider the worst-case ranking.  Instead of wanting wins
early and often, we want losses early and often, leading 1 digits
instead of leading 0 digits.  Thus we can construct a dual algorithm
in terms of l, the number of remaining teams we can lose against.
But since l = i, we can just go ahead and use team number i directly:

    worst_rank(0, 0) = 0
    worst_rank(N, 0) = 0 * 2^(N-1) + worst_rank(N-1, 0) = 0
    worst_rank(N, i) = 1 * 2^(N-1) + worst_rank(N-1, (i-1)//2)

By comparing the dual algorithms, we can see that worst_rank(N, i) is
the one's complement of best_rank(N, i) and vice versa:

    worst_rank(N, i) = (2^N - 1) - best_rank(N, i)
    best_rank(N, w)  = (2^N - 1) - worst_rank(N, w)

Thus we need implement only one of the algorithms.

Now let us return to the original problem.  We are asked to find the
largest-numbered team that is guaranteed to win a prize, and the
largest-numbered team that could win a prize.  That is, we want
Y and Z, where

    Y = max { i | worst_rank(N, i) <= P - 1 },
    Z = max { i | best_rank(N, i)  <= P - 1 }.

Since i = 0..2^N-1 for N as large a 50, we need some way to speed the
search for the maximum i that satisfies the test.  Fortunately,
best_rank and worst_rank are both nondecreasing functions of i (see
proofs below) and we can use a bisection search to find Y and Z.  Each
search takes O(log N) calls to the appropriate ranking function, for
an overall run time of O(N log N) for each solution. This is fast
enough to solve the "large" problem set almost instantly.

But can we go farther?

Looking at the worst_rank algorithm, it is clear that its output will
always be an N-bit number with the leading bits all ones and the
remaining bits all zeroes.  Thus there are only N+1 possible distinct
worst-case ranks to assign to the 2^N values of team number:

    j  W(j)
   --- ----------------
    0  W(0) = 000...000
    1  W(1) = 100...000
    2  W(2) = 110...000
    3  W(3) = 111...000
   ...     ...
    N  W(N) = 111...111
   --- ----------------

Given a rank W(j), which team numbers i will worst_rank map to it?
Look again at the recursive algorithm:

    worst_rank(N, 0) = 0
    worst_rank(N, i) = 2^(N-1) + worst_rank(N-1, (i-1)//2)

It is apparent from the base case that only team number i = 0 can
achieve W(0) = 0.

Now let's consider W(1).  If that's the final ranking, the algorithm
had to have recursed once and only once.  Therefore, the algorithm
must have hit the base case i = 0 after this single recursive call.
So, before that single call, what values could i have had?  To answer
this question, let's look at the mapping for i in the recursive call:

    i  :->  (i - 1) // 2

Can we reverse this mapping?  First, let's undo the floor division:

    2*i + C  :->  i - 1    where C is in {0, 1}

And, next, let's undo the subtraction by one:

    2*i + 1 + C  :->  i    where C is in {0, 1}

Therefore, if i = 0 in the final iteration of the recursive algorithm,
i had to have been 1 or 2 in the previous iteration.  Since the
original problem asks for the largest team number that could achieve a
given ranking, we can fix C to its largest possible value 1, and
iterate in this way, backward from i = 0 up to the largest i for which
the corresponding W(j) <= P - 1.  This gives us a linear-time
algorithm to find the highest-numbered team i that can receive one of
P prizes in a tournament of N rounds, given worst-case conditions.

A similar approach works for the best-case conditions, but here we are
iterating on w, and since smaller w values correspond to larger i
values (recall that w = 2^N - 1 - i), we use C = 0 for the reverse
mapping to minimize w and, consequently, maximize i.


Proofs
======

A. Best-case rank is a nondecreasing function of team number.

We proceed by contradiction.  Let I be team i's lowest possible rank.
Now assume that with a certain tournament list a higher-numbered team
j > i is able to achieve a lower rank of J < I.  If we swap i and j in
this list, team i will win every game that j would have won (since i <
j) and achieve a rank no greater than J.  But J < I, which means that
team i would, under this swapped list, achieve a lower rank than its
lowest possible rank, which is a contradiction.  Therefore, no list
exists that allows a higher-numbered team to achieve a lower best-case
rank than a lower-numbered team, and it follows that best-case rank is
a nondecreasing function of team number.

B. Worst-case rank is a nondecreasing function of team number.

This proof is the dual to the proof above.  Replace win with lose,
better with worse, higher with lower, greater than with less than, and
so on, and the same conclusion follows.

Another proof option is to use the one's complement relationship.  For
a given team number i we have its worst-case rank given by

    worst_rank(N, i) = (2^N - 1) - best_rank(N, i)

Thus, worst_rank varies with its second argument in the opposite
direction as best_rank.  And we know from our earlier proof that
best_rank(N, w = 2^N - 1 - i) is nondecreasing with team number i and
hence nonincreasing with w, its second argument, which appears with
the opposite sign.  Therefore, worst_rank is nondecreasing with *its*
second argument, which is team number.  Therefore, worst-case rank is
a nondecreasing function of team number.


Note on Google's Contest Analysis
=================================

In Google's contest analysis, the following sample code is offered
as a solution:

    def LowRankCanWin(N, P):
      matches_won = 0
      size_of_group = 2 ** N
      while size_of_group > P:
        matches_won += 1
        size_of_group /= 2
      return 2 ** N - 2 ** matches_won

    def ManyPrizes(N, P):
      print 2 ** N - LowRankCanWin(N, 2 ** N - P) - 2, LowRankCanWin(N, P)

But this logic will produce erroneous results.  For example, in a
tournament of N = 3 rounds, if P = 8 prizes are awarded, every one of
the 2^N = 8 teams will get a prize.  Thus the correct answer for
ManyPrizes(3, 8) should be (7, 7).  The sample code, however, produces
the following:

    >>> ManyPrizes(3, 8)
    14 7

"""

import fileinput

def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print 'Case #%r: %s' % (i, s)


# O(N) time solution

def solve(problem):
    N, P = problem
    Y = max_team_worst_case(N, P)
    Z = max_team_best_case(N, P)
    return '{} {}'.format(Y, Z)

def max_team_worst_case(N, P):
    n = N
    i = 0
    W = 1 << (N - 1)
    while n and P > W:
        W |= W >> 1
        i = 2*i + 2  # to maximize i, use max C = 1
        n -= 1
    return min(i, (1 << N) - 1)

def max_team_best_case(N, P):
    n = N
    W = (1 << N) - 1
    w = 0
    while n and W >= P:
        W >>= 1
        w = 2*w + 1  # to maximize i, minimize w, and so use min C = 0
        n -= 1
    i = (1 << N) - 1 - w
    return i


# O(N log N) time solution

def solve_O_N_log_N(problem):
    N, P = problem
    n_teams = 1 << N
    def worst(i):
        return worst_rank(N, i)
    def best(i):
        return n_teams - 1 - worst(n_teams - 1 - i)
    Y = find_int_by_bisection(worst, 0, n_teams - 1, P - 1)
    Z = find_int_by_bisection(best, 0, n_teams - 1, P - 1)
    return '{} {}'.format(Y, Z)

def worst_rank(N, l, pos=0):
    """Find worst possible N-round ranking when l teams have lower numbers."""
    if l == 0:
        # we're the lowest numbered and must take wins for remaining rounds
        return pos << N
    else:
        # otherwise, we can play a lower-numbered team to force a loss
        return worst_rank(N - 1, (l - 1) // 2, (pos << 1) | 1)

def find_int_by_bisection(f, lo, hi, y):
    while lo < hi:
        mid = lo + ((hi - lo) >> 1)
        if f(mid) <= y:
            lo = mid + 1
        else:
            hi = mid - 1
    return lo if f(lo) <= y else lo - 1

def read_problems(lines):
    T = int(lines.next())
    for _ in xrange(T):
        yield read_problem(lines)

def read_problem(lines):
    N, P = read_ints(lines)
    return N, P

def read_ints(lines):
    return [int(s) for s in lines.next().split()]

if __name__ == '__main__':
    main()
