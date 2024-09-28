#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-05-14

"""Solution to "" Code Jam problem


"""

def memo_ack(n, m):
    def ack_(n, m):
        if n == 0:
            return m + 1
        if m == 0:
            return ack(n - 1, 1)
        return ack(n - 1, ack(n, m - 1))
    cache = {}
    def ack(*args):
        if args in cache:
            return cache[args]
        ret = cache[args] = ack_(*args)
        return ret
    ret = ack(n, m)
    print('memo table has {} entries: {}'.format(len(cache), cache))
    print(ret)

import functools
def cps(f):
    @functools.wraps(f)
    def g(*args):
        stack = []
        maxdepth = 0
        fun, args, cont, cargs = f(*args)
        while True:
            maxdepth = max(maxdepth, len(stack))
            # print 'fun=%r, args=%r, cont=%r, cargs=%r, stack=%r' % (fun,args,cont,cargs,stack)
            if fun is None:
                if cont is None:
                    if not stack:
                        print('maxdepth = %r' %1 (maxdepth, ))
                        return args
                    cont, cargs = stack.pop()
                # print 'invoking cont=%r(arg=%r, cargs=%r); stack=%r' % (cont, args, cargs, stack)
                fun, args, cont, cargs = cont(args, *cargs)
            else:
                if cont:
                    stack.append((cont, cargs))
                # print 'invoking fun=%r(args=%r); stack=%r' % (fun, args, stack)
                fun, args, cont, cargs = fun(*args)
    return g

def Val(x):
    return None, x, None, None

def Exp(f, *args):
    return f, args, None, None

def ValTo(x):
    def g(cont, *cargs):
        return None, x, cont, cargs
    return g

def ExpTo(f, *args):
    def g(cont, *cargs):
        return f, args, cont, cargs
    return g

def ack(n, m):
    while True:
        if n == 0:
            return m + 1
        if m == 0:
            n, m = n - 1, 1
            continue
        x = ack(n, m - 1)
        n, m = n - 1, x

@cps
def ack(n, m):
    def body(n, m):
        while True:
            if n == 0:
                return Val(m + 1)
            if m == 0:
                n, m = n - 1, 1
                continue
            return ExpTo(body, n, m - 1)(bot, n)
    def bot(x, n):
        return Exp(body, n - 1, x)
    return Exp(body, n, m)

@cps
def ack(n, m):
    cache = {}
    def body(n, m):
        if (n, m) in cache:
            return cache[(n, m)]
        while True:
            if n == 0:
                return Val(m + 1)
            if m == 0:
                n, m = n - 1, 1
                continue
            return ExpTo(body, n, m - 1)(bot, n)
    def bot(x, n):
        return Exp(body, n - 1, x)
    return Exp(body, n, m)




def test_ack():
    for m in range(10):
        assert ack(0, m) == m + 1
    assert ack(1, 2) == 4
    assert ack(2, 2) == 7
    assert ack(3, 1) == 13
    assert ack(3, 4) == 125
    print('all tests pass')

def main():
    test_ack()

if __name__ == '__main__':
    main()
