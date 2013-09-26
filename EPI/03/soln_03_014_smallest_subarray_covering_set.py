#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-09-25

"""Solution to "Smallest Subarray Covering Set" problem, 12.14 from EPI.

Discussion.

I had a few false starts before I noticed the following property of
minimum covering ranges:  If i and j delimit the smallest range in A
that contains all of the distinct elements in Q, the elements at A[i]
and A[j] cannot be duplicated within the range A[i..j].

(To prove this claim, assume the contrary, that for some A and Q the
shortest covering range is i..j and that the element e = A[i] is
repeated at some later location within the range.  If e is repeated,
we can remove A[i] from the range and still have a valid covering.
But this new range, if it existed, would be one element shorter than
the shortest covering range, contradicting our assumption that i..j
was the shortest.  Therefore, the shortest covering range cannot
contain a duplicate of its leading element A[i].  The same logic holds
for the final element A[j], completing the proof.)

With this property in mind, a linear-time algorithm suggests itself.
We can walk through the elements of A, skipping elements not in Q, and
keeping track of the shortest covering range that *ends* with the
current element.  We append each new element to the tail of the
current range and then remove from the range's head any elements that
are duplicated.  The result is the shortest valid range that ends at
the current element.  If it's shorter than the current shortest range,
we have found a new shortest range.  After we've examined the final
element, we will have found the shortest valid range that ends with
one of A's elements also in Q.  And since all valid shortest ranges
must end with such an element, and since we have examined all such
ranges, our final shortest range must be the shortest in all of A.

The key to making the algorithm fast is choosing the right data
structures.  To keep track of the elements in the candidate range, we
pair a double-ended queue with a dictionary of element counts.  With
this pairing, we can quickly add a new element to the end of the range
by appending it to the back of the deque and incrementing its count in
the dictionary.  We can also quickly remove from the deque's front any
element that has a count greater than one.  All of the operations take
O(1) time and since each element in A can be involved in at most two
deque and two dictionary operations, the overall running time of the
algorithm is O(|A|).  Worst-case storage requirements are O(|A|) for
the deque and O(|Q|) for the dictionary of counts, for O(|A|+|Q|)
overall, or just O(|A|) if we expect that |Q| < |A|.  Typical storage
use is likely to be much better, however, since we only store elements
in the deque that are contributing to the current shortest candidate,
which can never be longer than the longest shortest candidate, which
is likely to be much shorter than A.  Thus the algorithm is
(worst-case) linear in both time and storage, but usually much
better on storage.

This algorithm also has the advantage of being amenable to streaming,
since we only examine elements of A sequentially and never need to
reexamine earlier elements.  (This claim is easy to prove by looking
at the code below.  We access A only through enumerate(A), which
provides elements via an iterator, which does not support random access.)


Tom Moertel <tom@moertel.com>
2013-09-25

"""

from collections import Counter, deque

def smallest_subarray_covering_set(A, Q):
    """Find smallest range (i,j) s.t. all q in Q are in A[i..j]."""

    # start with no best and an empty candidate covering range
    Q = set(Q)  # want O(1) membership test
    min_size = None
    min_covering_range = None
    cand_locs = deque()
    cand_counts = Counter()

    # stream elements of A, maintaining the shortest covering range
    # that ends at the current element
    for loc, elem in enumerate(A):

        # skip elements that can't contribute to a covering
        if elem not in Q:
            continue

        # extend the candidate range with the current elem
        cand_locs.append((elem, loc))
        cand_counts.update(elem)  # bumps count

        # trim from the candidate any initial elems that are redundant
        while cand_counts and cand_counts[cand_locs[0][0]] > 1:
            elem, _ = cand_locs.popleft()
            cand_counts.subtract(elem)

        # if the new candidate is legal and better, make it the current best
        if len(cand_counts) == len(Q):
            i, j = cand_locs[0][1], cand_locs[-1][1]
            if min_size is None or j - i < min_size:
                min_size = j - i
                min_covering_range = i, j

    return min_covering_range


def test():
    from nose.tools import assert_equal as eq
    S = smallest_subarray_covering_set
    eq(S("", "a"), None)
    eq(S("..a", "a"), (2, 2))
    eq(S("aa", "a"), (0, 0))  # when many ranges are smallest, earliest wins
    eq(S("aab", "ab"), (1, 2))
    eq(S("aab", "aba"), (1, 2))  # dupes in Q must not affect result
    eq(S("acaaaabc", "abc"), (5, 7))
    eq(S("acaaaabbc", "abc"), (5, 8))
    eq(S("acaaaabbcccc", "abc"), (5, 8))
    return 'ok'

if __name__ == '__main__':
    test()
