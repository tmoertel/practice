from soln_12_014_smallest_subarray_covering_set import smallest_subarray_covering_set


def test_smallest_subarray_covering_set():
    S = smallest_subarray_covering_set
    assert S("a", "") == (0, -1)  # 0-length covering exists
    assert S("", "a") is None
    assert S("..a", "a") == (2, 2)
    assert S("aa", "a") == (0, 0)  # when many ranges are smallest, earliest wins
    assert S("aab", "ab") == (1, 2)
    assert S("aab", "aba") == (1, 2)  # dupes in Q must not affect result
    assert S("acaaaabc", "abc") == (5, 7)
    assert S("acaaaabbc", "abc") == (5, 8)
    assert S("acaaaabbcccc", "abc") == (5, 8)
