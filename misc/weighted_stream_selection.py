# Suggested code may be subject to a license. Learn more: ~LicenseLog:3601272973.
# Suggested code may be subject to a license. Learn more: ~LicenseLog:3442675363.
"""Write a function to generate a weighted random sample from a stream."""

import random


def select_weighted_value(weighted_values):
    """Return a randomly selected value from a stream of weighted values.

    Args:
      weighted_values: an iterable stream of (w, x) pairs, where w is a
        non-negative integer weight and x is a value.

    Returns:
      A randomly selected value. Each value's chance of being selected
      is proportional to its corresponding weight.

    Raises:
      ValueError if the stream has negative weights or lacks any
      positive weights.

    """
    no_selection = object()  # Create distinct no-selection indicator.
    selected_value = no_selection
    total_weight = 0
    for weight, value in weighted_values:
        if weight < 0:
            raise ValueError("received negative weight %r" % weight)
        total_weight += weight
        if 0 < total_weight and random.randint(1, total_weight) <= weight:
            selected_value = value
    if selected_value is no_selection:
        raise ValueError("there were no positively weighted values")
    return selected_value


"""Proof of correctness.

Suppose for input the function is given a series of non-negatively
weighted values (w_i, x_i) for i = 1..N.  Let W = sum(w_i for all i)
be greater than 0.  We want to show that, when the loop exits, each
value x_i will have had a w_i/W probability of having been selected.
Our proof will proceed by induction on N.

First, the base case of N = 1.  In this case, there is only one
value to select and thus the only properly weighted selection is
that value (provided that w_1 > 0, which our assumption that W > 0
implies when N = 1).  When the final if-statement within the loop
is evaluated, weight = total_weight = w_1, and x_1 will always be
selected since all randomly selected integers within the range
1..w_1 are less than or equal to w_1.  Thus, when N = 1, the
algorithm always returns a properly weighted selection.

As our induction hypothesis, suppose that the algorithm works for
inputs of length N - 1.  Now consider inputs of length N.  When the
loop finally exits, it will have just considered the final input value
x_N.  At that time, total_weight will have accumulated all of the
input weights and will equal W.  Therefore, when x_N was considered,
it must have been given exactly the proper w_N/W probability of having
been selected.  If x_N was selected, then, the algorithm returns a
properly weighted selection.  Otherwise, x_N can ruled out, and the
problem becomes equivalent to returning a properly weighted selection
from the remaining N - 1 inputs.  In this case, the algorithm returns
whatever was already in selected_value.  This value is the same as
what would have been returned by the algorithm had it been called on
just the first N - 1 inputs.  By our induction hypothesis, this is
also a properly weighted selection.  Q.E.D.

"""


import pytest


def test_sampling_an_empty_set_must_raise_error():
    with pytest.raises(ValueError):
        select_weighted_value([])


def test_negative_weights_must_raise_error():
    with pytest.raises(ValueError):
        select_weighted_value([(-1, "value")])


def test_zero_total_weight_must_raise_error():
    with pytest.raises(ValueError):
        select_weighted_value([(0, "value")])


def test_singleton_value_must_always_be_selected():
    for weight in range(1, 10):
        assert select_weighted_value([(weight, "value")]) == "value"


def test_zero_weighted_value_must_never_be_selected():
    for weight in range(1, 10):
        assert select_weighted_value([(0, "x"), (weight, "value")]) == "value"
        assert select_weighted_value([(weight, "value"), (0, "x")]) == "value"
