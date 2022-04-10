#! /usr/bin/env python3

import random

KEY = random.randint(0, 0xFF)

with open("../flag.txt", "rb") as f:
    flag = f.read()

encrypted = bytearray([j ^ (i ^ 0xFF) ^ KEY for i, j in enumerate(flag)])

with open("flag.txt.encrypted", "wb") as f:
    f.write(encrypted)
