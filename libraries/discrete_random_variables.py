"""Discrete random variables that you can draw random values from in O(1) time."""

from collections.abc import Iterable
import collections
import random
from typing import Any

# Internally, we pack two weighted values into a block of fixed total weight,
# where the low value occupies the bottom `low_weight / (low_weight +
# high_weight)` share of the block. (Since all blocks have the same fixed total
# weight, we don't need to store the high weight; it is known implicitly.)
TwoValues = collections.namedtuple("TwoValue", "low_weight, low_value, high_value")


class DiscreteRandomVariable:
    """Represents a discrete random variable that you can draw values from."""

    def __init__(self, value_and_weight_pairs: Iterable[tuple[Any, int]]):
        """Creates a discrete random variable.

        Args:
          value_and_weight_pairs: An iterable series of (value, weight) pairs
            specifying the wanted distribution. For example, to represent a
            fair coin toss, you could use the series `[('heads', 1), ('tails', 1)]`.

        REQUIRED: All weights must be integer values, at least zero, and the
        total weight of the pairs must be greater than zero.

        GUARANTEED: Constructing the instance takes time and memory linear in
        the length of the pairs series.

        """
        # Convert the pairs into a list we can iterate over repeatedly.
        value_and_weight_pairs = list(value_and_weight_pairs)

        # Weights must be non-negative integers.
        for _, w in value_and_weight_pairs:
            if not isinstance(w, int):
                raise TypeError("weights must be int values")
            if w < 0:
                raise ValueError("weights cannot be less than 0")

        # The distribution must have a positive total weight.
        if not any(w > 0 for _, w in value_and_weight_pairs):
            raise ValueError("at least one weight must be greater than 0")

        # Rescale all weights so that they can be evenly divided by the count of
        # pairs. This will guarantee that if the weights have integer values,
        # the mean weight will have an integer value also. Note that the mean
        # after rescaling is equal to the total before rescaling.
        self.mean_weight = sum(w for _, w in value_and_weight_pairs)
        n = len(value_and_weight_pairs)
        value_and_weight_pairs = [(v, w * n) for v, w in value_and_weight_pairs]

        # Partition the pairs by whether they are below the mean or not.
        def is_below_mean(pair):
            _, weight = pair
            return weight < self.mean_weight

        below_pairs = [vw for vw in value_and_weight_pairs if is_below_mean(vw)]
        not_below_pairs = [vw for vw in value_and_weight_pairs if not is_below_mean(vw)]

        # Repack the weighted pairs into a single array of blocks, each having a
        # weight of exactly the mean and each representing one or two of the
        # original values.
        self.packed_blocks = []
        while below_pairs:
            # While there are values having a weight w_low below the mean, there
            # must exist values having a weight w_high not below the mean. We
            # combine one of each to form a two-value block having a weight
            # w_low + w_high, which must be greater than the mean.
            v_low, w_low = below_pairs.pop()
            v_high, w_high = not_below_pairs.pop()
            self.packed_blocks.append(TwoValues(w_low, v_low, v_high))

            # We trim off the excess weight and add it back to the list of
            # below-mean or not-below-mean pairs, as its weight demands.
            w_leftover = w_low + w_high - self.mean_weight
            (below_pairs if w_leftover < self.mean_weight else not_below_pairs).append(
                (v_high, w_leftover)
            )

        # When no more below-mean pairs exist, the `not_below_pairs` list may
        # still contain some pairs having a weight of exactly the mean. These we
        # add to the packed-block array as degenerate two-value blocks, each
        # having a low value that occupies the entire block.
        self.packed_blocks.extend(TwoValues(w, v, None) for v, w in not_below_pairs)

    def draw(self, randrange=random.randrange):
        """Returns a value from the distribution at random.

        Args:
          randrange: (optional) A function that when called with an integer
            argument `n` returns a random integer from the set {0,1,2,...,n-1}.
            This function will be used to provide the randomness used to draw a
            value from the distribution. Defaults to `random.randrange`. You
            won't need to provide this argument unless you are testing or are
            trying to control the randomness regime, e.g., for a game with
            repeatable procedural generation mechanics.

        GUARANTEED to call `randrange` exactly once and perform only
        constant-time work.

        """
        # If we imagine the n packed blocks as an n * u rectangular area, where
        # u is the mean weight, our goal is to throw a random dart in this area
        # to pick one of the original values. Instead of having to generate two
        # random numbers -- one for the x coordinate in [0, n), and one for the
        # y in [0, u) -- we instead generate a single number in [0, n * u) and
        # unpack it into the dart's x-y coordinates.
        n = len(self.packed_blocks)
        dart_combined_coordinates = randrange(n * self.mean_weight)
        x = dart_combined_coordinates // self.mean_weight
        y = dart_combined_coordinates % self.mean_weight
        # Now that we know where the dart hit, we determine which block it selected.
        block = self.packed_blocks[x]
        # ... and, within that block, which of the block's two values the dart hit.
        value = block.low_value if y < block.low_weight else block.high_value
        return value
