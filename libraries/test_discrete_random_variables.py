import collections
from discrete_random_variables import DiscreteRandomVariable


def test_discrete_random_variables_raise_error_when_initialized_with_non_integer_weights():
    import pytest

    with pytest.raises(TypeError):
        DiscreteRandomVariable([("value_with_non_integer_weight", 1.23)])


def test_discrete_random_variables_raise_error_when_initialized_with_a_negative_weight():
    import pytest

    with pytest.raises(ValueError):
        DiscreteRandomVariable([("value_with_negative_weight", -2)])


def test_discrete_random_variables_raise_error_when_initialized_with_zero_total_weight():
    import pytest

    with pytest.raises(ValueError):
        DiscreteRandomVariable([])
    with pytest.raises(ValueError):
        DiscreteRandomVariable(
            [("value_with_zero_weight", 0), ("another_value_with_zero_weight", 0)]
        )


def test_discrete_random_variables_exactly_represent_their_underlying_distributions():
    """This function tests the following property:

    For all nonempty sequences `kws` of (key, weight) pairs having distinct keys,
    non-negative integer weights, and a total weight greater than zero,
    `DiscreteRandomVariable(kws).draw()` returns each key in `kws` with probability
    proportional to its corresponding weight. In other words, if Y is a random
    variable representing the result of calling `DiscreteRandomVariable(kws).draw()`,
    Y's distribution is *exactly* as given by `kws`.

    Assumption: Python's `random.randrange(n)` works as advertised. That is, it
    returns a random integer uniformly from the set {0, 1, 2, ..., n-1}.

    """
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
            # `random.randrange` logic and instead sweep uniformly over
            # the range of possible numbers Python could generate. This allows
            # us to observe exactly the distribution represented by the random
            # variable we're testing. This test relies on knowledge of the
            # variable's internal logic, namely that if its internal
            # distribution has n weights and a total weight of t, then it will
            # request random integers X in the range 0 <= X < n * t.
            total_weight = sum(weights)
            actual_distribution = collections.Counter(
                [
                    random_variable.draw(randrange=(lambda _: i))
                    for i in range(num_values * total_weight)
                ]
            )
            expected_distribution = collections.Counter(
                {value: num_values * weight for value, weight in values_and_weights}
            )
            assert actual_distribution == expected_distribution
