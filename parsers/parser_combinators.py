#!/usr/bin/python

"""Parser combinators for Python.

We define a parser to be a function that takes a string `s` and a
position `i` within that string to start parsing at, and it yields one
pair `(v, i')` for each possible parsing, where `v` is the resulting
value and `i'` is the first character in `s` left unconsumed.

"""

class Parser(object):
    """Base class for all parsers."""
    def __call__(self, _s, _i):
        raise NotImplementedError('Parser instances must override __call__')
    def __add__(self, other):
        return Bind(self, other)
    def __or__(self, other):
        return Choice(self, other)

class Bind(Parser):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    def __call__(self, s, i):
        for v1, i in self.p1(s, i):
            for v2, i in self.p2(s, i):
                yield (v1, v2), i

class Choice(Parser):
    """Matches what p1 does or, if p1 fails, what p2 does."""
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    def __call__(self, s, i):
        p1_produced_output = False
        for v, i in self.p1(s, i):
            p1_produced_output = True
            yield v, i
        if not p1_produced_output:
            for v, i in self.p2(s, i):
                yield v, i

class Zero(Parser):
    """Always fails."""
    def __call__(self, _s, _i):
        return  # Yields nothing.

class Char(Parser):
    """Matches a character."""
    def __init__(self, c):
        self.c = c
    def __call__(self, s, i):
        if i < len(s) and s[i] == self.c:
            yield self.c, i + 1

class Many(Parser):
    """Matches zero or more of what `p` does."""
    def __init__(self, p):
        self.p = p
    def __call__(self, s, i):
        values = []
        while True:
            for v, i in self.p(s, i):
                values.append(v)
                break
            else:
                break
        yield values, i

class Many1(Many):
    """Matches one or more of what `p` does."""
    def __call__(self, s, i):
        for v, i in Many.__call__(self, s, i):
            if v:
                yield v, i
