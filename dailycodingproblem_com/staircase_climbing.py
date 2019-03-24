#!/usr/bin/python

"""Solution to a problem about climbing a staircase.

* Problem

  (This problem comes from https://www.dailycodingproblem.com/.)

  There's a staircase with N steps, and you can climb 1 or 2 steps at
  a time. Given N, write a function that returns the number of unique
  ways you can climb the staircase. The order of the steps matters.

  For example, if N is 4, then there are 5 unique ways:

  1, 1, 1, 1
  2, 1, 1
  1, 2, 1
  1, 1, 2
  2, 2

  What if, instead of being able to climb 1 or 2 steps at a time, you
  could climb any number from a set of positive integers X? For
  example, if X = {1, 3, 5}, you could climb 1, 3, or 5 steps at a
  time. Generalize your function to take in X.


* Solution

Let's start by considering a simpler problem: What is the number of
distinct ways to climb a staircase of N stairs if we are allowed to
climb only j steps at a time? Let's say that ways(N) gives the answer.

Now let's consider the possibilities. If j > N, then ways(j) must be
zero since there are no ways to climb N steps: we'll always overshoot.
If j == N, then there's only one way: take one j-sized step and we're
done.  And if j < N, we can safely take a j-sized step, leaving N - j
steps to go, which is equivalent to our original staircase but with j
fewer steps, so by definition our answer must be ways(N - j).

These observations give us a recurrence and a base case, all we need
for a recursive solution:

    ways(N) | if j > N   = 0
            | if j == N  = 1
            | otherwise  = ways(N - j)

A useful simplification comes from realizing that we can subtract
j from both sides of the equality tests without changing anything:

  ways(N) | if 0 > N - j   = 0
          | if 0 == N - j  = 1
          | otherwise      = ways(N - j)

Then we can eliminate the need to subtract j from N in the equality
tests by taking advantage of the fact that the recursive call
subtracts j from N already, so recursing one additional time will let
us identify the same base cases:

  ways(N) | if 0 > N   = 0            # Zero ways to go backward.
          | if 0 == N  = 1            # One way to go zero steps.
          | otherwise  = ways(N - j)  # Reduce to equivalent smaller problem.

Now let's consider the more complex version of the problem in which
j may be drawn from a set of positive integers, which I'll call js.

In this more complex problem, the base cases are the same as
before. There are still no ways to go backward. There is still only
one way to go zero steps forward: take no steps, resulting in the
empty sequence of steps.

But the recursive case is more complex now because we can try going
forward j steps for all j in js. For each j, we have ways(N - j) more
distinct paths we can take; we just need to add up the possibilities.

Putting it all together, we arrive at the final recurrence:

  ways(N) | if 0 > N   = 0
          | if 0 == N  = 1
          | otherwise  = sum(ways(N - j) for j in js)

As a double-check of this recurrence, let's try it out with the
example instance of the problem, when N = 4 and js = {1, 2}.

N(4) = N(3) + N(2)  = 3 + 2 = 5
N(3) = N(2) + N(1)  = 2 + 1 = 3
N(2) = N(1) + N(0)  = 1 + 1 = 2
N(1) = N(0) + N(-1) = 1
N(0) = 1

As expected, N(4) = 5.

One thing to note from the calculations above is that we needed to
compute N(1) and N(2) multiple times. Eliminating this repetitive work
is something we should think about during implementation.


* Implementation options

Now let's consider the ways we can implement our solution.

** A memoized recursive function

The simplest thing we could do would be to implement a recursive
function from our recurrence. The problem, as we discovered earlier,
is that a naive recursive function will end up doing repetitive work.
To eliminate this work, we can memoize the function so that it will
cache the answer to each subproblem it solves. Should it encounter a
subproblem again, it can just use the cached answer.  This approach
leads to a straightforward solution that runs in O(N) time and space.

** Linear algebra

[TODO: Write this section: Linear recurrence. Matrix form. Fast
exponentiation.]

"""

import functools

def memoize(f):
    """Make a memoized version of f that returns cached results."""
    cache = {}
    @functools.wraps(f)
    def g(*args):
        ret = cache.get(args, cache)
        if ret is cache:
            ret = cache[args] = f(*args)
        return ret
    return g

def number_of_distinct_step_sequences(steps_to_climb, allowed_step_multiples):
    # Sanity check arguments.
    assert all(j > 0 for j in allowed_step_multiples)
    assert len(allowed_step_multiples) == len(set(allowed_step_multiples))
    # Memoize the solution recurrence to prevent us from having to
    # recompute solutions for overlapping subproblems.
    @memoize
    def ways(N):
        if N < 0:
            return 0
        if N == 0:
            return 1
        return sum(ways(N - j) for j in allowed_step_multiples)
    # Solve the problem using the recurrance.
    return ways(steps_to_climb)

def test():
    assert number_of_distinct_step_sequences(4, (1, 2)) == 5

    assert number_of_distinct_step_sequences(0, (1,)) == 1

    assert number_of_distinct_step_sequences(1, (2,)) == 0
    assert number_of_distinct_step_sequences(1, (2, 3)) == 0

    for i in range(0, 100):
        assert number_of_distinct_step_sequences(i, (1,)) == 1
        assert number_of_distinct_step_sequences(2 * i, (2,)) == 1
