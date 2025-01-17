import pytest
from parser_combinators import Char, Zero, Many, Many1


def test_char():
    p = Char("a")
    assert list(p("abc", 0)) == [("a", 1)]
    assert list(p("bcd", 0)) == []
    assert list(p("", 0)) == []
    assert list(p("a", 1)) == []


def test_zero():
    p = Zero()
    assert list(p("abc", 0)) == []
    assert list(p("", 0)) == []
    assert list(p("a", 1)) == []


def test_bind():
    p = Char("a") + Char("b")
    assert list(p("abc", 0)) == [(("a", "b"), 2)]
    assert list(p("acb", 0)) == []
    assert list(p("cba", 0)) == []
    assert list(p("ab", 1)) == []
    assert list(p("ab", 0)) == [(("a", "b"), 2)]
    p = Char("a") + (Char("b") + Char("c"))
    assert list(p("abc", 0)) == [(("a", ("b", "c")), 3)]
    p = (Char("a") + Char("b")) + Char("c")
    assert list(p("abc", 0)) == [((("a", "b"), "c"), 3)]


def test_choice():
    p = Char("a") | Char("b")
    assert list(p("abc", 0)) == [("a", 1)]
    assert list(p("bcd", 0)) == [("b", 1)]
    assert list(p("cde", 0)) == []
    p = Char("a") | Zero()
    assert list(p("abc", 0)) == [("a", 1)]
    assert list(p("bcd", 0)) == []
    p = Zero() | Char("b")
    assert list(p("abc", 0)) == []
    assert list(p("bcd", 0)) == [("b", 1)]


def test_many():
    p = Many(Char("a"))
    assert list(p("aaabc", 0)) == [(["a", "a", "a"], 3)]
    assert list(p("bc", 0)) == [([], 0)]
    assert list(p("", 0)) == [([], 0)]
    assert list(p("aaa", 0)) == [(["a", "a", "a"], 3)]
    assert list(p("aaabbb", 0)) == [(["a", "a", "a"], 3)]
    p = Many(Char("a") | Char("b"))
    assert list(p("abababc", 0)) == [(["a", "b", "a", "b", "a", "b"], 6)]


def test_many1():
    p = Many1(Char("a"))
    assert list(p("aaabc", 0)) == [(["a", "a", "a"], 3)]
    assert list(p("bc", 0)) == []
    assert list(p("aaa", 0)) == [(["a", "a", "a"], 3)]
    assert list(p("", 0)) == []
    assert list(p("aaabbb", 0)) == [(["a", "a", "a"], 3)]
    p = Many1(Char("a") | Char("b"))
    assert list(p("abababc", 0)) == [(["a", "b", "a", "b", "a", "b"], 6)]
    assert list(p("cde", 0)) == []
