#!/usr/bin/python
#
# Tom Moertel <tom@moertel.com>
# 2013-03-05

"""Solve Dijkstra's "Dutch National Flag" problem.

http://programmingpraxis.com/2013/03/05/dutch-national-flag/

"""


# Our stategy is to partition A into red, mid, and blue segments,
# where the red segment A[:red] contains exclusively 'r' values, and
# the blue segment A[blue:] contains exclusively 'b' values.  The mid
# segment A[red:blue] contains everything else, partitioned by i:
# A[blue:i] are values known to be 'w', and A[i:red} are unexamined
# values. Initially, then, the unexamined mid segment owns the entire
# array, but as we examine elements we swap them into the red and blue
# segments, which grow correspondingly.  When we've examined all of
# the elements, there will be no unexamined elements in the mid
# segment, which must therefore be all 'w' values; hence the array
# will be sorted by color (into the 'r', 'w', 'b' order of the Dutch
# National Flag).

def dnf_sort(A):
    """Sort (in-place) a 3-colored array."""

    def swap(i, j):
        A[i], A[j] = A[j], A[i]

    red = i = 0
    blue = len(A)

    while i < blue:
        # invariant: all elems in A[blue:i] are 'w'
        # invariant: all elems in A[i:red] are unexamined
        if A[i] == 'r':
            swap(i, red)
            red += 1
            i += 1
        elif A[i] == 'b':
            blue -= 1
            swap(i, blue)
            # don't advance i: after swap A[i] is now unexamined
        else:
            i += 1

# Test code

COLORS = 'rwb'
VALUES = [0, 1, 2]
cval = dict(zip(COLORS, VALUES)).get
cvals = lambda cs: map(cval, cs)

def test_dnf_sort():
    for l in xrange(8):
        for cs in combinations([COLORS] * l):
            assert_sorted(cs)

def combinations(xss):
    if xss == []:
        return [[]]
    return [list(x) + ys
            for ys in combinations(xss[1:])
            for x in xss[0]]

def assert_sorted(cs):
    expected = sorted(cvals(cs))
    dnf_sort(cs)
    assert cvals(cs) == expected
