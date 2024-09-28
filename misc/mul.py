# Problem: Write a function to multiply two unsigned integers using
# only shifts, bit operations, and logical tests (i.e., no built-in
# arithmetic operators).
#
# Tom Moertel <tom@moertel.com>
# Mon 26 Aug 2013 12:58:22 PM EDT

def mul(x, y):
    z = 0
    while x and y:
        if x & 1:
            z = add(z, y)
        x >>= 1
        y <<= 1
    return z

def add(x, y):
    bit = 1
    carry = z = 0
    while carry or x or y:
        if (x & 1) ^ (y & 1) ^ carry:
            z |= bit
        carry = x & y & 1 or carry & (x ^ y)
        x >>= 1
        y >>= 1
        bit <<= 1
    return z

def test_mul():
    for x in range(25):
        for y in range(25):
            assert x * y == mul(x, y)

def test_add():
    for x in range(25):
        for y in range(25):
            assert x + y == add(x, y)
