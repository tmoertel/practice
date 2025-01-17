from dutch_national_flag import dnf_sort

import itertools

# Test code.

COLOR_VALUE_MAP = dict(r=0, w=1, b=2)
COLORS = COLOR_VALUE_MAP.keys()
VALUES = COLOR_VALUE_MAP.values()


def colors_to_values(cs):
    return [COLOR_VALUE_MAP[c] for c in cs]


# We test the following property: For all input sequences cs having
# at most three distinct values, dnf_sort(cs) sorts the values.
def test_dnf_sort():
    for test_length in range(8):
        for cs in itertools.combinations(COLORS, test_length):
            cs = list(cs)
            dnf_sort(cs)  # Sorts in place.
            assert colors_to_values(cs) == sorted(colors_to_values(cs))
