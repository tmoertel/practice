#!/usr/bin/python
#
# Tom Moertel <tom@moertel.com>
# 2013-04-03


"""Solution to "Alien Language" problem
http://code.google.com/codejam/contest/90101/dashboard#s=p0

The idea is to build a prefix tree of the alien language and then, for
each pattern, perform a parallel depth-first search over this tree and
the tree formed from the pattern, pruning the search where the two
trees do not correspond, and counting each leaf we reach as a match.

"""

import fileinput
import itertools


def main():
    lang, pats = read_problem(fileinput.input())
    for i, soln in enumerate(solve(lang, pats), 1):
        print("Case #%r: %s" % (i, soln))


def solve(lang, pats):
    tree = prefix_tree(lang)
    for pat in pats:
        matches = 0
        stack = [(parse_pattern(pat), tree)]
        while stack:
            tokens, root = stack.pop()
            if not tokens:
                matches += 1
            else:
                lead_token, remaining_tokens = tokens[0], tokens[1:]
                for c in lead_token:
                    if c in root:
                        stack.append((remaining_tokens, root[c]))
        yield matches


def parse_pattern(pat):
    tokens = []
    while pat:
        if pat[0] == "(":
            i = pat.index(")")
            tokens.append(pat[1:i])
            pat = pat[i + 1 :]
        else:
            tokens.append(pat[0])
            pat = pat[1:]
    return tokens


def prefix_tree(words):
    tree = {}
    for word in words:
        root = tree
        for c in word:
            root = root.setdefault(c, {})
    return tree


def read_problem(lines):
    L, D, N = list(map(int, lines.next().split()))
    lang = set(" ".join(itertools.islice(lines, D)).split())
    assert all(len(word) == L for word in lang)
    pats = " ".join(itertools.islice(lines, N)).split()
    return lang, pats


if __name__ == "__main__":
    main()
