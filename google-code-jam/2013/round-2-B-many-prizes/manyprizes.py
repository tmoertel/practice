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

Thus we need to implement only one of the algorithms.

Now let us return to the original problem.  We are asked to find the
largest-numbered team that is guaranteed to win a prize, and the
largest-numbered team that could win a prize.  That is, we want
Y and Z, where

    Y = max { i | worst_rank(N, i) <= P - 1 },
    Z = max { i | best_rank(N, i)  <= P - 1 }.

Since i = 0..2^N-1 for N as large a 50, we need some way to speed the
search for the maximum i that satisfies the test.  Fortunately,
best_rank and worst_rank are both nondecreasing functions of i (see
proofs below) and we can use a binary search to find Y and Z.  Each
search takes O(log 2^N) = O(N) calls to the appropriate ranking
function, and the ranking functions take O(N) time, giving an overall
run time of O(N^2) for each solution.  This is fast enough to solve
the "large" problem set almost instantly since N <= 50.


But can we go farther?
======================

Looking at the worst_rank algorithm, it is clear that its output will
always be an N-bit number with the leading bits all ones and the
remaining bits all zeroes.  Thus there are only N+1 possible distinct
worst-case ranks W(j) to assign to the 2^N values of team number:

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
given ranking, we can fix C to its largest possible value of 1 and
declare the solution to be 2.  Iteratively applying this logic lets us
compute the largest team numbers to have final rankings W(2), W(3),
and so on.

This gives us a simple, linear-time algorithm to solve the original
problem for the worst-case scenario.  Start with i = j = 0 and update
j := j + 1 and i := 2*i + 2 while W(j) <= P.  The final value of i is
the solution.

As a refinement, we could note that for any value of j, the
corresponding value of i is going to be given by the linear recurrence

    i[j] = 2 * i[j-1] + 2,

where i[0] = 0.  Solving for a closed form gives us the following
formula,

    i(j) = 2^(j+1) - 2,

which lets us remove i from the iterations.  Now we can just find the
maximum j such that W(j) <= P and then return i(j) as the solution.
The only wrinkle is that if P = 2^N, j will run all the way up to N,
and i(N) = 2^(N+1) - 2, which is greater than the maximum team number
2^N - 1.  So we must handle j = N as a special case: i(N) = 2^N - 1.

As before, we can get a best-case algorithm from the worst-case
algorithm -- or vice versa -- by appealing to fact that every
best-case scenario has a worst-case dual (see Proof C).  Of the two,
I chose to implement the best-case algorithm because its closed form
solution for i(j) is 2^j - 1 (because C = 0) and thus never exceeds
the maximum team number 2^N - 1.  This eliminates the need to test
for the special case j = N.


Proofs
======

A. Best-case rank is a nondecreasing function of team number.

Let an arbitrary team j's lowest possible rank be J.  Now take an
arbitrary team i < j.  If team i plays under the tournament list that
allowed team j to achieve rank J, it will win every game that j had
won (and possibly more) and achieve a ranking no worse than J.  Thus J
is the worst that team i's best-case rank I could possibly be.  Since
i and j were chosen arbitrarily, we have established that i < j
implies I <= J, and therefore that best-case rank is a nondecreasing
function of team number.


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

C.  Duality of best- and worst-case maximal prize-winning teams

Let there be a tournament of N rounds and let T = 2^N be the total
number of teams.  If BC(P) and WC(P) give the highest-numbered teams
that can win one of P prizes under best- and worst-case conditions,
respectively, then

    BC(P) = T - WC(T - P) - 2, and           (1)
    WC(P) = T - BC(T - P) - 2.               (2)

Proof.  First, we introduce c(t), the one's complement function that
maps the range of team numbers, 0..T-1, onto itself, mapping 0 <=>
T-1, 1 <=> T-2, and so on:

    c(t) = T - t - 1

Note that c is an involution, i.e., its own inverse: c(c(t)) = t.

Also note that if i < j, c(i) > c(j).  Thus, under the tournament
rules, any game played between i and j will have its outcome reversed
if the same teams play again under their complementary numbers.

Now let i = BC(P) be the highest-numbered team to win a prize under
best-case conditions.  If we take the tournament list that led to this
outcome and replay it with every team t renumbered as its complement
c(t), every win will become a loss and vice versa.  The P teams that
had done the best will now do the worst.  Therefore, if we award T - P
prizes, none of the P teams that had originally won a prize will win
one now.  Therefore, under these now worst-case conditions for the
original team i, we know that the team must not only be prizeless but
that its number in the new tournament, c(i), must be the lowest
non-prize-winning team number.  Consequently, c(i) - 1 must be the
highest prize-winning number, and we have

    WC(T - P) = c(i) - 1
              = c(BC(P)) - 1
              = (T - BC(P) - 1) - 1
              = T - BC(P) - 2

Solving for BC(P), we complete our proof for equation (1):

    BC(P) = T - WC(T - P) - 2.

Since (1) holds for any P such that 0 <= P <= T, the proof of (2)
follows immediately from substituting P :-> T - P into equation (1)
and solving for WC(P).

And that completes our proof.


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

But this logic will produce erroneous results when P = 2^N.  For
example, in a tournament of N = 3 rounds, if P = 8 prizes are awarded,
every one of the 2^N = 8 teams will get a prize.  Thus the correct
answer for ManyPrizes(3, 8) should be (7, 7).  The sample code,
however, produces the following:

    >>> ManyPrizes(3, 8)
    14 7

The problem is that LowRankCanWin doesn't work properly when P = 0.
While P = 0 is ruled out as a legal input value, P = 2^N is not.  And
when ManyPrizes is called with P = 2^N, it calls LowRankCanWin with
the dual value of P = 0.

Therefore, if we're going to use duality to avoid implementing one of
the solvers, the solver we do implement must handle P = 0 properly.

So what should the result be for P = 0?  The dual formulas from Proof
C give us the answer.  Instead of finding BC(0), we can instead find
the equivalent and well-defined 2^N - WC(2^N) - 2.  Since WC(2^N) is
obviously 2^N - 1, we have our answer: BC(0) = -1.

Thus we can fix the sample code by inserting the following test into
LowRankCanWin:

    def LowRankCanWin(N, P):
      if P == 0:
        return -1
      # rest of code as before

"""

import fileinput

def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print('Case #%r: %s' % (i, s))


# O(N) time solution

def solve(problem):
    N, P = problem
    n_teams = 1 << N
    Y = n_teams - 2 - max_team_best_case(N, n_teams - P)
    Z = max_team_best_case(N, P)
    return '{} {}'.format(Y, Z)

def max_team_best_case(N, P):
    if P == 0:  # need to handle this case because it's dual to P == 2^N
        return -1
    j = longest_initial_winning_streak(N, P)
    return (1 << N) - (1 << j)

def longest_initial_winning_streak(N, P):
    k = 0
    W = 1
    while W < P:
        W = (W << 1) | 1
        k += 1
    return N - k


# O(N^2) time solution

def solve_ON2(problem):
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

# helpers

def read_problems(lines):
    T = int(next(lines))
    for _ in range(T):
        yield read_problem(lines)

def read_problem(lines):
    N, P = read_ints(lines)
    return N, P

def read_ints(lines):
    return [int(s) for s in lines.next().split()]

if __name__ == '__main__':
    main()
