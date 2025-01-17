from soln_11_001_find_first_match import find_first, find_first_1

from random import randrange, sample


def test_find_first_match():
    for f in find_first, find_first_1:
        check_function(f)


def check_function(find_first):
    # The defining property of find_first is this:
    # For all values k,
    # for all counts n,
    # for all sorted series xs such that all(x < k for x in xs),
    # for all sorted series ys such that all(y > k for y in ys),
    # find_first(xs + [k]*n + ys) == -1        if n == 0
    #                             == len(xs)   otherwise.
    for k in range(-2, 3):
        assert find_first([], k) == -1
        for n in range(1, 5):
            assert find_first([k] * n, k) == 0
        for _ in range(1000):
            before = sorted(sample(range(-100, -2), randrange(5)))
            after = sorted(sample(range(3, 100), randrange(5)))
            assert find_first(before + after, k) == -1
            for n in range(1, 5):
                xs = [k] * n
                assert find_first(before + xs + after, k) == len(before)
