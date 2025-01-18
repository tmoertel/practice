from recursion_to_iteration import (
    factorial,
    factorial1a,
    factorial1b,
    factorial1c,
    factorial1d,
    factorial1e,
    factorialt,
    fib,
    fib1a,
    fib1b,
    fib1c,
    fib1d,
    fib1e,
    fib1f,
    fib1g,
    fib1h,
    fibcps1,
    fibcps2,
    fibcps3,
    fibcps4,
)

import functools
import pytest


@pytest.mark.parametrize(
    "f",
    [
        factorial,
        factorial1a,
        factorial1b,
        factorial1c,
        factorial1d,
        factorial1e,
        factorialt,
    ],
)
def test_refactored_factorial(f):
    for n in range(5):
        assert f(n) == functools.reduce(int.__mul__, [1] + list(range(1, n + 1)))


@pytest.mark.parametrize(
    "f",
    [
        fib,
        fib1a,
        fib1b,
        fib1c,
        fib1d,
        fib1e,
        fib1f,
        fib1g,
        fib1h,
        fibcps1,
        fibcps2,
        fibcps3,
        fibcps4,
    ],
)
def test_refactored_fib(f):
    assert list(map(f, list(range(10)))) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
