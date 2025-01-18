#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-03-31


"""Solution to "Milkshakes" problem
http://code.google.com/codejam/contest/32016/dashboard#s=p1

Claim 1.  If all customers like at least one unmalted shake, making
all batches unmalted satisfies all customers.

Claim 2.  If a customer's only like is a malted shake, and if there is
a solution, then in that solution the batch for that shake must be
prepared malted.

In light of these claims, we can arrive at an optimal solution by
finding a customer whose only like is a malted shake, making the
corresponding batch malted, and removing from the problem all
customers satisfied by that choice, resulting in a new smaller
problem, to which we can apply the same strategy.  If we can find no
such customer, all remaining customers (by Claim 1) can be satisfied
by unmalted batches, and we have a solution, and it must be optimal
since we have made no malted batches but those strictly required
(Claim 2).  However if making one of the required malted batches
eliminates the last chance to satisfy some other customer, no solution
is possible.

"""

import collections
import fileinput
import sys


def main():
    sys.setrecursionlimit(2000)
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        s = solve(p)
        print("Case #%r: %s" % (i, s))


def solve(problem):
    N, _M, likes_by_cust = problem
    likes_by_flavor = collections.defaultdict(set)
    customers_liking_only_a_malt = []
    for cust, likes in likes_by_cust.items():
        for flavor, is_malted in likes:
            likes_by_flavor[flavor].add((cust, is_malted))
        if len(likes) == 1:
            flavor, is_malted = list(likes)[0]
            if is_malted:
                customers_liking_only_a_malt.append((cust, flavor))
    malts = set()
    while customers_liking_only_a_malt:
        cust, flavor = customers_liking_only_a_malt.pop()
        if cust not in likes_by_cust:
            continue  # customer is already satisfied
        malts.add(flavor)
        for cust, is_malted in likes_by_flavor[flavor]:
            if cust in likes_by_cust:
                if is_malted:
                    del likes_by_cust[cust]  # we've just satisfied this cust
                else:
                    likes_by_cust[cust].remove((flavor, is_malted))
                    if len(likes_by_cust[cust]) == 0:
                        return "IMPOSSIBLE"
                    elif len(likes_by_cust[cust]) == 1:
                        flavor0, is_malted0 = list(likes_by_cust[cust])[0]
                        if is_malted0:
                            customers_liking_only_a_malt.append((cust, flavor0))
    return " ".join(("1" if flavor in malts else "0") for flavor in range(1, N + 1))


def read_problems(lines):
    C = int(next(lines))
    for _ in range(C):
        yield read_problem(lines)


def read_problem(lines):
    N = int(next(lines))  # flavor count
    M = int(next(lines))  # customer count
    cust_likes = read_cust_likes(M, lines)
    return N, M, cust_likes


def read_cust_likes(M, lines):
    likes = collections.defaultdict(set)
    for cust in range(M):
        like_spec = list(map(int, lines.next().split()))
        T = like_spec.pop(0)
        spec_items = iter(like_spec)
        for _ in range(T):
            likes[cust].add((next(spec_items), bool(next(spec_items))))
    return likes


if __name__ == "__main__":
    main()
