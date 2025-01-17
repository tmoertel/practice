from soln_07_001_merge_two_sorted_lists import Cons, merge


# We test the following property claim:
# For all sorted singly linked lists xs and ys, merge(xs, ys) produces results
# identical to sorting the combined elements of xs and ys.
def test_merge_sorted_lists():
    for xs in powerset(list(range(7))):
        for ys in powerset(list(range(7))):
            spec = sorted(xs + ys)
            result = merge(from_seq(xs), from_seq(ys))
            assert to_pylist(result) == spec


# Helper functions.


def powerset(xs):
    "Generates the sets within the powerset of the set `xs`."
    if not xs:
        yield []
    else:
        x, rest = xs[0], xs[1:]
        for ys in powerset(rest):
            yield [x] + ys
        for ys in powerset(rest):
            yield ys


def from_seq(xs):
    """Makes a linked list from a Python sequence."""
    head = None
    for x in reversed(xs):
        head = Cons(x, head)
    return head


def to_pylist(xs):
    """Converts a linked list into a Python list (array)."""
    ys = []
    while xs:
        ys.append(xs.head)
        xs = xs.tail
    return ys
