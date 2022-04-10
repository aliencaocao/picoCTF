# with open('flag.txt.encrypted', 'rb') as f:
#     flag = f.read()
#
# for key in range(256):
#     encrypted = bytearray([j ^ (i ^ 0xFF) ^ key for i, j in enumerate(flag)])
#     if encrypted.hex().startswith('CTFSG{'):
#         with open('flag.txt', 'wb') as f:
#             f.write(encrypted)
#         print(key)
#         break
# else:
#     print('No key found')

with open('flag.txt.encrypted', 'rb') as f:
    flag = f.read()

flag = [j ^ (i ^ 0xFF) for i, j in enumerate(flag)]
print(flag)