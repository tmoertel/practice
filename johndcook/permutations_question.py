# This is the original function from John's blog at
# https://www.johndcook.com/blog/2025/03/15/permutations-question/
#
# This function requires O(n) space and O(n) time.
def Q3(n):
    q = [1]*(n+2)
    for k in range(2, n+1):
        q[k] = k*q[k-1] + (k-1)*q[k-2]
    return q[n]


# Here's my version, which requires only O(1) space. Note that
# in the original formula, only two previous values are used
# for all `k`: `q[k-1]` and `q[k-2]`. Here, we store them directly
# in variables `qkm1` and `qkm2` rather than across an O(n) array.
def Q3_constant_space(n):
    qkm2 = qkm1 = 1
    for k in range(2, n + 1):
        qkm2, qkm1 = qkm1, k * qkm1 + (k - 1) * qkm2
    return qkm1


def test_Q3_and_Q3_constant_space_are_equivalent():
    for n in range(10):
        assert Q3(n) == Q3_constant_space(n)
