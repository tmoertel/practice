from soln_13_005_intersect_sorted_arrays import (
    intersect,
    intersect_by_mid_mid,
    intersect_by_mid_search,
)

import pytest


@pytest.mark.parametrize(
    "implementation", (intersect, intersect_by_mid_mid, intersect_by_mid_search)
)
def test_intersect_sorted_arrays(implementation):
    # Fundamental property:
    # Forall sorted arrays A, B. intersect(A, B) == sorted(set(A) & set(B)).
    from math import factorial
    from random import randrange

    for N in range(8):
        for _ in range(factorial(N)):  # get decent sample of problem space
            m, n = randrange(N + 1), randrange(N + 1)
            A = sorted(randrange(N + 1) for _ in range(m))
            B = sorted(randrange(N + 1) for _ in range(n))
            got = implementation(A, B)
            expected = sorted(set(A) & set(B))
            # print 'A={} B={}, f(A, B)={}, ref={}'.format(A, B, got, expected)
            assert got == expected
