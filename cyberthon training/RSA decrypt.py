import gmpy2
from Crypto.Util.number import *

p = 0
q = 0
n = p*q
e = 65537

# if given cipher is in binary
# with open('flag.txt.encrypted', 'rb') as f:
#     c = bytes_to_long(f.read())
c = 0  # crypt text

q = n // p
assert p * q == n
d = gmpy2.invert(e, (p - 1) * (q - 1))
m = pow(c, d, n)
byt = long_to_bytes(m)
print(byt.decode('ascii', errors='ignore'))
