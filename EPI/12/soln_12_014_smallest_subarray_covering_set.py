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
the current element. After we've examined the final element, we will
have found the shortest valid range that ends with one of A's elements
also in Q.  And since all valid shortest ranges must end with such an
element, and since we have examined all such ranges, our final
shortest range must be the shortest in all of A.

The key to making the algorithm fast and efficient is choosing the
right data structures.  To keep track of the elements in the candidate
range, we could pair a double-ended queue with a dictionary of element
counts.  With this pairing, we could quickly add a new element to the
end of the range by appending it to the back of the deque and
incrementing its count in the dictionary.  We could also quickly
remove from the deque's front any element that has a count greater
than one.  All of the operations take O(1) time and since each element
in A can be involved in at most two deque and two dictionary
operations, the overall running time of the algorithm is O(|A|), which
is the best we would hope for.  Worst-case storage requirements are
also O(|A|) (for the deque), however.

Can we do better?  Do we really need to store the candidate range's
duplicated elements?  They can't affect the size of the range since
they'll never occur in the front position (because we remove such
duplicates), nor can they affect the back position (since it's always
the current element's position).  The only time the duplicates come
into play, then, is when an earlier duplicate is removed, making what
was an interior element into a front element.  But if this newly
exposed element is a duplicate, it too will be removed.  Thus we need
only store, for each element in Q, the position of its rightmost
occurrence within the candidate range -- the only one that won't
be removed when it comes to the front.

This we can do with a dictionary mapping elements to positions.  But
we'll also need to maintain the order of the elements since we'll need
to quickly determine the first element's position to compute the size
of the candidate range.  This we can do having the dictionary store
pointers to a doubly linked list of positions.  The first position is
available in O(1) time, and any element's position can be moved to the
end of the list in O(1) time when we encounter a new occurrence of
that element.  For example, when A = "aabacad" and Q = "abc" and we've
just advanced the end of the candidate range to position j = 5, we
will update our data structures to look like this:

                        j
                     | ||
                   0123456
              A = "aabacad"   Q = "abc"

              -------------------------
                b         c         a                dictionary
              -------------------------
                |         |         |
                v         v         v
    front --> +---+ --> +---+ --> +---+ --> /
              | 2 |     | 4 |     | 5 |              linked list
        / <-- +---+ <-- +---+ <-- +---+ <-- back

Luckily, the Python data type OrderedDict provides exactly this
dict-and-list combo, making implementation of our algorithm
straightforward.

The algorithm requires storage only for O(|Q|) entries and, since each
element in A participate in at most two O(1) OrderedDict operations,
the running time is O(|A|).


Tom Moertel <tom@moertel.com>
2013-09-25

"""

from collections import OrderedDict

def smallest_subarray_covering_set(A, Q):
    """Find smallest range (i,j) s.t. all q in Q are in A[i..j]."""

    # handle 0-length covering
    if not Q:
        return 0, -1

    # start with no best and an empty candidate covering range
    Q = set(Q)  # want O(1) membership test
    min_size = None
    min_covering_range = None
    cand_locs = OrderedDict()

    # stream elements of A, maintaining the shortest covering range
    # that ends at the current element
    for j, elem in enumerate(A):

        # skip elements that can't contribute to a covering
        if elem not in Q:
            continue

        # extend the candidate range with the current elem,
        # removing any previous instance of the same elem
        cand_locs.pop(elem, None)
        cand_locs[elem] = j  # will be added in final position

        # if the new candidate is legal and better, make it the current best
        if len(cand_locs) == len(Q):
            i = cand_locs.itervalues().next()  # get front position, O(1) time
            if min_size is None or j - i < min_size:
                min_size = j - i
                min_covering_range = i, j

    return min_covering_range


def test():
    from nose.tools import assert_equal as eq
    S = smallest_subarray_covering_set
    eq(S("a", ""), (0, -1))  # 0-length covering exists
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
