#!/usr/bin/python

"""Library of code snippets I've written for use in programming contests.

Tom Moertel <tom@moertel.com>
2013-04-27

"""

# numeric functions

def find_int_by_bisection(f, lo, hi, goal):
    """Find maximal int x in [lo, hi] such that f(x) <= goal."""
    if goal < f(lo):
        raise ValueError('solution is below lower bound')
    if goal > f(hi):
        raise ValueError('solution is above upper bound')
    while lo < hi:
        mid = lo + ((hi - lo) >> 1)
        if f(mid) <= goal:
            lo = mid + 1
        else:
            hi = mid - 1
    if f(lo) <= goal:
        return lo
    return lo - 1

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
    dot_product_mod.__doc__ = ("Compute dot product of equal-length vectors "
                               "u and v (mod %r)." % m)
    return dot_product_mod

def dot_product_mod(u, v, n):
    return mk_dot_product_mod(n)(u, v)


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


# tests

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

def test_find_int_by_bisection_exc():
    """find_by_bisection must report out-of-bounds errors."""
    # exceptional cases (normal cases are tested by test_isqrt)
    def identity(x):
        return x
    from nose.tools import raises
    @raises(ValueError)
    def check_bound(x):
        return find_int_by_bisection(identity, 0, 5, x)
    check_bound(-1)  # below lower bound
    check_bound(6)   # above upper bound

def test_fast_pow():
    for x in xrange(10):
        for n in xrange(10):
            assert x**n == fast_pow(x, n)

def test_fast_gpow():
    from operator import mul
    for x in xrange(10):
        for n in xrange(10):
            assert x**n == fast_gpow(x, n, mul, 1)

def test_matrix_pow_mod():
    A = [[6, -4], [1, 0]]
    A1K1 = matrix_pow_mod(A, 1001, 371)
    assert A1K1 == [[131, 286], [114, 189]]
    assert matrix_pow_mod(A, 0, 371) == identity_matrix(2)
