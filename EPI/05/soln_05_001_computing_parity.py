#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-10-22

r"""Solution to "Computing Parity" problem, 5.1 from EPI.

The problem is this:

    How would you go about finding the parity of a very large number
    of 64-bit nonnegative integers?

Discussion.

The parity of a bunch of bits is the sum of the bits, modulo 2.  So,
given a large number of 64-bit nonnegative integers, say an array A of
length N, we could compute their parity with the following naive code:

    def array_parity(A):
      bit_total = 0
      for elem in A:
        for j in xrange(64)
          bit_total += bit(elem, j)
      return bit_total % 2

In other words, we're computing

    N-1   63
    ====  ====
    \     \
     >     >    bit(A[i], j) (mod 2)
    /     /
    ====  ====
    i=0   j=0

This method requires 64 N fairly expensive operations, each involving
a shift and addition.  Can we do better?

Yes.  Look at the summation above.  We can visualize it as an N-by-64
matrix of bits that we scan row by row, adding the bits in each row to
the running total.  But we could just as well compute the sum column
by column, in effect reordering the two summations:

    63    N-1
    ====  ====
    \     \
     >     >     bit(A[i], j) (mod 2)
    /     /
    ====  ====
    j=0   i=0

Now each column accumulates its own running total, and these column
totals are combined to give the final sum.  Since the final sum is to
be taken modulo 2, we can compute its constituent column totals modulo
2, as well.  And, addition of bits modulo 2 is the same as XOR.
Further, we can perform XOR for all 64 of an integer's bits in
parallel on most hardware.  So we can compute the final parity as the
parity of the single 64-bit summary of column parities.  That is:

    63
    ====
    \
     >   bit(xsum, j) (mod 2),
    /
    ====
    j=0

where xsum = XOR(A[i] for i = 0..N-1) = reduce(XOR, A, 0).

This gives us an algorithm that requires only N fast XOR operations,
with O(1) overhead to compute the final parity from the summary of
column parities.  I've implemented this algorithm in the array_parity
function below.

More discussion.

Looking at the authors' suggested solution for the problem, I can now
see that they intended their question to be read as follows:

    How would you go about finding the *parities* of a very
    large number of *individual* 64-bit nonnegative integers?

In other words, they want you to find a fast way of computing the
parity of an integer because you'll be computing a very large number
of such parities.

Well, I solved a different problem, but it was fun, too  :-)


"""

from operator import xor

def array_parity(xs):
    xsum = reduce(xor, xs, 0)
    return int_parity(xsum)

def int_parity(x):
    parity = 0
    while x:
        parity ^= 1
        x &= x - 1  # erase least-significant 1 bit
    return parity

def test():
    assert array_parity([]) == 0
    assert array_parity([0]) == 0
    assert array_parity([1]) == 1
    assert array_parity([2]) == 1
    assert array_parity([3]) == 0
    assert array_parity([0, 0]) == 0
    assert array_parity([1, 1]) == 0
    assert array_parity([2, 2]) == 0
    assert array_parity([3, 3]) == 0
