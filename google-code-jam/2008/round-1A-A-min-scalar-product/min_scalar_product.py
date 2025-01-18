#!/usr/bin/python
#
# Tom Moertel <tom@moertel.com>
# 2013-03-31


"""Solution to "Minimum Scalar Product" problem
http://code.google.com/codejam/contest/32016/dashboard#s=p0

The key is to pair off the least elements of one vector with the
greatest of the other.

Proof.  We proceed by contradiction.  First, assume that Y is the
minimum scalar product (MSP) of U and V, and in Y the least element of
U, u, is *not* paired with the maximum element of V, v, but instead
with some smaller element v' < v.  Since v is not paired with u, it
must be paired with some greater element u' > u.  Thus the
contribution of u, u', v, and v' to Y is

  u*v' + u'*v.

However, since u*v < u*v' and u'*v' < u'*v, we can reduce both of the
terms in the sum above by re-pairing u with v and u' with v',
contradicting our assumption that Y is the MSP.  Therefore, in the MSP
of U and V, the least element of U must be paired with the greatest
element in V.

A similar argument applies to rest of U and V.  Once we pair off u
with v, the remaining elements of U and V represent smaller vectors U'
and V' whose MSP must account for the rest of U and V's MSP; that is:

  MSP(U, V) = u*v + MSP(U', V')

Thus we apply the same reasoning to MSP(U', V') and so on, until we
have paired all of U's elements with V's.

"""

import fileinput


def main():
    for i, p in enumerate(read_problems(fileinput.input()), 1):
        y = solve(p)
        print("Case #%r: %r" % (i, y))


def solve(problem):
    us, vs = problem
    return sum(u * v for u, v in zip(sorted(us), sorted(vs, reverse=True)))


def read_problems(lines):
    N = int(next(lines))
    for _ in range(N):
        yield read_problem(lines)


def read_problem(lines):
    next(lines)  # skip vector length; it's implicit in following lines

    def read_two_vectors():
        for _ in range(2):
            yield [int(s) for s in lines.next().split()]

    return list(read_two_vectors())


if __name__ == "__main__":
    main()
