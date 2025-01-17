from soln_15_011_levenshtein_distances import (
    levenshtein_distance1,
    levenshtein_distance2,
    levenshtein_distance3,
)


def test_levenshtein_distances():
    for ld in (levenshtein_distance1, levenshtein_distance2, levenshtein_distance3):
        assert 0 == ld("", "")
        assert 0 == ld("ab", "ab")
        assert 0 == ld("abc", "abc")

        assert 1 == ld("a", "")
        assert 1 == ld("", "b")
        assert 1 == ld("bc", "abc")
        assert 1 == ld("ac", "abc")
        assert 1 == ld("ab", "abc")
        assert 1 == ld("abc", "bc")
        assert 1 == ld("abc", "ac")
        assert 1 == ld("abc", "ab")
        assert 1 == ld("xbc", "abc")
        assert 1 == ld("axc", "abc")
        assert 1 == ld("abx", "abc")
        assert 1 == ld("abc", "xbc")
        assert 1 == ld("abc", "axc")
        assert 1 == ld("abc", "abx")

        assert 2 == ld("c", "abc")
        assert 2 == ld("a", "abc")
        assert 2 == ld("abc", "c")
        assert 2 == ld("abc", "a")
        assert 2 == ld("xxc", "abc")
        assert 2 == ld("axx", "abc")
        assert 2 == ld("xbx", "abc")
        assert 2 == ld("abc", "xxc")
        assert 2 == ld("abc", "axx")
        assert 2 == ld("abc", "xbx")
