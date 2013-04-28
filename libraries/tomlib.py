#!/usr/bin/python

"""Library of code snippets I've written for use in programming contests.

Tom Moertel <tom@moertel.com>
2013-04-27

"""

# decorators

import functools
import sys

def memoize(f):
    """Make a memoized version of f that returns cached results."""
    cache = {}
    @functools.wraps(f)
    def g(*args):
        ret = cache.get(args, cache)
        if ret is cache:
            ret = cache[args] = f(*args)
        return ret
    return g

def trace(f, printer=None):
    """Make a version of f that prints a trace of its calls."""
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


# numeric functions

EPSILON = sys.float_info.epsilon ** 0.5  # default to half of system precision

def find_real_by_newtons_method(f, f_prime, x, y, e=EPSILON):
    """From a guess x, find an improved x within e of the true soln f(x) = y.

    You must supply f_prime, the first derivative of f.

    Caveats: This method may converge slowly if f(x) - y = 0 has roots
    with multiplicity > 1.  This method may fail outright if the first
    derivative of f has zeros in the region of interest.  Use instead
    find_real_by_bisection for slower but more robust convergence.

    """
    update = e
    while abs(update) >= e:
        update = (y - f(x)) / f_prime(x)
        x += update
    return x

def find_real_by_bisection(f, lo, hi, y, e=EPSILON):
    """Find x in [lo, hi] such that f(x) <= y < f(x + e).

    Note: f must be monotonic within the range [lo, hi].

    """
    _check_bisection_bounds(f, lo, hi, y)
    while lo < hi:
        mid = (lo + hi) / 2.0
        if f(mid) <= y:
            lo = mid + e
        else:
            hi = mid - e
    return lo if f(lo) <= y else lo - e

def find_int_by_bisection(f, lo, hi, y):
    """Find maximal int x in [lo, hi] such that f(x) <= y.

    Note: f must be monotonic within the range [lo, hi].

    """
    _check_bisection_bounds(f, lo, hi, y)
    while lo < hi:
        mid = lo + ((hi - lo) >> 1)
        if f(mid) <= y:
            lo = mid + 1
        else:
            hi = mid - 1
    return lo if f(lo) <= y else lo - 1

def _check_bisection_bounds(f, lo, hi, y):
    if lo > hi:
        raise ValueError('lower bound is above upper bound')
    if y < f(lo):
        raise ValueError('solution is below lower bound')
    if y > f(hi):
        raise ValueError('solution is above upper bound')

def isqrt(y):
    """Find maximal int x > 0 such that x * x <= y."""
    if y < 0:
        raise ValueError('isqrt is not defined for negative values')
    def f(x):
        return x * x
    return find_int_by_bisection(f, 0, y, y)

def fast_pow(x, n):
    """Raise numeric x to integer power n."""
    if n == 0:
        return 1
    def go(x, n):
        if n == 1:
            return x
        if n & 1:
            return x * go(x, n - 1)
        return go(x * x, n >> 1)
    return go(x, n)

def fast_gpow(x, n, mul, mul_identity):
    """Raise generalized numeric x to integer power n."""
    if n == 0:
        return mul_identity
    def go(x, n):
        if n == 1:
            return x
        if n & 1:
            return mul(x, go(x, n - 1))
        return go(mul(x, x), n >> 1)
    return go(x, n)


# vectors

def dot_product(u, v):
    """Compute dot product of equal-length vectors u and v."""
    return sum(u[i] * v[i] for i in xrange(len(u)))

def mk_dot_product_mod(m):
    """Make a dot-product function that computes mod m."""
    def dot_product_mod(u, v):
        return sum((u[i] * v[i]) % m for i in xrange(len(u))) % m
    return dot_product_mod

def dot_product_mod(u, v, m):
    """Compute dot product of equal-length vectors u and v (mod m)."""
    return mk_dot_product_mod(m)(u, v)


# matrices

def mk_matrix_mul(dot=dot_product):
    """Make matrix multiplier using a given dot-product function."""
    def matrix_mul(A, B):
        """Compute product of matrices A and B."""
        if not len(A[0]) == len(B) > 0:
            raise ValueError('matrices are mismatched for multiplication')
        Bt = zip(*B)  # transpose B to get column order
        return [[dot(row, col) for col in Bt] for row in A]
    return matrix_mul

matrix_mul = mk_matrix_mul()  # common-case version

def matrix_mul_mod(A, B, m):
    """Compute product of matrices A and B (mod m)."""
    return mk_matrix_mul(mk_dot_product_mod(m))(A, B)

def identity_matrix(n):
    """Make n*n identity matrix."""
    A = [[0] * n for _ in xrange(n)]
    for i in xrange(n):
        A[i][i] = 1
    return A

def matrix_pow(A, n, dot=dot_product):
    """Raise matrix A to the integer power n."""
    if n == 0:
        return identity_matrix(len(A))
    return fast_gpow(A, n, mk_matrix_mul(dot), None)

def matrix_pow_mod(A, n, m):
    """Raise matrix A to the integer power n (mod m)."""
    if n == 0:
        return identity_matrix(len(A))
    return fast_gpow(A, n, mk_matrix_mul(mk_dot_product_mod(m)), None)


# number theory

from bisect import bisect_right

def primes_upto(n):
    """Get an increasing list of all primes <= n.

    Prefer primes_upto_at_least if you can tolerate extra primes > n.
    """
    global PRIMES, PRIME_TABLE_CUTOFF
    if n > PRIME_TABLE_CUTOFF:
        PRIME_TABLE_CUTOFF *= 2
        PRIMES = _prime_sieve(PRIME_TABLE_CUTOFF)
    return PRIMES[:bisect_right(PRIMES, n)]

def primes_upto_at_least(n):
    """Get an increasing list of all primes <= m for some m >= n."""
    return PRIMES if n <= PRIME_TABLE_CUTOFF else primes_upto(n)

def _prime_sieve(n):
    """Get an increasing list of all primes <= n."""
    candidates = [True] * (n + 1)
    primes = []
    for i in xrange(2, n + 1):
        if candidates[i]:
            primes.append(i)
            for j in xrange(i + i, n + 1, i):
                candidates[j] = False
    return primes

PRIME_TABLE_CUTOFF = 2**16
PRIMES = _prime_sieve(PRIME_TABLE_CUTOFF)

def prime_factors(n):
    """Get an ordered list of the prime factors of n."""
    if n < 1:
        raise ValueError('n=%r cannot have prime factors' % (n, ))
    if n == 1:
        return [1]
    primes = primes_upto_at_least(isqrt(n) + 1)
    factors = []
    for p in primes:
        if p * p > n:
            break
        while True:
            q, r = divmod(n, p)
            if r:
                break
            factors.append(p)
            n = q
    if n > 1:
        factors.append(n)
    return factors


# tests

def test_memoize():
    counters = [0] * 5
    def f(i):
        counters[i] += 1
        return counters[i]
    for i in xrange(5):
        assert f(i) != f(i)  # un-memoized f returns changing values
    f = memoize(f)
    for i in xrange(5):
        assert f(i) == f(i)  # memoized f must return cached values

def test_trace():
    from nose.tools import raises
    output = []
    def recorder(*args):
        output.append(args)
    ex = Exception('Bang!')
    def exploder():
        raise ex
    exploder = trace(exploder, recorder)
    raises(Exception)(exploder)()
    assert output == [(0, 'exploder', (), ex)]
    output[:] = []  # reset flight recorder for next test
    def factorial(i):
        if i < 2:
            return i
        return i * factorial(i - 1)
    factorial = trace(factorial, recorder)
    factorial(3)
    assert output == [(2, 'factorial', (1,), 1),
                      (1, 'factorial', (2,), 2),
                      (0, 'factorial', (3,), 6)]

def test_isqrt():
    """isqrt(y) must return maximal x such that 0 <= x*x <= y."""
    # normal cases
    for base in xrange(32):
        for frac in xrange(-base, base):
            y = base * base + frac
            x = isqrt(y)
            assert x * x <= y             # must not exceed y
            assert (x + 1) * (x + 1) > y  # must be maximal
    # exceptional cases
    from nose.tools import raises
    raises(ValueError)(isqrt)(-1)

def test_find_real_by_newtons_method():
    # use +/- inverse square root as oracle
    scenarios = [[ 1, lambda x:  x*x, lambda x:  2*x],
                 [-1, lambda x: -x*x, lambda x: -2*x]]
    e = EPSILON
    for sign, f, f_prime in scenarios:
        y = sign * e
        while abs(y) < 100.0:
            x = find_real_by_newtons_method(f, f_prime, 1.0, y, e)
            assert ((f(x) <= y and (f(x + e) > y or f(x - e) > y)) or
                    (f(x) >= y and (f(x + e) < y or f(x - e) < y)))
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
    from nose.tools import raises
    raises(ValueError)(find_real_by_bisection)(f, 1.0, 0.0, 2.0)  # lo > hi
    raises(ValueError)(find_real_by_bisection)(f, 2.0, 3.0, 2.0)  # f(lo) > y
    raises(ValueError)(find_real_by_bisection)(f, 2.0, 3.0, 9.9)  # f(hi) < y

def test_find_int_by_bisection_exc():
    """find_by_bisection must report out-of-bounds errors."""
    # exceptional cases (normal cases are tested by test_isqrt)
    def identity(x):
        return x
    from nose.tools import raises
    raises(ValueError)(find_int_by_bisection)(identity, 1, 0, 0)  # lo > hi
    raises(ValueError)(find_int_by_bisection)(identity, 1, 2, 0)  # f(lo) > y
    raises(ValueError)(find_int_by_bisection)(identity, 1, 2, 3)  # f(hi) < y

def test_fast_pow():
    for x in xrange(10):
        for n in xrange(10):
            assert x**n == fast_pow(x, n)

def test_fast_gpow():
    from operator import mul
    for x in xrange(10):
        for n in xrange(10):
            assert x**n == fast_gpow(x, n, mul, 1)

def test_matrix_pow_():
    A = [[6, -4], [1, 0]]
    A1K1 = matrix_pow(A, 1001)
    assert ([[A1K1[0][0] % 371, A1K1[0][1] % 371],
             [A1K1[1][0] % 371, A1K1[1][1] % 371]] == [[131, 286], [114, 189]])
    assert matrix_pow(A, 0) == identity_matrix(2)

def test_matrix_pow_mod():
    A = [[6, -4], [1, 0]]
    A1K1 = matrix_pow_mod(A, 1001, 371)
    assert A1K1 == [[131, 286], [114, 189]]
    assert matrix_pow_mod(A, 0, 371) == identity_matrix(2)

def test_prime_factors():
    assert prime_factors(1) == [1]
    for m in PRIMES[:5]:
        for n in xrange(1, 10):
            factors = prime_factors(m**n)
            assert all(f == m for f in factors)
            assert len(factors) == n
    from operator import mul
    for n in xrange(2, 1000):
        assert reduce(mul, prime_factors(n)) == n
    from nose.tools import raises
    raises(ValueError)(prime_factors)(-1)
    raises(ValueError)(prime_factors)(0)

def test_primes_upto():
    primes = _prime_sieve(PRIME_TABLE_CUTOFF + 1000)
    l = len(PRIMES)
    for i, p in list(enumerate(primes, 1))[l-10:l+10]:
        ps = primes_upto(p)
        assert p in ps
        assert len(ps) == i
        assert ps == primes[:i]

def test_primes_upto_at_least():
    primes = _prime_sieve(PRIME_TABLE_CUTOFF + 1000)
    l = len(PRIMES)
    for i, p in list(enumerate(primes, 1))[l-10:l+10]:
        ps = primes_upto_at_least(p)
        assert p in ps
        assert len(ps) >= i
        assert ps[:i] == primes[:i]
