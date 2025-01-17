from simulate_seven_sided_die import rand7

import collections


def test_rand7():
    # Generate a sample of random draws and compute its distribution.
    N = 10000
    counts = collections.Counter(rand7() for _ in range(N))
    # All value counts must be in the range 1 to 7.
    assert sorted(counts) == list(range(1, 8))
    # The counts must be approximately equally distributed.
    expected_mean_count = N / 7
    for count in list(counts.values()):
        assert 0.9 * expected_mean_count < count < 1.1 * expected_mean_count
