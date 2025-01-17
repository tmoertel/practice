from soln_06_001_dutch_national_flag import partition
import math
import random


def test_dutch_national_flag_partition():
    # Partitions the elements by main force.
    # We use this as a reference implementation for our test.
    def reference_partition(A, x):
        return (
            [a for a in A if a < x] + [a for a in A if a == x] + [a for a in A if a > x]
        )

    for n in range(5):
        for _ in range(2 * math.factorial(n)):
            A = random.choices(range(n), k=n)
            for i in range(n):
                x = A[i]
                AP = partition(A, i)
                # Must preserve all input elements.
                assert sorted(AP) == sorted(A)
                # Must correctly partition the input elements.
                assert AP == reference_partition(AP, x)
