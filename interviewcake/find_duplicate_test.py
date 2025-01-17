from find_duplicate import (
    FindDupeViaInPlaceSort,
    FindDupeViaDivideAndConquerOverIntegers,
)

import pytest
import random


@pytest.mark.parametrize(
    "f, only_strictly_legal_instances",
    ((FindDupeViaInPlaceSort, False), (FindDupeViaDivideAndConquerOverIntegers, True)),
)
def test_find_duplicate(f, only_strictly_legal_instances):
    import math

    for array_size in range(7):
        for _random_case in range(math.factorial(array_size)):
            for num_dupes in range(array_size + 1):
                A, dupes = _MakeRandomArrayWithDupes(array_size, num_dupes)
                if only_strictly_legal_instances and not _IsStrictlyLegal(A):
                    continue
                result = f(A)
                if dupes:
                    assert result in dupes
                else:
                    assert result is None


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
    for i, count in list(reps.items()):
        A.extend([i] * count)
    random.shuffle(A)
    assert len(A) == array_size
    return A, dupes


def _IsStrictlyLegal(A):
    N = len(A) - 1
    return N > 0 and all(1 <= a <= N for a in A)
