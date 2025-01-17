#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Tom Moertel <tom@moertel.com>
# 2013-10-22

from soln_05_001_computing_parity import array_parity

def test_array_parity():
    assert array_parity([]) == 0
    assert array_parity([0]) == 0
    assert array_parity([1]) == 1
    assert array_parity([2]) == 1
    assert array_parity([3]) == 0
    assert array_parity([0, 0]) == 0
    assert array_parity([1, 1]) == 0
    assert array_parity([2, 2]) == 0
    assert array_parity([3, 3]) == 0
