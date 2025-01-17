# Suggested code may be subject to a license. Learn more: ~LicenseLog:45758302.
# Suggested code may be subject to a license. Learn more: ~LicenseLog:4087070036.
# Suggested code may be subject to a license. Learn more: ~LicenseLog:2522741966.
#!/usr/bin/python
#
# Tom Moertel <tom@moertel.com>
# 2013-10-02


"""Rotate an M*N matrix 90 degrees.

Source: http://www.careercup.com/question?id=5667482614366208

Discussion.

Given an MxN matrix A, let the rows be designated i = 0..M-1 and the
columns j = 0..N-1.  Rotating A clockwise creates an NxM matrix Ar in
which A's columns have become rows and the elements in the new rows
have been reversed.  In Python, zip(*) and reversed() make it easy:

    Ar = [list(reversed(row)) for row in zip(*A)] .

But when A is large, rearranging its elements is expensive.  Can we
avoid this cost?

Let us designate the element in the i'th row and j'th column by the
coordinate vector (i, j).  With a little scratch work, it is evident
that a clockwise rotation results in a new matrix in which A's entry
at (i, j) appears at the new coordinates (j, M - i - 1).  Therefore,
rotation can be seen not merely as a rearrangement of elements but,
alternatively, as a transformation of coordinates.  (It is not,
however, a linear transformation since (0, 0) is not mapped to itself.
But we can make it one by transforming (i, j, k) instead and by fixing
k = 1 for all of our operations.)

This alternative view provides an another means of rotating a matrix,
one that is advantageous when the element array is large: leave the
elements alone and instead transform the coordinates by which the
elements are accessed.  In this way we can rotate the matrix in O(1)
time and, further, we can represent the coordinate transform itself as
a 3x3 matrix, allowing us to compose transformations using matrix
multiplication.  Further, all of the transformed versions of a
matrix will share the original's underlying element storage.

In this example, I just use (an expensive) matrix multiplication for
each element access.  In a real implementation we would probably
generate optimized element-access code whenever we update the
coordinate transformation matrix.  All of the matrix multiplications
(for these matrices) can be resolved to additions and subtractions,
making the coordinate transforms fast and practical.

"""

from copy import copy


# brute-force implementation that rearranges all elements


def rot90(A):
    """Return matrix that is A rotated 90 degrees clockwise ."""
    return [list(reversed(row)) for row in zip(*A)]


# O(1) implementation that uses coordinate transforms


class CoordTransform(object):
    """Represents a coordinate transformation via a 3x3 matrix.

                                        [a, b, c]
    The class wraps around a matrix T = [d, e, f] to create
                                        [0, 0, 1]

    a coordinate transformer C that can transform a coordinate
    pair (i, j) into a related pair (i', j') = C(i, j) where


      [ i' ]     [ i ]
      [ j' ] = T [ j ] .
      [ 1  ]     [ 1 ]

    Two transformers C1 and C2 can be composed via the binary '*'
    operator to create a new transformer:

        (C1 * C2)(i, j) = C1(*(C2(i, j))).

    """

    def __init__(self, transformation_matrix):
        self.T = transformation_matrix

    def __call__(self, i, j):
        """Transform the coordinate pair (i, j) into a new pair (i', j')."""
        return [row[0] * i + row[1] * j + row[2] for row in self.T[:2]]

    def __mul__(self, T):
        """Compose this transform with another to create a new one."""
        return CoordTransform(mmul(self.T, T.T))


identity_xform = CoordTransform([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

transpose_xform = CoordTransform([[0, 1, 0], [1, 0, 0], [0, 0, 1]])


def mk_rev_cols_xform(N):
    """Make a CoordTransform to reverse the cols of an N-col matrix."""
    return CoordTransform([[1, 0, 0], [0, -1, N - 1], [0, 0, 1]])


class Matrix(object):
    """A 2D matrix based on an invariant backing array."""

    def __init__(self, arr, dims):
        """Create a 2D matrix from a 1D backing array."""
        self.arr = arr
        self.dims = self.arr_dims = dims
        self.coord_xform = identity_xform

    def get(self, i, j):
        """Get the element at the i'th row and j'th column."""
        i, j = self.coord_xform(i, j)
        return self.arr[i * self.arr_dims[1] + j]

    def tolists(self):
        """Convert the matrix into its list of lists representation."""
        return [
            [self.get(i, j) for j in range(self.dims[1])] for i in range(self.dims[0])
        ]

    def rot_cw(self):
        """Rotate the matrix clockwise via O(1) coordinate change."""
        return self.transpose().reverse_cols()

    def rot_ccw(self):
        """Rotate the matrix counter-clockwise via O(1) coordinate change."""
        return self.reverse_cols().transpose()

    def transpose(self):
        """Transpose the matrix via O(1) coordinate change."""
        A = copy(self)
        A.dims = tuple(reversed(A.dims))
        A.coord_xform *= transpose_xform
        return A

    def reverse_cols(self):
        """Reverse the columns of a matrix via O(1) coordinate change."""
        A = copy(self)
        A.coord_xform *= mk_rev_cols_xform(A.dims[1])
        return A


def mmul(A, B):
    """Compute matrix product A*B."""
    Bt = list(zip(*B))
    return [[sum(map(int.__mul__, r, c)) for c in Bt] for r in A]


def test():
    def eq(x, y):
        assert x == y

    # Rotate via brute-force element arrangement.
    assert rot90([["a", "b"], ["c", "d"]]) == [["c", "a"], ["d", "b"]]

    # Transpose via coordinate transformation.
    A = Matrix("abcdef", (2, 3))
    assert A.transpose().tolists() == [["a", "d"], ["b", "e"], ["c", "f"]]

    # Reverse columns via coordinate transformation.
    assert A.reverse_cols().tolists() == [["c", "b", "a"], ["f", "e", "d"]]

    # Rotate via coordinate transformation.
    assert A.rot_cw().tolists() == [["d", "a"], ["e", "b"], ["f", "c"]]
    assert A.rot_ccw().tolists() == [["c", "f"], ["b", "e"], ["a", "d"]]
    assert A.rot_cw().rot_cw().tolists() == [["f", "e", "d"], ["c", "b", "a"]]
    assert A.rot_ccw().rot_cw().tolists() == [["a", "b", "c"], ["d", "e", "f"]]
    assert A.rot_cw().rot_ccw().tolists() == [["a", "b", "c"], ["d", "e", "f"]]

    # 4 rotations must be equivalent to identity transform
    Arrrr = A.rot_ccw().rot_ccw().rot_ccw().rot_ccw()
    assert Arrrr.coord_xform.T == identity_xform.T

    # Clockwise and counter-clockwise rotations must be inverses.
    assert A.rot_ccw().rot_cw().tolists() == A.tolists()
    assert A.rot_cw().rot_ccw().coord_xform.T == identity_xform.T
