#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Interview problem: find the first missing positive integer in an array.

* Problem

This problem comes from Daily Coding Problem on 2019-03-28 and was
classified as Hard difficulty:

  Reported source: Stripe.

  Find the smallest missing positive integer in a given array.
  The array may contain arbitrary integers, including negatives
  and duplicates.

  For example, the input [3, 6, -3, 1] should give 2. The input [2, 1,
  0] should give 3.

  You can modify the input array in-place.

* Solution

The positive integers are 1, 2, 3, ..., so we are looking for the
first number in that series that does not occur in the given array.
One way to solve the problem then, would be to create a set from the
array's elements and then look up 1, 2, 3, and so on until we find the
first integer missing from the set. In Python, the solution would look
like this:

    def first_missing_postive_integer(ints):
        ints = set(ints)
        i = 1
        while i in ints:
            i += 1
        return i

This solution runs in linear time, as required, but not in constant
space because it allocates a set that is the same size as the input
array. We can possibly reduce the size of the set by observing that we
will never look up any values outside of the range 1..n+1, where n is
the length of the input array: the pigeonhole principle guarantees
that an array of length n cannot contain n+1 distinct integers, and
therefore at least one number in the range 1..n+1 must be absent from
any such array. In the worst case, however, the array will contain all
but one of the integers in 1..n+1, so the set will be O(n) in size.

However, the pigeonhole principle suggests another approach: we create
not a set but a "pigeonhole array" of size n+1, with elements indexed
by 1..n+1. Then we can iterate over the elements of the input array
and, if an element is in the range 1..n+1, we can set its
corresponding pigeonhole as filled. When we're done, the first empty
pigeonhole will identify the first missing positive integer.

This approach, too, requires O(n) space, but -- here's an idea -- can
we use the input array as the pigeonhole array? If the array contains
a value i in the range 1..n, then we can swap that value into position
i, displacing whatever value was there. If we perform this procedure
for every element in the array, when we're done, every position i in
the array should have value i, provided that i was somewhere in the
original input. If we find a position i that doesn't contain value i,
we know that i was missing from the input, and the first such i gives
us the answer we're looking for. If all of the positions are filled
with their expected values, we know that the original input contained
all of the integers 1..n, and thus the answer is n+1.

This new solution requires only constant additional space, and
satisfies the requirements of the problem statement.

"""

# Runs in O(n) time and space.
def first_missing_postive_integer_1(ints):
    """Returns the least positive integer not in `ints`."""
    ints = set(ints)
    i = 1
    while i in ints:
        i += 1
    return i

# Runs in O(n) time and O(1) space.
def first_missing_postive_integer_2(ints):
    """Returns the least positive integer not in `ints` (modifies ints)."""
    n = len(ints)
    # Helper functions to treat `ints` as a 1-indexed array.
    def get(i):
        """Gets the value at position i (or None if i is out of bounds)."""
        if 1 <= i <= n:
            return ints[i - 1]
        return None
    def place(i):
        """Stores i at position i and returns any displaced value."""
        x = get(i)
        if x is None or x == i:
            return None
        ints[i - 1] = i
        return x
    # Place all values in the array into their home positions.
    for i in ints:
        i = place(i)
        while i is not None:
            i = place(i)
    # Try to find the first position that is missing its expected
    # value. If we succeed, the missing expected value is our answer.
    for i in range(1, n + 1):
        if get(i) != i:
            return i
    # If all positions were filled as expected, the array must cover
    # the integers 1..n, so n + 1 is the answer.
    return n + 1

def test():
    for soln in first_missing_postive_integer_1, first_missing_postive_integer_2:
        assert soln([]) == 1
        assert soln([0]) == 1
        assert soln([-1]) == 1
        assert soln([3, 4, -1, 1]) == 2
        assert soln([1, 2,  0]) == 3
        for x in range(1, 10):
            assert soln(list(range(1, x))) == x
