from mapsandsets import GrabBag

import pytest


def test_grabbag():
    b = GrabBag()

    for x in range(5):
        # At this point, b has no x values and one y value for 0 <= y < x.
        assert x not in b
        pytest.raises(ValueError, lambda: b.remove(x))

        # When x is not in b, x must not be one of the random possibilities.
        if x == 0:
            pytest.raises(ValueError, b.random_val)  # b is empty.
        else:
            for _ in range(1000):
                if b.random_val() == x:
                    raise Exception("got {} as random value".format(x))

        b.insert(x)  # 1 x value in b
        assert x in b

        b.insert(x)  # 2 x values in b
        assert x in b

        b.remove(x)  # 1 x values in b
        assert x in b

        # When x is in b, x must be one of the random possibilities.
        for _ in range(1000):
            if b.random_val() == x:
                break
        else:
            raise Exception("never got {} as random value".format(x))

        # Remove final copy of x.
        b.remove(x)

        # Leave one x around for the next round of tests on x + 1.
        b.insert(x)
