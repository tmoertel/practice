from soln_10_001_merge_stock_trades import merge_iters

from itertools import chain
from math import factorial
from random import randrange


# For all lists of sorted lists xss, merge_iters(xss) must produce results
# identical to sorting the concatenation of the lists within xss.
# Here we test this claim for many randomly generated values of xss.
def test_merge_iters():
    for N in range(8):
        for _ in range(factorial(N)):
            xss = []
            for _ in range(N):
                size = randrange(2 * N + 1) + 1
                xs = sorted([randrange(size) for _ in range(randrange(size))])
                xss.append(xs)
            sorted(chain(*xss)) == list(merge_iters(xss))
