flag1 = [0x66, 0x78, 0x71, 0x66, 0x74, 0x69, 0x75, 0x75, 0x75, 0x73, 0x7F]
flag2 = [0x77, 0x60, 0x61, 0x61, 0x61, 0x61, 0x61, 0x61, 0x61, 0x61, 0x61, 0x27, 0x61, 0x6f]
flag = flag1 + flag2
assert len(flag) == 25

xor_key = 18

xored = [flag[i] ^ xor_key for i in range(len(flag))]
print(''.join([chr(i) for i in xored]))