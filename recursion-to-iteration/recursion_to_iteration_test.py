
import functools


def test_refactored_factorial():
    fns = dict(globals())
    for fname, f in sorted(fns.items()):
        if fname.startswith("factorial"):
            print(("testing {}".format(fname)))
            for n in range(5):
                assert f(n) == functools.reduce(
                    int.__mul__, [1] + list(range(1, n + 1))
                )
        if "fib" in fname:
            print(("testing {}".format(fname)))
            assert list(map(f, list(range(10)))) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
