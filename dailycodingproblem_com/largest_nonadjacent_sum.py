#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Solve interview problem: largest sum of non-adjacent numbers.

* Problem

This problem comes from Daily Coding Problem on 2019-04-02 and was
classified as Hard difficulty:

  Reported source: Airbnb.

  Write a function that, given a sequence of integers, returns the
  greatest sum of non-adjacent values. Values can be 0 or negative.

  For example, given [2, 3, 7, 1, 5], the function should return 14,
  since the best it can pick is 2, 7, and 5. Given [6, 2, 3, 5], the
  function should return 11, since it can pick no better than 6 and 5.

  Follow-up: Can you do this in O(N) time and constant space?


* Solution

It helps to consider small cases in order to build intuition about
the problem.

If soln(X) is the solution for the sequence of numbers X, what should
it give us when X = [] (the empty sequence)? Although the problem
statement doesn't tell us, I'd suggest that 0 is the least-surprising
answer. That's because our intuition is that if you're asked for the
sum of dollar bills in your wallet, and your wallet is empty, you
naturally say that you have zero dollars.

What about soln([x]) for some value x? Again, the problem statement
doesn't give a clear answer for this case. That is, it's not clear
what the "non-adjacent" requirement implies when X contains a single
number, since there are no adjacent numbers. It could be that the
problem statement is literally saying that the sums in question must
be over non-adjacent numbers and, because [x] contains only a single
number that cannot participate in a non-adjacency relation with any
other number in X, there is no legal sum for this case. But I suspect
that what the interviewer actually wants is the largest sum over any
of X's numbers, provided that no two numbers in the sum are adjacent
in X. (In a real interview, I'd ask the interviewer a question about
this point and offer my suggested interpretation to clarify our shared
understanding of the problem.)

With this clarification in place, then, soln([x]) is clearly x.

Or is it? What if x is negative? At this point, I'd suggest to the
interviewer that a better sum might be zero, under the policy that
when we choose the numbers in X to sum over, one of the sensible
options is to choose none of the numbers.

To support this suggestion, I would argue that this is the policy that
underlies many real-world optimization problems. For example, imagine
that X contained the expected returns on a series of possible trades
that an investment firm could choose to make, and trading restrictions
prevented the firm from participating in two trades in a row. If it
turned out that all of the possible trades were expected to lose
money, the firm would naturally choose to participate in none of them,
for an expected total return of zero, which is preferable to a loss.

Having considered the smaller cases, now let's think about arbitrarily
large cases. Say we know the optimal value for soln(X) for some large
sequence X. If we consider just the final element in X -- let's call
it x -- there are two possibilities:

  (1) x does not participate in the sum
  (2) x does participate in the sum

If x does not participate in the sum, then soln(X) must be the same as
soln(X[:-1]). (Here I'm using Python slicing notation. X[:-1] denotes
all of the elements in X except for the last.)

If x participates in the sum, it can only be because the element
before x does not; otherwise, we would have violated the non-adjacency
requirement. Therefore, we can infer that soln(X) = soln(X[:-2]) + x.

Since soln(X) by definition gives the largest sum, we know that the
largest of possibilities (1) and (2) was chosen. This fact, plus the
base cases we discussed earlier, gives a recurrence for soln(X):

  soln(X) | x is empty = 0
          | otherwise  = max(soln(X[:-2]) + x, soln(X[:-1]))

And this recurrence is the basis for our Python implementations.


** Implementations.

For our Python implementations, I start with a straight translation of
the recurrence into a recursive function. One optimization I'll
perform is to eliminate the expensive list slices by passing not the
sequence X into the recursive function but instead the index i
indicating the slice within X that we are currently operating on.

Nevertheless, this solution is pretty inefficient, having a run-time
cost recurrence of

  T(n) = T(n - 1) + T(n - 2) + O(1),

which grows faster than the Fibonacci series.

My second implementation uses dynamic programming and is much more
efficient. We start with the base case of soln([]) = 0 and use the
recurrence to build up from there to the full input X, one element at
a time. This implementation satisfies the follow-up challenge from the
problem statement: it runs in linear time and constant space
w.r.t. the length of the input sequence X.

"""


def largest_nonadjacent_sum_recursive(X):
    def soln(i):
        if i < 0:
            return 0
        return max(X[i] + soln(i - 2), soln(i - 1))

    return soln(len(X) - 1)


def largest_nonadjacent_sum_dp(X):
    max_sum = max_sum_lag_1 = max_sum_lag_2 = 0
    for x in X:
        max_sum = max(x + max_sum_lag_2, max_sum_lag_1)
        max_sum_lag_2 = max_sum_lag_1
        max_sum_lag_1 = max_sum
    return max_sum


def test():
    for soln in largest_nonadjacent_sum_recursive, largest_nonadjacent_sum_dp:
        assert soln([]) == 0
        assert soln([-3]) == 0
        assert soln([3]) == 3
        assert soln([2, 4, 6, 2, 5]) == 13
        assert soln([5, 1, 1, 5]) == 10
        assert soln([5, 1, -10, 1, 5]) == 10
