# uncompyle6 version 3.5.0
# Python bytecode 3.7 (3394)
# Decompiled from: Python 2.7.5 (default, Nov 16 2020, 22:23:17)
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-44)]
# Embedded file name: main.py
# Size of source mod 2**32: 402 bytes
from functools import reduce

def phase1(x: list, y: int) -> list:
    if x:
        if x[(-2)] == y:
            if x[(-1)] < 255:
                x[(-1)] += 1
        return x
    else:
        x.extend([y, 1])
        return x


def reverse_phase1(x: list, y: int) -> list:
    if x:
        if x[(-2)] == y:
            if x[(-1)] > 1:
                x[(-1)] -= 1
        return x
    else:
        x.extend([y, 255])
        return x


def phase2(x: int) -> int:
    return ~x & 255


# with open('flag.jpg', 'rb') as (f):
#     data = f.read()
# encoded = map(phase2, reduce(phase1, data, []))
# with open('flag.jpg.encoded', 'wb') as (f):
#     f.write(bytes(encoded))



with open('flag.jpg.encoded', 'rb') as f:
    data = f.read()


def reverse_phase2(x: int) -> int:
    return ~x

data = map(reverse_phase2, data)
print(list(data))