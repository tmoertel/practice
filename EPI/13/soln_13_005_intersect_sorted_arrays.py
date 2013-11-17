#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-11-16

"""Solution to "Intersect Sorted Arrays", problem 13.5 in EPI

"Problem 13.5: Given sorted arrays A and B of lengths n and m
respectively, return an array C containing elements common to A and
B. The array C should be free of duplicates.  How would you perform
this intersection if (1) n is near m and (2) n is much less than m?"

Source: _Elements of Programming Interviews_, Aziz, Prakash, and Lee,
v. 1.3.1.

Discussion.  Since A and B are both sorted, their elements are
nondecreasing.  That is, for all valid indices i, j, i + 1, and j + 1,

    A[i + 1] >= A[i],                  (1)
    B[j + 1] >= B[j].                  (2)

Now consider that, if we compare A[i] to B[j], there are three
possibilities.  The first is that A[i] < B[j].  In that case, by
inequality (1) and transitivity, we know that B[j] cannot be matched
by A[i] or any preceding element in A; they are all too low.  Thus, if
there is a match to be found in A for B[j] (or any following and
therefore still greater value in B), it must be some A[k] where k > i.
As a consequence, we can eliminate A[i] and all preceding elements,
and consider only A[i + 1] and following elements.

The second case is that A[i] > B[j].  This is the opposite of the
first case.  Rewriting the inequality as B[j] < A[i] gives us the same
form as our first case but with A and B substituted for each other.
Therefore, the same logic holds, and we get the same conclusion as
before but with A and B swapped:  We can eliminate B[j] and all
preceding elements, and consider only B[j + 1] and following elements.

The third and final case is that A[i] = B[j].  In this case, we have
found a match and can add x = A[i] to our array of matches C.  Then
we can advance both i and j until A[i] != x and B[j] != x.

Starting with i = j = 0 and applying this 3-case logic until both A
and B have been exhausted gives us a linear-time intersection
algorithm that on each iteration does O(1) work and, worst case,
eliminates one element from either A or B.  Therefore it uses O(m + n)
time in the worst case.  In the best case, when A's elements are all
less than B's, the run time is O(m), or when B's are all less than
A's, it's O(n).  This algorithm is implemented below as the function
named intersect.

Variations.

The problem statement asks us to consider what we could do with the
knowledge that A is much smaller than B.  Since the maximum number of
output elements in C is min(m, n) = m (for this scenario), paying a
much larger price O(m + n) to get those few elements seems wasteful.
For example, when x = A[i] is under consideration, and B[j] is smaller
than x, we're probably going to have to advance j many times before
finding a B[j] >= x.  Rather than search linearly, then, we could use
a binary search over the remaining elements of B.  Each search
costs a worst-case O(log n) for an overall run-time of O(m * log n).

But we don't need to search over all n elements of B each time, do we?
If we knew, for example, that A[i] is smaller than B[j] for some j,
the search over B for an element equal to A[i] needs only to cover
elements to the right of j; no element to the left could possibly
equal A[i].  So we could narrow the search over B.

But this idea works both ways, doesn't it?  With that same knowledge
that A[i] < B[j], we could conclude that no element in A to the left
of i could match B[j] or any element to the right of j in B.  Thus
this one piece of knowledge, that A[i] < B[j], allows us to rule out
any element in A[0..i] from ever matching any element in B[j..n-1].

So what if we picked two values, a and b, from the midpoints of A and
B, respectively, and compared them?  From this single comparison, what
conclusions could we draw about the possible matches in A and B?

Let's consider the three possible comparison results and what they
each imply about the partitions of A and B formed w.r.t. a and b,
respectively.  Each result case breaks into 9 subcases on the
intersection of the partitions.  Here's the summary truth table:

                     Does A[i] == B[j] ?

                       Case 1: a < b

               A[i] < a   A[i] == a   a < A[i]
               ---------  ----------  ----------
   B[j] < b  : Maybe      Maybe       Maybe
   b == B[j] : No         No          Maybe
   b <= B[j] : No         No          Maybe


                       Case 2: b < a

               A[i] < a   a == A[i]   a < A[i]
               ---------  ----------  ----------
   B[j] <  b : Maybe      No          No
   b == B[j] : Maybe      No          No
   b < B[j]  : Maybe      Maybe       Maybe


                       Case 3: a == b

               A[i] < a   a == A[i]   a < A[i]
               ---------  ----------  ----------
   B[j] <  b : Maybe      No          No
   b == B[j] : No         Yes!        No
   b < B[j]  : No         No          Maybe

Armed with this knowledge, we can devise a recursive, divide-and-
conquer algorithm to find the intersection.  The idea is to compare
the midpoint value of A against the midpoint value of B -- an
O(1)-time test -- and, based on the result, rule out the excluded part
of the m-by-n search space.  In the a < b and b < a cases, we can rule
out a corner of the search space, leaving an L shape.  We can carve up
the L in at least 3 ways:

    (1) into 3 chunks having worst-case size (m/2, n/2) each
    (2) into 2 chunks having worst-case size (m/2, n) and (m/2, n/2)
    (3) into 2 chunks having worst-case size (m, n/2) and (m/2, n/2)

    (ignoring floors and ceilings)

Since the problem statement for this scenario tells us that m is much
smaller than n, we choose option (2) to ensure that the smaller m is
always halved on every iteration and that we have only 2 subproblems
instead of 3.  Thus our recurrence formula for the cost of this
approach is given by

    T(0, n) = 0
    T(m, n) = 1 + T(m/2, n) + T(m/2, n/2).

When m = 1 or n = 1, our 2-D recurrence reduces to that of a normal
binary search, and (once we account for the floors and ceilings) we
have, as expected,

    T(1, n) = 1 + T(0, n) + T(1, n/2) = 1 + T(1, n/2) = lg n.

To solve the general recurrence, I'll follow Richard Bird's analysis
in the closely related "Improving on saddleback search" chapter of the
wonderful book _Pearls of Functional Algorithm Design_ (2010).  Let

    U(i, j) = T(2^i, 2^j),

from which it follows that

    U(0, j) = j
    U(i, j) = 1 + U(i - 1, j) + U(i - 1, j - 1).

The solution is (again following Bird)

    U(i, j) = 2^i * (j - i/2 + 1) - 1.

Substituting U :-> T, i :-> lg m, and j :-> lg n, we have

    T(m, n) = 2^lg(m) * (lg(n) - lg(m)/2 + 1) - 1
            = m * (lg(n) - lg(m)/2 + 1) - 1
            = m * (lg(n) - lg(sqrt(m)) + 1) - 1
            = m * (lg(n/sqrt(m)) + 1) - 1
            = O(m * log(n/sqrt(m))).

So this approach, which I have implemented in intersect_by_mid_mid
below, does slightly better than the m-binary-searches approach,
having a running time of O(m * log n).

Going further.

But here's another option!  Consider again our truth table for Case 3,
a == b.  In that case, we can rule out all but two quarter-sized
rectangular regions of the search space, reducing the space by half.
And, for any given b, we can find the largest a <= b in A for the low,
low cost of a binary search over the smaller array A.  So another
algorithm takes shape:

    Find b = midpoint value of B for cost O(1)
    Find largest a in A such that a <= b for cost O(log m)
    Use Case 3 from above to divide and conquer

This gives us the new recurrence formula

    T(m, n) = O(log m) + 2 * T(m/2, n/2),

which, assuming m < n, has the more satisfying closed-form solution

    T(m, n) = O(m * log(n/m)).

Further, by the analysis in Bird (2010), this solution is
asymptotically optimal!  I have implemented this algorithm below
as the function intersect_by_mid_search.

"""

def intersect(A, B):
    # strategy: parallel left-to-right scan of both arrays
    C = []
    i = j = 0
    while i < len(A) and j < len(B):
        x = A[i]
        if x < B[j]:
            i += 1
        elif x > B[j]:
            j += 1
        else:
            C.append(x)
            # skip equal elements in both arrays
            while i < len(A) and A[i] == x:
                i += 1
            while j < len(B) and B[j] == x:
                j += 1
    return C

def intersect_by_mid_mid(A, B):
    # strategy: compare midpoints of both arrays, divide & conquer
    C = []
    def go(alo, ahi, blo, bhi):
        if alo > ahi or blo > bhi:
            return
        amid = alo + ((ahi - alo) >> 1)
        bmid = blo + ((bhi - blo) >> 1)
        a, b = A[amid], B[bmid]
        if a < b:
            # case 1: elems in A <= a cannot match elems in B >= b
            go(alo, amid, blo, bmid - 1)
            go(amid + 1, ahi, blo, bhi)
        elif b < a:
            # case 2: elems in B <= b cannot match elems in A >= a
            go(alo, amid - 1, blo, bhi)
            go(amid, ahi, bmid + 1, bhi)
        else:
            # case 3: a == b
            go(alo, amid - 1, blo, bmid - 1)
            if not C or C[-1] != a:
                C.append(a)  # must occur between amid-1 and amid+1 calls
            go(amid + 1, ahi, bmid + 1, bhi)
    go(0, len(A) - 1, 0, len(B) - 1)
    return C

def intersect_by_mid_search(A, B):
    # strategy: take midpoint of B, find nearest value in A, divide & conquer
    C = []
    def go(alo, ahi, blo, bhi):
        if alo > ahi or blo > bhi:
            return
        bmid = blo + ((bhi - blo) >> 1)
        b = B[bmid]
        amid = alo if A[alo] > b else bsearch(A.__getitem__, alo, ahi, b)
        a = A[amid]
        if a < b:
            go(alo, amid, blo, bmid - 1)
            go(amid + 1, ahi, bmid, bhi)
        elif a > b:
            go(alo, ahi, bmid + 1, bhi)
        elif a == b:
            go(alo, amid - 1, blo, bmid - 1)
            if not C or C[-1] != a:
                C.append(a)  # must occur between amid-1 and amid+1 calls
            go(amid + 1, ahi, bmid + 1, bhi)
    go(0, len(A) - 1, 0, len(B) - 1)
    return C

def bsearch(f, lo, hi, y):
    """For monotonic f, find largest x in [lo, hi] such that f(x) <= y."""
    hi0 = hi
    while lo <= hi:
        mid = lo + ((hi - lo) >> 1)
        if f(mid) <= y:
            lo = mid + 1
        else:
            hi = mid - 1
    return lo - 1 if lo > hi0 or f(lo) > y else lo


# testing logic

def test():
    for name, f in globals().iteritems():
        if name.startswith('intersect'):
            print 'testing {}...'.format(name),
            check_function(f)
            print 'ok'

def check_function(f):
    # fundamental property:
    # forall sorted arrays A, B. intersect(A, B) == sorted(set(A) & set(B))
    from math import factorial
    from random import randrange
    from nose.tools import assert_equal
    for N in xrange(8):
        for _ in xrange(factorial(N)):  # get decent sample of problem space
            m, n = randrange(N + 1), randrange(N + 1)
            A = sorted(randrange(N + 1) for _ in xrange(m))
            B = sorted(randrange(N + 1) for _ in xrange(n))
            got = f(A, B)
            expected = sorted(set(A) & set(B))
            # print 'A={} B={}, f(A, B)={}, ref={}'.format(A, B, got, expected)
            assert_equal(got, expected)
