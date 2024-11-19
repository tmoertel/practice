"""Discrete random variables that you can draw values from."""

from collections.abc import Iterable
import collections
import random
from typing import Any

TwoValues = collections.namedtuple("TwoValue", "low_weight, low, high")


class DiscreteRandomVariable:
    """Represents a discrete random variable that you can draw values from."""

    def __init__(self, value_and_weight_pairs: Iterable[tuple[Any, int]]):
        """Creates a discrete random variable.

        Args:
          value_and_weight_pairs: An iterable series of (value, weight) pairs
            specifying the wanted distribution. For example, to represent a
            fair coin toss, you could use the series `[(1, 'heads'), (1, 'tails')]`.

        REQUIRED: All weights must be integer values, at least zero, and the
        total weight of the pairs must be greater than zero.

        """
        # Convert the pairs into a list we can iterate over repeatedly.
        value_and_weight_pairs = list(value_and_weight_pairs)

        # Weights must be non-negative integers.
        assert all(isinstance(w, int) and w >= 0 for _, w in value_and_weight_pairs)

        # The distribution must have a positive total weight.
        assert any(w >= 0 for _, w in value_and_weight_pairs)

        # Rescale all weights so that they can be evenly divided by the count of
        # pairs. This will guarantee that if the weights have integer values,
        # the mean weight will have an integer value also. Note that the mean
        # after rescaling is equal to the total before scaling.
        mean_weight = sum(w for _, w in value_and_weight_pairs)
        n = len(value_and_weight_pairs)
        value_and_weight_pairs = [(v, w * n) for v, w in value_and_weight_pairs]

        # Partition the pairs by whether they are below the mean or not.
        def is_below_mean(pair):
            _, weight = pair
            return weight < mean_weight

        below_pairs = [vw for vw in value_and_weight_pairs if is_below_mean(vw)]
        not_below_pairs = [vw for vw in value_and_weight_pairs if not is_below_mean(vw)]

        # Repack the weighted pairs into a single array of mean-weighted blocks
        # each representing one or two of the original values.
        self.draw_array = []
        self.mean_weight = mean_weight
        while below_pairs:
            # While there are values having a weight w_low below the mean, there
            # must exist values having a weight w_high not below the mean. We
            # combine one of each to form a two-value block having a weight
            # w_low + w_high, which must be greater than the mean.
            v_low, w_low = below_pairs.pop()
            v_high, w_high = not_below_pairs.pop()
            self.draw_array.append(TwoValues(w_low, v_low, v_high))

            # We trim off the excess weight and add it back to the list of
            # below-mean or not-below-mean pairs, as its weight demands.
            w_leftover = w_low + w_high - mean_weight
            (below_pairs if w_leftover < mean_weight else not_below_pairs).append(
                (v_high, w_leftover)
            )

        # When no more below-mean pairs exist, the `not_below_pairs` list may
        # still contain some pairs having a weight of exactly the mean. These
        # we add to the draw array as degenerate two-value blocks having a
        # low value that occupies the entire block.
        self.draw_array.extend(TwoValues(w, v, None) for v, w in not_below_pairs)

    def draw(self, randrange=random.randrange):
        """Returns a value from the distribution at random.

        Args:
          randrange: (optional) A function that when called with an integer
            argument `n` returns a random integer from the set {0, 1, 2, ..., n - 1}.
            This function will be used to provide the randomness used to draw the
            value from the distribution. Defaults to `random.randrange`.

        GUARANTEED to call `randrange` exactly once and perform only
        constant-time work.

        """
        n = len(self.draw_array)
        k = randrange(n * self.mean_weight)
        block = self.draw_array[k // self.mean_weight]
        value = block.low if k % self.mean_weight < block.low_weight else block.high
        return value


def test_discrete_random_variables_exactly_represent_their_underlying_distributions():
    import math
    from random import randint, shuffle

    # We will test distributions having up to this many values. Note that the number
    # of internal test instances grows as the factorial of this setting, so larger
    # numbers will require longer test times that may be prohibitive.
    MAX_NUM_VALUES = 7

    for num_values in range(1, MAX_NUM_VALUES):
        # To get good coverage, we will test factorial(num_values) instances.
        for _ in range(math.factorial(num_values)):
            # Generate a test instance: a series of (value, weight) pairs.
            values = list(range(num_values))
            shuffle(values)
            weights = [randint(0, 20) for _ in range(num_values)]
            weights[0] += 1  # Guarantee that total weight is greater than zero.
            values_and_weights = list(zip(values, weights))

            # In case we have a failure, emit the test instance.
            print(repr(values_and_weights))

            # Create the random variable we'll be testing.
            random_variable = DiscreteRandomVariable(values_and_weights)

            # To test this variable, we will override Python's normal
            # random-number generation logic and instead sweep uniformly over
            # the range of possible numbers Python could generate. This allows
            # us to observe exactly the distribution represented by the random
            # variable we're testing. This test relies on knowledge of the
            # variable's internal logic, namely that if its internal
            # distribution has n weights and a total weight of t, then it will
            # request random integers X in the range 0 <= X < n * t.

            total_weight = sum(weights)
            actual_distribution = collections.Counter(
                [
                    random_variable.draw(lambda _: i)
                    for i in range(num_values * total_weight)
                ]
            )
            expected_distribution = collections.Counter(
                {
                    value: num_values * weight
                    for value, weight in values_and_weights
                }
            )
            assert actual_distribution == expected_distribution
