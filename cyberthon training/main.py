from pwn import *
from random import randint
from binascii import hexlify

KEY_LENGTH = 16
KEY = bytearray([randint(0, 255) for _ in range(KEY_LENGTH)])
print(KEY)

steve = open('steve.txt', 'rb').read()
dave = open('dave.txt', 'rb').read()

print(f'Steve: {hexlify(xor(steve, KEY)).decode()}')
print(f'Dave: {hexlify(xor(dave, KEY)).decode()}')