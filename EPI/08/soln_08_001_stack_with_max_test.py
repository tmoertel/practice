from soln_08_001_stack_with_max import EmptyStack, MaxStack

from math import factorial
import pytest
from random import randrange


def test_stack_with_max():
    """Test MaxStack by comparing it to an oracle in many random-use trials."""

    for N in range(8):
        for _ in range(factorial(N)):
            # Set up a test case of N pushes intermixed with some
            # number of pops (about half as many on average).
            mstack = MaxStack()
            oracle = []  # use built-in Python stack as oracle
            xs = [randrange(N) for _ in range(N)]  # elems to push

            def assert_mstack_matches_oracle():
                assert len(oracle) == len(mstack)
                if oracle:
                    assert max(oracle) == mstack.max()

            # Play out randomized the test scenario, comparing our impl to
            # our oracle, until we exhaust our supply of elems to push.
            while True:
                assert_mstack_matches_oracle()

                if not xs:
                    break  # We've exhausted our elem supply.

                die_roll = randrange(3)
                if die_roll < 2:
                    # Push 2/3rd of time.
                    x = xs.pop()
                    oracle.append(x)
                    mstack.push(x)
                else:
                    # Pop 1/3rd of time.
                    if oracle:
                        ox = oracle.pop()
                        x = mstack.pop()
                        assert ox == x
                    else:
                        # Empty stacks must raise exception on pop and max.
                        pytest.raises(EmptyStack, mstack.pop)
                        pytest.raises(EmptyStack, mstack.max)

                # Wrap around to check our stack vs. oracle after op.
