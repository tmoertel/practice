import functools
import pytest
import tomlib
from tomlib import *
from hypothesis import given
from hypothesis.strategies import lists, integers, sets, tuples

"""Tests for `tomlib`, my library of helper functions."""


def approx_eq(x, y):
    return abs(x - y) < EPSILON


def test_memoize():
    counters = [0] * 5

    def f(i):
        counters[i] += 1
        return counters[i]

    for i in range(5):
        assert f(i) != f(i)  # Un-memoized f returns changing values.
    f = memoize(f)
    for i in range(5):
        assert f(i) == f(i)  # Memoized f must return cached values.


def test_trace():
    output = []

    def recorder(*args):
        output.append(args)

    ex = Exception("Bang!")

    def exploder():
        raise ex

    exploder = trace(exploder, recorder)
    with pytest.raises(Exception):
        exploder()
    assert output == [(0, "exploder", (), ex)]
    output[:] = []  # Reset flight recorder for next test.

    def factorial(i):
        if i < 2:
            return i
        return i * factorial(i - 1)

    factorial = trace(factorial, recorder)
    factorial(3)
    assert output == [
        (2, "factorial", (1,), 1),
        (1, "factorial", (2,), 2),
        (0, "factorial", (3,), 6),
    ]


def test_isqrt():
    """isqrt(y) must return maximal x such that 0 <= x*x <= y."""
    # Normal cases.
    for base in range(32):
        for frac in range(-base, base):
            y = base * base + frac
            x = isqrt(y)
            assert x * x <= y  # Must not exceed y.
            assert (x + 1) * (x + 1) > y  # Must be maximal.
    # Exceptional cases.
    with pytest.raises(ValueError):
        isqrt(-1)


def test_find_minimum_by_newtons_method():
    def make_objective_for_parabola(X, Y, a, b):
        X = float(X)
        Y = float(Y)
        a = float(a)
        b = float(b)

        def f(x):
            y = (a * (x - b * X)) ** 2 + Y
            return y

        def f1(x):
            return 2 * a**2 * (x - b * X)

        def f2(x):
            return 2 * a**2

        return f, f1, f2

    for X in range(-10, 11):
        for Y in range(-10, 11):
            for a in range(1, 6):
                for b in range(1, 6):
                    f, f1, f2 = make_objective_for_parabola(X, Y, a, b)
                    for guess in range(-5, 6):
                        x = find_minimum_by_newtons_method(f, f1, f2, guess)
                        assert approx_eq(x, b * X)


def test_find_real_by_newtons_method():
    # Use +/- inverse square root as oracle.
    scenarios = [
        [1, lambda x: x * x, lambda x: 2 * x],
        [-1, lambda x: -x * x, lambda x: -2 * x],
    ]
    e = EPSILON
    for sign, f, f_prime in scenarios:
        y = sign * e
        while abs(y) < 100.0:
            x = find_real_by_newtons_method(f, f_prime, 1.0, y, e)
            assert (f(x) <= y and (f(x + e) > y or f(x - e) > y)) or (
                f(x) >= y and (f(x + e) < y or f(x - e) < y)
            )
            y *= 1.1


def test_find_real_by_bisection():
    HIGH = 100.0

    def f(x):
        return x * x

    def check(y, in_range):
        while in_range(y):
            x = find_real_by_bisection(f, 0.0, HIGH, y)
            assert f(x) <= y < f(x + EPSILON)
            y *= y

    check(1.0 - EPSILON, lambda y: y > EPSILON)
    check(1.0 + EPSILON, lambda y: y < HIGH)

    pytest.raises(ValueError, find_real_by_bisection, f, 1.0, 0.0, 2.0)  # lo > hi
    pytest.raises(ValueError, find_real_by_bisection, f, 2.0, 3.0, 2.0)  # f(lo) > y
    pytest.raises(ValueError, find_real_by_bisection, f, 2.0, 3.0, 9.9)  # f(hi) < y


def test_find_int_by_bisection_exc():
    """find_by_bisection must report out-of-bounds errors."""

    # Exceptional cases (normal cases are tested by test_isqrt).
    def identity(x):
        return x

    pytest.raises(ValueError, find_int_by_bisection, identity, 1, 0, 0)  # lo > hi
    pytest.raises(ValueError, find_int_by_bisection, identity, 1, 2, 0)  # f(lo) > y
    pytest.raises(ValueError, find_int_by_bisection, identity, 1, 2, 3)  # f(hi) < y


def test_fast_pow():
    for x in range(10):
        for n in range(10):
            assert x**n == fast_pow(x, n)


def test_fast_gpow():
    from operator import mul

    for x in range(10):
        for n in range(10):
            assert x**n == fast_gpow(x, n, mul, 1)


def test_matrix_pow_():
    A = [[6, -4], [1, 0]]
    A1K1 = matrix_pow(A, 1001)
    assert [
        [A1K1[0][0] % 371, A1K1[0][1] % 371],
        [A1K1[1][0] % 371, A1K1[1][1] % 371],
    ] == [[131, 286], [114, 189]]
    assert matrix_pow(A, 0) == identity_matrix(2)


def test_matrix_pow_mod():
    A = [[6, -4], [1, 0]]
    A1K1 = matrix_pow_mod(A, 1001, 371)
    assert A1K1 == [[131, 286], [114, 189]]
    assert matrix_pow_mod(A, 0, 371) == identity_matrix(2)


def test_prime_factors():
    assert prime_factors(1) == [1]
    for m in PRIMES[:5]:
        for n in range(1, 10):
            factors = prime_factors(m**n)
            assert all(f == m for f in factors)
            assert len(factors) == n
    from operator import mul

    for n in range(2, 1000):
        assert functools.reduce(mul, prime_factors(n)) == n

    with pytest.raises(ValueError):
        prime_factors(-1)
    with pytest.raises(ValueError):
        prime_factors(0)


def test_primes_upto():
    primes = tomlib._prime_sieve(PRIME_TABLE_CUTOFF + 1000)
    l = len(PRIMES)
    for i, p in list(enumerate(primes, 1))[l - 10 : l + 10]:
        ps = primes_upto(p)
        assert p in ps
        assert len(ps) == i
        assert ps == primes[:i]


def test_primes_upto_at_least():
    primes = tomlib._prime_sieve(PRIME_TABLE_CUTOFF + 1000)
    l = len(PRIMES)
    for i, p in list(enumerate(primes, 1))[l - 10 : l + 10]:
        ps = primes_upto_at_least(p)
        assert p in ps
        assert len(ps) >= i
        assert ps[:i] == primes[:i]


def test_mk_union_find_domain():
    from random import randint, sample, shuffle

    xs = list(range(100))
    for _ in range(100):
        # Use a newly shuffled set of elements.
        shuffle(xs)
        union, find = mk_union_find_domain(xs)
        # break it into desired subsets
        n_cuts = randint(1, len(xs))
        cuts = sorted(sample(range(len(xs)), n_cuts)) + [len(xs)]
        subsets = [xs[cuts[i - 1] : cuts[i]] for i in range(1, len(cuts))]
        subsets = [_f for _f in subsets if _f]
        # Join the elements of each subset.
        for subset in subsets:
            subset = list(subset)
            shuffle(subset)
            for i in range(1, len(subset)):
                union(subset[i - 1], subset[i])

        # Now verify:
        def rep_elem_set(subset):
            return set(find(e) for e in subset)

        rep_elem_sets = list(map(rep_elem_set, subsets))
        # For each subset, all elems must have the same representative elem.
        for res in rep_elem_sets:
            assert len(res) == 1
        # None of the disjoint subsets should share a representative element.
        assert len(functools.reduce(set.union, rep_elem_sets)) == len(subsets)


@given(sets(integers()), lists(tuples(integers(), integers())))
def test_union_find_properties(initial_elements, pairs):
    elements = set(initial_elements)
    for a, b in pairs:
        elements.add(a)
        elements.add(b)
    elements = list(elements)
    if not elements:
        return

    union, find = mk_union_find_domain(elements)

    # After a union of two elements, they must be in the same set.
    for a, b in pairs:
        union(a, b)
        assert find(a) == find(b)

    # Verify idempotence of find.
    for x in elements:
        assert find(x) == find(find(x))

    # Verify that representatives are their own representatives.
    for x in elements:
        rep = find(x)
        assert find(rep) == rep

    # Verify that the number of disjoint sets is correct.
    num_disjoint_sets = len(set(find(e) for e in elements))

    # Count connected components in the graph representation.
    adj = {e: [] for e in elements}
    for a, b in pairs:
        adj[a].append(b)
        adj[b].append(a)

    num_components = 0
    visited = set()
    for elem in elements:
        if elem not in visited:
            num_components += 1
            q = [elem]
            visited.add(elem)
            while q:
                u = q.pop(0)
                for v in adj[u]:
                    if v not in visited:
                        visited.add(v)
                        q.append(v)

    assert num_disjoint_sets == num_components


def test_binomial():
    from operator import __eq__
    from math import factorial as fact

    assert isinstance(real_binomial(1, 1), float)
    for f, eq in ((binomial, __eq__), (real_binomial, approx_eq)):
        for n in range(20):
            for k in range(n + 10):
                if k > n:
                    assert eq(f(n, k), 0)
                else:
                    assert eq(f(n, k), fact(n) / fact(k) / fact(n - k))
                    if k > 0:
                        assert eq(f(n, -k), 0)
    # To prove correct our implementation of the binomial coefficient
    # C(r, k) for real r, int k, we only need one non-integer test
    # case beyond our tests for r = integer n above.  This case shows
    # that we're not using floor division.
    assert approx_eq(real_binomial(-5.5, 2), 17.875)
