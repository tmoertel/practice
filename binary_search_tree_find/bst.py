#!/usr/bin/env python
# Tom Moertel <tom@moertel.org>
# 2011-12-12


"""Solve a simple binary-search-tree exercise.

Problem:

    Given a binary search tree, write code to find a particular
    value.  If you can't find the value, then return me the next
    smallest value.  For example, if the tree contains 1, 2, 3, and 5,
    and I ask for 4, then return 3.

    Source:  http://news.ycombinator.com/item?id=3339418

"""

import unittest


def find_min(bst, val, next_smallest=None):
    """Get closest match <= val in bst or, failing that, next_smallest."""
    if bst is None:
        return next_smallest
    elif val == bst.val:
        return val
    elif val < bst.val:
        return find_min(bst.left, val, next_smallest)
    else:
        return find_min(bst.right, val, bst.val)


"""Correctness proof.

Claim: find_min(bst, val, next_smallest) returns val if it exists in
the binary search tree bst or, failing that, the next smallest value
in bst or, failing that, next_smallest, assuming next_smallest <=
min(bst).  (Note:  We let None be the smallest possible value.)

Proof:  We proceed by induction on the height of the tree.  Assume we
know that find_min(bst, val, next_smallest) is correct for
height(bst) == N && next_smallest < val && next_smallest <= min(bst).

Base case:  height(bst) == 0.  Trivially correct:  next_smallest.

Now we try height(bst) == N + 1.  There are three cases:

Case 1:  val == bst.val.  Here we return val, which is obviously correct.

Case 2: val < bst.val.  Here we know that bst.val > val and cannot be
a match or even the next-smallest match.  Therefore, this node and its
right subtree cannot contribute to the result, and find_min of the
the whole tree bst must be the same as of its subtree bst.left:

   find_min(bst, val, next_smallest) = find_min(bst.left, val, next_smallest).

Since the left subtree has height N, next_smallest <= min(bst) <=
min(bst.left), and next_smallest is unchanged and therefore still <=
val, our induction hypothesis holds, and this case is correct.

Case 3: val > bst.val.  Here we know that bst.val < val and cannot be
a match, but it must at least as good as the current best
next-smallest match, since it's smaller than val and yet it is at
least as large as min(bst), which is at least as large as our current
next_smallest.  Therefore, the original call must equal find_min of
the right subtree with the improved next_smallest:

   find_min(bst, val, next_smallest) = find_min(bst.right, val, bst.val).

Again, since the right subtree is of height N and bst.val (our new
next_smallest) is < val and also <= min(bst.right), our induction
hypothesis holds, and this final case is correct, too.

Q.E.D.

"""


# Non-recursive translations of the find_min


def find_min_iterative(bst, val, next_smallest=None):
    while True:
        if bst is None:
            return next_smallest
        elif val == bst.val:
            return val
        elif val < bst.val:
            bst = bst.left
        else:
            bst, next_smallest = bst.right, bst.val


def find_min_iterative2(bst, val, next_smallest=None):
    while bst is not None:
        if val == bst.val:
            return val
        elif val < bst.val:
            bst = bst.left
        else:
            bst, next_smallest = bst.right, bst.val
    return next_smallest


# BST implementation and tests


class BSTNode(object):
    """Binary search tree node."""

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return "(%s, %r, %r)" % (self.val, self.left, self.right)

    def is_bst(self):
        """Test whether the node represents a binary search tree."""
        return _is_bst(self)

    @classmethod
    def from_str(cls, s):
        tree = cls._parse(s)[0]
        if tree is None or tree.is_bst():
            return tree
        return None  # reject trees that aren't BSTs

    @staticmethod
    def _parse(s):
        s = s.lstrip()
        if s[:1] == "(":
            val, s = s[1:].split(",", 1)
            left, s = BSTNode._parse(s)
            _, s = s.split(",", 1)
            right, s = BSTNode._parse(s)
            s = s.lstrip()
            if s[:1] == ")":
                return BSTNode(val, left, right), s[1:]
        return None, s


def _is_bst(tree, min_val=None, max_val=None):
    """Test whether a tree represents a binary search tree."""
    if tree is None:
        return True
    return (
        (min_val is None or tree.val >= min_val)
        and (max_val is None or tree.val <= max_val)
        and _is_bst(tree.left, min_val=min_val, max_val=tree.val)
        and _is_bst(tree.right, min_val=tree.val, max_val=max_val)
    )


TEST_CASES = [
    # (expected_result, val, bst_tree_spec)
    (None, "c", ""),
    ("c", "c", "(c,,)"),
    ("a", "c", "(a,,)"),
    (None, "c", "(d,,)"),
    ("a", "c", "(d,(a,,),)"),
    ("c", "c", "(d,(c,,),)"),
    (None, "b", "(d,(c,,),)"),
    ("a", "c", "(a,,(d,,))"),
    ("c", "c", "(c,,(d,,))"),
    (None, "c", "(d,,(d,,))"),
    ("a", "c", "(a,,(d,,))"),
    (None, "a", "(c,(b,,),(d,,))"),
    ("a", "b", "(c,(a,,),(d,,))"),
    ("c", "c", "(c,(a,,),(d,,))"),
    ("d", "d", "(c,(a,,),(d,,))"),
    ("d", "e", "(c,(a,,),(d,,))"),
    (None, "a", "(c,(b,,),(d,,))"),
    (None, "c", "(a,(d,,),)"),  # not a valid BST
    (None, "c", "(c,(a,,(d,,)),)"),  # not a valid BST
]


class Tests(unittest.TestCase):
    def test_cases(self):
        for f in find_min, find_min_iterative, find_min_iterative2:
            for case in TEST_CASES:
                expected_result, val, bst_tree_spec = case
                bst = BSTNode.from_str(bst_tree_spec)
                result = f(bst, val)
                self.assertEqual(
                    result,
                    expected_result,
                    msg=("%s: %r -> %r" % (f.__name__, case, result)),
                )


if __name__ == "__main__":
    unittest.main()
