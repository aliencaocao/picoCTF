from pwn import *

io = remote('chals.cyberthon22t.ctf.sg', 30101)
#io = process('./defuse_me')

# lvl 1
lvl1 = [0x1201C743, 0x536F83AF, 0x6C77C87B, 0xE48CA057]
payload = b''
for i in lvl1:
    payload += p32(i)
io.sendline(payload)

# lvl 2
io.sendline(b'20517396')
pause()

# lvl 3 v1
v2 = b'0'  # gives eax=2, works
v3 = b'\x01'  # gives eax=3, shld give 1
v4 = b'a'  # gives eax=3 ,works
v5 = b'0'  # gives eax=3, shld give 2
v6 = b'3'  # gives eax=4, works
io.sendline(v2 + v3 + v4 + v5 + v6)

# # lvl 3 v2
# v2 = b'1'  # gives eax=3, works
# v3 = b'1'  # gives eax=3, works
# v4 = b'a'  # gives eax=3, shld give 5
# v5 = b'0'  # gives eax=2, works
# v6 = b'0'  # gives eax=2, works
# io.sendline(v2 + v3 + v4 + v5 + v6)
pause()
io.interactive()
