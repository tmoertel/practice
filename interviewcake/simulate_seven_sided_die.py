#!/usr/bin/python

"""Solution to the "simulate 7-sided die" problem from Interview Cake.

Tom Moertel <tom@moertel.com>
Mon Oct 23 23:26:50 EDT 2017

Problem: You have a function rand5() that generates a random integer
from 1 to 5. Use it to write a function rand7() that generates a
[uniformly distributed] random integer from 1 to 7.

Source: https://www.interviewcake.com/question/java/simulate-7-sided-die

Solution:

We are given rand5, which returns a uniformly distributed integer from
1 to 5. From rand5 we can create a rand4 that narrows the range to 1
to 4 by calling rand5 until it returns a number that's not 5. The
distribution of rand4 is uniform (see proof below).

Each call to rand4 gives us two bits of randomness. We only need 3
bits of randomness to create a rand8, which we can narrow to rand7 by
reusing our earlier strategy: call rand8 until it returns a number
that isn't 8.

Analysis:

The expected memory use of this implementation is O(1). We allocate
no memory but a bounded number of O(1)-sized stack frames (we don't
recurse).

We can compute the expected runtime cost of rand7, in terms of calls
to rand5, by starting with rand4 and working to rand7:

  Cost(rand4)
    = E[# of calls to rand5 for each call to rand4]
    = sum(i * P(need exactly i calls to rand5) for i = 1..infinity)
    = sum(i * (1/5)^(i-1) * (4/5) for i = 1..infinity)
    = 4/5 * sum(i * (1/5)^(i-1) for i = 1..infinity)
    = 4 * sum(i * (1/5)^i for i = 1..infinity)
    = 4 * ((1/5) / (1 - (1/5))^2)  { closed form of sum; see below }
    = 4 * (1/5) / (4/5)^2
    = 5/4.

  Cost(rand8)
    = 2 * Cost(rand4)
    = 5/2.

  Cost(rand7)
    = Cost(rand8) * E[# of calls to rand8 for each call to rand7]
    = (5/2) * sum(i * (1/8)^(i-1) * (7/8) for i = 1..infinity)
    = (5/2) * 7 * sum(i * (1/8)^i for i = 1..infinity)
    = (5/2) * 7 * ((1/8) / (1 - (1/8))^2)  { closed form of sum }
    = (5/2) * 7 * ((1/8) / 7/8)^2)
    = (5/2) * 7 * (1/8) * (64/49)
    = (5/2) * (8/7)
    = 20/7 =~ 2.9.

Therefore, the amortized cost of rand7 is < 3 calls to rand5.


Proof that sum(i * a^i for i = 1..infinity) = a / (1 - a)^2 for a < 1.

Let's call the summation in question S. Except for the factor of i in
each term, our S summation is similar to a common geometric series

  G = sum(a^i for i = 1..infinity),

which has the well-known closed-form solution a / (1 - a) for a < 1.

Can we transform the G summation into our S summation? If so, we may
be able apply the same transformation to the closed form of G to
derive a closed-form solution for S.

To introduce the needed i term into the summation for G, let’s take G's
derivative with respect to a:

  G’ = sum(i * a^(i - 1) for i = 1..infinity)

And then, to get the needed exponent of i, we can multiply by a:

  a * G’ = sum(i * a^i for i = 1..infinity)

Thus a * G’ is the same as our summation S. So let's apply the same
transformations to the closed form of G to get a closed form for S:

S = a * G’
  = a * d/da (a / (1 - a))
  = a * (1 / (1 - a)^2)
  = a / (1 - a)^2.

QED.


Proof that rand4 is uniformly distributed.

Let X be a random variable representing the output of rand5. We are
given that X is uniformly distributed from 1 to 5. Therefore, P(X = i)
= 1/5 for i = 1..5. Our implementation of rand4 returns X only if it's
< 5. If Y is the distribution of rand4, P(Y = i) = P(X = i | X < 5)
for i = 1..4. From basic probability, we can compute Y's distribution:

  P(X = i | X < 5)
        { P(AB) = P(A|B) P(B) }
    = P(X = i and X < 5) / P(X < 5)
        { X = i and i = 1..4 implies X < 5  }
    = P(X = i) / P(X < 5)
        { X is uniformly distributed from 1 to 5 (used twice) }
    = (1/5) / (4/5)
        { simplify }
    = 1/4.

Therefore, Y is uniformly distributed from 1 to 4, and so is rand4.
A similar proof holds for rand7. QED.

"""


import random


def rand5():
    return random.randint(1, 5)


def rand4():
    while True:
        i = rand5()
        if i < 5:
            return i

def rand8():
    rand_0_to_15 = ((rand4() - 1) << 2) | (rand4() - 1)
    return 1 + (rand_0_to_15 & 0x7)


def rand7():
    while True:
        i = rand8()
        if i < 8:
            return i


def test_rand7():
    import collections
    # Generate a sample of random draws and compute its distribution.
    N = 10000
    counts = collections.Counter(rand7() for _ in range(N))
    # All value counts must be in the range 1 to 7.
    assert sorted(counts) == range(1, 8)
    # The counts must be approximately equally distributed.
    expected_mean_count = N / 7
    for count in counts.values():
        assert 0.9 * expected_mean_count < count < 1.1 * expected_mean_count
    print('All tests pass.')


if __name__ == '__main__':
    test_rand7()
