#!/usr/bin/evn python

import operator



def product_div_elems(xs):
    prod = product(xs)
    return list(prod / x for x in xs)

def product(xs):
    return reduce(operator.mul, xs, 1)

def test_product_div_elems():
    a = [1,2,3,4,5,6,7,8,9,10]
    print product_div_elems(a)



def max_consecutive_sum(xs):
    """Return the maximum sum of consecutive integers in a series."""
    current_sum = current_max = 0
    for x in xs:
        current_sum += x
        current_max = max(current_max, current_sum)
        current_sum = max(0, current_sum)  # start fresh series if it's better
    return current_max





### Find the n points closest to origin in a set of millions of
### points in 3 dimensional space.


def find_closest_to_origin__naive(points, n=5):
    """Find the points closest to the origin in an any-dimensional space.

    Running time:  O(N lg N) for len(points) = N.

    """
    def sq_dist(point):
        return sum(x * x for x in point)
    return sorted(points, key=sq_dist)[:n]


import heapq
def find_closest_to_origin(points, n=5):
    """Find the points closest to the origin in an any-dimensional space.

    Running time:  O(N lg n) (= O(N) for len(points) = N and n < const k).

    """
    def sq_dist(point):
        return sum(x * x for x in point)
    return heapq.nsmallest(n, points, key=sq_dist)

def find_closest_to_origin_old(points, n=5):
    """Find the points closest to the origin in an any-dimensional space.

    Running time:  O(N lg n) ~ O(N) for len(points) = N and small n.

    """
    def sq_dist(point):
        return sum(x * x for x in point)
    def score(point):
        return (-sq_dist(point), point)
    closest = map(score, points[:n])
    heapq.heapify(closest)
    for pt in points[n:]:
        heapq.heappushpop(closest, score(pt))
    return [scored_pt[1] for scored_pt in sorted(closest, reverse=True)]


### Write a function that takes in an array of ints and an int, then
### find two integers in the array that when you sum them, would equal
### to that int that was passed in. Return true, if two numbers like
### that exist, and false if not.
###
### Source: http://www.glassdoor.com/Interview/Amazon-com-Interview-Questions-E6036_P2.htm


def do_pairs_sum_to(xs, t):
    """Return True iff any pair of elements in xs adds to t."""
    seen = set()
    for x in xs:
        if t - x in seen:
            return True
        seen.add(x)
    return False

# Claims:
#
# (1) If there exist in xs two elements x[i] and x[j], such that i < j
#     <= len(xs) and x[i] + x[j] == t, then do_pairs_sum_to will
#     return True.
#
# (2) If not, it will return False.
#
# Proof of (1).  Proceed by contradiction.  Assume (a) that x[i] +
# x[j] == t, for some i < j, and (b) that the function returned False.
# Since the function didn't return True, we infer that t - x[j] must
# not have been previously seen when the function vistied element j.
# But, since i < j and by (a) we know x[i] equals t - x[j], t - x[j]
# must have been seen before, leading to a contradiction.
#
# Proof of (2). Again, by contradiction.  Assume (a) that there exist
# no indices i and j, such that i < j and x[i] + x[j] == t and (b)
# that the function returned True.  If the function returned True,
# there must have been some j for which t - x[j] was previously seen.
# Therefore, there must have been some i < j such that x[i] = t - x[j].
# But this contradicts (a).


### Implement integer division (without, of course, using the built-in
### division operator).

def div_naive(x, y):
    """Return floor(x/y)."""
    if y == 0:
        raise ZeroDivisionError()
    neg = (x < 0) != (y < 0)
    x = abs(x)
    y = abs(y)
    q = 0
    while q * y < x:
        q += 1  # slow and horrible linear search for quotient
    if q * y != x and not neg:
        q -= 1
    if neg:
        q = -q
    return q

def div_reasonable(x, y):
    """Return floor(x/y)."""
    if y == 0:
        raise ZeroDivisionError()

    # convert to all-positive case
    neg = (x < 0) != (y < 0)
    remainder = abs(x)
    y = abs(y)

    # find b = pow of 2 >= remainder
    b = 1
    while b < remainder:
        b <<= 1

    # extract successively lower powers of two times y from remainder
    # until nothing remains
    q = 0
    while b and remainder:
        d = remainder - b * y
        if d >= 0:
            q |= b
            remainder = d
        b >>= 1

    # fix the quotient's sign if needed
    if neg:
        q = -q
        if q * y != -abs(x):
            q -= 1  # mimic Python's round-down semantics

    # we're done
    return q

def div(x, y):
    """Return floor(x/y)."""
    if y == 0:
        raise ZeroDivisionError()

    # convert to all-positive case
    neg = (x < 0) != (y < 0)
    remainder = abs(x)
    y = abs(y)

    # find b = pow of 2 >= remainder, then scale y by that power
    b = 1
    yb = y
    while b < remainder:
        b <<= 1
        yb <<= 1

    # extract successively lower powers of two times y from remainder
    # until nothing remains
    q = 0
    while b and remainder:
        d = remainder - yb
        if d >= 0:
            q |= b
            remainder = d
        b >>= 1
        yb >>= 1

    # fix the quotient's sign if needed
    if neg:
        q = -q
        if remainder:
            q -= 1  # mimic Python's round-down semantics

    # we're done
    return q


def test_div():
    for x in xrange(-100, 101):
        for y in xrange(-100, 101):
            if y == 0:
                continue
            if div(x, y) != x/y:
                print('div(%r, %r) == %r != %r' % (x, y, div(x, y), x/y))
                return


### Find all pairs of nodes that sum upto twice the root value in a BST

# my BST rep = None | (val, left subtree, right subtree)

def find_bst_pairs_twice_root(bst):
    elems = flatten_preorder(bst)
    def search():
        if elems:
            target = 2 * elems[0]
            seen = dict()  # maintains counts of times we've seen values
            for x in elems:
                y = target - x
                for _ in xrange(seen.get(y, 0)):
                    yield (x, y)
                seen.setdefault(x, 0)
                seen[x] += 1
    return list(search())

def flatten_preorder(bst):
    out = list()
    def pre(bst):
        if bst is not None:
            out.append(bst[0])
            pre(bst[1])
            pre(bst[2])
    pre(bst)
    return out



### You are given an array that represents bills in certain currency
### (For example 1, 2, 5, 10) and an amount, for example 17. You
### should output the number of possible combinations of bills that
### sum to the given amount.
###
### For example, {10, 5, 2} is valid combination, {10, 5, 1 ,1} also.

import functools


def memoize(fn):
    cache = dict()
    @functools.wraps(fn)
    def memoized_fn(*args):
        args = tuple(args)
        if args in cache:
            return cache[args]
        return cache.setdefault(args, fn(*args))
    return memoized_fn


def make_change(denominations, desired_total):
    ds = sorted(denominations, reverse=True)
    solns = []
    def search(change, ds, total):  # memoize
        if total == 0:
            solns.append(change)
        elif ds and total > 0:
            search(change + [ds[0]], ds, total - ds[0])
            search(change, ds[1:], total)
    search([], ds, desired_total)
    return solns
