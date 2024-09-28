#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-11-15

"""Solution to "Stack with Maximum Operation" problem, EPI problem 8.1.

Problem: Design a stack that supports a max operation, which returns
the maximum value stored in the stack, and throws an exception if the
stack is empty. Assume elements are comparable. All operations must be
O(1) time. You can use O(n) additional space, beyond what is required
for the elements themselves.

Discussion.

"""

class Error(Exception):
    """Base class for all MaxStack exceptions."""

class EmptyStack(Error):
    """Thrown when you try to extract an element from an empty MaxStack."""

class MaxStack(object):
    """Stack that supports a max query over all elements."""

    # The idea is this:  When we push a new element x onto the stack,
    # it could be the new maximum element, so we must compute a new
    # whole-stack maximum, call it y.  This we store with x as the
    # pair (x, y) for instant access.  Under this scheme, the current
    # whole-stack maximum will always be the top y value on the stack.
    # All operations preserve this invariant.  Thus computing the new
    # whole-stack maximum is just new_y = max(x, prev_y), an O(1)-time
    # operation.  Later, when we need to find the whole-stack maximum,
    # we can just return the top y value.  When elements x are popped,
    # their corresponding y values are removed, as well, restoring the
    # stack to a previous state in which the invariant held and thus
    # still holds.

    def __init__(self):
        self.stack = []

    def __len__(self):
        return len(self.stack)

    def push(self, x):
        stack_max = x if not self else max(x, self.max())
        self.stack.append((x, stack_max))

    def pop(self):
        self._require_nonempty()
        return self.stack.pop()[0]  # return x, discard stack_max

    def max(self):
        self._require_nonempty()
        return self.stack[-1][1]    # return top stack_max value

    def _require_nonempty(self):
        if not self:
            raise EmptyStack()


def test():
    """Test MaxStack by comparing it to an oracle in many random-use trials."""

    from math import factorial
    from random import randrange
    from nose.tools import raises, assert_equal

    for N in range(8):

        for _ in range(factorial(N)):

            # set up a test case of N pushes intermixed with some
            # number of pops (about half as many on average)
            mstack = MaxStack()
            oracle = []  # use built-in Python stack as oracle
            xs = [randrange(N) for _ in range(N)]  # elems to push

            def assert_mstack_matches_oracle():
                assert_equal(len(oracle), len(mstack))
                if oracle:
                    assert_equal(max(oracle), mstack.max())

            # play out randomized test scenario, comparing impl to
            # oracle, until we exhaust our supply of elems to push
            while True:

                assert_mstack_matches_oracle()

                if not xs:
                    break  # we've exhausted our elem supply

                die_roll = randrange(3)
                if die_roll < 2:
                    # push 2/3rd of time
                    x = xs.pop()
                    oracle.append(x)
                    mstack.push(x)
                else:
                    # pop 1/3rd of time
                    if oracle:
                        ox = oracle.pop()
                        x = mstack.pop()
                        assert_equal(ox, x)
                    else:
                        # empty stacks must raise exception on pop and max
                        raises(EmptyStack)(mstack.pop)()
                        raises(EmptyStack)(mstack.max)()

                # wrap around to check our stack vs. oracle after op
