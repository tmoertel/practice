#!/usr/bin/python

"""Solution to the "Find a duplicate" problem from Interview Cake.

Tom Moertel <tom@moertel.com>
Wed Oct 25 22:22:54 EDT 2017

Problem: Given an array of length n + 1 containing integers in the
range 1..n, find an integer that occurs more than once. Also: Optimize
for space use.

https://www.interviewcake.com/question/java/find-duplicate-optimize-for-space

Solution:

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

"""

import random

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
                # print('f({}; {}) => {}'.format(A, dupes, result))
                if dupes:
                    assert result in dupes
                else:
                    assert result is None
    print('All tests pass for {}.'.format(f.__name__))


if __name__ == '__main__':
    _Test(FindDupeViaInPlaceSort)
