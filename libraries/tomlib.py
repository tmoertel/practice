#!/usr/bin/python

"""Library of code snippets I've written for use in programming contests.

Tom Moertel <tom@moertel.com>
2013-04-27

"""

import functools
import sys
from functools import reduce
from bisect import bisect_right

# Decorators.


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
        print("%s%s%r => %r" % ("  " * depth, fnm, args, ret))

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


# Numeric functions.

EPSILON = sys.float_info.epsilon**0.5  # default to half of system precision


def find_minimum_by_newtons_method(f, f1, f2, x, e=EPSILON, a=0.25, b=0.5):
    """Find x' near x such that f(x') is a local minimum.

    You must supply f, the objective function, which must be convex
    in the region of x.  You must also supply its first and second
    derivatives, f1 and f2, which must exist within the region.

    Reference: _Convex Optimization_, Boyd and Vandenberghe, 2004, p. 484.

    """
    while True:
        # Find descent direction.
        f1x = f1(x)
        delta = -f1x / max(0.001, abs(f2(x)))  # keep f2(x) positive
        # Check stopping criterion.
        if -delta * f1x <= 2 * e:
            return x
        # Choose step size `t` via backtracking search.
        t = 1.0
        fx = f(x)
        while f(x + t * delta) > fx + a * t * delta * f1x:
            t *= b
        # Update location.
        x += t * delta
    return x


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
    hi0 = hi  # Save upper bound.
    while lo < hi:
        mid = (lo + hi) / 2.0
        if f(mid) <= y:
            lo = mid + e
        else:
            hi = mid - e
    return lo if lo <= hi0 and f(lo) <= y else lo - e


def find_int_by_bisection(f, lo, hi, y):
    """Find maximal int x in [lo, hi] such that f(x) <= y.

    Note: f must be monotonic within the range [lo, hi].

    """
    _check_bisection_bounds(f, lo, hi, y)
    hi0 = hi  # Save upper bound.
    while lo < hi:
        mid = lo + ((hi - lo) >> 1)
        if f(mid) <= y:
            lo = mid + 1
        else:
            hi = mid - 1
    return lo if lo <= hi0 and f(lo) <= y else lo - 1


def _check_bisection_bounds(f, lo, hi, y):
    if lo > hi:
        raise ValueError("lower bound is above upper bound")
    if y < f(lo):
        raise ValueError("solution is below lower bound")
    if y > f(hi):
        raise ValueError("solution is above upper bound")


def isqrt(y):
    """Find maximal int x > 0 such that x * x <= y."""
    if y < 0:
        raise ValueError("isqrt is not defined for negative values")

    def f(x):
        return x * x

    return find_int_by_bisection(f, 0, y, y)


def fast_pow(x, n):
    """Raise numeric x to integer power n."""
    # I first wrote this algorithm recursively and then translated it into
    # the iterative form you see in the implementation, as explained in
    # http://blog.moertel.com/posts/2013-05-11-recursive-to-iterative.html.
    #
    # For comparison, here is the recursive version:
    #
    # def fast_pow(x, n):
    #     if n == 0:
    #         return 1
    #     if n & 1:
    #         return x * fast_pow(x, n - 1)
    #     return fast_pow(x * x, n >> 1)
    m = 1
    while n > 0:
        if n & 1:
            m *= x
            n -= 1
        else:
            x *= x
            n >>= 1
    return m


def fast_gpow(x, n, mul, mul_identity):
    """Raise generalized numeric x to integer power n."""
    m = mul_identity
    while n > 0:
        if n & 1:
            m = mul(m, x)
            n -= 1
        else:
            x = mul(x, x)
            n >>= 1
    return m


# Vectors.


def dot_product(u, v):
    """Compute dot product of equal-length vectors u and v."""
    return sum(u[i] * v[i] for i in range(len(u)))


def mk_dot_product_mod(m):
    """Make a dot-product function that computes mod m."""

    def dot_product_mod(u, v):
        return sum((u[i] * v[i]) % m for i in range(len(u))) % m

    return dot_product_mod


def dot_product_mod(u, v, m):
    """Compute dot product of equal-length vectors u and v (mod m)."""
    return mk_dot_product_mod(m)(u, v)


# Matrices.


def mk_matrix_mul(dot=dot_product):
    """Make matrix multiplier using a given dot-product function."""

    def matrix_mul(A, B):
        """Compute product of matrices A and B."""
        if not len(A[0]) == len(B) > 0:
            raise ValueError("matrices are mismatched for multiplication")
        Bt = list(zip(*B))  # Transpose B to get column order.
        return [[dot(row, col) for col in Bt] for row in A]

    return matrix_mul


matrix_mul = mk_matrix_mul()  # Common-case version.


def matrix_mul_mod(A, B, m):
    """Compute product of matrices A and B (mod m)."""
    return mk_matrix_mul(mk_dot_product_mod(m))(A, B)


def identity_matrix(n):
    """Make n*n identity matrix."""
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        A[i][i] = 1
    return A


def matrix_pow(A, n, dot=dot_product):
    """Raise matrix A to the integer power n."""
    return fast_gpow(A, n, mk_matrix_mul(dot), identity_matrix(len(A)))


def matrix_pow_mod(A, n, m):
    """Raise matrix A to the integer power n (mod m)."""
    return fast_gpow(
        A, n, mk_matrix_mul(mk_dot_product_mod(m)), identity_matrix(len(A))
    )


# Combinatorics.


def binomial(n, k):
    """Compute binomial coefficient "n choose k" for integers n and k."""
    # Use the identity `C(n, k) = C(n - 1, k - 1) * n // k` as the basis for
    # a recursive algorithm to compute the coefficient. This algorithm is
    # implemented here iteratively.
    if k > n - k:
        k = n - k
    if k < 0:
        return 0
    p = 1
    n = n - k + 1
    for k in range(1, k + 1):
        p = p * n // k
        n += 1
    return p


def real_binomial(r, k):
    """Compute binomial coefficient "r choose k" for real r and integer k."""
    # Use the identity `C(r, k) = C(r - 1, k - 1) * r / k` as the basis for
    # a recursive algorithm to compute the coefficient. This algorithm is
    # implemented here iteratively.
    if k < 0:
        return 0
    p = 1.0
    r = r - k + 1
    for k in range(1, k + 1):
        p = p * r / k
        r += 1
    return p


# Number theory.


def primes_upto(n):
    """Get an increasing list of all primes <= n.

    Prefer primes_upto_at_least if you can tolerate extra primes > n.
    """
    global PRIMES, PRIME_TABLE_CUTOFF
    if n > PRIME_TABLE_CUTOFF:
        while PRIME_TABLE_CUTOFF < n:
            PRIME_TABLE_CUTOFF *= 2
        PRIMES = _prime_sieve(PRIME_TABLE_CUTOFF)
    return PRIMES[: bisect_right(PRIMES, n)]


def primes_upto_at_least(n):
    """Get an increasing list of all primes <= m for some m >= n."""
    return PRIMES if n <= PRIME_TABLE_CUTOFF else primes_upto(n)


def _prime_sieve(n):
    """Get an increasing list of all primes <= n."""
    candidates = [True] * (n + 1)
    primes = []
    for i in range(2, n + 1):
        if candidates[i]:
            primes.append(i)
            for j in range(i + i, n + 1, i):
                candidates[j] = False
    return primes


PRIME_TABLE_CUTOFF = 2**16
PRIMES = _prime_sieve(PRIME_TABLE_CUTOFF)


def prime_factors(n):
    """Get an ordered list of the prime factors of n."""
    if n < 1:
        raise ValueError("n=%r cannot have prime factors" % (n,))
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


# Disjoint sets, supporting union and find operations.


def mk_union_find_domain(elems):
    """Make union and find methods over disjoint singleton sets from elems."""
    d = dict((e, e) for e in elems)
    r = dict((e, 1) for e in d)  # ranks

    def union(u, v):
        urep = find(u)
        vrep = find(v)
        if urep != vrep:
            rank_diff = r[urep] - r[vrep]
            if rank_diff < 0:
                d[urep] = vrep
            else:
                d[vrep] = urep
                if rank_diff == 0:
                    r[urep] += 1

    def find(u):
        urep = d[u]
        if urep != u:
            urep = d[u] = find(urep)
        return urep

    return union, find
