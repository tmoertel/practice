#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Solution to the "Find a duplicate" problem from Interview Cake.

Tom Moertel <tom@moertel.com>
Wed Oct 25 22:22:54 EDT 2017

Problem: Given an array of length n + 1 containing integers in the
range 1..n, find an integer that occurs more than once. Also: Optimize
for space use.

https://www.interviewcake.com/question/java/find-duplicate-optimize-for-space

Solution 1:

The first solution I came up with requires O(1) space and O(N) time.

The idea is this: Assume there are no duplicates in the array. If
that's true, we have integers 1..n in an array A having indices 1..n
(assuming 1-indexed arrays). Therefore, we ought to be able to put
every value i into position i in the array, sorting the integers. We
can do this in linear time by starting with position i = 0 and, if
A[i] = i, advancing i and repeating. But if A[i] = j != i, then we can
swap A[i] and A[j] to put element j into its place. Then we'll have a
new A[i] and can continue our process on it. In this way, we can
advance while swapping integers into place until i > n, at which time
all of the elements will be sorted into their respective positions.

Now assume that there *are* duplicates in the array. Then there will
be some time when we try to swap an integer j into A[j] but A[j] will
already contain a j. Therefore, we can solve the find-a-duplicate
problem by implementing our sorting scheme with the additional
check for encountering a duplicate along the way.

Solution 2:

The Interview Cake web site poses a variant of the problem in which
you are not allowed to modify the input array. The obvious way to
solve this problem is to compute the histogram of the array's
contents, with each integer getting its own bin, and then find bin
whose count greater than one. But this approach requires O(N) space,
and the problem asks for a solution that minimizes space use.

To reduce space use to O(1), we can reduce the number of bins in the
histogram to a small constant, say 2. If we let M = floor(N/2), the
first bin will cover the integers 1..M and the second bin (M+1)..N.
If there are no duplicates in the array, the first bin must accumulate
a count of M, and the second bin a count of (N - M). Therefore, if we
find a bin that has a greater count than expected, we know it must
contain at least one duplicate. Then we can repeat the process,
focusing only on the integers covered by that bin, until we find
an overly full bin of width one, identifying a duplicate integer.

Unfortunately, this scheme doesn't quite work. Consider the input
1133. For this input, N = 4 and thus M = 2, giving us a bin for the
integers 1..2 and another for the integers 3..4. For this input, both
bins will contain a count of 2, the same as if there had been no
duplicates. (Consider that the duplicate-free input 1234 has the same
bins and counts.)

OK. What if we don't *count* the integers that fall into each but
*add* them? Then we could identify bins that contain duplicates by
looking for incorrect sums. For the bin 1..2, we'd expect a sum of 3.
But, for the input 1133, the sum for that bin would be only 2, calling
attention to the duplicate it contains.

However, this scheme is also flawed. Consider the input 11446677,
giving rise to the bins 1..4 and 5..8. Both bins would accumulate
that expected sums (and counts if we tried the counting scheme).

"""

import random

def trace(f, printer=None):
    """Make a version of f that prints a trace of its calls."""
    import functools
    fnm = f.__name__
    depth = [0]
    def default_printer(depth, fnm, args, ret):
        print '%s%s%r => %r' % ('  ' * depth, fnm, args, ret)
    printer = printer or default_printer
    @functools.wraps(f)
    def g(*args):
        depth[0] += 1
        try:
            ret = f(*args)
        except Exception as e:
            ret = e
            raise
        finally:
            depth[0] -= 1
            printer(depth[0], fnm, args, ret)
        return ret
    return g

def FindDupeViaInPlaceSort(A):
    """Finds a duplicate in A if it exists.

    Returns None if there is no duplicate.
    Raises ValueError if there's a value not in 1..len(A).

    """
    i = 1
    while i <= len(A):
        # See what value is in i's place.
        j = A[i - 1]
        # If it's i, the array is sorted up to i, so advance.
        if j == i:
            i += 1
            continue
        # Otherwise, inspect j and try to swap it into its place.
        if not 1 <= j <= len(A):
            return ValueError('Encountered illegal value {} in array of len {}'.
                              format(j, len(A)))
        if A[j - 1] == j:
            return j  # Already a j in j's place: we've found a duplicate!
        A[i - 1], A[j - 1] = A[j - 1], A[i - 1]
    # All elements of the array are in their place, so there are no duplicates.
    return None


def FindDupeViaDivideAndConquerOverIntegers(A):
    """Finds a duplicate in A if it exists.

    Returns None if there is no duplicate.
    Raises ValueError if there's a value not in 1..len(A).

    """
    for x in A:
        if not 0 < x <= len(A):
            return ValueError('Encountered illegal value {} in array of len {}'.
                              format(x, len(A)))
    @trace
    def Signature(elems):
        sig1 = 0
        sig2 = 1
        for x in elems:
            sig1 += 1
            sig2 += x * x
        return sig1
    lo = 1
    hi = len(A)
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        expected_sig = Signature(range(lo, mid + 1))
        actual_sig = Signature([x for x in A if lo <= x <= mid])
        if actual_sig > expected_sig:
            if lo == hi:
                return lo
            hi = mid
            continue
        expected_sig = Signature(range(mid + 1, hi + 1))
        actual_sig = Signature([x for x in A if mid + 1 <= x <= hi])
        if actual_sig > expected_sig:
            lo = mid + 1
            continue
        return None
    return None

def _MakeRandomArrayWithDupes(array_size, num_dupes):
    dupes = set()
    reps = {i: 1 for i in range(1, array_size + 1)}
    while num_dupes:
        i = random.choice(list(reps))
        potential_victims = list(set(reps) - dupes - set([i]))
        if not potential_victims:
            break
        j = random.choice(potential_victims)
        dupes.add(i)
        reps[i] += 1
        del reps[j]
        num_dupes -= 1
    A = []
    for i, count in reps.items():
        A.extend([i] * count)
    random.shuffle(A)
    assert len(A) == array_size
    return A, dupes


def _Test(f):
    import math
    for array_size in range(7):
        for _random_case in range(math.factorial(array_size)):
            for num_dupes in range(array_size + 1):
                A, dupes = _MakeRandomArrayWithDupes(array_size, num_dupes)
                result = f(A)
                print('f({}; {}) => {}'.format(A, dupes, result))
                if dupes:
                    assert result in dupes
                else:
                    assert result is None
    print('All tests pass for {}.'.format(f.__name__))


if __name__ == '__main__':
    _Test(FindDupeViaDivideAndConquerOverIntegers)
    _Test(FindDupeViaInPlaceSort)