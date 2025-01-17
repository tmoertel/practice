from soln_12_009_anonymous_letter import is_subdocument


def test_anonymous_letter():
    for xs in "", "x", "xx", "xyx", "xyyx":
        for ys in "", "1", "2", "12", "123":
            assert is_subdocument(xs, xs + ys)
            assert is_subdocument(ys, xs + ys)
            assert is_subdocument(xs, ys + xs)
            assert is_subdocument(ys, ys + xs)
            if ys:
                assert not is_subdocument(xs + ys, xs)
                assert not is_subdocument(ys + xs, xs)
            if xs:
                assert not is_subdocument(xs + ys, ys)
                assert not is_subdocument(ys + xs, ys)
