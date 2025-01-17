#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-11-12

"""Solution to "Water Holding Capacity" problem.

The following problem comes from a blog post "I Failed a Twitter
Interview" [1] by Michael Kozakov.

The problem is as follows, reworded for clarity:

Imagine that you have a strip of land sandwiched between two infinite
sheets of glass, allowing you to see the strip from its side.  Let us
further imagine that, if we divide the strip into segments of unit
width, we can describe its profile with an array giving the height of
each segment above sea level.  For example, the array A = [2, 5, 1, 2,
3, 4, 7, 7, 6] describes the following strip:

                           ___
                          |   |_
                 _        |     |
                | |      _|     |
                | |    _|       |
               _| |  _|         |
              |   |_|           |
     ~~~~~~~~~|                 |~~~~~~~~~ sea level

     A[i]:     2 5 1 2 3 4 7 7 6

     i:        0 1 2 3 4 5 6 7 8


Our problem then is this: Given such an array describing a strip of
land, determine the volume of water (given in square units) that can
be held within the strip.  Assume that the strip is of impermeable
rock surrounded by an infinite sea of constant height 0 and that water
never evaporates.

For example, given the array A from above, the correct answer is 10,
as shown below:

                           ___
                          |   |_
                 _        |     |
                | |~ ~ ~ ~|     |
                | |~ ~ ~|       |
               _| |~ ~|         |
              |   |~|           |
     ~~~~~~~~~|                 |~~~~~~~~~ sea level


Discussion.

To understand the nature of a problem I usually start with the
simplest cases, trying to gain intuition.  Then I use notation to
capture the intuition as I build up to a more general solution.

For this problem, then, what's the simplest case?  It's a strip of
land with zero segments:

     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ sea level

In this case, there is no land, and so no water can be held above it.
So if we let W(A) denote the water-holding capacity of the strip given
by the array A, we have a base case

    W([]) = 0.

Moving on, what's the next simplest case?  It's a strip of just one
segment.  Let's say this segment is h units above sea level.  How much
water can be held above the segment?

That's hard to say.  To answer the question, we need to know the water
level around the segment, and that requires knowledge about what's
going on to the left and right.  For example, if there's no higher
land to either side, just sea, then there is nothing to hold any water
above the segment in place; it will all run away:

                       _
                      | | h
     ~~~~~~~~~~~~~~~~~| |~~~~~~~~~~~~~~~~~ sea level


(Unless, of course, h is negative, representing a hole.  Then
the hole will hold -h units of water.)

But if there is higher land on both sides of our segment, hole or not,
then that land will support water up to some level before overflowing.
If we let lm (for "left maximum") be the height that water can reach
before overflowing to the left, and if we let rm be the same for the
right, then the water level around our segment will be given by
min(lm, rm), and the water held above our segment will be that
quantity less h:

                                 _
             _                  | | rm
         lm | |~~...~~~~~~~...~~| |
            | |        _        | |
            | |       | | h     | |
     ~~~...~| |.......| |.......| |~...~~~~ sea level


Of course, if h is higher than the surrounding water, which is
entirely possible, the result of the subtraction will turn out to be
negative, which doesn't correspond to the physical reality that Nature
doesn't let negative quantities of water come into existence.  So, as
a final touch, we must amend our formula to respect Nature's lower
bound of zero.  Thus, after augmenting our W() notation to accept lm
and rm values, we arrive at what seems like a reasonable answer for
our one-segment case:

    W([h], lm, rm) = max(0, min(lm, rm) - h).

To review, so far we have solutions for the 0- and 1-segment base
cases.  Putting them in parallel form:

    W([],  lm, rm) = 0
    W([h], lm, rm) = max(0, min(lm, rm) - h)

Now, what about the general case of n > 1 segments?  One way to solve
it would be to break it into n little one-segment problems, which we
already know how to solve:

    W(A, lm, rm) = sum(W([A[i]], lmi[i], rmi[i]) for i = 0..n-1)

But that would require computing the needed lm and rm values for each
segment i's subproblem:

    lmi[i] = max(lm, max(A[j] for j < i))
    rmi[i] = max(rm, max(A[j] for j > i))

And that takes O(n) operations for each segment i.  We can reduce that
cost to O(n) for *all* i, however, by noting that the adjacent lmi and
rmi values are related as follows:

    lmi[i] = max(A[i - 1], lmi[i - 1])    for i > 0,
    rmi[i] = max(A[i + 1], rmi[i + 1])    for i < n - 1.

Thus we can precompute the lmi array by starting with lmi[0] = lm and
working our way to the right, and we can precompute rmi by starting
with rmi[n - 1] = rm and working left.  With these arrays precomputed,
the overall solution takes O(n) time:

    precompute lmi and rmi:               O(n)
    compute and combine n 1-seg solns:         + n * O(1)
    total:                                                = O(n)

But the lmi and rmi arrays each take O(n) extra space.  Can we do
better?

Well, we can compute lmi's entries left-to-right, and since we also
traverse A left-to-right in the summation, we can compute the needed
value of lmi[i] in passing to eliminate the need for the lmi array:

    def water_holding_capacity(A, lm, rm):
        rmi = precompute_rmi(rm)  # as before
        total = 0
        for i, h in enumerate(A):
            total += max(0, min(lm, rmi[i]) - h)
            lm = max(lm, h)
        return total

But we still have O(n) space use for the rmi array.  Can we do better?

The tricky spot seems to be that for each segment i we need both
lmi[i] and rmi[i], but the lmi and rmi arrays can only be computed
efficiently from traversals in opposite directions.  And, since we
must also traverse A in *some* direction during the summation, only
one of lmi or rmi can be computed in passing.  The other array, it
seems, must be precomputed and stored for lookup when needed.

But do we really need to compute the summation via a single-direction
traversal?  Addition is commutative and associative, so we can
rearrange a summation's terms without affecting the sum.  Can we,
then, find some other ordering that is advantageous?

For clues, let's look at the interesting facts we've discovered.  We
know that, for the first and last segments of a strip, their lmi and
rmi values, respectively, are the same as the entire strip's lm and rm
values.  So maybe we ought to examine these segments first, as they
need access to only one precomputed array each, not two as usual.
That is, the first segment's contribution to the sum will be given by

    max(0, min(lm, rmi[0]) - A[0])

and the last segment's will be given by

    max(0, min(lmi[n - 1], rm) - A[n - 1]).

Can we eliminate the need for rmi in the first expression or lmi in
the second?  At this point, our opportunity sensors should be bleeping
with hope because in both expressions we're taking the minimum of a
maximum.  This is often a signal that sub-computations can be pruned
away.  So let's revisit what we know about lmi[n - 1] and rmi[0].
Here again are the formulas for lmi[i] and rmi[i]:

    lmi[i] = max(lm, max(A[j] for j < i))
    rmi[i] = max(rm, max(A[j] for j > i))

Note that, for all i, the following inequalities must hold:

    lm <= lmi[i]
    rm <= rmi[i]

Now let's say that we compare lm and rm.  If lm is less than rm,
we can combine our inequalities above into the following one,

    lm < rm <= rmi[i],

and it will let us simplify the summation term for the first land
segment from

    max(0, min(lm, rmi[0]) - A[0])

to

    max(0, lm - A[0])

since lm < rmi[0] implies that min(lm, rmi[0]) = lm.

By similar logic, if it turns out that lm >= rm, we can do the same
thing for the final land segment's term, reducing it to

    max(0, rm - A[n - 1]).

So now we have another way of solving our original problem for cases
of n > 1 segments.  We can break that problem into two smaller ones.
One will be a one-segment problem formed from either the first or last
land segment, depending on which is larger, lm or rm.  The second will
be the remaining land segments recast as a slightly smaller problem of
n - 1 segments.  This gives us the following recurrence:

                        1-segment prob            n-1 segment prob
    W(A, lm, rm)      ~~~~~~~~~~~~~~~~~~   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
       | lm < rm   =  max(0, lm - A[ 0]) + W(A[1: ], max(lm, A[ 0]), rm)
       | lm >= rm  =  max(0, rm - A[-1]) + W(A[:-1], lm, max(rm, A[-1]))

(Note that I'm using the Python indexing convention that i = -1 is the
same as i = n - 1.)

This recurrence formula, along with our original base case for a
0-segment strip, gives us a way to compute a solution with n O(1)-time
operations (= O(n) total time) and O(1) space consumption.

In the code below, I first translate this recurrence directly into
Python for correctness.  Then I mechanically translate the recursive
code into an efficient iterative version, using tail recursion as a
stepping stone.  (See [2] for more on converting recursive algorithms
into iterative ones.)  It's a straightforward translation except for
one thing:  Rather than slicing the array A over and over, I use the
indices i and j to delimit the portion under consideration.

And that's how I solved the problem.


Links:

[1] http://qandwhat.apps.runkite.com/i-failed-a-twitter-interview/

[2] http://blog.moertel.com/posts/2013-05-11-recursive-to-iterative.html

"""


def water_holding_capacity_recursive(A):
    def whc(i, j, lm, rm):
        # base case: 0-width strip => can hold no water
        if j < i:
            return 0
        # non-empty strip: consume left- or right-end segment
        if lm < rm:
            return max(0, lm - A[i]) + whc(i + 1, j, max(lm, A[i]), rm)
        else:
            return max(0, rm - A[j]) + whc(i, j - 1, lm, max(rm, A[j]))

    return whc(0, len(A) - 1, 0, 0)


def water_holding_capacity_tail_recusrive(A):
    def whc(i, j, lm, rm, vol):
        # base case: 0-width strip => can hold no water
        if j < i:
            return vol
        # non-empty strip: consume left- or right-end segment
        if lm < rm:
            return whc(i + 1, j, max(lm, A[i]), rm, vol + max(0, lm - A[i]))
        else:
            return whc(i, j - 1, lm, max(rm, A[j]), vol + max(0, rm - A[j]))

    return whc(0, len(A) - 1, 0, 0, 0)


def water_holding_capacity_iterative(A):
    (i, j) = (0, len(A) - 1)
    lm = rm = vol = 0
    # while segments remain, consume left- or right-end segment
    while i <= j:
        if lm < rm:
            vol += max(0, lm - A[i])
            lm = max(lm, A[i])
            i += 1
        else:
            vol += max(0, rm - A[j])
            rm = max(rm, A[j])
            j -= 1
    return vol


# Tests.


import pytest

@pytest.mark.parametrize("f", [
    water_holding_capacity_recursive,
    water_holding_capacity_tail_recusrive,
    water_holding_capacity_iterative,
])
def test_func(f):
    from random import randrange
    from math import factorial

    # the empty strip must hold no water
    assert f([]) == 0

    # all 1-segment strips above sea level must hold no water
    for h in range(10):
        assert f([h]) == 0

    # all 1-segment strips below sea level must hold their depth in water
    for h in range(10):
        assert f([-h]) == h

    # must solve example problem
    A = [2, 5, 1, 2, 3, 4, 7, 7, 6]
    assert f(A) == 10

    # forall A. solution(A) must equal solution(reversed(A))
    for N in range(8):
        for _ in range(factorial(N)):  # use N! samples for coverage
            A = [randrange(N) for _ in range(N)]
            assert f(list(reversed(A))) == f(A)
