#!/usr/bin/python
#
# Solution to http://www.interviewcake.com/question/reverse-string-in-place
#
# Tom Moertel <tom@moertel.com>
# Thu Oct 17 10:33:38 EDT 2013

def reverse(xs):
    """Reverse an array xs (Python list) in place."""
    i, j = 0, len(xs) - 1
    while i < j:
        xs[i], xs[j] = xs[j], xs[i]
        i += 1
        j -= 1
    return xs

# Claim: reverse(xs) reverses the array xs.

# Proof:  We proceed by induction on the length N of the array.  First,
# the base cases N = 0 and N = 1:
#
# For the N = 0 case, i = 0 and j = -1 at the start of the while loop,
# so the loop exits immediately, and reverse([]) = [], as expected.
# For the N = 1 case, i = j = 0 at the start of the loop, the loop
# exits immediately, and for all x, reverse([x]) = [x], as expected.
#
# For the induction step, assume that reverse works correctly for all
# arrays of length N - 2.  Then, given an array xs of length N > 2,
# i = 0 and j = N - 1 at the start of the while loop, and the loop's
# body executes, causing the first and last elements to be swapped and
# i to move one position to the right and j one to the left.  Now i =
# 1 and j = N - 2, delimiting a subarray of length N - 2.  Continuing
# the loop from this point is the same as calling reverse on the
# subarray, which by our induction hypothesis will be reversed
# correctly.  Thus the final result is xs with its first and last
# elements swapped and the subarray of in-between elements reversed.
# Thus xs will have been reversed in whole, completing the proof.


def test():
    assert reverse([]) == []
    assert reverse([1]) == [1]
    assert reverse([1, 2]) == [2, 1]
    assert reverse([1, 2, 3]) == [3, 2, 1]
